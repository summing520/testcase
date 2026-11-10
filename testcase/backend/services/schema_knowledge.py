"""
全库表结构知识文档：生成 / 更新 docs/knowledge/数据库表结构.md，
包含各库摘要、库库/表表关联（外键知识图谱）与列级明细；指纹变化时由 generate_test_cases 前刷新。
"""

from __future__ import annotations

import hashlib
import logging
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import inspect, text
from sqlalchemy.engine import Connection, Engine

from backend.integrations.database.client import DatabaseConfigError, get_engine

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = PROJECT_ROOT / "docs" / "knowledge" / "数据库表结构.md"
FP_PATH = PROJECT_ROOT / "data" / "db_schema_knowledge.sha256"


@dataclass(frozen=True)
class _FkConstraint:
    constraint_schema: str
    constraint_name: str
    table_schema: str
    table_name: str
    ref_schema: str
    ref_table: str


def _doc_enabled() -> bool:
    return (os.environ.get("DB_SCHEMA_DOC_ENABLED", "1") or "").strip().lower() not in (
        "0",
        "false",
        "no",
        "off",
    )


def _ignored_mysql_schemas() -> frozenset[str]:
    raw = os.environ.get(
        "DB_SCHEMA_DOC_IGNORE",
        "mysql,performance_schema,information_schema,sys",
    )
    parts = {p.strip() for p in raw.replace(";", ",").split(",") if p.strip()}
    return frozenset(parts)


def _graph_max_table_edges() -> int:
    try:
        return max(100, min(int(os.environ.get("DB_SCHEMA_DOC_GRAPH_MAX_EDGES", "2500")), 50000))
    except ValueError:
        return 2500


def _mermaid_max_edges() -> int:
    try:
        return max(20, min(int(os.environ.get("DB_SCHEMA_DOC_MERMAID_MAX_EDGES", "100")), 400))
    except ValueError:
        return 100


def _safe_sql_string_list(values: frozenset[str]) -> str:
    out: list[str] = []
    for v in sorted(values):
        if not re.fullmatch(r"[a-zA-Z0-9_]+", v):
            continue
        out.append("'" + v + "'")
    return ",".join(out) if out else "'__none__'"


def _esc_md_cell(v: Any) -> str:
    if v is None:
        return ""
    s = str(v).replace("\r\n", "\n").replace("\r", "\n").replace("\n", " ")
    return s.replace("|", "\\|")


def _esc_mermaid_label(s: str) -> str:
    return str(s).replace('"', "'").replace("[", "(").replace("]", ")")[:80]


def _mermaid_id(prefix: str, key: str) -> str:
    return prefix + hashlib.sha1(key.encode("utf-8")).hexdigest()[:10]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def _read_stored_fingerprint() -> str | None:
    try:
        if FP_PATH.is_file():
            return FP_PATH.read_text(encoding="utf-8").strip().splitlines()[0].strip()
    except OSError:
        pass
    return None


def _write_fingerprint(fp: str) -> None:
    FP_PATH.parent.mkdir(parents=True, exist_ok=True)
    FP_PATH.write_text(fp + "\n", encoding="utf-8", newline="\n")


def _mysql_columns_query(ignore: frozenset[str]):
    in_list = _safe_sql_string_list(ignore)
    return text(
        f"""
        SELECT TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION, COLUMN_NAME, COLUMN_TYPE,
               IS_NULLABLE, COLUMN_KEY, EXTRA, COLUMN_DEFAULT, COLUMN_COMMENT
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA NOT IN ({in_list})
        ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION
        """
    )


def _mysql_fk_usage_query(ignore: frozenset[str]):
    in_list = _safe_sql_string_list(ignore)
    return text(
        f"""
        SELECT CONSTRAINT_SCHEMA, CONSTRAINT_NAME, TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME,
               REFERENCED_TABLE_SCHEMA, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE REFERENCED_TABLE_NAME IS NOT NULL
          AND TABLE_SCHEMA NOT IN ({in_list})
          AND COALESCE(REFERENCED_TABLE_SCHEMA, TABLE_SCHEMA) NOT IN ({in_list})
        ORDER BY CONSTRAINT_SCHEMA, CONSTRAINT_NAME, TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME
        """
    )


def _mysql_combined_stream_fingerprint(conn: Connection, ignore: frozenset[str]) -> str:
    h = hashlib.sha256()
    q1 = _mysql_columns_query(ignore)
    r1 = conn.execution_options(stream_results=True).execute(q1)
    for row in r1.mappings():
        line = "|".join(
            str(row.get(k, ""))
            for k in (
                "TABLE_SCHEMA",
                "TABLE_NAME",
                "ORDINAL_POSITION",
                "COLUMN_NAME",
                "COLUMN_TYPE",
                "IS_NULLABLE",
                "COLUMN_KEY",
                "EXTRA",
                "COLUMN_DEFAULT",
                "COLUMN_COMMENT",
            )
        )
        h.update((line + "\n").encode("utf-8"))
    r1.close()
    h.update(b"\n--FK--\n")
    q2 = _mysql_fk_usage_query(ignore)
    r2 = conn.execution_options(stream_results=True).execute(q2)
    for row in r2.mappings():
        line = "|".join(str(row.get(k, "")) for k in row.keys())
        h.update((line + "\n").encode("utf-8"))
    r2.close()
    return h.hexdigest()


def _mysql_column_rows(conn: Connection, ignore: frozenset[str]) -> list[dict[str, Any]]:
    q = _mysql_columns_query(ignore)
    rows = conn.execute(q).mappings().all()
    return [dict(r) for r in rows]


def _mysql_fk_raw_rows(conn: Connection, ignore: frozenset[str]) -> list[dict[str, Any]]:
    q = _mysql_fk_usage_query(ignore)
    return [dict(r) for r in conn.execute(q).mappings().all()]


def _mysql_table_meta(conn: Connection, ignore: frozenset[str]) -> dict[tuple[str, str], dict[str, Any]]:
    in_list = _safe_sql_string_list(ignore)
    q = text(
        f"""
        SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE, ENGINE, TABLE_COMMENT, TABLE_ROWS
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA NOT IN ({in_list})
        ORDER BY TABLE_SCHEMA, TABLE_NAME
        """
    )
    out: dict[tuple[str, str], dict[str, Any]] = {}
    for r in conn.execute(q).mappings().all():
        key = (r["TABLE_SCHEMA"], r["TABLE_NAME"])
        out[key] = dict(r)
    return out


def _normalize_ref_schema(row: dict[str, Any]) -> str:
    rs = row.get("REFERENCED_TABLE_SCHEMA")
    if rs is None or str(rs).strip() == "":
        return str(row.get("TABLE_SCHEMA") or "")
    return str(rs)


def _aggregate_fk_constraints(fk_rows: list[dict[str, Any]]) -> list[_FkConstraint]:
    seen: set[tuple[str, str, str, str, str, str]] = set()
    out: list[_FkConstraint] = []
    for r in fk_rows:
        ref_s = _normalize_ref_schema(r)
        key = (
            str(r.get("CONSTRAINT_SCHEMA") or ""),
            str(r.get("CONSTRAINT_NAME") or ""),
            str(r.get("TABLE_SCHEMA") or ""),
            str(r.get("TABLE_NAME") or ""),
            ref_s,
            str(r.get("REFERENCED_TABLE_NAME") or ""),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(
            _FkConstraint(
                constraint_schema=key[0],
                constraint_name=key[1],
                table_schema=key[2],
                table_name=key[3],
                ref_schema=key[4],
                ref_table=key[5],
            )
        )
    return out


def _token_hints(table_names: list[str], top_n: int = 8) -> str:
    tokens: Counter[str] = Counter()
    for name in table_names:
        for part in re.split(r"[_\d]+", name.lower()):
            if len(part) >= 3:
                tokens[part] += 1
    common = [t for t, _ in tokens.most_common(top_n)]
    return "、".join(common) if common else "—"


def _build_db_summaries_section(
    columns: list[dict[str, Any]],
    table_meta: dict[tuple[str, str], dict[str, Any]],
    fk_constraints: list[_FkConstraint],
) -> str:
    tables_per_schema: dict[str, set[str]] = defaultdict(set)
    cols_per_schema: Counter[str] = Counter()
    for c in columns:
        sch = str(c.get("TABLE_SCHEMA") or "")
        tbl = str(c.get("TABLE_NAME") or "")
        if sch:
            tables_per_schema[sch].add(tbl)
            cols_per_schema[sch] += 1

    cross_targets: dict[str, set[str]] = defaultdict(set)
    fk_out_count: Counter[str] = Counter()
    for fk in fk_constraints:
        fk_out_count[fk.table_schema] += 1
        if fk.ref_schema != fk.table_schema:
            cross_targets[fk.table_schema].add(fk.ref_schema)

    lines: list[str] = ["## 各库摘要", ""]
    for sch in sorted(tables_per_schema.keys()):
        tset = tables_per_schema[sch]
        n_tab = len(tset)
        n_col = cols_per_schema[sch]
        hints = _token_hints(sorted(tset))

        row_estimates: list[tuple[str, int]] = []
        for t in tset:
            meta = table_meta.get((sch, t)) or {}
            try:
                tr = int(meta.get("TABLE_ROWS") or 0)
            except (TypeError, ValueError):
                tr = 0
            row_estimates.append((t, tr))
        row_estimates.sort(key=lambda x: (-x[1], x[0]))
        top_tables = row_estimates[:6]
        top_s = "，".join(f"`{a}`（估 {b} 行）" for a, b in top_tables if b > 0) or "（无有效行数估计）"

        cross = cross_targets.get(sch, set())
        cross_txt = "、".join(f"`{x}`" for x in sorted(cross)) if cross else "无"
        lines.append(f"### 库 `{sch}` 摘要")
        lines.append("")
        lines.append(
            f"- **规模**：**{n_tab}** 张表（含视图则与 information_schema 一致）、约 **{n_col}** 条列定义。"
        )
        lines.append(
            f"- **外键**：本库作为源表端的外键约束共 **{fk_out_count[sch]}** 个；"
            f"跨库引用指向：{cross_txt}。"
        )
        lines.append(f"- **行数估计（information_schema，仅供参考）**：{top_s}")
        lines.append(f"- **表名高频词根（启发式，非业务结论）**：{hints}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n\n"


def _build_db_graph_section(fk_constraints: list[_FkConstraint]) -> str:
    lines: list[str] = ["## 知识图谱：库与库关联", ""]
    weights: Counter[tuple[str, str]] = Counter()
    for fk in fk_constraints:
        if fk.table_schema != fk.ref_schema:
            weights[(fk.table_schema, fk.ref_schema)] += 1
    if not weights:
        lines.append("> 未发现跨库外键引用（或当前账号在 `information_schema` 中不可见）。")
        lines.append("")
        return "\n".join(lines)

    lines.append("以下为基于 **外键引用** 的库级有向关系（边权为外键约束列声明条数近似）。")
    lines.append("")
    lines.append("### Mermaid（库级）")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart LR")
    db_ids: dict[str, str] = {}
    for db in sorted({d for e in weights for d in e}):
        db_ids[db] = _mermaid_id("db", db)
        lines.append(f'  {db_ids[db]}["{_esc_mermaid_label(db)}"]')
    cap = _mermaid_max_edges()
    shown = 0
    for (src, tgt), w in weights.most_common():
        if shown >= cap:
            break
        lab = _esc_mermaid_label(str(w))
        lines.append(f'  {db_ids[src]} -->|"{lab}"| {db_ids[tgt]}')
        shown += 1
    lines.append("```")
    lines.append("")
    if len(weights) > cap:
        lines.append(f"> Mermaid 中仅绘制权重最高的前 **{cap}** 条库对边（共 {len(weights)} 条）。")
        lines.append("")
    lines.append("### 库对边列表")
    lines.append("")
    lines.append("| 源库 | 目标库 | 外键列声明条数（近似） |")
    lines.append("| --- | --- | --- |")
    for (src, tgt), w in sorted(weights.items(), key=lambda x: (-x[1], x[0][0], x[0][1])):
        lines.append(f"| `{src}` | `{tgt}` | {w} |")
    lines.append("")
    return "\n".join(lines)


def _build_table_graph_sections(fk_constraints: list[_FkConstraint]) -> str:
    lines: list[str] = ["## 知识图谱：表与表外键", ""]
    lines.append("本节含 **按库子图的 Mermaid（节选）** 与 **外键约束明细表（节选）**。")
    lines.append("")

    by_schema: dict[str, list[_FkConstraint]] = defaultdict(list)
    for fk in fk_constraints:
        by_schema[fk.table_schema].append(fk)

    m_max = _mermaid_max_edges()
    lines.append("### Mermaid（按源表所在库分子图，边数上限）")
    lines.append("")
    drawn = 0
    for sch in sorted(by_schema.keys()):
        fks = by_schema[sch]
        edge_list: list[tuple[str, str, str]] = [
            (
                f"{fk.table_schema}.{fk.table_name}",
                f"{fk.ref_schema}.{fk.ref_table}",
                fk.constraint_name,
            )
            for fk in fks
        ]
        edge_list = edge_list[:m_max]
        if not edge_list:
            continue
        lines.append(f"#### 库 `{sch}`")
        lines.append("")
        lines.append("```mermaid")
        lines.append("flowchart TB")
        node_ids: dict[str, str] = {}
        nodes: set[str] = set()
        for src, tgt, _c in edge_list:
            nodes.add(src)
            nodes.add(tgt)
        for node in sorted(nodes):
            node_ids[node] = _mermaid_id("t", node)
            short = node.split(".", 1)[-1]
            lines.append(f'  {node_ids[node]}["{_esc_mermaid_label(short)}"]')
        for src, tgt, cname in edge_list:
            lab = _esc_mermaid_label(str(cname)[:32])
            lines.append(f'  {node_ids[src]} -->|"{lab}"| {node_ids[tgt]}')
            drawn += 1
        lines.append("```")
        lines.append("")
        if len(fks) > m_max:
            lines.append(f"> 本库共 **{len(fks)}** 条外键约束，上图仅前 **{m_max}** 条；完整列表见下方明细表。")
            lines.append("")

    if drawn == 0:
        lines.append("> 无外键元数据可绘制。")
        lines.append("")

    lines.append("### 外键约束明细（节选）")
    lines.append("")
    max_rows = _graph_max_table_edges()
    lines.append(f"| 源库.源表 | 目标库.目标表 | 约束（schema.name） |")
    lines.append("| --- | --- | --- |")
    for i, fk in enumerate(fk_constraints):
        if i >= max_rows:
            break
        src = f"`{fk.table_schema}.{fk.table_name}`"
        tgt = f"`{fk.ref_schema}.{fk.ref_table}`"
        cstr = f"`{fk.constraint_schema}.{fk.constraint_name}`"
        lines.append(f"| {src} | {tgt} | {cstr} |")
    lines.append("")
    if len(fk_constraints) > max_rows:
        lines.append(f"> 共 **{len(fk_constraints)}** 条外键约束，上表仅列前 **{max_rows}** 条。可调大环境变量 `DB_SCHEMA_DOC_GRAPH_MAX_EDGES`。")
        lines.append("")
    return "\n".join(lines)


def _build_detail_columns_section(
    columns: list[dict[str, Any]], table_meta: dict[tuple[str, str], dict[str, Any]]
) -> str:
    lines: list[str] = ["## 详细表结构（列级）", ""]
    cur_schema: str | None = None
    cur_key: tuple[str, str] | None = None
    buf_cols: list[dict[str, Any]] = []

    def flush_table() -> None:
        nonlocal buf_cols, cur_key
        if cur_key is None:
            return
        sch, tbl = cur_key
        meta = table_meta.get(cur_key) or {}
        ttype = meta.get("TABLE_TYPE") or ""
        eng = meta.get("ENGINE") or ""
        comment = (meta.get("TABLE_COMMENT") or "").strip()
        lines.append(f"### `{sch}`.`{tbl}`")
        meta_bits = [x for x in (ttype, eng) if x]
        if meta_bits:
            lines.append("")
            lines.append(f"- 类型 / 引擎：`{'` / `'.join(meta_bits)}`")
        if comment:
            lines.append(f"- 表注释：{comment}")
        tr = meta.get("TABLE_ROWS")
        if tr is not None:
            lines.append(f"- 估算行数（information_schema）：{_esc_md_cell(tr)}")
        lines.append("")
        lines.append("| # | 列名 | 类型 | 可空 | 键 | 额外 | 默认值 | 列注释 |")
        lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
        for c in buf_cols:
            lines.append(
                "| "
                + " | ".join(
                    [
                        _esc_md_cell(c.get("ORDINAL_POSITION")),
                        _esc_md_cell(c.get("COLUMN_NAME")),
                        _esc_md_cell(c.get("COLUMN_TYPE")),
                        _esc_md_cell(c.get("IS_NULLABLE")),
                        _esc_md_cell(c.get("COLUMN_KEY")),
                        _esc_md_cell(c.get("EXTRA")),
                        _esc_md_cell(c.get("COLUMN_DEFAULT")),
                        _esc_md_cell(c.get("COLUMN_COMMENT")),
                    ]
                )
                + " |"
            )
        lines.append("")

    for row in columns:
        key = (row["TABLE_SCHEMA"], row["TABLE_NAME"])
        if cur_key != key:
            flush_table()
            cur_key = key
            buf_cols = []
            sch = key[0]
            if sch != cur_schema:
                lines.append(f"## 库 `{sch}`")
                lines.append("")
                cur_schema = sch
        buf_cols.append(row)
    flush_table()
    return "\n".join(lines).rstrip() + "\n"


def _build_full_mysql_document(
    columns: list[dict[str, Any]],
    table_meta: dict[tuple[str, str], dict[str, Any]],
    fk_rows: list[dict[str, Any]],
    fingerprint: str,
) -> str:
    fk_cons = _aggregate_fk_constraints(fk_rows)
    header = "\n".join(
        [
            "# 数据库表结构知识",
            "",
            "> 本文件由系统在检测到 **元数据或外键关系变化** 或首次生成时，根据 `.env` 中 `DB_QUERY_URL` 自动拉取并写入。",
            f"> **结构指纹**：`{fingerprint}`",
            f"> **生成时间**：{_utc_now_iso()}",
            "",
            "> 摘要为基于表名、行数估计、外键的**启发式统计**，非业务建模结论。",
            "> 知识图谱边来自 `information_schema.KEY_COLUMN_USAGE` 外键声明。",
            "> 可通过 `DB_SCHEMA_DOC_ENABLED=0` 关闭生成用例前同步；`DB_SCHEMA_DOC_IGNORE` 排除系统库。",
            "",
            "---",
            "",
        ]
    )
    summaries = _build_db_summaries_section(columns, table_meta, fk_cons)
    db_graph = _build_db_graph_section(fk_cons)
    tbl_graph = _build_table_graph_sections(fk_cons)
    detail = _build_detail_columns_section(columns, table_meta)
    return (header + summaries + db_graph + tbl_graph + detail).rstrip() + "\n"


def _sync_mysql(engine: Engine) -> bool:
    ignore = _ignored_mysql_schemas()
    prev = _read_stored_fingerprint()
    with engine.connect() as conn:
        fp = _mysql_combined_stream_fingerprint(conn, ignore)
        if prev == fp and DOC_PATH.is_file():
            return False
        cols = _mysql_column_rows(conn, ignore)
        meta = _mysql_table_meta(conn, ignore)
        fk_rows = _mysql_fk_raw_rows(conn, ignore)
    body = _build_full_mysql_document(cols, meta, fk_rows, fp)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    _write_fingerprint(fp)
    logger.info("schema_knowledge: updated %s (fp=%s)", DOC_PATH, fp[:16])
    return True


def _sqlite_body_and_fingerprint(engine: Engine) -> tuple[str, str]:
    insp = inspect(engine)
    tables = sorted(insp.get_table_names())
    h = hashlib.sha256()
    fk_edges: list[tuple[str, str, str | None]] = []
    for t in tables:
        for fk in insp.get_foreign_keys(t):
            rt = fk.get("referred_table")
            if rt:
                name = fk.get("name")
                fk_edges.append((t, str(rt), str(name) if name else None))
                h.update(f"{t}->{rt}\n".encode())
    parts: list[str] = [
        "## 各库摘要",
        "",
        "### 库 `main` 摘要",
        "",
        f"- **规模**：**{len(tables)}** 张表（SQLite `main`）。",
        "",
        "## 知识图谱：库与库关联",
        "",
        "> SQLite 单文件仅 `main` 一库，无库间边。",
        "",
        "## 知识图谱：表与表外键",
        "",
    ]
    if fk_edges:
        parts.append("```mermaid")
        parts.append("flowchart LR")
        nodes: dict[str, str] = {}
        for frm, to, _eid in fk_edges[: _mermaid_max_edges()]:
            for n in (frm, to):
                if n not in nodes:
                    nodes[n] = _mermaid_id("s", n)
                    parts.append(f'  {nodes[n]}["{_esc_mermaid_label(n)}"]')
        for frm, to, _eid in fk_edges[: _mermaid_max_edges()]:
            parts.append(f"  {nodes[frm]} --> {nodes[to]}")
        parts.append("```")
        parts.append("")
        parts.append("| 源表 | 目标表 |")
        parts.append("| --- | --- |")
        for frm, to, _e in fk_edges[: _graph_max_table_edges()]:
            parts.append(f"| `{frm}` | `{to}` |")
        parts.append("")
    else:
        parts.append("> 未声明外键或无法解析 PRAGMA。")
        parts.append("")

    parts.append("## 详细表结构（列级）")
    parts.append("")
    parts.append("## 库 `main`")
    parts.append("")
    h.update(b"\n--COL--\n")
    for t in tables:
        cols = insp.get_columns(t)
        h.update(f"{t}\n".encode())
        parts.append(f"### `main`.`{t}`")
        parts.append("")
        parts.append("| # | 列名 | 类型 | 可空 | 默认值 |")
        parts.append("| --- | --- | --- | --- | --- |")
        for i, c in enumerate(cols, start=1):
            h.update(
                f"{c.get('name')}|{c.get('type')}|{c.get('nullable')}|{c.get('default')}\n".encode()
            )
            parts.append(
                "| "
                + " | ".join(
                    [
                        str(i),
                        _esc_md_cell(c.get("name")),
                        _esc_md_cell(c.get("type")),
                        _esc_md_cell(c.get("nullable")),
                        _esc_md_cell(c.get("default")),
                    ]
                )
                + " |"
            )
        parts.append("")
    fp = h.hexdigest()
    header = "\n".join(
        [
            "# 数据库表结构知识",
            "",
            "> SQLite 单文件模式。",
            f"> **结构指纹**：`{fp}`",
            f"> **生成时间**：{_utc_now_iso()}",
            "",
            "---",
            "",
        ]
    )
    body = header + "\n".join(parts).rstrip() + "\n"
    return body, fp


def _sync_sqlite(engine: Engine) -> bool:
    body, fp = _sqlite_body_and_fingerprint(engine)
    prev = _read_stored_fingerprint()
    if prev == fp and DOC_PATH.is_file():
        return False
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOC_PATH.write_text(body, encoding="utf-8", newline="\n")
    _write_fingerprint(fp)
    logger.info("schema_knowledge: updated SQLite doc (fp=%s)", fp[:16])
    return True


def sync_schema_knowledge_document() -> bool:
    """
    若已启用且已配置 DB_QUERY_URL：对比结构指纹，变化则重写
    docs/knowledge/数据库表结构.md。
    Returns True if file was (re)written.
    """
    if not _doc_enabled():
        return False
    try:
        engine = get_engine()
    except DatabaseConfigError:
        logger.debug("schema_knowledge: skip, no DB_QUERY_URL")
        return False
    try:
        dialect = engine.dialect.name
        if dialect in ("mysql", "mariadb"):
            return _sync_mysql(engine)
        if dialect == "sqlite":
            return _sync_sqlite(engine)
        logger.warning("schema_knowledge: unsupported dialect %s, skip", dialect)
        return False
    except Exception as exc:  # noqa: BLE001
        logger.warning("schema_knowledge: sync failed: %s", exc)
        return False


def rebuild_schema_knowledge_document() -> bool:
    """忽略指纹文件，强制重写文档并更新指纹。"""
    if FP_PATH.is_file():
        try:
            FP_PATH.unlink()
        except OSError:
            pass
    if DOC_PATH.is_file():
        try:
            DOC_PATH.unlink()
        except OSError:
            pass
    return sync_schema_knowledge_document()

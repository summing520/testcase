# -*- coding: utf-8 -*-
"""
Trim docs/knowledge/数据库表结构.md to only tables referenced in:
  - docs/knowledge/APP用户流程涉及表.md
  - docs/knowledge/HUB用户流程涉及表.md

Only schemas present in the current 数据库表结构.md are considered (ams/cis/hub/lcs/lps/mds/tds).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DOC = ROOT / "docs" / "knowledge" / "数据库表结构.md"
FLOW_DOCS = [
    ROOT / "docs" / "knowledge" / "APP用户流程涉及表.md",
    ROOT / "docs" / "knowledge" / "HUB用户流程涉及表.md",
]

QUALIFIED_RE = re.compile(r"`([a-zA-Z0-9_]+)\.([a-zA-Z0-9_]+)`")
BARE_RE = re.compile(r"`([a-zA-Z0-9_]+)`")
TABLE_HEADER_RE = re.compile(r"^### `([a-zA-Z0-9_]+)`\.`([a-zA-Z0-9_]+)`\s*$")

SCHEMA_ORDER = ["ams", "cis", "hub", "lcs", "lps", "mds", "tds"]


def load_all_table_pairs(lines: list[str]) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    for line in lines:
        m = TABLE_HEADER_RE.match(line.rstrip("\n"))
        if m:
            pairs.add((m.group(1).lower(), m.group(2).lower()))
    return pairs


def _next_table_or_lib_header(lines: list[str], start: int) -> int:
    """First index > start that begins the next table or library section."""
    n = len(lines)
    for j in range(start + 1, n):
        line = lines[j]
        if TABLE_HEADER_RE.match(line.rstrip("\n")):
            return j
        if line.startswith("## 库 `"):
            return j
    return n


def iter_table_blocks(lines: list[str]) -> list[tuple[tuple[str, str], int, int]]:
    """Return [(schema, table, start_idx, end_idx), ...] in file order."""
    starts: list[tuple[tuple[str, str], int]] = []
    for i, line in enumerate(lines):
        m = TABLE_HEADER_RE.match(line.rstrip("\n"))
        if m:
            starts.append(((m.group(1).lower(), m.group(2).lower()), i))
    blocks: list[tuple[tuple[str, str], int, int]] = []
    for j, ((s, t), start) in enumerate(starts):
        end = _next_table_or_lib_header(lines, start)
        blocks.append(((s, t), start, end))
    return blocks


def resolve_qualified(
    schema: str, table: str, all_pairs: set[tuple[str, str]]
) -> set[tuple[str, str]]:
    s, t = schema.lower(), table.lower()
    if (s, t) in all_pairs:
        return {(s, t)}
    if t.endswith("_x"):
        prefix = t[:-2]
        return {
            pair
            for pair in all_pairs
            if pair[0] == s and re.fullmatch(re.escape(prefix) + r"_\d+", pair[1])
        }
    return set()


def resolve_bare(
    table: str, all_pairs: set[tuple[str, str]]
) -> set[tuple[str, str]]:
    t = table.lower()
    if "." in t:
        return set()
    if t.endswith("_x"):
        prefix = t[:-2]
        return {
            pair
            for pair in all_pairs
            if re.fullmatch(re.escape(prefix) + r"_\d+", pair[1])
        }
    hits = [pair for pair in all_pairs if pair[1] == t]
    if len(hits) == 1:
        return {hits[0]}
    return set()


def collect_wanted_pairs(all_pairs: set[tuple[str, str]]) -> set[tuple[str, str]]:
    schemas_in_doc = {s for s, _ in all_pairs}
    wanted: set[tuple[str, str]] = set()

    for path in FLOW_DOCS:
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            qualified_spans: list[tuple[int, int]] = []
            for m in QUALIFIED_RE.finditer(line):
                qualified_spans.append((m.start(), m.end()))
                sch, tbl = m.group(1).lower(), m.group(2).lower()
                if sch not in schemas_in_doc:
                    continue
                wanted |= resolve_qualified(sch, tbl, all_pairs)

            for m in BARE_RE.finditer(line):
                start, end = m.start(), m.end()
                if any(qs <= start and end <= qe for qs, qe in qualified_spans):
                    continue
                token = m.group(1)
                if "." in token:
                    continue
                wanted |= resolve_bare(token, all_pairs)

    return wanted


def build_summary_lines(wanted: set[tuple[str, str]]) -> list[str]:
    lines_out: list[str] = ["## 各库摘要\n", "\n"]
    for sch in SCHEMA_ORDER:
        tables = sorted(t for s, t in wanted if s == sch)
        if not tables:
            continue
        lines_out.append(f"### 库 `{sch}` 摘要\n\n")
        lines_out.append(f"- **收录表数（来自流程清单）**：**{len(tables)}**\n")
        lines_out.append(
            "- **表清单**："
            + "，".join(f"`{sch}`.`{tbl}`" for tbl in tables)
            + "\n\n"
        )
    return lines_out


def filter_fk_rows(
    fk_lines: list[str], wanted: set[tuple[str, str]]
) -> list[str]:
    out: list[str] = []
    i = 0
    n = len(fk_lines)
    while i < n:
        line = fk_lines[i]
        if line.startswith("### 外键约束明细"):
            out.append(line)
            i += 1
            while i < n and fk_lines[i].strip() == "":
                out.append(fk_lines[i])
                i += 1
            header_row: str | None = None
            sep_row: str | None = None
            data_rows: list[str] = []
            while i < n and fk_lines[i].startswith("|"):
                row = fk_lines[i]
                if "---" in row:
                    sep_row = row
                    i += 1
                    continue
                parts = re.findall(r"`([a-zA-Z0-9_]+)\.([^`]+)`", row)
                if len(parts) >= 2:
                    p1 = (parts[0][0].lower(), parts[0][1].lower())
                    p2 = (parts[1][0].lower(), parts[1][1].lower())
                    if p1 in wanted and p2 in wanted:
                        data_rows.append(row)
                elif "源库" in row or "目标库" in row:
                    header_row = row
                i += 1
            if not header_row:
                header_row = (
                    "| 源库.源表 | 目标库.目标表 | 约束（schema.name） |\n"
                )
            if not sep_row:
                sep_row = "| --- | --- | --- |\n"
            out.append(header_row)
            out.append(sep_row)
            if data_rows:
                out.extend(data_rows)
            else:
                out.append(
                    "\n> （流程所选表与 `information_schema` 节选外键无交集。）\n"
                )
            continue
        if line.strip().startswith("> （流程所选表与"):
            i += 1
            continue
        out.append(line)
        i += 1
    return out


def strip_kg_fk_mermaid(fk_lines: list[str]) -> list[str]:
    """Remove Mermaid blocks; keep title lines until ### 外键."""
    out: list[str] = []
    i = 0
    n = len(fk_lines)
    while i < n:
        line = fk_lines[i]
        if line.startswith("### Mermaid"):
            i += 1
            while i < n and not fk_lines[i].startswith("### 外键约束明细"):
                i += 1
            continue
        if "按库子图的 Mermaid" in line:
            out.append(
                "> 已从原稿移除 Mermaid 子图；外键明细仅保留两端表均在流程清单中的行。\n\n"
            )
            i += 1
            continue
        out.append(line)
        i += 1
    return out


def main() -> None:
    out_path = SCHEMA_DOC
    if len(sys.argv) > 1:
        out_path = Path(sys.argv[1])

    lines = SCHEMA_DOC.read_text(encoding="utf-8").splitlines(keepends=True)
    all_pairs = load_all_table_pairs(lines)
    wanted = collect_wanted_pairs(all_pairs)
    if not wanted:
        raise SystemExit("no tables matched; check flow docs and schema file")

    blocks = iter_table_blocks(lines)
    wanted_blocks = [b for b in blocks if b[0] in wanted]

    i_detail = next(i for i, l in enumerate(lines) if l.startswith("## 详细表结构"))
    i_kg_db = next(i for i, l in enumerate(lines) if l.startswith("## 知识图谱：库与库关联"))
    i_kg_fk = next(i for i, l in enumerate(lines) if l.startswith("## 知识图谱：表与表外键"))

    header_end = next(
        i for i, l in enumerate(lines) if l.startswith("## 各库摘要")
    )

    out: list[str] = []
    for h in range(0, header_end):
        ln = lines[h]
        if ln.startswith("> **结构指纹**"):
            out.append(
                "> **结构指纹**：（已按《APP用户流程涉及表》《HUB用户流程涉及表》裁剪，"
                "原全库指纹不再适用）\n"
            )
            continue
        if ln.startswith("> **保留库**"):
            continue
        if ln.startswith("> **生成时间**"):
            out.append(ln)
            out.append(
                "> **裁剪依据**：仅保留上述两份流程清单中出现的、且在本文件中已有列定义的表。\n"
            )
            continue
        out.append(ln)

    out.extend(build_summary_lines(wanted))

    out.append("\n")
    out.extend(lines[i_kg_db:i_kg_fk])

    fk_src = lines[i_kg_fk:i_detail]
    fk_trim = strip_kg_fk_mermaid(fk_src)
    fk_rows = filter_fk_rows(fk_trim, wanted)
    out.extend(fk_rows)

    out.append("\n")
    out.append(lines[i_detail])
    if not lines[i_detail].endswith("\n"):
        out[-1] += "\n"
    out.append("\n")

    by_schema: dict[str, list[tuple[str, str]]] = {s: [] for s in SCHEMA_ORDER}
    for s, t in wanted:
        if s in by_schema:
            by_schema[s].append((s, t))
    for s in SCHEMA_ORDER:
        by_schema[s].sort(key=lambda x: x[1])

    pair_to_lines = {pair: lines[s:e] for pair, s, e in blocks}

    for s in SCHEMA_ORDER:
        tables_here = by_schema[s]
        if not tables_here:
            continue
        out.append(f"## 库 `{s}`\n\n")
        for pair in tables_here:
            if pair not in pair_to_lines:
                raise SystemExit(f"missing block for {pair}")
            out.extend(pair_to_lines[pair])

    out_path.write_text("".join(out), encoding="utf-8")
    print(f"Wrote {out_path} — {len(wanted)} tables")


if __name__ == "__main__":
    main()

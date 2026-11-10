import json
import logging
import re
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)

from backend.agents.testcase_agent import run_testcase_agent, run_testcase_agent_with_reporter
from backend.db import tables as t
from backend.db.connection import get_connection, json_load, now_utc, parse_datetime
from backend.integrations.feishu.service import feishu_url_to_markdown
from backend.services.channel_knowledge_doc import (
    refresh_channel_knowledge_file,
    refresh_institution_knowledge_file,
)
from backend.services.checklist_memory import (
    checklist_memory_fingerprint,
    extract_memory_entity_key,
    load_memory_for_items,
    memory_entity_label,
    upsert_checklist_item_memories,
)
from backend.services.schema_knowledge import sync_schema_knowledge_document
from backend.models.task import (
    CheckItemResult,
    CheckItemUpdate,
    TaskCreateRequest,
    TaskSummary,
    TestCaseLibraryItem,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _resolve_markdown_path(path_value: str) -> Path:
    raw = Path(path_value)
    candidate = raw if raw.is_absolute() else (PROJECT_ROOT / raw)
    resolved = candidate.resolve()

    if not resolved.exists():
        raise FileNotFoundError(f"Markdown file not found: {path_value}")
    if resolved.suffix.lower() != ".md":
        raise ValueError(f"Only markdown files are supported: {path_value}")
    return resolved


def _list_markdown_files_under(relative_dir: str) -> list[str]:
    base_dir = (PROJECT_ROOT / relative_dir).resolve()
    if not base_dir.exists() or not base_dir.is_dir():
        return []

    files: list[str] = []
    for path in base_dir.rglob("*.md"):
        if path.is_file():
            files.append(path.relative_to(PROJECT_ROOT).as_posix())
    return sorted(files)


def list_step1_doc_options() -> dict[str, list[str]]:
    return {
        "knowledge_biz_docs": _list_markdown_files_under("docs/knowledge/biz"),
        "knowledge_interface_docs": _list_markdown_files_under("docs/knowledge/interface"),
        "knowledge_db_docs": _list_markdown_files_under("docs/knowledge/db"),
        "checklist_docs": _list_markdown_files_under("docs/checklist"),
        "rule_docs": _list_markdown_files_under("docs/rules"),
        "demo_docs": _list_markdown_files_under("docs/demo"),
    }


def get_markdown_file_content(path_value: str) -> str:
    """
    Read markdown content by relative path.
    Only files under docs/ are allowed.
    """
    if not path_value:
        raise ValueError("path is required")

    normalized = path_value.replace("\\", "/").strip()
    if not normalized.startswith("docs/"):
        raise ValueError("Only files under docs/ are allowed")

    resolved = _resolve_markdown_path(normalized)
    docs_root = (PROJECT_ROOT / "docs").resolve()
    if docs_root not in resolved.parents:
        raise ValueError("Only files under docs/ are allowed")

    return resolved.read_text(encoding="utf-8")


def _load_markdown_docs(paths: list[str]) -> dict[str, str]:
    contents: dict[str, str] = {}
    for p in paths:
        try:
            resolved = _resolve_markdown_path(p)
            contents[p] = resolved.read_text(encoding="utf-8")
        except FileNotFoundError:
            logger.warning("task_service: markdown 文件不存在，已跳过: %s", p)
    return contents


_CHECK_TABLE_HEADER = frozenset(
    {"check项", "check项:", "检查项", "检查项:"}
)


def _normalize_check_table_header_cell(cell: str) -> str:
    return cell.replace(" ", "").replace("\u3000", "")


def _is_markdown_table_row(line: str) -> bool:
    """表格行：以 | 开头即可（兼容缺少行尾 | 的 Markdown 表格）。"""
    return bool(line.strip().startswith("|"))


def _split_markdown_table_cells(line: str) -> list[str]:
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def _extract_check_items_from_check_table(text: str) -> list[str] | None:
    """
    If the doc contains a markdown table whose first column header is check项/检查项,
    return only the first-column values from that table (one section), in order.
    Stops at the first non-table line after the header — so prose like「识别逻辑」with
    numbered/bullet lists is never treated as check items.
    Returns None when no such table header exists (caller may use loose extraction).
    """
    items: list[str] = []
    in_table = False
    saw_header = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if in_table and saw_header:
                break
            continue

        if line.startswith("#"):
            if in_table and saw_header:
                break
            continue

        if _is_markdown_table_row(line):
            cells = _split_markdown_table_cells(line)
            cells = [c for c in cells if c]
            if not cells:
                continue
            first_cell = cells[0]
            normalized = _normalize_check_table_header_cell(first_cell)
            if normalized in _CHECK_TABLE_HEADER:
                in_table = True
                saw_header = True
                continue
            if in_table and saw_header:
                if re.fullmatch(r"[-:\s]+", normalized):
                    continue
                items.append(first_cell)
            continue

        if in_table and saw_header:
            break

    if not saw_header:
        return None
    return items


def _extract_check_items_loose(text: str) -> list[str]:
    """Legacy: bullets, numbered lines, and any table first-column (no check-table guard)."""
    items: list[str] = []
    checklist_pattern = re.compile(r"^[-*]\s+\[(?: |x|X)\]\s+(.*)")
    bullet_pattern = re.compile(r"^[-*]\s+(.*)")
    numbered_pattern = re.compile(r"^\d+[.)]\s+(.*)")

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if _is_markdown_table_row(line):
            cells = _split_markdown_table_cells(line)
            cells = [c for c in cells if c]
            if not cells:
                continue
            first_cell = cells[0]
            normalized = _normalize_check_table_header_cell(first_cell)
            if normalized in _CHECK_TABLE_HEADER:
                continue
            if re.fullmatch(r"[-:\s]+", normalized):
                continue
            items.append(first_cell)
            continue

        m = checklist_pattern.match(line)
        if m:
            items.append(m.group(1).strip())
            continue

        m = bullet_pattern.match(line)
        if m:
            items.append(m.group(1).strip())
            continue

        m = numbered_pattern.match(line)
        if m:
            items.append(m.group(1).strip())
            continue

    return items


def _extract_check_items(markdown_docs: dict[str, str]) -> list[str]:
    items: list[str] = []
    for text in markdown_docs.values():
        table_only = _extract_check_items_from_check_table(text)
        if table_only is not None:
            items.extend(table_only)
        else:
            items.extend(_extract_check_items_loose(text))

    deduped: list[str] = []
    seen = set()
    for item in items:
        if item and item not in seen:
            seen.add(item)
            deduped.append(item)
    return deduped


def _match_single_item(requirement_text: str, item_text: str) -> str | None:
    req = requirement_text or ""
    if not req.strip():
        return None

    if item_text in req:
        return item_text

    tokens = [t for t in re.split(r"[\s,.;:，。；：/()（）]+", item_text) if len(t) >= 3]
    for token in tokens:
        idx = req.find(token)
        if idx >= 0:
            start = max(0, idx - 50)
            end = min(len(req), idx + len(token) + 80)
            return req[start:end].strip()
    return None


_ITEM_AMC_BILL_MERGE = "上线机构的AMC账单是否合并"
_ITEM_CHANNEL_BORROWING_MODES = "渠道支持的借款模式"


def _amc_bill_merge_means_merged(matched: str | None) -> bool:
    """True when extracted value indicates AMC bills are merged (per checklist □ 合并)."""
    if matched is None:
        return False
    t = str(matched).strip()
    if not t:
        return False
    compact = re.sub(r"\s+", "", t)
    if "不合并" in compact or "未合并" in compact:
        return False
    if "合并" in compact:
        return True
    low = t.lower()
    if low in ("是", "y", "yes", "true", "1"):
        return True
    return False


def _strip_amc_mode_from_borrowing_list(text: str | None) -> str | None:
    """Remove AMC模式 from comma/顿号-separated borrowing mode list."""
    if text is None:
        return None
    s = str(text).strip()
    if not s or "amc" not in s.lower():
        return text
    parts = re.split(r"[,，、;；]+", s)
    segs = [p.strip() for p in parts if p.strip()]
    if not segs:
        return text

    def is_amc_mode_token(p: str) -> bool:
        c = re.sub(r"\s+", "", p).lower()
        return c in ("amc模式", "amc")

    filtered = [p for p in segs if not is_amc_mode_token(p)]
    if len(filtered) == len(segs):
        return text
    if not filtered:
        return None
    joiner = "," if "," in s and "，" not in s else "，"
    return joiner.join(filtered)


def _apply_amc_merge_borrowing_constraint(
    resolved: dict[str, tuple[str | None, str]],
) -> None:
    """
    Checklist rule: when AMC bills are merged, channel borrowing modes must not include AMC模式.
    Enforced after LLM/rule extraction so behavior does not depend on model compliance alone.
    """
    merge_val = resolved.get(_ITEM_AMC_BILL_MERGE, (None,))[0]
    if not _amc_bill_merge_means_merged(merge_val):
        return
    if _ITEM_CHANNEL_BORROWING_MODES not in resolved:
        return
    text, _src = resolved[_ITEM_CHANNEL_BORROWING_MODES]
    new_text = _strip_amc_mode_from_borrowing_list(text)
    if new_text == text:
        return
    resolved[_ITEM_CHANNEL_BORROWING_MODES] = (new_text, "校正")


def _strip_code_fence(text: str) -> str:
    cleaned = (text or "").strip()
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()
    return cleaned


_ATX_HEADING_RE = re.compile(r"^#{1,6}\s")


def _apply_title_to_testcase_markdown(markdown: str, title: str) -> str:
    """Replace the first ATX heading with title, or prepend one if the doc has none."""
    final_title = (title or "").strip()
    if not final_title:
        return markdown or ""
    body = markdown or ""
    lines = body.splitlines()
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if _ATX_HEADING_RE.match(stripped):
            indent = line[: len(line) - len(stripped)]
            lines[i] = f"{indent}# {final_title}"
            return "\n".join(lines).rstrip() + "\n"
    if body.strip():
        return f"# {final_title}\n\n{body.rstrip()}\n"
    return f"# {final_title}\n"


def _format_checklist_reference_for_llm(checklist_contents: dict[str, str]) -> str:
    """Full checklist markdown (table hints + 识别逻辑等) for value inference."""
    if not checklist_contents:
        return ""
    parts: list[str] = []
    for name, body in checklist_contents.items():
        text = (body or "").strip()
        if text:
            parts.append(f"## 检查清单文件: {name}\n\n{text}")
    return "\n\n---\n\n".join(parts)


def _format_historical_memory_for_llm(historical: dict[str, str] | None) -> str:
    if not historical:
        return ""
    lines: list[str] = []
    for k, v in historical.items():
        vv = (v or "").strip()
        if k and vv:
            lines.append(f"- {k}: {vv}")
    if not lines:
        return ""
    return (
        "以下为同套检查清单下，用户曾在其他需求中最终确认过的取值（仅供参考）。\n"
        "请结合「当前需求文本」独立判断：能明确推出则以当前需求为准；与历史一致可沿用；\n"
        "当前需求无法判断时，可参考历史取值但仍须符合检查清单识别逻辑与互斥规则。\n\n"
        "历史确认参考：\n"
        + "\n".join(lines)
        + "\n\n"
    )


def _extract_check_item_values_with_llm(
    requirement_text: str,
    check_items: list[str],
    llm,
    checklist_reference: str | None = None,
    historical_memory: dict[str, str] | None = None,
    biz_profile_reference: str | None = None,
    integration_kind: str | None = None,
) -> dict[str, str | None]:
    """
    Use LLM to extract value for each checklist key.
    Returns a map: {check_item: extracted_value_or_none}.
    """
    if llm is None or not check_items:
        return {}

    ref_block = ""
    if checklist_reference and checklist_reference.strip():
        ref_block = (
            "以下为所选检查清单的完整 Markdown（含各检查项可选值说明及文末「识别逻辑」等规则）。\n"
            "请结合「需求文本」与这些规则做推断；若规则要求根据其他字段推导，请一并完成。\n\n"
            f"{checklist_reference.strip()}\n\n"
        )

    memory_block = _format_historical_memory_for_llm(historical_memory)

    biz_block = ""
    if biz_profile_reference and biz_profile_reference.strip():
        biz_block = (
            "以下为历史机构/渠道概要信息（仅供参考，取值仍须以本次需求正文为准）：\n\n"
            f"{biz_profile_reference.strip()}\n\n"
        )

    kind_hint = ""
    if integration_kind == "institution":
        kind_hint = (
            "当前任务为**机构对接**：只填写机构检查项（如机构编码、类型、流程概要），"
            "勿填写渠道字段（如内部渠道号、渠道名称）。\n\n"
        )
    elif integration_kind == "channel":
        kind_hint = (
            "当前任务为**渠道对接**：只填写渠道检查项，勿填写机构专属字段。\n\n"
        )

    prompt = (
        "你是需求分析助手。请从给定需求文本中提取每个检查项的值。\n"
        f"{kind_hint}"
        "要求：\n"
        "1) 只输出 JSON 对象，不要输出其他文字。\n"
        "2) JSON 的 key 必须与检查项原文完全一致（与下方检查项列表中的字符串逐字相同）。\n"
        "3) 取值优先依据需求原文；若检查清单中给出了识别规则或选项说明，且需求信息足以推断，"
        "请按规则填写（例如从利率类型、AMC 配置等推断借款模式或定价模式）。\n"
        "4) 识别逻辑中若有多条规则，须**全部**遵守，并注意**先后顺序与缩减关系**："
        "若某条规则给出「候选集合」，后续规则若写「不得支持」「不支持」「须删除」「排除」等，必须在最终结果上落实，"
        "不能因为前一条规则列举了较多模式就保留被排除项。\n"
        "5) 常见互斥：当清单或需求表明「上线机构的AMC账单是否合并」为合并/是时，"
        "「渠道支持的借款模式」的输出中**不得**包含「AMC模式」。\n"
        "6) 若仍无法确定，填空字符串 \"\"。\n\n"
        f"{memory_block}"
        f"{biz_block}"
        f"{ref_block}"
        "检查项列表（JSON数组）：\n"
        f"{json.dumps(check_items, ensure_ascii=False)}\n\n"
        "需求文本：\n"
        f"{requirement_text}\n"
    )

    try:
        result = llm.invoke(prompt)
        content = result.content if hasattr(result, "content") else str(result)
        content = _strip_code_fence(content)
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            return {}
    except Exception:
        return {}

    output: dict[str, str | None] = {}
    for item in check_items:
        value = parsed.get(item)
        if value is None:
            output[item] = None
        elif isinstance(value, str):
            normalized = value.strip()
            output[item] = normalized if normalized else None
        else:
            normalized = str(value).strip()
            output[item] = normalized if normalized else None
    return output


def _interface_doc_fields(row) -> tuple[str | None, str | None]:
    """从任务行解析接口文档路径与展示标签（列表查询可不加载 markdown 正文）。"""
    raw_path = ""
    try:
        raw_path = (row["interface_doc_path"] or "").strip()
    except (KeyError, IndexError, TypeError):
        raw_path = ""

    if raw_path:
        norm = raw_path.replace("\\", "/")
        label = norm.split("/")[-1] or norm
        if label.startswith("用户上传"):
            return norm, label
        return norm, label

    url = ""
    try:
        url = (row["external_cooperation_url"] or "").strip()
    except (KeyError, IndexError, TypeError):
        url = ""
    if url:
        short = url if len(url) <= 56 else url[:53] + "..."
        return url, short

    has_md = False
    try:
        has_md = bool(row["has_external_markdown"])
    except (KeyError, IndexError, TypeError):
        md = row.get("external_cooperation_markdown") if hasattr(row, "get") else None
        if md is None:
            try:
                md = row["external_cooperation_markdown"]
            except (KeyError, IndexError, TypeError):
                md = None
        has_md = bool(md and str(md).strip())

    if has_md:
        return "用户上传", "用户上传"

    return None, None


def _row_to_task_summary(row) -> TaskSummary:
    adopted_title = None
    try:
        raw = row["adopted_test_case_title"]
        adopted_title = (raw or "").strip() or None
    except (KeyError, IndexError, TypeError):
        adopted_title = None

    iface_path, iface_label = _interface_doc_fields(row)

    return TaskSummary(
        id=row["id"],
        status=row["status"],
        requirement_url=row["requirement_url"],
        requirement_kind=(row["requirement_kind"] or "unknown"),
        inferred_checklist_doc=(row["inferred_checklist_doc"] or None),
        adopted_test_case_title=adopted_title,
        selected_knowledge_docs=json_load(row["selected_knowledge_docs"], []),
        selected_checklist_docs=json_load(row["selected_checklist_docs"], []),
        selected_rule_docs=json_load(row["selected_rule_docs"], []),
        interface_doc_path=iface_path,
        interface_doc_label=iface_label,
        created_at=parse_datetime(row["created_at"]),
        updated_at=parse_datetime(row["updated_at"]),
    )


def _infer_requirement_kind(requirement_markdown: str) -> str:
    from backend.services.integration_matching import infer_kind_from_markdown

    return infer_kind_from_markdown(requirement_markdown)


def _resolve_requirement_kind(
    *,
    requirement_markdown: str,
    markdown_kind: str,
    check_item_labels: list[str],
    checklist_doc: str | None,
    requirement_url: str | None = None,
    requirement_title: str | None = None,
) -> str:
    from backend.services.integration_matching import effective_requirement_kind

    return effective_requirement_kind(
        markdown_kind,
        check_item_labels=check_item_labels,
        checklist_doc=checklist_doc,
        requirement_markdown=requirement_markdown,
        requirement_url=requirement_url,
        requirement_title=requirement_title,
    )


def _default_checklist_for_kind(kind: str) -> str | None:
    from backend.services.integration_matching import default_checklist_doc_for_kind

    return default_checklist_doc_for_kind(kind)


def create_task(request: TaskCreateRequest) -> TaskSummary:
    task_id = str(uuid.uuid4())
    now = now_utc()

    conn = get_connection()
    try:
        conn.execute(
            f"""
            INSERT INTO {t.TASKS} (
                id, status, requirement_url,
                selected_knowledge_docs, selected_checklist_docs, selected_rule_docs,
                requirement_markdown, confirmed_check_items, generated_testcase_markdown,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                "draft",
                request.requirement_url,
                json.dumps(request.selected_knowledge_docs, ensure_ascii=False),
                json.dumps(request.selected_checklist_docs, ensure_ascii=False),
                json.dumps(request.selected_rule_docs, ensure_ascii=False),
                None,
                None,
                None,
                now,
                now,
            ),
        )
        conn.commit()
        row = conn.execute(f"SELECT * FROM {t.TASKS} WHERE id = ?", (task_id,)).fetchone()
    finally:
        conn.close()

    if row is None:
        raise RuntimeError("Task creation failed")
    return _row_to_task_summary(row)


def list_tasks() -> list[TaskSummary]:
    conn = get_connection()
    try:
        rows = conn.execute(
            f"""
            SELECT
              tasks.*,
              lib.title AS adopted_test_case_title,
              (
                tasks.external_cooperation_markdown IS NOT NULL
                AND CHAR_LENGTH(tasks.external_cooperation_markdown) > 0
              ) AS has_external_markdown
            FROM {t.TASKS} AS tasks
            LEFT JOIN {t.TEST_CASE_LIBRARY} AS lib
              ON lib.task_id = tasks.id
            ORDER BY tasks.created_at DESC
            """
        ).fetchall()
    finally:
        conn.close()

    return [_row_to_task_summary(row) for row in rows]


def get_task(task_id: str):
    conn = get_connection()
    try:
        task_row = conn.execute(
            f"""
            SELECT
              tasks.*,
              lib.title AS adopted_test_case_title
            FROM {t.TASKS} AS tasks
            LEFT JOIN {t.TEST_CASE_LIBRARY} AS lib
              ON lib.task_id = tasks.id
            WHERE tasks.id = ?
            """,
            (task_id,),
        ).fetchone()
        if task_row is None:
            return None

        item_rows = conn.execute(
            f"""
            SELECT item_key, item_text, matched_text, confirmed_text, match_source, is_edited
            FROM {t.TASK_CHECK_ITEMS}
            WHERE task_id = ?
            ORDER BY id ASC
            """,
            (task_id,),
        ).fetchall()

        check_items = [
            CheckItemResult(
                item_key=row["item_key"],
                item_text=row["item_text"],
                matched_text=row["matched_text"],
                confirmed_text=row["confirmed_text"],
                match_source=row["match_source"],
                is_edited=bool(row["is_edited"]),
            )
            for row in item_rows
        ]
        return {
            "task": _row_to_task_summary(task_row),
            "requirement_markdown": task_row["requirement_markdown"],
            "external_cooperation_markdown": task_row["external_cooperation_markdown"],
            "check_items": check_items,
            "generated_testcase_markdown": task_row["generated_testcase_markdown"],
        }
    finally:
        conn.close()


def parse_task_requirement(task_id: str, llm=None):
    return parse_task_requirement_with_reporter(task_id, llm=llm, reporter=None)


def parse_task_requirement_with_reporter(
    task_id: str,
    llm=None,
    reporter=None,
    *,
    requirement_title: str | None = None,
):
    def emit(stage: str, message: str, **extra) -> None:
        if reporter:
            payload = {"stage": stage, "message": message}
            payload.update(extra)
            reporter(payload)

    conn = get_connection()
    try:
        task_row = conn.execute(f"SELECT * FROM {t.TASKS} WHERE id = ?", (task_id,)).fetchone()
        if task_row is None:
            return None

        requirement_url = task_row["requirement_url"]
        title_hint = (requirement_title or "").strip()
        if not title_hint:
            try:
                from backend.integrations.feishu.service import feishu_resolve_url_preview

                preview = feishu_resolve_url_preview(requirement_url)
                title_hint = (preview.get("title") or "").strip()
            except Exception:
                title_hint = ""

        emit("feishu", "正在调用飞书文档解析工具…")
        requirement_markdown = feishu_url_to_markdown(requirement_url)

        from backend.services.integration_matching import (
            default_biz_profile_doc_for_kind,
            default_checklist_doc_for_kind,
            infer_kind_from_texts,
            kind_label_zh,
        )

        emit("kind", "正在识别需求类型（机构/渠道）…")
        kind_for_checklist = infer_kind_from_texts(
            requirement_markdown,
            requirement_url,
            title=title_hint,
        )
        emit(
            "kind",
            f"初步识别：{kind_label_zh(kind_for_checklist)}（将加载对应检查项表）",
        )

        checklist_docs = json_load(task_row["selected_checklist_docs"], [])

        if kind_for_checklist == "unknown":
            emit("kind", "识别为其它需求：跳过检查项提取与确认")
            now = now_utc()
            conn.execute(
                f"""
                UPDATE {t.TASKS}
                SET requirement_markdown = ?, status = ?, updated_at = ?,
                    requirement_kind = ?, inferred_checklist_doc = ?,
                    selected_checklist_docs = ?
                WHERE id = ?
                """,
                (
                    requirement_markdown,
                    "parsed_confirming",
                    now,
                    "unknown",
                    "",
                    json.dumps([], ensure_ascii=False),
                    task_id,
                ),
            )
            conn.execute(f"DELETE FROM {t.TASK_CHECK_ITEMS} WHERE task_id = ?", (task_id,))
            conn.commit()
            emit("db", "保存完成")
            updated_row = conn.execute(
                f"SELECT * FROM {t.TASKS} WHERE id = ?", (task_id,)
            ).fetchone()
            emit("done", "解析完成")
            return {
                "task": _row_to_task_summary(updated_row),
                "requirement_markdown": requirement_markdown,
            }

        inferred_checklist_doc = None
        if not checklist_docs:
            inferred_checklist_doc = default_checklist_doc_for_kind(kind_for_checklist)
            if inferred_checklist_doc:
                checklist_docs = [inferred_checklist_doc]
            elif kind_for_checklist == "unknown":
                emit(
                    "kind",
                    "未能识别机构/渠道：请确认飞书标题或正文含「机构对接」或「渠道对接」",
                )

        emit("checklist", f"正在加载检查清单：{len(checklist_docs)} 个文件…")
        checklist_contents = _load_markdown_docs(checklist_docs)
        emit("checklist", "正在提取检查项…")
        check_items = _extract_check_items(checklist_contents)
        emit("checklist", f"检查项提取完成：{len(check_items)} 条")

        checklist_doc_path = (
            inferred_checklist_doc
            or (checklist_docs[0] if checklist_docs else None)
        )
        kind = _resolve_requirement_kind(
            requirement_markdown=requirement_markdown,
            markdown_kind=kind_for_checklist,
            check_item_labels=check_items,
            checklist_doc=checklist_doc_path,
            requirement_url=requirement_url,
            requirement_title=title_hint,
        )
        if kind != kind_for_checklist and kind in ("institution", "channel"):
            expected = default_checklist_doc_for_kind(kind)
            if expected and expected not in checklist_docs:
                emit("kind", f"按最终类型 {kind_label_zh(kind)} 重新加载检查项表…")
                checklist_docs = [expected]
                inferred_checklist_doc = expected
                checklist_contents = _load_markdown_docs(checklist_docs)
                check_items = _extract_check_items(checklist_contents)

        emit("kind", f"对接类型：{kind_label_zh(kind)}（{kind}）")
        checklist_ref = _format_checklist_reference_for_llm(checklist_contents)

        biz_doc_path = default_biz_profile_doc_for_kind(kind)
        biz_profile_ref = ""
        if biz_doc_path:
            biz_contents = _load_markdown_docs([biz_doc_path])
            biz_profile_ref = _format_checklist_reference_for_llm(biz_contents)
            emit("checklist", f"已加载业务概要：{biz_doc_path.split('/')[-1]}")

        entity_key = extract_memory_entity_key(kind, requirement_markdown=requirement_markdown)
        fp = checklist_memory_fingerprint(kind, entity_key, checklist_docs)
        emit("memory", "正在读取历史记忆参考…")
        historical = load_memory_for_items(fp, check_items)
        if entity_key:
            emit(
                "memory",
                f"历史记忆读取完成：{len(historical or {})} 条（{memory_entity_label(kind)}={entity_key}）",
            )
        else:
            emit(
                "memory",
                f"历史记忆读取完成：{len(historical or {})} 条（未识别{memory_entity_label(kind)}，未命中实体维度记忆）",
            )
        if llm is not None:
            emit(
                "model",
                f"模型：{getattr(llm, 'model_name', None) or getattr(llm, 'model', None) or 'unknown'}",
            )
            emit("llm", "正在调用大模型推断检查项取值…")
        ai_values = _extract_check_item_values_with_llm(
            requirement_markdown,
            check_items,
            llm,
            checklist_reference=checklist_ref,
            historical_memory=historical or None,
            biz_profile_reference=biz_profile_ref,
            integration_kind=kind,
        )
        if llm is not None:
            emit("llm", "大模型推断完成")

        now = now_utc()
        emit("db", "正在保存解析结果…")
        conn.execute(
            f"""
            UPDATE {t.TASKS}
            SET requirement_markdown = ?, status = ?, updated_at = ?,
                requirement_kind = ?, inferred_checklist_doc = ?,
                selected_checklist_docs = ?
            WHERE id = ?
            """,
            (
                requirement_markdown,
                "parsed_confirming",
                now,
                kind,
                inferred_checklist_doc or "",
                json.dumps(checklist_docs, ensure_ascii=False),
                task_id,
            ),
        )
        conn.execute(f"DELETE FROM {t.TASK_CHECK_ITEMS} WHERE task_id = ?", (task_id,))

        resolved: dict[str, tuple[str | None, str]] = {}
        for item in check_items:
            rule_match = _match_single_item(requirement_markdown, item)
            ai_match = ai_values.get(item)
            matched_text = ai_match or rule_match
            match_source = "AI" if ai_match else ("规则" if rule_match else "空")
            resolved[item] = (matched_text, match_source)

        for item in check_items:
            matched_text, match_source = resolved[item]
            if (matched_text is None or not str(matched_text).strip()) and historical.get(item):
                resolved[item] = (historical[item], "记忆")

        _apply_amc_merge_borrowing_constraint(resolved)

        for idx, item in enumerate(check_items, start=1):
            key = f"item_{idx:03d}"
            matched_text, match_source = resolved[item]
            conn.execute(
                f"""
                INSERT INTO {t.TASK_CHECK_ITEMS} (
                    task_id, item_key, item_text, matched_text, confirmed_text, match_source,
                    is_edited, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (task_id, key, item, matched_text, matched_text, match_source, 0, now, now),
            )

        conn.commit()
        emit("db", "保存完成")
        updated_row = conn.execute(f"SELECT * FROM {t.TASKS} WHERE id = ?", (task_id,)).fetchone()
    finally:
        conn.close()

    if updated_row is None:
        return None
    emit("done", "解析完成")
    return {
        "task": _row_to_task_summary(updated_row),
        "requirement_markdown": requirement_markdown,
    }


def update_check_items(task_id: str, updates: list[CheckItemUpdate]):
    now = now_utc()
    conn = get_connection()
    try:
        task_row = conn.execute(f"SELECT * FROM {t.TASKS} WHERE id = ?", (task_id,)).fetchone()
        if task_row is None:
            return None

        for item in updates:
            conn.execute(
                f"""
                UPDATE {t.TASK_CHECK_ITEMS}
                SET confirmed_text = ?, is_edited = 1, updated_at = ?
                WHERE task_id = ? AND item_key = ?
                """,
                (item.confirmed_text, now, task_id, item.item_key),
            )

        item_rows = conn.execute(
            f"""
            SELECT item_text, confirmed_text, matched_text
            FROM {t.TASK_CHECK_ITEMS} WHERE task_id = ? ORDER BY id ASC
            """,
            (task_id,),
        ).fetchall()
        labels = [r["item_text"] for r in item_rows]
        checklist_docs = json_load(task_row["selected_checklist_docs"], [])
        checklist_doc = (
            (task_row["inferred_checklist_doc"] or "").strip()
            or (checklist_docs[0] if checklist_docs else None)
        )
        kind = _resolve_requirement_kind(
            requirement_markdown=task_row["requirement_markdown"] or "",
            markdown_kind=task_row["requirement_kind"] or "unknown",
            check_item_labels=labels,
            checklist_doc=checklist_doc,
            requirement_url=task_row["requirement_url"] or "",
        )
        conn.execute(
            f"UPDATE {t.TASKS} SET updated_at = ?, requirement_kind = ? WHERE id = ?",
            (now, kind, task_id),
        )
        conn.commit()
    finally:
        conn.close()

    return get_task(task_id)


def generate_test_cases(task_id: str, llm):
    task = get_task(task_id)
    if task is None:
        return None
    return generate_test_cases_with_reporter(task_id, llm, reporter=None)


def generate_test_cases_with_reporter(task_id: str, llm, reporter=None):
    task = get_task(task_id)
    if task is None:
        return None
    summary = task["task"]
    kind = getattr(summary, "requirement_kind", None) or "unknown"
    check_pairs: list[tuple[str, str]] = []
    to_store: list[tuple[str, str]] = []
    for item in task["check_items"]:
        final = item.confirmed_text if item.confirmed_text is not None else item.matched_text
        text = (final or "").strip()
        if text:
            to_store.append((item.item_text, text))
            check_pairs.append((item.item_text, text))
    entity_key = extract_memory_entity_key(
        kind,
        check_items=check_pairs,
        requirement_markdown=task.get("requirement_markdown") or "",
    )
    fp = checklist_memory_fingerprint(
        kind,
        entity_key,
        summary.selected_checklist_docs,
    )
    upsert_checklist_item_memories(fp, to_store, task_id)
    if reporter:
        if entity_key and kind in ("institution", "channel"):
            reporter(
                {
                    "stage": "memory",
                    "message": f"已写入检查项记忆：{len(to_store)} 条（{memory_entity_label(kind)}={entity_key}）",
                }
            )
        else:
            reporter({"stage": "memory", "message": f"已写入检查项记忆：{len(to_store)} 条"})
    if kind in ("institution", "channel"):
        if kind == "institution":
            refresh_institution_knowledge_file(
                llm,
                task.get("requirement_markdown") or "",
                to_store,
                task_id,
            )
        else:
            refresh_channel_knowledge_file(
                llm,
                task.get("requirement_markdown") or "",
                to_store,
                task_id,
            )
        if reporter:
            reporter(
                {
                    "stage": "knowledge",
                    "message": "已刷新渠道知识文档"
                    if kind != "institution"
                    else "已刷新机构知识文档",
                }
            )
    elif reporter:
        reporter({"stage": "knowledge", "message": "其它需求：跳过机构/渠道知识文档刷新"})
    sync_schema_knowledge_document()
    if reporter:
        reporter({"stage": "schema", "message": "已同步数据库结构知识文档"})
    if reporter:
        reporter({"stage": "agent", "message": "开始生成测试用例（Agent 迭代）"})
    run_testcase_agent_with_reporter(task_id, llm, reporter=reporter)
    return get_task(task_id)


def update_task_preview_markdown(task_id: str, kind: str, markdown: str):
    """Update markdown shown on preview/edit pages (requirement or generated test case)."""
    kind = (kind or "").strip()
    if kind not in ("requirement", "test-case"):
        raise ValueError(f"Unsupported kind for markdown update: {kind}")

    now = now_utc()
    conn = get_connection()
    try:
        row = conn.execute(f"SELECT id FROM {t.TASKS} WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return None
        column = (
            "requirement_markdown"
            if kind == "requirement"
            else "generated_testcase_markdown"
        )
        conn.execute(
            f"UPDATE {t.TASKS} SET {column} = ?, updated_at = ? WHERE id = ?",
            (markdown, now, task_id),
        )
        conn.commit()
    finally:
        conn.close()
    return get_task(task_id)


def clear_external_cooperation_doc(task_id: str):
    """清除任务已保存的对接文档（用户未上传时步骤2可不携带接口文档生成）。"""
    now = now_utc()
    conn = get_connection()
    try:
        row = conn.execute(f"SELECT * FROM {t.TASKS} WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return None
        conn.execute(
            f"""
            UPDATE {t.TASKS}
            SET external_cooperation_markdown = NULL,
                external_cooperation_url = '',
                interface_doc_path = '',
                updated_at = ?
            WHERE id = ?
            """,
            (now, task_id),
        )
        conn.commit()
    finally:
        conn.close()
    return get_task(task_id)


def update_external_cooperation_doc(
    task_id: str,
    markdown: str,
    url: str | None = None,
    *,
    source_path: str | None = None,
):
    now = now_utc()
    conn = get_connection()
    try:
        row = conn.execute(f"SELECT * FROM {t.TASKS} WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return None
        iface_path = (source_path or "").strip()
        conn.execute(
            f"""
            UPDATE {t.TASKS}
            SET external_cooperation_markdown = ?,
                external_cooperation_url = ?,
                interface_doc_path = ?,
                updated_at = ?
            WHERE id = ?
            """,
            (markdown, (url or "").strip(), iface_path, now, task_id),
        )
        conn.commit()
    finally:
        conn.close()
    return get_task(task_id)


def update_task_config(
    task_id: str,
    *,
    selected_knowledge_docs: list[str] | None = None,
    selected_rule_docs: list[str] | None = None,
    generation_options: dict | None = None,
):
    now = now_utc()
    conn = get_connection()
    try:
        row = conn.execute(f"SELECT * FROM {t.TASKS} WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return None

        fields = []
        values = []
        if selected_knowledge_docs is not None:
            fields.append("selected_knowledge_docs = ?")
            values.append(json.dumps(selected_knowledge_docs, ensure_ascii=False))
        if selected_rule_docs is not None:
            fields.append("selected_rule_docs = ?")
            values.append(json.dumps(selected_rule_docs, ensure_ascii=False))
        if generation_options is not None:
            fields.append("generation_options_json = ?")
            values.append(json.dumps(generation_options, ensure_ascii=False))

        if not fields:
            return get_task(task_id)

        values.extend([now, task_id])
        conn.execute(
            f"UPDATE {t.TASKS} SET {', '.join(fields)}, updated_at = ? WHERE id = ?",
            tuple(values),
        )
        conn.commit()
    finally:
        conn.close()

    return get_task(task_id)


def adopt_generated_test_case(task_id: str, title: str | None):
    conn = get_connection()
    try:
        task_row = conn.execute(f"SELECT * FROM {t.TASKS} WHERE id = ?", (task_id,)).fetchone()
        if task_row is None:
            return None

        generated = task_row["generated_testcase_markdown"]
        if not generated:
            raise ValueError("Task has no generated test case yet")

        adopted_at = now_utc()
        final_title = title or f"Task {task_id} generated test cases"
        content = _apply_title_to_testcase_markdown(generated, final_title)

        conn.execute(
            f"""
            INSERT INTO {t.TEST_CASE_LIBRARY} (task_id, title, content_markdown, adopted_at)
            VALUES (?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE
                title = VALUES(title),
                content_markdown = VALUES(content_markdown),
                adopted_at = VALUES(adopted_at)
            """,
            (task_id, final_title, content, adopted_at),
        )
        conn.execute(
            f"""
            UPDATE {t.TASKS}
            SET status = ?, generated_testcase_markdown = ?, updated_at = ?
            WHERE id = ?
            """,
            ("adopted", content, adopted_at, task_id),
        )
        conn.commit()
    finally:
        conn.close()

    return get_task(task_id)


def list_adopted_test_cases() -> list[TestCaseLibraryItem]:
    conn = get_connection()
    try:
        rows = conn.execute(
            f"""
            SELECT id, task_id, title, content_markdown, adopted_at
            FROM {t.TEST_CASE_LIBRARY}
            ORDER BY adopted_at DESC
            """
        ).fetchall()
    finally:
        conn.close()

    return [
        TestCaseLibraryItem(
            id=row["id"],
            task_id=row["task_id"],
            title=row["title"],
            content_markdown=row["content_markdown"],
            adopted_at=parse_datetime(row["adopted_at"]),
        )
        for row in rows
    ]


def delete_task(task_id: str) -> bool:
    """
    Delete a task and its related rows.
    Returns False when task does not exist.
    """
    conn = get_connection()
    try:
        row = conn.execute(f"SELECT id FROM {t.TASKS} WHERE id = ?", (task_id,)).fetchone()
        if row is None:
            return False

        conn.execute(f"DELETE FROM {t.TASK_CHECK_ITEMS} WHERE task_id = ?", (task_id,))
        conn.execute(f"DELETE FROM {t.TASK_AGENT_RUNS} WHERE task_id = ?", (task_id,))
        conn.execute(f"DELETE FROM {t.TEST_CASE_LIBRARY} WHERE task_id = ?", (task_id,))
        conn.execute(f"DELETE FROM {t.TASKS} WHERE id = ?", (task_id,))
        conn.commit()
        return True
    finally:
        conn.close()

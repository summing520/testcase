import json
import logging
import os
import re
from pathlib import Path
from typing import Any

from langchain_core.messages import BaseMessage, HumanMessage

from backend.db import tables as t
from backend.db.connection import get_connection, json_load, now_utc

logger = logging.getLogger(__name__)
from backend.models.task import CheckItemResult
from backend.prompts.agent_prompts import (
    AGENT_EVALUATE_PROMPT,
    AGENT_GENERATE_DRAFT_PROMPT,
    AGENT_DB_SUPPLEMENT_PROMPT,
    AGENT_INSTITUTION_DB_SUPPLEMENT_PROMPT,
    AGENT_REVISE_PROMPT,
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _resolve_markdown_path(path_value: str) -> Path:
    raw = Path(path_value)
    candidate = raw if raw.is_absolute() else (PROJECT_ROOT / raw)
    resolved = candidate.resolve()
    if not resolved.exists() or resolved.suffix.lower() != ".md":
        raise FileNotFoundError(f"Markdown file not found: {path_value}")
    return resolved


def _env_int(name: str, default: int) -> int:
    try:
        return int((os.environ.get(name) or str(default)).strip())
    except ValueError:
        return default


def _truncate_block(path: str, content: str, max_chars: int) -> str:
    if max_chars <= 0 or len(content) <= max_chars:
        return content
    omitted = len(content) - max_chars
    return (
        f"> 提示：文件 `{path}` 过长，以下仅保留前 **{max_chars}** 字符（约省略 **{omitted}** 字）。完整内容见仓库。\n\n"
        + content[:max_chars]
    )


def _load_markdown_docs(paths: list[str], *, kind: str) -> dict[str, str]:
    """
    kind: 'knowledge' | 'rule' — 使用不同单文件上限与知识库总预算，避免超出 LLM 上下文。
    """
    if kind == "rule":
        per_file = _env_int("TCG_RULE_DOC_MAX_CHARS", 60000)
        total_cap = _env_int("TCG_RULE_DOCS_TOTAL_MAX_CHARS", 120000)
    else:
        per_file = _env_int("TCG_KNOWLEDGE_DOC_MAX_CHARS", 22000)
        total_cap = _env_int("TCG_KNOWLEDGE_TOTAL_MAX_CHARS", 90000)

    output: dict[str, str] = {}
    budget_left = total_cap
    for i, p in enumerate(paths):
        if budget_left <= 0:
            for p2 in paths[i:]:
                output[p2] = (
                    f"> 未注入正文（{kind} 总字符预算已用尽）：`{p2}`\n\n"
                    "请在步骤1减少勾选知识文档，或调大 `.env` 中 `TCG_KNOWLEDGE_TOTAL_MAX_CHARS` / "
                    "`TCG_RULE_DOCS_TOTAL_MAX_CHARS`（仍受模型 token 上限约束）。"
                )
            break
        try:
            raw = _resolve_markdown_path(p).read_text(encoding="utf-8")
        except FileNotFoundError:
            logger.warning("task_tools: %s 文档路径不存在，已跳过: %s", kind, p)
            continue
        cap = min(per_file, budget_left)
        body = _truncate_block(p, raw, cap)
        output[p] = body
        budget_left -= len(body)
    return output


def _finish_reason(msg: Any) -> str | None:
    """OpenAI-compatible APIs set finish_reason to e.g. stop | length."""
    if msg is None:
        return None
    md = getattr(msg, "response_metadata", None) or {}
    if isinstance(md, dict):
        r = md.get("finish_reason")
        if r is not None and str(r).strip():
            return str(r).strip().lower()
    ak = getattr(msg, "additional_kwargs", None) or {}
    if isinstance(ak, dict):
        r = ak.get("finish_reason")
        if r is not None and str(r).strip():
            return str(r).strip().lower()
    return None


def _invoke_llm_with_length_continuation(llm: Any, initial_user_text: str) -> str:
    """
    单次 max_tokens 达到上限时 finish_reason 常为 length，输出会在用例中途截断。
    通过多轮对话续写并拼接，降低「生成到一半」的概率。
    """
    max_extra = _env_int("TCG_MAX_LLM_CONTINUATION_ROUNDS", 15)
    tail_chars = _env_int("TCG_CONTINUATION_TAIL_CHARS", 8000)

    messages: list[BaseMessage] = [HumanMessage(content=initial_user_text)]
    chunks: list[str] = []
    extra_used = 0

    while True:
        msg = llm.invoke(messages)
        text = (msg.content if getattr(msg, "content", None) is not None else "") or ""
        chunks.append(text)
        messages.append(msg)

        reason = _finish_reason(msg)
        if reason != "length":
            break
        if extra_used >= max_extra:
            logger.warning(
                "task_tools: LLM 仍返回 length 但已达 TCG_MAX_LLM_CONTINUATION_ROUNDS=%s，输出可能仍不完整",
                max_extra,
            )
            break

        extra_used += 1
        accumulated = "".join(chunks)
        tail = accumulated[-tail_chars:] if len(accumulated) > tail_chars else accumulated
        follow = (
            "上文为测试用例 Markdown，因单次回复长度限制可能尚未写完。\n"
            "请紧接前文**继续输出后续内容**，要求：\n"
            "1) 不要重复已完整出现的用例标题与正文；\n"
            "2) 若前文最后一行停在半句或半条步骤，请先补完该行再继续；\n"
            "3) 保持相同的 Markdown 结构与用例编号风格；\n"
            "4) 不要输出任何开场白或说明性文字；\n"
            "5) 若确实已全部写完，只输出一行：<!-- GENERATION_COMPLETE -->\n\n"
            "--- 前文尾部（用于衔接） ---\n"
            f"{tail}"
        )
        logger.info(
            "task_tools: 检测到 finish_reason=length，发起第 %s 次续写（tail %s 字符）",
            extra_used,
            len(tail),
        )
        messages.append(HumanMessage(content=follow))

    out = "".join(chunks)
    if "<!-- GENERATION_COMPLETE -->" in out:
        out = out.replace("<!-- GENERATION_COMPLETE -->", "").rstrip()
    return _sanitize_llm_testcase_markdown(out)


_ATX_HEADING_LINE_RE = re.compile(r"^#{1,6}\s+\S")
_LLM_PREAMBLE_LINE_RE = re.compile(
    r"(?:"
    r"^好的[，,].*|"
    r".*测试用例修订专家.*|"
    r".*评审反馈.*|"
    r".*修订后的完整.*测试用例.*|"
    r".*Markdown\s*正文如下.*|"
    r"^以下是.*(?:测试用例|Markdown).*"
    r")",
    re.IGNORECASE,
)


def _sanitize_llm_testcase_markdown(text: str) -> str:
    """Strip LLM conversational preamble; keep Markdown body from first ATX heading."""
    cleaned = _strip_code_fence(text or "")
    if not cleaned.strip():
        return ""
    lines = cleaned.splitlines()
    for i, line in enumerate(lines):
        if _ATX_HEADING_LINE_RE.match(line.strip()):
            return "\n".join(lines[i:]).strip() + "\n"
    kept: list[str] = []
    skipping = True
    for line in lines:
        stripped = line.strip()
        if skipping:
            if not stripped:
                continue
            if _LLM_PREAMBLE_LINE_RE.match(stripped):
                continue
            skipping = False
        kept.append(line)
    body = "\n".join(kept).strip()
    return (body + "\n") if body else cleaned.strip() + "\n"


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


def _safe_json_load(text: str, default: dict) -> dict:
    try:
        return json.loads(_strip_code_fence(text))
    except Exception:
        return default


def load_task_bundle(task_id: str) -> dict:
    conn = get_connection()
    try:
        task_row = conn.execute(f"SELECT * FROM {t.TASKS} WHERE id = ?", (task_id,)).fetchone()
        if task_row is None:
            raise ValueError("Task not found")

        item_rows = conn.execute(
            f"""
            SELECT item_key, item_text, matched_text, confirmed_text, match_source, is_edited
            FROM {t.TASK_CHECK_ITEMS}
            WHERE task_id = ?
            ORDER BY id ASC
            """,
            (task_id,),
        ).fetchall()
    finally:
        conn.close()

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

    selected_knowledge_docs = json_load(task_row["selected_knowledge_docs"], [])
    selected_rule_docs = json_load(task_row["selected_rule_docs"], [])
    generation_options = json_load(task_row["generation_options_json"], {})
    if not isinstance(generation_options, dict):
        generation_options = {}
    req_kind = (task_row["requirement_kind"] or "unknown").strip() or "unknown"
    inferred_kind = (
        generation_options.get("inferred_kind")
        if isinstance(generation_options, dict)
        else None
    )
    if inferred_kind not in ("institution", "channel"):
        inferred_kind = req_kind if req_kind in ("institution", "channel") else "unknown"

    if inferred_kind in ("institution", "channel"):
        from backend.services.integration_matching import (
            apply_biz_knowledge_doc_selection,
            resolve_generation_rule_docs,
        )
        from backend.services.task_service import list_step1_doc_options

        def _final_check_text(row) -> str:
            c = row["confirmed_text"]
            if c is not None and str(c).strip():
                return str(c).strip()
            return str(row["matched_text"] or "").strip()

        check_pairs = [(row["item_text"], _final_check_text(row)) for row in item_rows]
        demo_docs = list_step1_doc_options().get("demo_docs", [])

        selected_knowledge_docs = apply_biz_knowledge_doc_selection(
            selected_knowledge_docs, inferred_kind
        )
        gen_opts = generation_options if isinstance(generation_options, dict) else {}
        req_title = str(gen_opts.get("requirement_title") or "").strip()
        selected_rule_docs = resolve_generation_rule_docs(
            inferred_kind,
            check_pairs,
            demo_docs,
            requirement_markdown=task_row["requirement_markdown"] or "",
            requirement_title=req_title,
        )
    else:
        selected_knowledge_docs = []
        selected_rule_docs = []

    knowledge_docs = (
        _load_markdown_docs(selected_knowledge_docs, kind="knowledge")
        if selected_knowledge_docs
        else {}
    )
    rule_docs = _load_markdown_docs(selected_rule_docs, kind="rule") if selected_rule_docs else {}

    external_doc = (task_row["external_cooperation_markdown"] or "").strip()
    if external_doc:
        knowledge_docs["external_cooperation_markdown"] = external_doc

    return {
        "task_id": task_row["id"],
        "requirement_markdown": task_row["requirement_markdown"] or "",
        "requirement_kind": req_kind,
        "check_items": check_items,
        "knowledge_docs": knowledge_docs,
        "rule_docs": rule_docs,
        "generation_options": generation_options,
    }


def load_single_markdown_doc(path_value: str, *, kind: str = "knowledge") -> str:
    """
    Load one markdown doc with truncation budget, consistent with knowledge/rule doc caps.
    kind: 'knowledge' | 'rule'
    """
    resolved = _resolve_markdown_path(path_value)
    raw = resolved.read_text(encoding="utf-8")
    if kind == "rule":
        cap = _env_int("TCG_RULE_DOC_MAX_CHARS", 60000)
    else:
        # DB 表文档通常更长，默认给更大单文件上限，但仍受模型 token 上限约束
        cap = _env_int("TCG_DB_DOC_MAX_CHARS", 60000)
    return _truncate_block(path_value, raw, cap)


def _truncate_requirement(md: str) -> str:
    cap = _env_int("TCG_REQUIREMENT_MAX_CHARS", 100000)
    if cap <= 0 or len(md) <= cap:
        return md
    omitted = len(md) - cap
    return (
        f"> 提示：需求正文过长，以下仅保留前 **{cap}** 字符（约省略 **{omitted}** 字）。\n\n"
        + md[:cap]
    )


def build_generation_context(bundle: dict) -> str:
    from backend.services.channel_generation_directives import (
        build_channel_mandatory_directives,
    )

    check_lines = []
    for item in bundle["check_items"]:
        final_text = item.confirmed_text if item.confirmed_text is not None else item.matched_text
        # Put values in code spans to discourage rewriting/translation by the LLM.
        value = (final_text or "").strip()
        check_lines.append(f"- {item.item_text}: `{value}`")

    knowledge_text = "\n\n".join(
        [f"## {k}\n{v}" for k, v in bundle["knowledge_docs"].items()]
    ) or "None"
    rule_text = "\n\n".join([f"## {k}\n{v}" for k, v in bundle["rule_docs"].items()]) or "None"
    req = _truncate_requirement(bundle["requirement_markdown"] or "")
    channel_directives = build_channel_mandatory_directives(bundle)

    parts = [
        f"Task ID: {bundle['task_id']}\n",
        "Requirement Markdown:\n",
        f"{req}\n",
        "IMPORTANT:\n",
        "- When referencing any value under “Checklist Confirmed Values”, keep the value EXACTLY as-is.\n",
        "  Do not translate codes to Chinese names, do not normalize synonyms, do not change separators.\n",
        "Checklist Confirmed Values:\n",
        f"{chr(10).join(check_lines) or 'None'}\n",
    ]
    if channel_directives:
        parts.extend(
            [
                channel_directives,
                "IMPORTANT (channel): The section「Channel Mandatory Directives」overrides "
                "conflicting Demo wording for 用信/导下载 scope (e.g. fixed land page vs Nacos-only). "
                "You MUST apply it when writing 用信环节 test cases.\n",
            ]
        )
    parts.extend(
        [
            "Knowledge Docs:\n",
            f"{knowledge_text}\n",
            "Rule Docs (STRUCTURE TEMPLATE — your entire answer must mirror this Markdown outline, "
            "heading levels, section order, and table layouts; fill with this task's requirement, "
            "checklist, and knowledge; do not copy placeholder/example rows verbatim):\n",
            f"{rule_text}\n",
        ]
    )
    return "".join(parts)


def generate_draft(bundle: dict, llm) -> str:
    prompt = AGENT_GENERATE_DRAFT_PROMPT.format(context=build_generation_context(bundle))
    return _invoke_llm_with_length_continuation(llm, prompt)


def evaluate_testcase(testcase_markdown: str, bundle: dict, llm) -> dict:
    check_items_text = "\n".join(
        [
            f"- {item.item_text}: {(item.confirmed_text if item.confirmed_text is not None else item.matched_text) or ''}"
            for item in bundle["check_items"]
        ]
    ) or "None"
    rules_text = "\n\n".join([f"## {k}\n{v}" for k, v in bundle["rule_docs"].items()]) or "None"

    prompt = AGENT_EVALUATE_PROMPT.format(
        check_items=check_items_text,
        rules=rules_text,
        testcases=testcase_markdown,
    )
    content = llm.invoke(prompt).content
    default = {
        "pass": False,
        "score": 0,
        "coverage": {"check_items_hit_rate": 0, "missing_items": []},
        "quality": {
            "clarity": 0,
            "executable": 0,
            "boundary_cases": 0,
            "negative_cases": 0,
            "permission_cases": 0,
        },
        "feedback": ["评估器返回非 JSON，建议人工复核。"],
    }
    result = _safe_json_load(content, default)
    if "score" not in result:
        result["score"] = 0
    if "pass" not in result:
        result["pass"] = False
    if "feedback" not in result or not isinstance(result["feedback"], list):
        result["feedback"] = ["请补充覆盖度和可执行性。"]
    return result


def revise_testcase(testcase_markdown: str, feedback: list[str], bundle: dict, llm) -> str:
    check_items_text = "\n".join(
        [
            f"- {item.item_text}: {(item.confirmed_text if item.confirmed_text is not None else item.matched_text) or ''}"
            for item in bundle["check_items"]
        ]
    ) or "None"
    rules_text = "\n\n".join([f"## {k}\n{v}" for k, v in bundle["rule_docs"].items()]) or "None"

    prompt = AGENT_REVISE_PROMPT.format(
        feedback="\n".join([f"- {x}" for x in feedback]) or "- 无",
        check_items=check_items_text,
        rules=rules_text,
        testcases=testcase_markdown,
    )
    return _invoke_llm_with_length_continuation(llm, prompt)


def supplement_db_testcases(testcase_markdown: str, db_doc_markdown: str, llm) -> str:
    prompt = AGENT_DB_SUPPLEMENT_PROMPT.format(
        db_doc=(db_doc_markdown or "").strip() or "None",
        testcases=(testcase_markdown or "").strip(),
    )
    return _invoke_llm_with_length_continuation(llm, prompt)


def supplement_institution_db_testcases(
    testcase_markdown: str,
    validation_doc_markdown: str,
    flow_tables_doc_markdown: str,
    llm,
    *,
    scope_context: str = "",
) -> str:
    prompt = AGENT_INSTITUTION_DB_SUPPLEMENT_PROMPT.format(
        scope_context=(scope_context or "").strip() or "（未提供范围约束，按全流程处理）",
        validation_doc=(validation_doc_markdown or "").strip() or "None",
        flow_tables_doc=(flow_tables_doc_markdown or "").strip() or "None",
        testcases=(testcase_markdown or "").strip(),
    )
    return _invoke_llm_with_length_continuation(llm, prompt)


def log_agent_run(
    task_id: str, iteration: int, action: str, observation: str, score_json: dict | None = None
) -> None:
    conn = get_connection()
    try:
        conn.execute(
            f"""
            INSERT INTO {t.TASK_AGENT_RUNS} (task_id, iteration, action, observation, score_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                task_id,
                iteration,
                action,
                observation[:3000],
                json.dumps(score_json, ensure_ascii=False) if score_json is not None else None,
                now_utc(),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def save_generated_result(
    task_id: str,
    markdown: str,
    score_report: dict,
    *,
    status: str = "generated",
) -> None:
    conn = get_connection()
    try:
        conn.execute(
            f"""
            UPDATE {t.TASKS}
            SET generated_testcase_markdown = ?, status = ?, updated_at = ?, confirmed_check_items = ?
            WHERE id = ?
            """,
            (
                markdown,
                status,
                now_utc(),
                json.dumps({"agent_score_report": score_report}, ensure_ascii=False),
                task_id,
            ),
        )
        conn.commit()
    finally:
        conn.close()

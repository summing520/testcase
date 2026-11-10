"""
Maintain biz knowledge docs by merging user-confirmed checklist rows
into an auto-managed section.

- Channel requirements -> docs/knowledge/biz/渠道概要信息.md (grouped by 渠道)
- Institution requirements -> docs/knowledge/biz/机构概要信息.md (grouped by 机构)
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REL_PATH_CHANNEL = Path("docs/knowledge/biz/渠道概要信息.md")
REL_PATH_INSTITUTION = Path("docs/knowledge/biz/机构概要信息.md")

MARKER_START = "<!-- channel-knowledge-auto:start -->"
MARKER_END = "<!-- channel-knowledge-auto:end -->"

DEFAULT_HEADER_CHANNEL = """# 渠道概要信息（渠道概况）

<!-- 以下按渠道分组区域在「步骤 2 用户确认检查项并生成用例」后由系统自动更新；同一渠道多任务合并去重。标记区外可手工补充。 -->

"""
DEFAULT_HEADER_INSTITUTION = """# 机构概要信息（机构概况）

<!-- 以下按机构分组区域在「步骤 2 用户确认检查项并生成用例」后由系统自动更新；同一机构多任务合并去重。标记区外可手工补充。 -->

"""


def _doc_path(kind: str) -> Path:
    if kind == "institution":
        return PROJECT_ROOT / REL_PATH_INSTITUTION
    return PROJECT_ROOT / REL_PATH_CHANNEL


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


def _extract_auto_block(full: str) -> str:
    if MARKER_START not in full or MARKER_END not in full:
        return ""
    try:
        _, rest = full.split(MARKER_START, 1)
        inner, _ = rest.split(MARKER_END, 1)
        return inner.strip()
    except ValueError:
        return ""


def _embed_auto_block(prefix: str, auto_body: str) -> str:
    """Ensure markers exist; replace inner with auto_body."""
    body = auto_body.strip()
    block = f"{MARKER_START}\n{body}\n{MARKER_END}\n"
    if MARKER_START in prefix and MARKER_END in prefix:
        pre, rest = prefix.split(MARKER_START, 1)
        _, post = rest.split(MARKER_END, 1)
        return pre.rstrip() + "\n" + block + post.lstrip()
    return prefix.rstrip() + "\n\n" + block


def _ensure_markers(full: str) -> str:
    if MARKER_START in full and MARKER_END in full:
        return full
    inner = _extract_auto_block(full)
    return _embed_auto_block(full, inner)


def _splice_auto_block(full: str, new_inner: str) -> str:
    full = _ensure_markers(full)
    pre, rest = full.split(MARKER_START, 1)
    _, post = rest.split(MARKER_END, 1)
    return (
        pre.rstrip()
        + "\n"
        + MARKER_START
        + "\n"
        + new_inner.strip()
        + "\n"
        + MARKER_END
        + "\n"
        + post.lstrip()
    )


def _build_prompt(
    *,
    kind: str,
    current_auto_markdown: str,
    confirmed_lines: str,
    requirement_excerpt: str,
) -> str:
    if kind == "institution":
        return (
            "你是机构知识库编辑。请把「本次用户确认的检查项」提炼为简洁要点，并按**机构**分组写入 Markdown。\n\n"
            "规则：\n"
            "1) 机构识别：优先用检查项「机构名称」的值作为分组标题；若缺机构名称则用「机构编码」或「机构ID」作标题。\n"
            "2) 每个机构下紧跟一张 Markdown 表：表头固定为 `| 字段 | 内容 |`；"
            "每行一条，第一列用 `**字段名**`，第二列为取值（合并同义表述）。\n"
            "3) 输入中「当前自动区」可能已有多个机构；请在合并后输出**完整**自动区正文："
            "保留仍有效的旧机构内容，对同一机构用新确认信息**更新或补充**（新信息优先），不要无故删除人工可读的结构。\n"
            "4) 不要输出一级标题 `#`；只使用二级 `## 机构…`，其下为上述表格（不要用无序列表承载同一组键值）。\n"
            "5) 不要输出代码围栏；不要输出任何前言或结语。\n\n"
            "--- 当前自动区 Markdown ---\n"
            f"{current_auto_markdown or '（尚无）'}\n\n"
            "--- 本次确认的检查项（原文键值）---\n"
            f"{confirmed_lines}\n\n"
            "--- 需求正文节选（供对齐机构与语境，可略）---\n"
            f"{requirement_excerpt}\n"
        )

    return (
        "你是渠道知识库编辑。请把「本次用户确认的检查项」提炼为简洁要点，并按**渠道**分组写入 Markdown。\n\n"
        "规则：\n"
        "1) 渠道识别：优先用检查项「渠道名称」的值作为分组标题；若有「内部渠道号」，标题写为 "
        "`## {渠道名称}（内部渠道号：xxx）`；若缺渠道名称则用内部渠道号作标题。\n"
        "2) 每个渠道下紧跟一张 Markdown 表：表头固定为 `| 字段 | 内容 |`；"
        "每行一条，第一列用 `**字段名**`，第二列为取值（合并同义表述）。\n"
        "3) 输入中「当前自动区」可能已有多个渠道；请在合并后输出**完整**自动区正文："
        "保留仍有效的旧渠道内容，对同一渠道用新确认信息**更新或补充**（新信息优先），不要无故删除人工可读的结构。\n"
        "4) 不要输出一级标题 `#`；只使用二级 `## 渠道…`，其下为上述表格（不要用无序列表承载同一组键值）。\n"
        "5) 不要输出代码围栏；不要输出任何前言或结语。\n\n"
        "--- 当前自动区 Markdown ---\n"
        f"{current_auto_markdown or '（尚无）'}\n\n"
        "--- 本次确认的检查项（原文键值）---\n"
        f"{confirmed_lines}\n\n"
        "--- 需求正文节选（供对齐渠道与语境，可略）---\n"
        f"{requirement_excerpt}\n"
    )


def refresh_channel_knowledge_file(
    llm,
    requirement_markdown: str,
    confirmed_pairs: list[tuple[str, str]],
    task_id: str,
) -> None:
    """
    Regroup and rewrite the auto section of 渠道概要信息.md using LLM.
    confirmed_pairs: (item_text, final_value).
    """
    if llm is None or not confirmed_pairs:
        return

    path = _doc_path("channel")
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.is_file():
        full = path.read_text(encoding="utf-8")
    else:
        full = DEFAULT_HEADER_CHANNEL

    full = _ensure_markers(full)
    current_inner = _extract_auto_block(full)

    lines = [f"- {k}: {v}" for k, v in confirmed_pairs if (k or "").strip() and (v or "").strip()]
    confirmed_lines = "\n".join(lines)
    if not confirmed_lines:
        return

    req = (requirement_markdown or "").strip()
    if len(req) > 12000:
        req = req[:12000] + "\n\n…（节选截断）"

    prompt = _build_prompt(
        kind="channel",
        current_auto_markdown=current_inner,
        confirmed_lines=confirmed_lines,
        requirement_excerpt=req,
    )

    try:
        result = llm.invoke(prompt)
        raw = result.content if hasattr(result, "content") else str(result)
        new_inner = _strip_code_fence(raw)
        if not new_inner.strip():
            logger.warning("channel_knowledge_doc: empty LLM output, task_id=%s", task_id)
            return
        out = _splice_auto_block(full, new_inner)
        path.write_text(out, encoding="utf-8", newline="\n")
    except Exception as exc:
        logger.warning("channel_knowledge_doc: update failed task_id=%s err=%s", task_id, exc)


def refresh_institution_knowledge_file(
    llm,
    requirement_markdown: str,
    confirmed_pairs: list[tuple[str, str]],
    task_id: str,
) -> None:
    """
    Regroup and rewrite the auto section of 机构概要信息.md using LLM.
    confirmed_pairs: (item_text, final_value).
    """
    if llm is None or not confirmed_pairs:
        return

    path = _doc_path("institution")
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.is_file():
        full = path.read_text(encoding="utf-8")
    else:
        full = DEFAULT_HEADER_INSTITUTION

    full = _ensure_markers(full)
    current_inner = _extract_auto_block(full)

    lines = [f"- {k}: {v}" for k, v in confirmed_pairs if (k or "").strip() and (v or "").strip()]
    confirmed_lines = "\n".join(lines)
    if not confirmed_lines:
        return

    req = (requirement_markdown or "").strip()
    if len(req) > 12000:
        req = req[:12000] + "\n\n…（节选截断）"

    prompt = _build_prompt(
        kind="institution",
        current_auto_markdown=current_inner,
        confirmed_lines=confirmed_lines,
        requirement_excerpt=req,
    )

    try:
        result = llm.invoke(prompt)
        raw = result.content if hasattr(result, "content") else str(result)
        new_inner = _strip_code_fence(raw)
        if not new_inner.strip():
            logger.warning("channel_knowledge_doc: empty LLM output, task_id=%s", task_id)
            return
        out = _splice_auto_block(full, new_inner)
        path.write_text(out, encoding="utf-8", newline="\n")
    except Exception as exc:
        logger.warning("channel_knowledge_doc: update failed task_id=%s err=%s", task_id, exc)

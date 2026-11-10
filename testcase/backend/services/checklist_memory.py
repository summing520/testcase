from __future__ import annotations

import hashlib
import json
import re

from backend.db import tables as t
from backend.db.connection import get_connection, now_utc

_CHANNEL_ENTITY_LABELS = ("内部渠道号",)
_INSTITUTION_ENTITY_LABELS = ("机构产品代码", "产品代码")
_HUB_CODE_PATTERN = re.compile(r"HUB_[A-Z0-9_]+", re.IGNORECASE)


def checklist_fingerprint(checklist_doc_paths: list[str]) -> str:
    """Stable id for the selected checklist file set (order-independent). Legacy fallback."""
    normalized = sorted((p or "").replace("\\", "/").strip() for p in checklist_doc_paths if p and str(p).strip())
    raw = json.dumps(normalized, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _label_matches(item_text: str, labels: tuple[str, ...]) -> bool:
    t = (item_text or "").strip()
    if not t:
        return False
    for label in labels:
        if t == label or label in t:
            return True
    return False


def _normalize_channel_entity(value: str) -> str:
    v = (value or "").strip()
    if not v:
        return ""
    match = _HUB_CODE_PATTERN.search(v)
    if match:
        return match.group(0).upper()
    return v.upper()


def _normalize_institution_entity(value: str) -> str:
    v = (value or "").strip().strip("`\"'")
    if not v:
        return ""
    return v.lower()


def _extract_from_markdown(kind: str, markdown: str) -> str | None:
    md = markdown or ""
    if not md.strip():
        return None

    if kind == "channel":
        for label in _CHANNEL_ENTITY_LABELS:
            match = re.search(
                rf"{re.escape(label)}\s*[:：=]\s*[`\"']?(HUB_[A-Za-z0-9_]+)",
                md,
                re.IGNORECASE,
            )
            if match:
                return _normalize_channel_entity(match.group(1))
        hub = _HUB_CODE_PATTERN.search(md)
        if hub:
            return _normalize_channel_entity(hub.group(0))
        return None

    if kind == "institution":
        for label in _INSTITUTION_ENTITY_LABELS:
            match = re.search(
                rf"{re.escape(label)}\s*[:：=]\s*[`\"']?([A-Za-z0-9_]+)",
                md,
                re.IGNORECASE,
            )
            if match:
                normalized = _normalize_institution_entity(match.group(1))
                if normalized and normalized not in ("osi", "api", "h5"):
                    return normalized
        return None

    return None


def extract_memory_entity_key(
    kind: str,
    *,
    check_items: list[tuple[str, str]] | None = None,
    requirement_markdown: str = "",
) -> str | None:
    """
    渠道对接：内部渠道号（HUB_*）；机构对接：机构产品代码。
    优先使用已确认/匹配的检查项，其次从需求 Markdown 抽取。
    """
    if kind == "channel":
        normalize = _normalize_channel_entity
        labels = _CHANNEL_ENTITY_LABELS
    elif kind == "institution":
        normalize = _normalize_institution_entity
        labels = _INSTITUTION_ENTITY_LABELS
    else:
        return None

    for item_text, value in check_items or []:
        if not _label_matches(item_text, labels):
            continue
        normalized = normalize(value)
        if normalized:
            return normalized

    return _extract_from_markdown(kind, requirement_markdown)


def memory_entity_label(kind: str) -> str:
    if kind == "channel":
        return "内部渠道号"
    if kind == "institution":
        return "机构产品代码"
    return "实体标识"


def checklist_memory_fingerprint(
    kind: str,
    entity_key: str | None,
    checklist_doc_paths: list[str] | None = None,
) -> str:
    """
    机构/渠道对接：以业务实体（机构产品代码 / 内部渠道号）为记忆维度；
    其它类型或缺少实体标识时回退为检查清单文件集合指纹。
    """
    key = (entity_key or "").strip()
    if kind in ("institution", "channel") and key:
        payload = {"kind": kind, "entity": key}
        raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return checklist_fingerprint(checklist_doc_paths or [])


def load_memory_for_items(fingerprint: str, item_texts: list[str]) -> dict[str, str]:
    if not fingerprint or not item_texts:
        return {}
    conn = get_connection()
    try:
        placeholders = ",".join("?" * len(item_texts))
        rows = conn.execute(
            f"""
            SELECT item_text, remembered_value
            FROM {t.CHECKLIST_ITEM_MEMORY}
            WHERE checklist_fingerprint = ? AND item_text IN ({placeholders})
            """,
            (fingerprint, *item_texts),
        ).fetchall()
    finally:
        conn.close()
    out: dict[str, str] = {}
    for row in rows:
        v = (row["remembered_value"] or "").strip()
        if v:
            out[row["item_text"]] = row["remembered_value"]
    return out


def upsert_checklist_item_memories(
    fingerprint: str, item_text_to_value: list[tuple[str, str]], source_task_id: str
) -> None:
    if not fingerprint or not item_text_to_value:
        return
    conn = get_connection()
    try:
        for item_text, value in item_text_to_value:
            if not item_text or not str(item_text).strip():
                continue
            v = (value or "").strip()
            if not v:
                continue
            conn.execute(
                f"""
                INSERT INTO {t.CHECKLIST_ITEM_MEMORY} (
                    checklist_fingerprint, item_text, remembered_value, source_task_id, updated_at
                ) VALUES (?, ?, ?, ?, ?)
                ON DUPLICATE KEY UPDATE
                    remembered_value = VALUES(remembered_value),
                    source_task_id = VALUES(source_task_id),
                    updated_at = VALUES(updated_at)
                """,
                (fingerprint, item_text.strip(), v, source_task_id, now_utc()),
            )
        conn.commit()
    finally:
        conn.close()

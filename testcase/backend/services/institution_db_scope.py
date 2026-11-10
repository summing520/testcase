"""
机构对接落库数据测试用例范围：依据流程模式、接口文档总览与已生成用例章节，
判定《机构对接落表数据验证项》中哪些业务环节须生成落库用例。
"""
from __future__ import annotations

import re
from typing import Iterable

from backend.services.integration_matching import (
    _is_borrow_repay_h5,
    _is_full_flow_api,
    _is_half_flow,
    _normalize_flow_text,
    collect_flow_mode_text,
    osi_interface_path_from_flow,
)

INSTITUTION_DB_VALIDATION_STAGES: tuple[str, ...] = ("准入", "授信", "绑卡", "提现", "还款")


def _final_check_item_text(item_text: str, confirmed: str | None, matched: str | None) -> str:
    if confirmed is not None and str(confirmed).strip():
        return str(confirmed).strip()
    return str(matched or "").strip()


def check_items_to_pairs(check_items: Iterable) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in check_items or []:
        confirmed = getattr(item, "confirmed_text", None)
        matched = getattr(item, "matched_text", None)
        item_text = getattr(item, "item_text", "") or ""
        value = _final_check_item_text(item_text, confirmed, matched)
        if value or item_text:
            pairs.append((item_text, value))
    return pairs


def institutions_db_stages_from_flow(normalized_flow: str) -> set[str]:
    """流程概要 → 默认落库验证环节（与《机构业务规则》三、流程概要一致）。"""
    if _is_half_flow(normalized_flow):
        return {"准入", "授信"}
    if _is_borrow_repay_h5(normalized_flow):
        return set(INSTITUTION_DB_VALIDATION_STAGES)
    if _is_full_flow_api(normalized_flow):
        return set(INSTITUTION_DB_VALIDATION_STAGES)
    # 未识别流程时保守取全流程；后续由接口总览 / 已生成用例收窄。
    return set(INSTITUTION_DB_VALIDATION_STAGES)


def parse_interface_overview_stages(interface_md: str) -> set[str]:
    """从对接文档「接口总览」表格解析涉及的业务环节。"""
    text = (interface_md or "").strip()
    if not text:
        return set()

    stages: set[str] = set()
    in_overview = False
    saw_table = False

    for line in text.splitlines():
        if re.search(r"接口总览", line):
            in_overview = True
            continue
        if not in_overview:
            continue

        stripped = line.strip()
        if stripped.startswith("## ") and "接口总览" not in stripped:
            if saw_table:
                break
            continue
        if stripped.startswith("# ") and saw_table:
            break
        if not stripped.startswith("|"):
            if saw_table and stripped.startswith("##"):
                break
            continue

        cols = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cols) < 2:
            continue
        if cols[0] in ("接口类型", "---", "") or re.match(r"^[-:\s|]+$", stripped):
            continue

        saw_table = True
        biz_stage = cols[1] if len(cols) > 1 else ""
        iface_name = cols[2] if len(cols) > 2 else ""
        combined = f"{biz_stage} {iface_name}"

        if "准入授信" in biz_stage or "准入" in combined:
            stages.add("准入")
            stages.add("授信")
            continue
        if biz_stage == "通用" or biz_stage.startswith("通用"):
            if any(k in combined for k in ("额度", "授信", "协议")):
                stages.add("授信")
            continue
        if "绑卡" in combined:
            stages.add("绑卡")
            continue
        if "借款" in biz_stage or any(
            k in combined for k in ("借款", "放款", "借据", "试算", "提现")
        ):
            stages.add("提现")
            continue
        if "还款" in combined:
            stages.add("还款")

    return stages


def infer_db_stages_from_testcase_markdown(md: str, normalized_flow: str) -> set[str]:
    """从已生成的接口流程用例章节标题推断涉及环节。"""
    text = (md or "").strip()
    if not text:
        return set()

    stages: set[str] = set()
    half_flow = _is_half_flow(normalized_flow)

    for header in re.findall(r"^#{2,3}\s+(.+)$", text, re.MULTILINE):
        h = header.strip()
        if not h:
            continue

        if any(k in h for k in ("准入", "撞库")):
            stages.add("准入")
        if "授信" in h:
            stages.add("授信")

        if half_flow and ("导下载" in h or "出额导下载" in h):
            continue

        if "绑卡" in h:
            stages.add("绑卡")
        if any(k in h for k in ("用信", "借款", "提现", "放款")) and "导下载" not in h:
            stages.add("提现")
        if "还款" in h:
            stages.add("还款")

    return stages


def resolve_institution_db_validation_scope(
    *,
    check_items: Iterable,
    requirement_markdown: str = "",
    requirement_title: str = "",
    external_cooperation_markdown: str = "",
    generated_testcase_markdown: str = "",
) -> dict:
    """
    返回落库验证范围：
    - included_stages / excluded_stages
    - flow_mode_text / normalized_flow
    - scope_summary：供 LLM prompt 使用的说明文本
    """
    pairs = check_items_to_pairs(check_items)
    flow_raw = collect_flow_mode_text(
        "institution",
        pairs,
        requirement_markdown=requirement_markdown,
        requirement_title=requirement_title,
    )
    normalized = _normalize_flow_text(flow_raw)

    flow_stages = institutions_db_stages_from_flow(normalized)
    iface_stages = parse_interface_overview_stages(external_cooperation_markdown)
    testcase_stages = infer_db_stages_from_testcase_markdown(
        generated_testcase_markdown, normalized
    )

    signals: list[set[str]] = [flow_stages]
    if iface_stages:
        signals.append(iface_stages)
    if testcase_stages:
        signals.append(testcase_stages)

    included = set.intersection(*signals) if len(signals) > 1 else set(flow_stages)
    if not included:
        included = flow_stages

    included_ordered = [s for s in INSTITUTION_DB_VALIDATION_STAGES if s in included]
    excluded = [s for s in INSTITUTION_DB_VALIDATION_STAGES if s not in included]

    flow_label = _flow_mode_label(normalized)
    iface_hint = "、".join(sorted(iface_stages)) if iface_stages else "（未能从接口文档解析）"
    tc_hint = "、".join(sorted(testcase_stages)) if testcase_stages else "（未能从已生成用例解析）"

    summary_lines = [
        f"- 流程概要识别：{flow_label or '未识别'}",
        f"- 流程默认落库环节：{'、'.join(s for s in INSTITUTION_DB_VALIDATION_STAGES if s in flow_stages)}",
        f"- 接口文档总览涉及环节：{iface_hint}",
        f"- 已生成接口用例涉及环节：{tc_hint}",
        f"- **本次须生成落库用例的环节**：{'、'.join(included_ordered) or '无'}",
    ]
    if excluded:
        summary_lines.append(
            f"- **本次勿生成的落库环节**（流程/接口/用例均未覆盖）：{'、'.join(excluded)}"
        )

    return {
        "included_stages": included_ordered,
        "excluded_stages": excluded,
        "flow_mode_text": flow_raw,
        "normalized_flow": normalized,
        "scope_summary": "\n".join(summary_lines),
        "interface_doc_path": osi_interface_path_from_flow(flow_raw),
    }


def _flow_mode_label(normalized_flow: str) -> str:
    if _is_half_flow(normalized_flow):
        return "半流程 · 出额导下载"
    if _is_borrow_repay_h5(normalized_flow):
        return "授信 API + 提现/还款 H5"
    if _is_full_flow_api(normalized_flow):
        return "全流程 API"
    if normalized_flow:
        return normalized_flow[:120]
    return ""

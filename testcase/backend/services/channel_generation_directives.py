"""
渠道对接生成用例时的可执行业务约束（由《渠道业务规则》等推导，注入 Agent 上下文）。
"""
from __future__ import annotations

import re
from typing import Iterable

from backend.services.integration_matching import (
    _is_half_flow,
    _item_value_fuzzy,
    _normalize_flow_text,
    collect_flow_mode_text,
)

# 着陆页 URL 形态（《渠道业务规则》五）
_LAND_PAGE_MARKERS = (
    "land/uni/fenqi",
    "/land/uni/",
    "xurongwl.com/land",
)

_FIXED_LINK_POSITIVE = (
    "固定下载链接",
    "本地配置下载链接",
    "本地配置下载",
    "python后台生成的着陆页",
    "python后台生成着陆页",
    "着陆页地址",
    "无需对接提现",
    "不对接提现",
    "不对接提现相关",
    "无提现接口",
)

def _normalize_corpus(*parts: str) -> str:
    return (
        "\n".join(p for p in parts if p)
        .lower()
        .replace("\u3000", "")
        .replace(" ", "")
    )


def _check_item_pairs_from_bundle(check_items: Iterable) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for item in check_items:
        label = (getattr(item, "item_text", None) or "").strip()
        confirmed = getattr(item, "confirmed_text", None)
        matched = getattr(item, "matched_text", None)
        value = (
            str(confirmed).strip()
            if confirmed is not None and str(confirmed).strip()
            else str(matched or "").strip()
        )
        if label:
            pairs.append((label, value))
    return pairs


def _demo_rule_text_from_bundle(rule_docs: dict[str, str]) -> str:
    for path, body in (rule_docs or {}).items():
        if "docs/demo/" in path.replace("\\", "/") or "/Demo-" in path:
            return body or ""
    return ""


def infer_uses_fixed_download_link(
    *,
    requirement_markdown: str = "",
    external_markdown: str = "",
    check_items: list[tuple[str, str]] | None = None,
    demo_rule_text: str = "",
) -> tuple[bool | None, list[str]]:
    """
    判定是否使用「本地配置的固定下载链接」（《渠道业务规则》第五章）。
    返回 (True/False/None, 判定依据摘要列表)。
    """
    check_items = check_items or []
    extra_values: list[str] = []
    for label, value in check_items:
        if not value:
            continue
        extra_values.append(value)
        if "固定下载链接" in label or "是否使用固定" in label:
            v = value.strip().lower()
            if v in ("是", "yes", "y", "true", "1", "使用", "有"):
                return True, [f"检查项「{label}」= {value}"]
            if v in ("否", "no", "n", "false", "0", "不使用", "无"):
                return False, [f"检查项「{label}」= {value}"]

    corpus = _normalize_corpus(
        requirement_markdown,
        external_markdown,
        demo_rule_text,
        *extra_values,
    )
    if not corpus:
        return None, []

    evidence: list[str] = []
    for marker in _LAND_PAGE_MARKERS:
        if marker.replace("/", "").lower() in corpus or marker.lower() in corpus:
            evidence.append(f"着陆页路径特征: {marker}")
    for phrase in _FIXED_LINK_POSITIVE:
        if phrase.replace(" ", "").lower() in corpus:
            evidence.append(f"需求/规则关键词: {phrase}")

    if evidence:
        return True, evidence

    neg_hits: list[str] = []
    if "查询场景页面地址" in corpus:
        neg_hits.append("对接查询场景页面地址（动态获取下载页）")
    if "hubchannelconfig" in corpus and "本地配置下载" not in corpus:
        neg_hits.append("仅 Nacos hubChannelConfig 动态配置下载链接")
    if neg_hits and "本地配置下载" not in corpus and not any(
        m in corpus for m in ("land/uni", "xurongwl.com/land")
    ):
        return False, neg_hits

    if "本地配置下载链接" in (demo_rule_text or ""):
        return True, ["参照 Demo 骨架：授信通过后本地配置下载链接"]

    return None, []


def _extract_land_page_example(text: str) -> str | None:
    m = re.search(
        r"https?://[^\s\)\]\"']+/land/uni/[^\s\)\]\"']+",
        text or "",
        re.IGNORECASE,
    )
    return m.group(0) if m else None


def build_channel_mandatory_directives(bundle: dict) -> str:
    """为渠道对接任务构建须写入生成上下文的强制约束（非仅依赖模型读规则文档）。"""
    gen_opts = bundle.get("generation_options") or {}
    if not isinstance(gen_opts, dict):
        gen_opts = {}
    if gen_opts.get("inferred_kind") != "channel":
        return ""

    check_pairs = _check_item_pairs_from_bundle(bundle.get("check_items") or [])
    requirement_md = bundle.get("requirement_markdown") or ""
    external_md = (bundle.get("knowledge_docs") or {}).get(
        "external_cooperation_markdown", ""
    )
    demo_text = _demo_rule_text_from_bundle(bundle.get("rule_docs") or {})

    flow_raw = collect_flow_mode_text(
        "channel",
        check_pairs,
        requirement_markdown=requirement_md,
        requirement_title=str(gen_opts.get("requirement_title") or ""),
    )
    half_flow = _is_half_flow(_normalize_flow_text(flow_raw))

    uses_fixed, evidence = infer_uses_fixed_download_link(
        requirement_markdown=requirement_md,
        external_markdown=external_md,
        check_items=check_pairs,
        demo_rule_text=demo_text,
    )

    td_channel = _item_value_fuzzy(check_pairs, "外部获客渠道编号")
    internal_hub = _item_value_fuzzy(check_pairs, "内部渠道号")
    channel_name = _item_value_fuzzy(check_pairs, "渠道名称")

    land_example = (
        _extract_land_page_example(requirement_md)
        or _extract_land_page_example(external_md)
        or _extract_land_page_example(demo_text)
    )

    lines: list[str] = [
        "## Channel Mandatory Directives（渠道生成强制约束）",
        "",
        "以下约束由系统根据《渠道业务规则》第五章「用信环节」及检查项/需求正文自动判定，"
        "**优先级高于 Rule Docs 中 Demo 骨架与之冲突的表述**（须按本段改写用信章节，不得忽略）。",
        "",
    ]

    if uses_fixed is True:
        lines.extend(
            [
                "### 判定：使用固定下载链接（是）",
                f"- 依据：{'；'.join(evidence[:5])}",
                "",
                "### 用信环节须覆盖（必须写入用例）",
                "1. 授信结果 `PASS` 且额度有效后，HUB/渠道侧返回 **本地配置的固定着陆页下载链接**（非「查询场景页面地址」类动态接口）。",
            ]
        )
        if land_example:
            lines.append(
                f"2. 验证下载链接形态与参数：示例 `{land_example}`；须含 `cvv`、`td_channelid` 等渠道参数且与环境一致。"
            )
        else:
            lines.append(
                "2. 验证下载链接为 Python 后台生成的着陆页（路径含 `/land/uni/fenqi`），"
                "参数含 `cvv`、`td_channelid`；`td_channelid` 与检查项「外部获客渠道编号」一致。"
            )
        if td_channel:
            lines.append(f"3. 检查项「外部获客渠道编号」= `{td_channel}`，用例中链接参数须与此一致。")
        if internal_hub:
            lines.append(f"4. 内部渠道号 `{internal_hub}` 与 Widek/Nacos 渠道配置一致。")
        lines.extend(
            [
                "5. 异常：未配置/错误链接时不出现空白页或错误域名；渠道侧有明确提示。",
                "",
                "### 禁止编写（必须删除或标「不涉及」）",
                "- HUB 侧 **提现/用信 API**：试算、绑卡、借款提交、放款查询、还款计划、还款试算等。",
                "- 勿将 Demo 中「Nacos hubChannelConfig 动态拼装下载链接」作为本渠道主路径（本渠道为固定着陆页）。",
                "- 勿编写「查询场景页面地址」接口联调用例（本渠道不对接）。",
            ]
        )
        if half_flow:
            lines.append(
                "- 半流程：借还在乐享借 APP 内，HUB 借还款接口章节标「不涉及」或删章（与《渠道业务规则》第六章一致）。"
            )
    elif uses_fixed is False:
        lines.extend(
            [
                "### 判定：使用固定下载链接（否）",
                f"- 依据：{'；'.join(evidence[:5])}",
                "- 用信/导下载按动态配置或接口文档（如 Nacos、查询场景页面地址）编写，勿强行套用固定着陆页模板。",
            ]
        )
        if half_flow:
            lines.extend(
                [
                    "",
                    "### 半流程补充（仍适用）",
                    "- 授信 `PASS` 后验证导下载入口与乐享借 APP 下载链接（Nacos/运营配置）。",
                    "- **禁止** HUB 侧试算、绑卡、借款提交、还款计划等借还款接口用例。",
                ]
            )
    else:
        if not half_flow:
            return ""
        lines.extend(
            [
                "### 判定：固定下载链接（未从需求明确识别）",
                "- 已识别为半流程/出额导下载；默认按《渠道业务规则》第六章编写导下载用例。",
                "- 若需求或对接文档写明「本地配置下载链接」「land/uni/fenqi」着陆页，则按固定链接模式改写用信章节并排除提现 API。",
                "",
                "### 半流程强制约束",
                "- **禁止** HUB 侧试算、绑卡、借款提交、还款计划等借还款接口用例。",
            ]
        )
        if channel_name or internal_hub:
            lines.append(
                f"- 渠道：{channel_name or '（见检查项）'}，内部渠道号：{internal_hub or '（见检查项）'}。"
            )

    return "\n".join(lines).strip() + "\n"

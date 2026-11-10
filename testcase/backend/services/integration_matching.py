"""
机构对接 / 渠道对接识别，以及接口文档、Demo 规则文档的匹配逻辑。
供 task_service 与前端工作台保持同一套规则。
"""
from __future__ import annotations

import re
from typing import Iterable

RequirementKind = str  # "institution" | "channel" | "unknown"

OSI_INTERFACE_FULL = "docs/knowledge/interface/OSI标准机构对接-接口文档.md"
OSI_INTERFACE_HALF_FLOW = "docs/knowledge/interface/OSI标准机构对接-半流程导下载-接口文档.md"
HOMO_INTERFACE = "docs/knowledge/interface/HOMO标准渠道对接-接口文档.md"
HOMO_INTERFACE_HALF = "docs/knowledge/interface/HOMO标准渠道对接-半流程导下载-接口文档.md"
HOMO_INTERFACE_FULL_API = "docs/knowledge/interface/HOMO标准渠道对接-全流程API-接口文档.md"
HOMO_INTERFACE_BORROW_H5 = "docs/knowledge/interface/HOMO标准渠道对接-借还H5-接口文档.md"

DEMO_CHANNEL_HALF = "docs/demo/Demo-标准渠道-半流程导下载-对接测试用例.md"
DEMO_CHANNEL_FULL_API = "docs/demo/Demo-标准渠道-全流程API对接-测试用例.md"
DEMO_INST_HALF = "docs/demo/Demo-标准机构-半流程导下载-测试用例.md"
DEMO_INST_BORROW_REPAY_H5 = "docs/demo/Demo-标准机构-借还H5-测试用例.md"

CHANNEL_CHECKLIST_DOC = "docs/checklist/渠道需求检查项.md"
INSTITUTION_CHECKLIST_DOC = "docs/checklist/机构需求检查项.md"
INSTITUTION_BIZ_PROFILE_DOC = "docs/knowledge/biz/机构概要信息.md"
CHANNEL_BIZ_PROFILE_DOC = "docs/knowledge/biz/渠道概要信息.md"
INSTITUTION_BIZ_RULES_DOC = "docs/rules/机构业务规则.md"
CHANNEL_BIZ_RULES_DOC = "docs/rules/渠道业务规则.md"
BIZ_TERMS_DOC = "docs/knowledge/biz/业务术语.md"

_INSTITUTION_CHECK_LABELS = frozenset(
    {
        "类型",
        "是否标准机构",
        "机构编码",
        "机构名称",
        "机构ID",
        "机构产品代码",
        "产品代码",
        "fundCode",
    }
)
_CHANNEL_CHECK_LABELS = frozenset(
    {
        "接口文档提供方",
        "内部渠道号",
        "渠道名称",
        "渠道流程模式",
        "渠道合作方",
        "外部获客渠道编号",
    }
)


def _normalize_flow_text(text: str) -> str:
    return (
        str(text or "")
        .lower()
        .replace("\u3000", "")
        .replace(" ", "")
        .replace("+", "")
    )


def _is_half_flow(normalized: str) -> bool:
    if not normalized:
        return False
    # 含「半流程」时优先于同段中的「全流程 API」字样（如检查项模板多选项并存）
    if "半流程" in normalized or "半流程导下载" in normalized:
        return True
    if "出额导下载" in normalized or "预授信导下载" in normalized:
        return True
    if "出额" in normalized and "导下载" in normalized:
        return True
    if "导下载" in normalized:
        if _is_full_flow_api(normalized) and "半流程" not in normalized and "出额" not in normalized:
            return False
        return True
    return False


def _is_borrow_repay_h5(normalized: str) -> bool:
    if not normalized:
        return False
    return (
        "借还h5" in normalized
        or "提现/还款h5" in normalized
        or "提现还款h5" in normalized
        or "还款h5" in normalized
        or ("借还" in normalized and "h5" in normalized)
        or ("全流程" in normalized and "借还" in normalized and "h5" in normalized)
    )


def _is_full_flow_api(normalized: str) -> bool:
    if not normalized:
        return False
    return ("全流程" in normalized and "api" in normalized) or "全流程api" in normalized


def _pick_title_hint(title: str | None, parts: Iterable[str]) -> str:
    explicit = (title or "").strip()
    if explicit:
        return explicit
    for p in parts:
        ps = str(p or "").strip()
        if not ps or ps.startswith("http") or len(ps) > 400:
            continue
        if "机构对接" in ps or "渠道对接" in ps:
            return ps
    return ""


def _hub_signals_channel_integration(md: str) -> bool:
    """「上线范围：APP、HUB」等为投放范围，不等同于 HUB 渠道对接。"""
    if re.search(r"HUB_[A-Z0-9]+", md, re.IGNORECASE):
        return True
    if "内部渠道号" in md or "渠道流程模式" in md or "HUB渠道" in md:
        return True
    if re.search(r"上线范围[：:]\s*APP[、,]\s*HUB", md):
        return False
    return False


def _resolve_when_both_phrases_present(md: str, title_text: str) -> RequirementKind:
    if title_text:
        if "机构对接" in title_text and "渠道对接" not in title_text:
            return "institution"
        if "渠道对接" in title_text and "机构对接" not in title_text:
            return "channel"

    institution_markers = (
        "产品code",
        "机构编码",
        "机构名称",
        "机构概要",
        "机构概况",
        "流程概要",
        "机构产品",
        "机构ID",
        "OSI标准机构",
        "标准机构",
    )
    if any(marker in md for marker in institution_markers):
        return "institution"
    if "内部渠道号" in md or "渠道流程模式" in md or _hub_signals_channel_integration(md):
        return "channel"
    return "institution"


def infer_kind_from_texts(*parts: str, title: str | None = None) -> RequirementKind:
    """从飞书标题（优先）、需求正文、链接识别机构/渠道对接。"""
    title_text = _pick_title_hint(title, parts)
    if title_text:
        if "机构对接" in title_text and "渠道对接" not in title_text:
            return "institution"
        if "渠道对接" in title_text and "机构对接" not in title_text:
            return "channel"

    combined = "\n".join(str(p or "") for p in parts if p is not None)
    md = combined
    if not md.strip():
        return "unknown"

    text = md.lower()

    if "机构对接" in md and "渠道对接" not in md:
        return "institution"
    if "渠道对接" in md and "机构对接" not in md:
        return "channel"
    if "机构对接" in md and "渠道对接" in md:
        return _resolve_when_both_phrases_present(md, title_text)

    channel_hits = 0
    if _hub_signals_channel_integration(md):
        channel_hits += 3
    if "内部渠道号" in md or "渠道流程模式" in md:
        channel_hits += 3
    if "对接渠道" in md:
        channel_hits += 3
    if "渠道名称" in md or "渠道合作方" in md:
        channel_hits += 2

    institution_hits = 0
    if "osi标准机构" in text or "OSI标准机构" in md:
        institution_hits += 3
    if "标准机构" in md and "非标准机构" not in md:
        institution_hits += 2
    if "机构对接" in md or "机构编码" in md or "fundcode" in text:
        institution_hits += 4
    if "机构概要" in md or "机构概况" in md:
        institution_hits += 2
    if "流程概要" in md or "流程摘要" in md or "产品code" in md:
        institution_hits += 2
    if re.search(r"机构(对接|编码|名称|产品)", md):
        institution_hits += 2

    if channel_hits == 0 and institution_hits == 0:
        return "unknown"
    if channel_hits > institution_hits:
        return "channel"
    if institution_hits > channel_hits:
        return "institution"
    return "unknown"


def infer_kind_from_markdown(requirement_markdown: str) -> RequirementKind:
    return infer_kind_from_texts(requirement_markdown)


def default_checklist_doc_for_kind(kind: str) -> str | None:
    if kind == "channel":
        return CHANNEL_CHECKLIST_DOC
    if kind == "institution":
        return INSTITUTION_CHECKLIST_DOC
    return None


def default_biz_profile_doc_for_kind(kind: str) -> str | None:
    if kind == "channel":
        return CHANNEL_BIZ_PROFILE_DOC
    if kind == "institution":
        return INSTITUTION_BIZ_PROFILE_DOC
    return None


def default_biz_rules_doc_for_kind(kind: str) -> str | None:
    if kind == "channel":
        return CHANNEL_BIZ_RULES_DOC
    if kind == "institution":
        return INSTITUTION_BIZ_RULES_DOC
    return None


def _norm_path(path: str) -> str:
    return (path or "").replace("\\", "/").strip()


def apply_biz_knowledge_doc_selection(
    selected_paths: list[str] | None,
    kind: str,
) -> list[str]:
    """生成用例时注入的业务知识（biz 目录）：默认含《业务术语》，不含已迁至 rules 的业务规则。"""
    result: list[str] = []
    seen: set[str] = set()
    for raw in selected_paths or []:
        p = _norm_path(raw)
        if not p or p in seen:
            continue
        seen.add(p)
        result.append(p)

    terms = _norm_path(BIZ_TERMS_DOC)
    if terms not in seen:
        result.insert(0, terms)

    return result


def filter_demo_docs(kind: str, demo_docs: list[str]) -> list[str]:
    """docs/demo 目录下的 Demo 用例骨架列表。"""
    demo = [
        p
        for p in demo_docs
        if _norm_path(p).startswith("docs/demo/")
        and "/Demo-" in _norm_path(p)
        and "HUB渠道对接测试用例骨架" not in p
    ]
    if kind == "channel":
        filtered = [p for p in demo if "渠道" in p.split("/")[-1]]
        return filtered or demo
    if kind == "institution":
        filtered = [p for p in demo if "机构" in p.split("/")[-1]]
        return filtered or demo
    return demo


def infer_demo_doc_path(
    kind: str,
    check_items: list[tuple[str, str]],
    demo_docs: list[str],
    *,
    requirement_markdown: str = "",
    requirement_title: str = "",
) -> str | None:
    if kind not in ("institution", "channel"):
        return None

    flow = collect_flow_mode_text(
        kind,
        check_items,
        requirement_markdown=requirement_markdown,
        requirement_title=requirement_title,
    )
    n = _normalize_flow_text(flow)

    preferred_full: str | None
    if kind == "channel":
        preferred_full = DEMO_CHANNEL_HALF if _is_half_flow(n) else DEMO_CHANNEL_FULL_API
    else:
        preferred_full = DEMO_INST_HALF if _is_half_flow(n) else DEMO_INST_BORROW_REPAY_H5

    catalog = filter_demo_docs(kind, demo_docs)
    preferred_name = preferred_full.split("/")[-1]
    for path in catalog:
        if _norm_path(path).endswith(preferred_name):
            return path
    return None


def resolve_generation_rule_docs(
    kind: str,
    check_items: list[tuple[str, str]],
    demo_docs: list[str],
    *,
    requirement_markdown: str = "",
    requirement_title: str = "",
) -> list[str]:
    """
    生成用例时的 Rule Docs：先 Demo 骨架（章节结构），后业务规则（测什么/不测什么）。
    """
    result: list[str] = []
    seen: set[str] = set()

    demo_path = infer_demo_doc_path(
        kind,
        check_items,
        demo_docs,
        requirement_markdown=requirement_markdown,
        requirement_title=requirement_title,
    )
    if demo_path:
        dp = _norm_path(demo_path)
        result.append(dp)
        seen.add(dp)

    biz_path = default_biz_rules_doc_for_kind(kind)
    if biz_path:
        bp = _norm_path(biz_path)
        if bp not in seen:
            result.append(bp)
            seen.add(bp)

    return result


def apply_rule_doc_selection(
    selected_paths: list[str] | None,
    kind: str,
    check_items: list[tuple[str, str]] | None = None,
    demo_docs: list[str] | None = None,
    *,
    requirement_markdown: str = "",
    requirement_title: str = "",
) -> list[str]:
    """生成用例时按对接类型解析规则文档；若提供检查项与 demo 目录则完全自动匹配。"""
    _ = selected_paths
    return resolve_generation_rule_docs(
        kind,
        check_items or [],
        demo_docs or [],
        requirement_markdown=requirement_markdown,
        requirement_title=requirement_title,
    )


def infer_kind_from_checklist_doc(checklist_doc: str | None) -> RequirementKind | None:
    path = (checklist_doc or "").replace("\\", "/")
    if not path:
        return None
    if "渠道需求检查项" in path or "HUB渠道" in path or "渠道概要" in path:
        return "channel"
    if "机构需求检查项" in path or "机构概要" in path:
        return "institution"
    return None


def infer_kind_from_check_item_labels(item_texts: Iterable[str]) -> RequirementKind | None:
    labels = {(t or "").strip() for t in item_texts}
    if labels & _INSTITUTION_CHECK_LABELS:
        return "institution"
    if labels & _CHANNEL_CHECK_LABELS:
        return "channel"
    return None


def effective_requirement_kind(
    markdown_kind: str,
    *,
    check_item_labels: Iterable[str] | None = None,
    checklist_doc: str | None = None,
    requirement_markdown: str | None = None,
    requirement_url: str | None = None,
    requirement_title: str | None = None,
) -> RequirementKind:
    from_text = infer_kind_from_texts(
        requirement_markdown or "",
        requirement_url or "",
        title=requirement_title or "",
    )
    if from_text in ("institution", "channel"):
        return from_text

    if check_item_labels:
        from_labels = infer_kind_from_check_item_labels(check_item_labels)
        if from_labels:
            return from_labels

    from_checklist = infer_kind_from_checklist_doc(checklist_doc)
    if from_checklist:
        return from_checklist

    if markdown_kind in ("institution", "channel"):
        return markdown_kind

    return markdown_kind or "unknown"


def _item_value(
    check_items: list[tuple[str, str]],
    label: str,
) -> str:
    for item_text, value in check_items:
        if (item_text or "").strip() == label:
            return (value or "").strip()
    return ""


def _item_value_fuzzy(
    check_items: list[tuple[str, str]],
    *labels: str,
) -> str:
    for item_text, value in check_items:
        t = (item_text or "").strip()
        for label in labels:
            if t == label or label in t:
                return (value or "").strip()
    return ""


def flow_mode_text(kind: str, check_items: list[tuple[str, str]]) -> str:
    if kind == "channel":
        return _item_value_fuzzy(check_items, "渠道流程模式")
    return _item_value_fuzzy(check_items, "流程概要", "流程摘要")


def interface_flow_text_for_matching(
    kind: str,
    check_items: list[tuple[str, str]],
) -> str:
    """
    步骤2 接口文档匹配专用：仅依据检查项「流程概要 / 流程摘要 / 渠道流程模式」
    及其确认值，不掺入需求正文，避免正文中的其它流程描述覆盖步骤1 已确认的流程。
    """
    primary = flow_mode_text(kind, check_items)
    if primary:
        return primary

    chunks: list[str] = []
    flow_field_keys = ("渠道流程模式", "流程概要", "流程摘要")
    for item_text, value in check_items:
        t = (item_text or "").strip()
        v = (value or "").strip()
        if not v:
            continue
        if t in flow_field_keys or any(k in t for k in ("流程模式", "流程概要", "流程摘要")):
            chunks.append(v)

    for item_text, value in check_items:
        v = (value or "").strip()
        n = _normalize_flow_text(v)
        if n and any(
            k in n
            for k in ("半流程", "导下载", "全流程", "借还", "出额", "预授信")
        ):
            chunks.append(v)

    return "\n".join(chunks)


def collect_flow_mode_text(
    kind: str,
    check_items: list[tuple[str, str]],
    *,
    requirement_markdown: str = "",
    requirement_title: str = "",
) -> str:
    """汇总流程模式信号：检查项字段、其它相关检查项、需求标题与正文。"""
    chunks: list[str] = []
    primary = flow_mode_text(kind, check_items)
    if primary:
        chunks.append(primary)

    flow_field_keys = ("渠道流程模式", "流程概要", "流程摘要")
    for item_text, value in check_items:
        t = (item_text or "").strip()
        v = (value or "").strip()
        if not v:
            continue
        if t in flow_field_keys or any(k in t for k in ("流程模式", "流程概要", "流程摘要")):
            if v != primary:
                chunks.append(v)

    if not primary:
        for item_text, value in check_items:
            v = (value or "").strip()
            n = _normalize_flow_text(v)
            if n and any(
                k in n
                for k in ("半流程", "导下载", "全流程", "借还", "出额", "预授信")
            ):
                chunks.append(v)

    title = (requirement_title or "").strip()
    if title:
        chunks.append(title)
    md = (requirement_markdown or "").strip()
    if md:
        chunks.append(md[:10000])

    return "\n".join(chunks)


def _pick_existing_interface_path(
    preferred_names: list[str],
    interface_docs: list[str],
    default: str,
) -> str:
    catalog = [_norm_path(p) for p in interface_docs if p]
    for name in preferred_names:
        target = _norm_path(name)
        for path in catalog:
            if path.endswith("/" + target) or path.split("/")[-1] == target:
                return path
    default_norm = _norm_path(default)
    for path in catalog:
        if path == default_norm or path.endswith("/" + default_norm.split("/")[-1]):
            return path
    return default


def _institution_type_value(check_items: list[tuple[str, str]]) -> str:
    return _item_value_fuzzy(check_items, "类型", "是否标准机构")


def _institution_is_non_standard(type_val: str) -> bool:
    if not type_val:
        return False
    return "非标准机构" in type_val or "按照机构提供的接口文档" in type_val


def _institution_is_standard(type_val: str) -> bool:
    if not type_val or _institution_is_non_standard(type_val):
        return False
    return "OSI标准机构" in type_val or "标准机构" in type_val


def osi_interface_path_from_flow(flow_raw: str) -> str:
    n = _normalize_flow_text(flow_raw)
    if not n:
        return OSI_INTERFACE_FULL
    if _is_half_flow(n):
        return OSI_INTERFACE_HALF_FLOW
    if _is_borrow_repay_h5(n) or _is_full_flow_api(n):
        return OSI_INTERFACE_FULL
    if "授信" in n and "api" in n and "h5" in n:
        return OSI_INTERFACE_FULL
    return OSI_INTERFACE_FULL


def homo_interface_path_from_flow(
    flow_raw: str,
    interface_docs: list[str] | None = None,
) -> str:
    n = _normalize_flow_text(flow_raw)
    catalog = list(interface_docs or [])
    if _is_half_flow(n):
        return _pick_existing_interface_path(
            [
                HOMO_INTERFACE_HALF.split("/")[-1],
                HOMO_INTERFACE.split("/")[-1],
            ],
            catalog,
            HOMO_INTERFACE_HALF,
        )
    if _is_borrow_repay_h5(n):
        return _pick_existing_interface_path(
            [
                HOMO_INTERFACE_BORROW_H5.split("/")[-1],
                "HOMO标准渠道对接-全流程借还H5-接口文档.md",
                HOMO_INTERFACE.split("/")[-1],
            ],
            catalog,
            HOMO_INTERFACE_BORROW_H5,
        )
    if _is_full_flow_api(n):
        return _pick_existing_interface_path(
            [
                HOMO_INTERFACE_FULL_API.split("/")[-1],
                HOMO_INTERFACE.split("/")[-1],
            ],
            catalog,
            HOMO_INTERFACE_FULL_API,
        )
    return _pick_existing_interface_path(
        [HOMO_INTERFACE.split("/")[-1]],
        catalog,
        HOMO_INTERFACE,
    )


def match_channel_interface_doc(
    check_items: list[tuple[str, str]],
    interface_docs: list[str],
    *,
    requirement_markdown: str = "",
    requirement_title: str = "",
) -> str:
    provider = _item_value(check_items, "接口文档提供方")
    if provider and "我方" in provider:
        flow = interface_flow_text_for_matching("channel", check_items)
        return homo_interface_path_from_flow(flow, interface_docs)

    names: list[str] = []
    for key in ("渠道名称", "渠道合作方", "内部渠道号"):
        val = _item_value(check_items, key)
        if val:
            names.append(val)

    for path in interface_docs:
        base = path.split("/")[-1]
        for name in names:
            if name and name in base:
                return path
    flow = interface_flow_text_for_matching("channel", check_items)
    return homo_interface_path_from_flow(flow, interface_docs)


def infer_interface_doc_path(
    kind: str,
    check_items: list[tuple[str, str]],
    interface_docs: list[str] | None = None,
    *,
    requirement_markdown: str = "",
    requirement_title: str = "",
) -> str | None:
    if kind not in ("institution", "channel"):
        return None

    catalog = list(interface_docs or [])

    if kind == "channel":
        return match_channel_interface_doc(
            check_items,
            catalog,
            requirement_markdown=requirement_markdown,
            requirement_title=requirement_title,
        )

    type_val = _institution_type_value(check_items)
    if _institution_is_non_standard(type_val):
        return None

    flow = interface_flow_text_for_matching(kind, check_items)
    return osi_interface_path_from_flow(flow)


def infer_rule_doc_path(
    kind: str,
    check_items: list[tuple[str, str]],
    rule_docs: list[str],
) -> str | None:
    """兼容旧调用：从 rule_docs 或 demo 路径列表中推断 Demo 文件。"""
    demo_catalog = [p for p in rule_docs if "docs/demo/" in _norm_path(p) or "/Demo-" in _norm_path(p)]
    return infer_demo_doc_path(kind, check_items, demo_catalog or rule_docs)


def kind_label_zh(kind: str) -> str:
    if kind == "channel":
        return "渠道对接"
    if kind == "institution":
        return "机构对接"
    return "其它需求"

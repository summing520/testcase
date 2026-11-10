"""机构/渠道识别 + 接口文档/Demo 匹配的回归测试。

为什么先测这几个模块：
1. `integration_matching` 是**纯函数**（不碰网络、不碰数据库），可离线、毫秒级跑完；
2. 它承载了整个流程里最"贵"的业务判断（机构 vs 渠道、半流程 vs 全流程），
   判错会导致后面所有生成内容全部跑偏，属于典型的**高风险 + 易测**区域；
3. 前端 `test_case_generator.html` 里有一份 JS 复刻逻辑，这份测试同时充当
   "后端语义的权威定义"，将来抽公共接口时可以作为对照基准。

注意：本模块的接口签名统一是 `check_items: list[tuple[item_text, value]]`，
不是 CheckItem 对象（那是 `institution_db_scope` / `channel_generation_directives`
的入参形式）。演算两套入参形式本身就是重构候选点之一。
"""

import pytest

from backend.services import integration_matching as im


INST_DEMOS = [
    "docs/demo/Demo-标准机构-半流程导下载-测试用例.md",
    "docs/demo/Demo-标准机构-借还H5-测试用例.md",
]
CHANNEL_DEMOS = [
    "docs/demo/Demo-标准渠道-半流程导下载-对接测试用例.md",
    "docs/demo/Demo-标准渠道-全流程API对接-测试用例.md",
]
ALL_DEMOS = INST_DEMOS + CHANNEL_DEMOS

INTERFACE_DOCS = [
    "docs/knowledge/interface/HOMO标准渠道对接-接口文档.md",
    "docs/knowledge/interface/HOMO标准渠道对接-半流程导下载-接口文档.md",
    "docs/knowledge/interface/小赢V2渠道对接文档.md",
    "docs/knowledge/interface/OSI标准机构对接-接口文档.md",
]


# ---------------------------------------------------------------------------
# 一、对接类型识别：机构 vs 渠道
# ---------------------------------------------------------------------------
class TestInferKind:
    def test_标题含机构对接时即使正文有导下载也判机构(self):
        """真实需求标题：「信用飞导下载我机构对接」。

        「导下载」是渠道半流程的常见词，若按正文关键词打分会被误判成渠道，
        因此标题优先级必须高于正文——这是本项目踩过的坑，用测试锁死。
        """
        assert im.infer_kind_from_texts("信用飞导下载我机构对接") == "institution"

    def test_正文含渠道对接(self):
        assert im.infer_kind_from_texts("本次渠道对接需求，接口文档由渠道提供") == "channel"

    @pytest.mark.parametrize(
        "text",
        [
            "上线范围：APP、HUB",
            "上线范围: APP,HUB",
        ],
    )
    def test_上线范围里的HUB不算渠道对接(self, text):
        """「上线范围：APP、HUB」描述的是投放端，不是 HUB 渠道对接。

        这是最容易被关键词坑到的一处，代码里有专门的反向规则。
        """
        assert im.infer_kind_from_texts(text) == "unknown"

    def test_两种表述并存时标题优先(self):
        text = "机构对接 渠道对接 都要看"
        assert im.infer_kind_from_texts(text, title="XX机构对接需求") == "institution"
        assert im.infer_kind_from_texts(text, title="XX渠道对接需求") == "channel"

    def test_两种表述并存且无标题时按机构特征词兜底(self):
        text = "机构对接 渠道对接 机构编码 juronghua 产品code"
        assert im.infer_kind_from_texts(text) == "institution"

    def test_渠道字段加权(self):
        assert im.infer_kind_from_texts("内部渠道号 HUB_MEIYIJIEQIAN") == "channel"
        assert im.infer_kind_from_texts("渠道流程模式：半流程") == "channel"

    def test_机构字段加权(self):
        assert im.infer_kind_from_texts("机构编码 juronghua") == "institution"
        assert im.infer_kind_from_texts("OSI标准机构 对接") == "institution"

    @pytest.mark.parametrize("text", ["", "   ", "一段和对接无关的普通需求"])
    def test_无信号时返回unknown(self, text):
        assert im.infer_kind_from_texts(text) == "unknown"

    def test_空入参也返回unknown(self):
        assert im.infer_kind_from_texts() == "unknown"


# ---------------------------------------------------------------------------
# 二、流程模式归一化（半流程 / 全流程API / 借还H5）
# ---------------------------------------------------------------------------
class TestFlowNormalization:
    @pytest.mark.parametrize(
        "raw",
        [
            "半流程(出额导下载)",
            "出额导下载",
            "预授信导下载",
            "半流程",
        ],
    )
    def test_半流程判定(self, raw):
        assert im._is_half_flow(im._normalize_flow_text(raw)) is True

    def test_半流程与全流程API并存时半流程优先(self):
        """检查项模板里多选项并存是常见情况，半流程语义更严格，优先采用。"""
        normalized = im._normalize_flow_text("半流程 全流程API")
        assert im._is_half_flow(normalized) is True

    @pytest.mark.parametrize("raw", ["全流程API", "全流程 API"])
    def test_全流程API不算半流程(self, raw):
        normalized = im._normalize_flow_text(raw)
        assert im._is_half_flow(normalized) is False
        assert im._is_full_flow_api(normalized) is True

    @pytest.mark.parametrize(
        "raw",
        ["全流程-借还H5", "提现/还款H5", "借还 H5"],
    )
    def test_借还H5判定(self, raw):
        assert im._is_borrow_repay_h5(im._normalize_flow_text(raw)) is True

    def test_归一化会去掉空格全角空格和加号(self):
        # 需求文档里「全 流程 + API」「全　流程+API」这类写法很常见，归一化后才能命中规则
        assert im._normalize_flow_text("全\u3000流程 + API") == "全流程api"
        assert im._is_full_flow_api(im._normalize_flow_text("全 流程 + API")) is True


# ---------------------------------------------------------------------------
# 三、Demo 骨架匹配（决定输出结构）
# ---------------------------------------------------------------------------
class TestDemoMatching:
    @pytest.mark.parametrize(
        "kind,flow,expected",
        [
            ("channel", "半流程(出额导下载)", "docs/demo/Demo-标准渠道-半流程导下载-对接测试用例.md"),
            ("channel", "全流程API", "docs/demo/Demo-标准渠道-全流程API对接-测试用例.md"),
            ("institution", "半流程-出额导下载机构APP", "docs/demo/Demo-标准机构-半流程导下载-测试用例.md"),
            ("institution", "全流程-授信API + 提现/还款H5", "docs/demo/Demo-标准机构-借还H5-测试用例.md"),
        ],
    )
    def test_按类型和流程匹配Demo(self, kind, flow, expected):
        items = [("渠道流程模式", flow), ("流程概要", flow)]
        assert im.infer_demo_doc_path(kind, items, ALL_DEMOS) == expected

    def test_其它需求不匹配Demo(self):
        assert im.infer_demo_doc_path("unknown", [("流程概要", "半流程")], ALL_DEMOS) is None

    def test_目录里没有对应Demo时返回None(self):
        """不能返回一个不存在的路径，否则生成阶段读文件会直接炸。"""
        assert im.infer_demo_doc_path("channel", [("渠道流程模式", "半流程")], []) is None

    def test_渠道任务不会匹配到机构Demo(self):
        matched = im.infer_demo_doc_path("channel", [("渠道流程模式", "半流程")], ALL_DEMOS)
        assert matched is not None and "渠道" in matched


# ---------------------------------------------------------------------------
# 四、Rule Docs 组装顺序
# ---------------------------------------------------------------------------
class TestRuleDocs:
    def test_演示文档在前业务规则在后(self):
        """顺序有意义：Demo 决定结构，业务规则限定边界，提示词里也按此顺序声明。"""
        docs = im.resolve_generation_rule_docs(
            "institution", [("流程概要", "半流程-出额导下载机构APP")], ALL_DEMOS
        )
        assert docs == [
            "docs/demo/Demo-标准机构-半流程导下载-测试用例.md",
            "docs/rules/机构业务规则.md",
        ]

    def test_渠道任务挂渠道业务规则(self):
        docs = im.resolve_generation_rule_docs("channel", [("渠道流程模式", "全流程API")], ALL_DEMOS)
        assert docs[-1] == "docs/rules/渠道业务规则.md"

    def test_其它需求不注入任何规则(self):
        assert im.resolve_generation_rule_docs("unknown", [], ALL_DEMOS) == []


# ---------------------------------------------------------------------------
# 五、步骤2 接口文档匹配
# ---------------------------------------------------------------------------
class TestInterfaceMatching:
    def test_非标准机构不自动给文档(self):
        """非标准机构必须按机构自有文档对接，系统不能瞎塞 OSI 默认文档。"""
        items = [("类型", "非标准机构（按照机构提供的接口文档对接）")]
        assert im.infer_interface_doc_path("institution", items, INTERFACE_DOCS) is None

    def test_标准机构半流程匹配半流程文档(self):
        items = [("类型", "OSI标准机构"), ("流程概要", "半流程-出额导下载机构APP")]
        assert im.infer_interface_doc_path("institution", items, INTERFACE_DOCS) == (
            "docs/knowledge/interface/OSI标准机构对接-半流程导下载-接口文档.md"
        )

    def test_标准机构全流程匹配全量文档(self):
        items = [("类型", "OSI标准机构"), ("流程概要", "全流程API")]
        assert im.infer_interface_doc_path("institution", items, INTERFACE_DOCS) == (
            "docs/knowledge/interface/OSI标准机构对接-接口文档.md"
        )

    def test_渠道我方提供按流程选HOMO(self):
        items = [("接口文档提供方", "我方提供"), ("渠道流程模式", "半流程")]
        assert im.match_channel_interface_doc(items, INTERFACE_DOCS) == (
            "docs/knowledge/interface/HOMO标准渠道对接-半流程导下载-接口文档.md"
        )

    def test_渠道提供时按渠道名称匹配文件名(self):
        items = [("接口文档提供方", "渠道提供"), ("渠道名称", "小赢V2")]
        assert im.match_channel_interface_doc(items, INTERFACE_DOCS) == (
            "docs/knowledge/interface/小赢V2渠道对接文档.md"
        )

    def test_渠道提供但匹配不到时回退HOMO(self):
        items = [("接口文档提供方", "渠道提供"), ("渠道名称", "不存在的渠道")]
        assert im.match_channel_interface_doc(items, INTERFACE_DOCS) == (
            "docs/knowledge/interface/HOMO标准渠道对接-接口文档.md"
        )

    def test_步骤2匹配不掺入需求正文(self):
        """接口文档匹配只看检查项确认值，避免正文里别的流程描述覆盖步骤1的结论。"""
        items = [("类型", "OSI标准机构"), ("流程概要", "半流程")]
        assert im.interface_flow_text_for_matching("institution", items) == "半流程"


# ---------------------------------------------------------------------------
# 六、最终类型校正（检查项表头 / 清单文件名）
# ---------------------------------------------------------------------------
class TestEffectiveKind:
    def test_检查项表头可反向校正类型(self):
        assert im.effective_requirement_kind("unknown", check_item_labels=["内部渠道号"]) == "channel"
        assert im.effective_requirement_kind("unknown", check_item_labels=["机构编码"]) == "institution"

    def test_需求正文优先级高于检查项表头(self):
        kind = im.effective_requirement_kind(
            "unknown",
            check_item_labels=["内部渠道号"],
            requirement_markdown="这是一次机构对接需求",
        )
        assert kind == "institution"

    def test_检查清单文件名可推断类型(self):
        assert im.infer_kind_from_checklist_doc("docs/checklist/渠道需求检查项.md") == "channel"
        assert im.infer_kind_from_checklist_doc("docs/checklist/机构需求检查项.md") == "institution"
        assert im.infer_kind_from_checklist_doc("docs/checklist/其他.md") is None

    def test_没有检查项标签时沿用已有类型(self):
        assert im.effective_requirement_kind("channel") == "channel"
        assert im.effective_requirement_kind("unknown") == "unknown"

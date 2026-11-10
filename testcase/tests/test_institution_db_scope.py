"""机构落库用例范围收敛的回归测试。

业务背景：机构对接勾选「数据库表」后，系统会在接口用例定稿后再补一轮落库用例。
但半流程（出额导下载）根本不走绑卡/提现/还款，若不做范围收敛，模型会凭空造出
这几段落库用例——这是最典型的一类「AI 幻觉」，必须用确定性逻辑挡住。

收敛思路（三个信号取交集）：
    信号1 流程模式  -> 默认环节
    信号2 接口文档「接口总览」表格 -> 实际涉及环节
    信号3 已生成用例的章节标题 -> 实际写了哪些环节
"""

from backend.services import institution_db_scope as scope_mod

ALL_STAGES = list(scope_mod.INSTITUTION_DB_VALIDATION_STAGES)


INTERFACE_OVERVIEW_MD = """## 接口总览

| 接口类型 | 业务环节 | 接口名称 |
| --- | --- | --- |
| API | 准入授信 | 撞库 / 授信申请 |
| API | 绑卡 | 绑卡申请 |
| API | 借款 | 借款提交 |
"""


class TestFlowStages:
    def test_半流程默认只做准入和授信(self):
        normalized = scope_mod._normalize_flow_text("半流程-出额导下载机构APP")
        assert scope_mod.institutions_db_stages_from_flow(normalized) == {"准入", "授信"}

    def test_全流程API覆盖全部环节(self):
        normalized = scope_mod._normalize_flow_text("全流程API")
        assert scope_mod.institutions_db_stages_from_flow(normalized) == set(ALL_STAGES)

    def test_授信API加借还H5覆盖全部环节(self):
        normalized = scope_mod._normalize_flow_text("全流程-授信API + 提现/还款H5")
        assert scope_mod.institutions_db_stages_from_flow(normalized) == set(ALL_STAGES)

    def test_流程未识别时保守取全流程(self):
        assert scope_mod.institutions_db_stages_from_flow("") == set(ALL_STAGES)


class TestInterfaceOverview:
    def test_解析接口总览表格(self):
        assert scope_mod.parse_interface_overview_stages(INTERFACE_OVERVIEW_MD) == {
            "准入",
            "授信",
            "绑卡",
            "提现",
        }

    def test_空文档返回空集合(self):
        assert scope_mod.parse_interface_overview_stages("") == set()

    def test_没有接口总览章节时返回空集合(self):
        assert scope_mod.parse_interface_overview_stages("## 一、授信环节\n没有表格") == set()


class TestScopeResolution:
    def test_半流程且无其它信号时只含准入授信(self, make_item):
        result = scope_mod.resolve_institution_db_validation_scope(
            check_items=[make_item("流程概要", "半流程-出额导下载机构APP")],
        )
        assert result["included_stages"] == ["准入", "授信"]
        assert result["excluded_stages"] == ["绑卡", "提现", "还款"]

    def test_三重信号取交集(self, make_item):
        """半流程（准入/授信）× 接口总览（准入/授信/绑卡/提现）× 已生成用例（准入/授信）

        交集仍应是 准入/授信 —— 半流程不允许越界写绑卡提现。
        """
        result = scope_mod.resolve_institution_db_validation_scope(
            check_items=[make_item("流程概要", "半流程")],
            external_cooperation_markdown=INTERFACE_OVERVIEW_MD,
            generated_testcase_markdown="## 一、授信环节\n### 准入\n### 授信\n",
        )
        assert result["included_stages"] == ["准入", "授信"]

    def test_无任何信号时保守给全流程(self):
        result = scope_mod.resolve_institution_db_validation_scope(check_items=[])
        assert result["included_stages"] == ALL_STAGES
        assert result["excluded_stages"] == []

    def test_接口总览可收窄全流程(self, make_item):
        """即使流程写的是全流程，若接口文档只覆盖到借款，也不应生成还款落库用例。"""
        result = scope_mod.resolve_institution_db_validation_scope(
            check_items=[make_item("流程概要", "全流程API")],
            external_cooperation_markdown=INTERFACE_OVERVIEW_MD,
            generated_testcase_markdown="",
        )
        assert result["included_stages"] == ["准入", "授信", "绑卡", "提现"]
        assert result["excluded_stages"] == ["还款"]

    def test_scope_summary含须生成与勿生成提示(self, make_item):
        result = scope_mod.resolve_institution_db_validation_scope(
            check_items=[make_item("流程概要", "半流程")],
        )
        summary = result["scope_summary"]
        assert "须生成落库用例的环节" in summary
        assert "勿生成的落库环节" in summary

    def test_返回的接口文档路径与流程一致(self, make_item):
        half = scope_mod.resolve_institution_db_validation_scope(
            check_items=[make_item("流程概要", "半流程")],
        )
        assert half["interface_doc_path"].endswith("半流程导下载-接口文档.md")


class TestStagesFromGeneratedMarkdown:
    def test_从章节标题推断环节(self):
        md = (
            "## 一、授信环节\n### 准入\n### 授信\n"
            "## 二、用信环节\n### 绑卡\n### 借款\n"
            "## 三、还款环节\n"
        )
        normalized = scope_mod._normalize_flow_text("全流程API")
        assert scope_mod.infer_db_stages_from_testcase_markdown(md, normalized) == {
            "准入",
            "授信",
            "绑卡",
            "提现",
            "还款",
        }

    def test_半流程下导下载章节不算提现(self):
        """半流程会出现「导下载」章节，不能把它当作用信/提现环节。"""
        md = "## 一、授信环节\n### 授信\n## 二、导下载环节\n"
        normalized = scope_mod._normalize_flow_text("半流程")
        assert "提现" not in scope_mod.infer_db_stages_from_testcase_markdown(md, normalized)

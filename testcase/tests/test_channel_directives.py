"""渠道「强制约束」判定的回归测试。

业务背景：渠道对接最容易写错的是用信环节——
如果渠道用的是「本地配置的固定下载链接」着陆页，那么 HUB 侧的试算/绑卡/借款/还款
接口根本不在链路里，写了就是无效用例（还会让评审误解范围）。

这个判定原先靠人读《渠道业务规则》第五章，现在变成代码：
`infer_uses_fixed_download_link()` 判真假，`build_channel_mandatory_directives()`
把判定结论和依据写成一段「优先级高于 Demo 骨架」的指令注入生成上下文。
"""

import pytest

from backend.services import channel_generation_directives as directives


def _bundle(check_items, requirement_markdown="", kind="channel", rule_docs=None):
    return {
        "generation_options": {"inferred_kind": kind},
        "check_items": check_items,
        "requirement_markdown": requirement_markdown,
        "knowledge_docs": {},
        "rule_docs": rule_docs or {},
    }


class TestInferFixedDownloadLink:
    def test_着陆页URL判定为使用固定链接(self):
        uses_fixed, evidence = directives.infer_uses_fixed_download_link(
            requirement_markdown="下载地址：https://test2.xurongwl.com/land/uni/fenqi?cvv=73889&td_channelid=23467"
        )
        assert uses_fixed is True
        assert any("land/uni/fenqi" in e for e in evidence)

    def test_关键词判定为使用固定链接(self):
        uses_fixed, evidence = directives.infer_uses_fixed_download_link(
            requirement_markdown="授信通过后返回本地配置下载链接"
        )
        assert uses_fixed is True
        assert evidence

    def test_查询场景页面地址判定为不使用固定链接(self):
        uses_fixed, evidence = directives.infer_uses_fixed_download_link(
            requirement_markdown="渠道通过查询场景页面地址接口动态获取下载页"
        )
        assert uses_fixed is False
        assert any("查询场景页面地址" in e for e in evidence)

    def test_检查项显式是或否优先于正文(self):
        yes, _ = directives.infer_uses_fixed_download_link(
            requirement_markdown="没有任何线索",
            check_items=[("是否使用固定下载链接", "是")],
        )
        assert yes is True

        no, _ = directives.infer_uses_fixed_download_link(
            requirement_markdown="https://test2.xurongwl.com/land/uni/fenqi?cvv=1&td_channelid=2",
            check_items=[("是否使用固定下载链接", "否")],
        )
        assert no is False

    def test_无线索时返回None(self):
        uses_fixed, evidence = directives.infer_uses_fixed_download_link(
            requirement_markdown="一段与下载链接无关的需求描述"
        )
        assert uses_fixed is None
        assert evidence == []


class TestBuildMandatoryDirectives:
    def test_非渠道类型不注入(self, make_item):
        bundle = _bundle([make_item("流程概要", "半流程")], kind="institution")
        assert directives.build_channel_mandatory_directives(bundle) == ""

    def test_判定为是时要求写固定着陆页并禁止借还接口(self, make_item):
        bundle = _bundle(
            [make_item("渠道流程模式", "半流程(出额导下载)")],
            requirement_markdown="使用本地配置下载链接 https://test2.xurongwl.com/land/uni/fenqi?cvv=73889&td_channelid=23467",
        )
        text = directives.build_channel_mandatory_directives(bundle)
        assert "使用固定下载链接（是）" in text
        assert "固定着陆页" in text
        assert "禁止编写" in text
        assert "提现" in text

    def test_外部获客渠道编号会被写入约束(self, make_item):
        bundle = _bundle(
            [
                make_item("渠道流程模式", "半流程"),
                make_item("外部获客渠道编号", "23467"),
            ],
            requirement_markdown="使用本地配置下载链接",
        )
        text = directives.build_channel_mandatory_directives(bundle)
        assert "23467" in text
        assert "外部获客渠道编号" in text

    def test_判定为否时要求按动态配置编写(self, make_item):
        bundle = _bundle(
            [make_item("渠道流程模式", "全流程API")],
            requirement_markdown="通过查询场景页面地址获取下载页",
        )
        text = directives.build_channel_mandatory_directives(bundle)
        assert "使用固定下载链接（否）" in text
        assert "查询场景页面地址" in text

    def test_半流程但判不出固定链接时仍禁止借还接口(self, make_item):
        bundle = _bundle(
            [make_item("渠道流程模式", "半流程(出额导下载)")],
            requirement_markdown="普通需求描述，没有链接线索",
        )
        text = directives.build_channel_mandatory_directives(bundle)
        assert "未从需求明确识别" in text
        assert "禁止" in text
        assert "借还款" in text

    def test_全流程且判不出固定链接时不注入(self, make_item):
        """全流程 API 本来就该写借还款接口，不能套半流程的禁止规则。"""
        bundle = _bundle(
            [make_item("渠道流程模式", "全流程API")],
            requirement_markdown="普通需求描述，没有链接线索",
        )
        assert directives.build_channel_mandatory_directives(bundle) == ""

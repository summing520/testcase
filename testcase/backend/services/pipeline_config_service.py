import json

from backend.db import tables as t
from backend.db.connection import get_connection, json_load, now_utc, parse_datetime
from backend.models.pipeline import PipelineConfig, PipelineConfigUpdateRequest, PipelineStepConfig


CONFIG_ID = "default"


def default_pipeline_config() -> PipelineConfig:
    return PipelineConfig(
        name="测试用例生成流程",
        steps=[
            PipelineStepConfig(
                key="step1",
                order=1,
                title="需求确认",
                description="解析飞书需求，识别机构/渠道对接类型并确认检查项（清单表决定对接类型）。",
                enabled=True,
                fields={
                    "skill_tools": ["feishu"],
                    "feishu_url_label": "飞书需求链接",
                    "feishu_url_placeholder": "https://c60v462yqp.feishu.cn/wiki/Nq0pw1OQXXXXXXX",
                    "parse_button_label": "开始解析",
                    "next_button_label": "下一步",
                    "progress_label": "解析进度（实时）",
                    "requirement_preview_label": "解析后的需求 Markdown",
                    "checklist_title": "检查项确认",
                    "checklist_hint": "请完善右侧输入框内容，点击「下一步」进入对接文档确认。",
                },
            ),
            PipelineStepConfig(
                key="step2",
                order=2,
                title="对接文档确认",
                description="按机构/渠道与流程模式自动匹配 interface 文档，或上传 Markdown。",
                enabled=True,
                fields={
                    "upload_label": "上传 Markdown 对接文档",
                    "interface_doc_hint": (
                        "机构对接：按「类型」「流程概要」匹配 OSI 接口文档；"
                        "渠道对接：我方提供用 HOMO，渠道提供则按渠道名称匹配（如小赢V2）；"
                        "非标准或无法识别时请上传 Markdown。详见 docs/测试用例生成流程.md。"
                    ),
                    "next_button_label": "下一步",
                },
            ),
            PipelineStepConfig(
                key="step3",
                order=3,
                title="生成用例",
                description="按对接类型与流程模式自动匹配 docs/demo 骨架与 docs/rules 业务规则，生成用例。",
                enabled=True,
                fields={
                    "generate_button_label": "生成测试用例",
                    "testcase_type_label": "用例类型",
                    "flow_type_label": "基本功能",
                    "db_type_label": "数据库表",
                    "db_type_default": False,
                    "rules_label": "应用规则（自动匹配）",
                    "demo_label": "参照 Demo（自动匹配）",
                    "progress_label": "生成过程（实时）",
                },
            ),
            PipelineStepConfig(
                key="step4",
                order=4,
                title="结果确认",
                description="预览结果并采纳保存到用例库。",
                enabled=True,
                fields={
                    "adopt_title_label": "设置测试用例标题（可选）",
                    "adopt_title_placeholder": "例如：支付需求v1测试用例",
                    "adopt_button_label": "保存用例",
                    "preview_label": "Markdown 预览",
                    "open_preview_label": "打开新页面预览",
                },
            ),
        ],
    )


_STEP3_OBSOLETE_FLOW_LABELS = frozenset({"应用规则（单选）", "接口流程（必选）"})


def _apply_pipeline_field_defaults(cfg: PipelineConfig) -> PipelineConfig:
    """合并 step3 默认文案，修正历史错误配置（如 flow_type_label 被写成「应用规则（单选）」）。"""
    defaults = {s.key: (s.fields or {}) for s in default_pipeline_config().steps}
    d3 = defaults.get("step3", {})
    for step in cfg.steps:
        if step.key != "step3":
            continue
        fields = dict(step.fields or {})
        flow_label = fields.get("flow_type_label") or ""
        if flow_label in _STEP3_OBSOLETE_FLOW_LABELS:
            fields["flow_type_label"] = d3.get("flow_type_label", "基本功能")
        if str(fields.get("rules_label") or "").startswith("应用规则（单选"):
            fields["rules_label"] = d3.get("rules_label", "应用规则（自动匹配）")
        if not fields.get("demo_label"):
            fields["demo_label"] = d3.get("demo_label", "参照 Demo（自动匹配）")
        step.fields = fields
    return cfg


def get_pipeline_config() -> PipelineConfig:
    conn = get_connection()
    try:
        row = conn.execute(
            f"SELECT config_json, updated_at FROM {t.PIPELINE_CONFIG} WHERE id = ?",
            (CONFIG_ID,),
        ).fetchone()
        if row is None:
            cfg = default_pipeline_config()
            now = now_utc()
            conn.execute(
                f"INSERT INTO {t.PIPELINE_CONFIG} (id, config_json, updated_at) VALUES (?, ?, ?)",
                (CONFIG_ID, cfg.model_dump_json(), now),
            )
            conn.commit()
            cfg.updated_at = parse_datetime(now)
            return cfg
        data = json_load(row["config_json"], {})
        cfg = PipelineConfig(
            name=data.get("name", "测试用例生成流程"),
            steps=[PipelineStepConfig(**s) for s in data.get("steps", [])],
            updated_at=parse_datetime(row["updated_at"]),
        )
        return _apply_pipeline_field_defaults(cfg)
    finally:
        conn.close()


def update_pipeline_config(request: PipelineConfigUpdateRequest) -> PipelineConfig:
    current = get_pipeline_config()
    name = request.name if request.name is not None else current.name
    steps = request.steps if request.steps is not None else current.steps
    steps = sorted(steps, key=lambda s: s.order)
    now = now_utc()
    payload = PipelineConfig(name=name, steps=steps, updated_at=parse_datetime(now))

    conn = get_connection()
    try:
        conn.execute(
            f"""
            INSERT INTO {t.PIPELINE_CONFIG} (id, config_json, updated_at)
            VALUES (?, ?, ?)
            ON DUPLICATE KEY UPDATE
                config_json = VALUES(config_json),
                updated_at = VALUES(updated_at)
            """,
            (CONFIG_ID, payload.model_dump_json(exclude={"updated_at"}), now),
        )
        conn.commit()
    finally:
        conn.close()
    return get_pipeline_config()


def reset_pipeline_config() -> PipelineConfig:
    defaults = default_pipeline_config()
    return update_pipeline_config(
        PipelineConfigUpdateRequest(name=defaults.name, steps=defaults.steps)
    )


def get_step_fields(step_key: str) -> dict:
    cfg = get_pipeline_config()
    for step in cfg.steps:
        if step.key == step_key and step.enabled:
            return step.fields or {}
    return {}

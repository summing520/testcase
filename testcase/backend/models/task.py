from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


TaskStatus = Literal["draft", "parsed_confirming", "generating", "generated", "adopted"]
RequirementKind = Literal["channel", "institution", "unknown"]


class TaskCreateRequest(BaseModel):
    requirement_url: str = Field(..., description="Feishu requirement document URL")
    selected_knowledge_docs: list[str] = Field(default_factory=list)
    selected_checklist_docs: list[str] = Field(default_factory=list)
    selected_rule_docs: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _require_checklist_and_rules(self) -> "TaskCreateRequest":
        # 新版流程中，检查项与规则可由系统根据需求自动加载；前端也可能在后续步骤再选择。
        # 为兼容旧接口/旧页面，仍允许传入非空列表，但不再强制要求。
        return self


class TaskSummary(BaseModel):
    id: str
    status: TaskStatus
    requirement_url: str
    requirement_kind: RequirementKind = "unknown"
    inferred_checklist_doc: str | None = None
    adopted_test_case_title: str | None = None
    selected_knowledge_docs: list[str]
    selected_checklist_docs: list[str]
    selected_rule_docs: list[str]
    interface_doc_path: str | None = None
    interface_doc_label: str | None = None
    created_at: datetime
    updated_at: datetime


class ParseTaskResponse(BaseModel):
    task: TaskSummary
    requirement_markdown: str


class CheckItemResult(BaseModel):
    item_key: str
    item_text: str
    matched_text: str | None = None
    confirmed_text: str | None = None
    match_source: str | None = None
    is_edited: bool = False


class CheckItemUpdate(BaseModel):
    item_key: str
    confirmed_text: str | None = None


class CheckItemsUpdateRequest(BaseModel):
    items: list[CheckItemUpdate]


class GenerateTaskResponse(BaseModel):
    task: TaskSummary
    generated_testcase_markdown: str


class TaskMarkdownUpdateRequest(BaseModel):
    kind: Literal["requirement", "test-case"]
    markdown: str = Field(..., description="Raw markdown content to persist")


class AdoptTaskRequest(BaseModel):
    title: str | None = None


class TaskDetailResponse(BaseModel):
    task: TaskSummary
    requirement_markdown: str | None = None
    external_cooperation_markdown: str | None = None
    check_items: list[CheckItemResult] = Field(default_factory=list)
    generated_testcase_markdown: str | None = None


class TestCaseLibraryItem(BaseModel):
    id: int
    task_id: str
    title: str
    content_markdown: str
    adopted_at: datetime


class FeishuUrlPreviewResponse(BaseModel):
    """飞书文档/知识库链接解析出的展示用标题与规范化 URL。"""

    title: str
    url: str

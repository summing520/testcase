from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class PipelineStepConfig(BaseModel):
    key: str = Field(..., description="step1 | step2 | step3 | step4")
    order: int
    title: str
    description: str = ""
    enabled: bool = True
    fields: dict[str, Any] = Field(default_factory=dict)


class PipelineConfig(BaseModel):
    name: str = "测试用例生成流程"
    steps: list[PipelineStepConfig] = Field(default_factory=list)
    updated_at: datetime | None = None


class PipelineConfigUpdateRequest(BaseModel):
    name: str | None = None
    steps: list[PipelineStepConfig] | None = None

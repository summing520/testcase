from pydantic import BaseModel, Field


class TestGenerationRequest(BaseModel):
    source_code: str = Field(..., description="Source code to analyze")
    language: str = Field(default="python", description="Source code language")
    framework: str = Field(default="pytest", description="Target test framework")
    extra_requirements: str | None = Field(
        default=None, description="Additional requirements for test generation"
    )


class TestGenerationResponse(BaseModel):
    analysis: str
    test_design: str
    generated_tests: str

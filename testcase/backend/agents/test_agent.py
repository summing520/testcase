from backend.chains.code_analyzer import CodeAnalyzerChain
from backend.chains.code_generator import CodeGeneratorChain
from backend.chains.test_designer import TestDesignerChain
from backend.models.test_case import TestGenerationRequest, TestGenerationResponse


class TestGenerationAgent:
    def __init__(self, llm):
        self.code_analyzer = CodeAnalyzerChain(llm)
        self.test_designer = TestDesignerChain(llm)
        self.code_generator = CodeGeneratorChain(llm)

    def run(self, request: TestGenerationRequest) -> TestGenerationResponse:
        analysis = self.code_analyzer.run(
            source_code=request.source_code,
            language=request.language,
        )
        test_design = self.test_designer.run(
            analysis=analysis,
            framework=request.framework,
            extra_requirements=request.extra_requirements,
        )
        generated_tests = self.code_generator.run(
            source_code=request.source_code,
            language=request.language,
            framework=request.framework,
            test_design=test_design,
        )
        return TestGenerationResponse(
            analysis=analysis,
            test_design=test_design,
            generated_tests=generated_tests,
        )

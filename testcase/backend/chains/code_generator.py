from langchain_core.prompts import ChatPromptTemplate

from backend.prompts.test_prompts import TEST_GENERATION_PROMPT


class CodeGeneratorChain:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template(TEST_GENERATION_PROMPT)
        self.chain = self.prompt | self.llm

    def run(self, source_code: str, language: str, framework: str, test_design: str) -> str:
        result = self.chain.invoke(
            {
                "source_code": source_code,
                "language": language,
                "framework": framework,
                "test_design": test_design,
            }
        )
        return result.content

from langchain_core.prompts import ChatPromptTemplate

from backend.prompts.test_prompts import TEST_DESIGN_PROMPT


class TestDesignerChain:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template(TEST_DESIGN_PROMPT)
        self.chain = self.prompt | self.llm

    def run(self, analysis: str, framework: str, extra_requirements: str | None) -> str:
        result = self.chain.invoke(
            {
                "analysis": analysis,
                "framework": framework,
                "extra_requirements": extra_requirements or "None",
            }
        )
        return result.content

from langchain_core.prompts import ChatPromptTemplate

from backend.prompts.test_prompts import CODE_ANALYSIS_PROMPT
from backend.utils.code_parser import extract_code_outline


class CodeAnalyzerChain:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_template(CODE_ANALYSIS_PROMPT)
        self.chain = self.prompt | self.llm

    def run(self, source_code: str, language: str) -> str:
        outline = extract_code_outline(source_code, language)
        outline_text = (
            f"\n\nQuick structural hints:\n"
            f"- line_count: {outline['line_count']}\n"
            f"- functions: {outline['functions']}\n"
            f"- classes: {outline['classes']}\n"
        )
        result = self.chain.invoke(
            {
                "source_code": source_code + outline_text,
                "language": language,
            }
        )
        return result.content

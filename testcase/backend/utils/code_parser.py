import re


def extract_code_outline(source_code: str, language: str) -> dict:
    """
    A lightweight parser for quick structural hints.
    This is intentionally simple and can be upgraded to AST-based parsing later.
    """
    function_pattern = r"def\s+([a-zA-Z_]\w*)\s*\(" if language.lower() == "python" else r"function\s+([a-zA-Z_]\w*)\s*\("
    class_pattern = r"class\s+([a-zA-Z_]\w*)"

    functions = re.findall(function_pattern, source_code)
    classes = re.findall(class_pattern, source_code)
    lines = len(source_code.splitlines())

    return {
        "line_count": lines,
        "functions": functions,
        "classes": classes,
    }

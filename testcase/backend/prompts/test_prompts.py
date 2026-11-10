CODE_ANALYSIS_PROMPT = """
You are a senior software engineer.
Analyze the provided {language} code and return:
1. Core business logic summary
2. Public APIs/functions/classes that need tests
3. Edge cases and error paths
4. Dependencies and side effects

Code:
{source_code}
"""


TEST_DESIGN_PROMPT = """
You are a test architect.
Given the code analysis below, design a test plan for {framework}.
Include:
1. Unit test scenarios
2. Boundary and edge cases
3. Negative/error scenarios
4. Suggested mocks/stubs

Additional requirements:
{extra_requirements}

Analysis:
{analysis}
"""


TEST_GENERATION_PROMPT = """
You are an expert test engineer.
Generate complete, runnable {framework} test code for {language}.
Rules:
- Keep tests clear and maintainable
- Cover the provided test plan
- Include setup and teardown if needed
- Avoid placeholder comments unless necessary

Test plan:
{test_design}

Original source code:
{source_code}
"""

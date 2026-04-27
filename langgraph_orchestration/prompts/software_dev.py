SOFTWARE_DEV_TASKS = ["code_generation", "unit_testing", "architectural_review"]
ROUTER_SYSTEM_PROMPT = "You are a precise task router. Return JSON only."

def build_dev_task_router_prompt(user_input: str) -> str:
    """Build routing prompt for selecting the software development plan"""
    return (
        "Select only the required software development tasks for this request.\n"
        f"Request: {user_input}\n\n"
        "Allowed tasks:\n"
        "- code_generation\n"
        "- unit_testing\n"
        "- architectural_review\n\n"
        'Return strict JSON only: {"steps": ["..."]}.\n'
        "Only include necessary tasks."
    )

def build_code_generation_prompt(user_input: str, attempt: int) -> str:
    return (
        "Produce implementation-ready code for the request below.\n"
        "Include assumptions when requirements are ambiguous and keep the solution maintainable.\n\n"
        f"Request:\n{user_input}\n\n"
        f"Generation attempt: {attempt}"
    )

def build_unit_testing_prompt(code_target: str) -> str:
    return (
        "Design focused unit tests for the provided code or component.\n"
        "Prioritize critical paths, edge cases, and failure behavior.\n\n"
        f"Code or component to test:\n{code_target}"
    )

def build_architectural_review_prompt(user_request: str, combined_outputs: str) -> str:
    return (
        "Perform an architectural review of the generated solution artifacts.\n"
        "Evaluate design quality, modularity, scalability, and maintainability.\n"
        "Provide concise, actionable recommendations ranked by impact.\n\n"
        f"Original request:\n{user_request}\n\n"
        f"Generated artifacts:\n{combined_outputs}"
    )
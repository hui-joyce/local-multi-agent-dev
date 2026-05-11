from langgraph_orchestration.prompts import render_prompt
from langgraph_orchestration.tooling.prompts import build_tooling_block

SOFTWARE_DEV_TASKS = ["code_generation", "unit_testing", "architectural_review"]
ROUTER_SYSTEM_PROMPT, _ROUTER_BODY = render_prompt(
    "software_dev/task_router.md",
    user_input="",
)

def build_dev_task_router_prompt(user_input: str) -> str:
    """Build routing prompt for selecting the software development plan"""
    _, body = render_prompt(
        "software_dev/task_router.md",
        user_input=user_input,
    )
    return body


def _prepend_tooling_block(user_input: str, task_focus: str, body: str) -> str:
    tooling_block = build_tooling_block(
        domain="software_dev",
        user_input=user_input,
        task_focus=task_focus,
    )
    return f"{tooling_block}\n\n{body}"

def build_code_generation_prompt(user_input: str, attempt: int) -> str:
    _, body = render_prompt(
        "software_dev/code_generation.md",
        user_input=user_input,
        attempt=attempt,
    )
    return _prepend_tooling_block(
        user_input=user_input,
        task_focus="Plan the change, gather surrounding context, and request file or repository tools before editing.",
        body=body,
    )

def build_unit_testing_prompt(code_target: str) -> str:
    _, body = render_prompt(
        "software_dev/unit_testing.md",
        code_target=code_target,
    )
    return _prepend_tooling_block(
        user_input=code_target,
        task_focus="Inspect the implementation and request any missing files or related tests before proposing coverage.",
        body=body,
    )

def build_architectural_review_prompt(user_request: str, combined_outputs: str) -> str:
    _, body = render_prompt(
        "software_dev/architectural_review.md",
        user_request=user_request,
        combined_outputs=combined_outputs,
    )
    return _prepend_tooling_block(
        user_input=user_request,
        task_focus="Inspect surrounding architecture and repository context before issuing recommendations.",
        body=body,
    )
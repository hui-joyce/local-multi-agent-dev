from typing import TYPE_CHECKING

from langgraph_orchestration.prompts import render_prompt

if TYPE_CHECKING:
    from langgraph_orchestration.inference.inference_engine import MLXInferenceEngine

def build_label_routing_prompt(inference_engine: "MLXInferenceEngine", user_input: str) -> str:
    """
    Build a prompt for label-based routing classification.
    Returns one of: SOFTWARE_DEV, REVERSE_ENGINEERING, or BOTH
    """
    system_prompt, user_message = render_prompt(
        "supervisor/label_routing.md",
        user_input=user_input,
    )
    
    return inference_engine.build_prompt(
        user_input=user_message,
        context=None,
        system_prompt=system_prompt,
    )

def build_split_tasks_prompt(inference_engine: "MLXInferenceEngine", user_input: str) -> str:
    """Build a prompt to extract domain-specific subtasks from a multi-domain request"""
    
    system_prompt, user_message = render_prompt(
        "supervisor/split_tasks.md",
        user_input=user_input,
    )
    
    return inference_engine.build_prompt(
        user_input=user_message,
        context=None,
        system_prompt=system_prompt,
    )
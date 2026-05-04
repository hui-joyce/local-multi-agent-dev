from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langgraph_orchestration.inference.inference_engine import MLXInferenceEngine

def build_label_routing_prompt(inference_engine: "MLXInferenceEngine", user_input: str) -> str:
    """
    Build a prompt for label-based routing classification.
    Returns one of: SOFTWARE_DEV, REVERSE_ENGINEERING, or BOTH
    """
    system_prompt = (
        "You are a routing classifier for a multi-agent system. "
        "Classify each request into one of three labels only."
    )
    
    user_message = (
        "Return EXACTLY one label and nothing else:\n"
        "- SOFTWARE_DEV\n"
        "- REVERSE_ENGINEERING\n"
        "- BOTH\n\n"
        "Rules:\n"
        "- SOFTWARE_DEV: implementation, coding, architecture, tests, feature delivery\n"
        "- REVERSE_ENGINEERING: decompilation, binary/code behavior analysis, security/vulnerability analysis\n"
        "- BOTH: request explicitly asks for implementation plus security/reverse-engineering analysis\n\n"
        "Request:\n"
        f"{user_input}"
    )
    
    return inference_engine.build_prompt(
        user_input=user_message,
        context=None,
        system_prompt=system_prompt,
    )

def build_split_tasks_prompt(inference_engine: "MLXInferenceEngine", user_input: str) -> str:
    """Build a prompt to extract domain-specific subtasks from a multi-domain request"""
    
    system_prompt = (
        "You are a task decomposition specialist. "
        "Extract domain-specific portions from a request that spans multiple domains. "
        "Return strict JSON only."
    )
    
    user_message = (
        "Extract and split this multi-domain request into software_dev and reverse_engineering tasks.\n"
        "Preserve the exact intent and requirements for each domain.\n\n"
        "Guidelines:\n"
        "- software_dev: Extract the implementation/building/coding portion.\n"
        "- reverse_engineering: Extract the analysis/security/vulnerability assessment portion.\n"
        "- Do NOT add new requirements; extract from the original request only.\n"
        "- Include all relevant context for each domain.\n\n"
        "Request:\n"
        f"{user_input}\n\n"
        'Return strict JSON: {"software_dev": "extracted task for implementation", '
        '"reverse_engineering": "extracted task for analysis"}'
    )
    
    return inference_engine.build_prompt(
        user_input=user_message,
        context=None,
        system_prompt=system_prompt,
    )
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


def build_json_routing_prompt(inference_engine: "MLXInferenceEngine", user_input: str) -> str:
    system_prompt = (
        "You are a routing supervisor for a multi-agent system. "
        "Use intent-based routing with only two valid domains: software_dev and reverse_engineering. "
        "Return strict JSON only."
    )
    
    user_message = (
        "Output ONLY one JSON object and nothing else.\n\n"
        "Task:\n"
        f"{user_input}\n\n"
        "Classify using these steps:\n"
        "1) Identify implementation intent (build/generate/test/design) -> software_dev\n"
        "2) Identify analysis/security/decompilation intent -> reverse_engineering\n"
        "3) If both intents are present, return both domains and split_tasks for each domain\n"
        "4) If only one intent is present, return one domain only\n\n"
        "Return strict JSON with schema:\n"
        '{"execution_domains": ["software_dev"] | ["reverse_engineering"] | ["software_dev", "reverse_engineering"], '
        '"primary_domain": "software_dev|reverse_engineering", '
        '"split_tasks": {} | {"software_dev": "...", "reverse_engineering": "..."}, '
        '"rationale": "short reason"}'
    )
    
    return inference_engine.build_prompt(
        user_input=user_message,
        context=None,
        system_prompt=system_prompt,
    )
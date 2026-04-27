REVERSE_ENGINEERING_TASKS = ["planning", "code_analysis", "vulnerability_detection"]
ROUTER_SYSTEM_PROMPT = "You are a precise task router. Return JSON only."

def build_re_task_router_prompt(user_input: str) -> str:
    """Build routing prompt for selecting the reverse engineering plan"""
    return (
        "Select only the required reverse engineering tasks for this request.\n"
        f"Request: {user_input}\n\n"
        "Allowed tasks:\n"
        "- planning\n"
        "- code_analysis\n"
        "- vulnerability_detection\n\n"
        'Return strict JSON only: {"steps": ["..."]}.\n'
        "Only include necessary tasks."
    )

def build_planning_prompt(user_input: str) -> str:
    return (
        "Create a clear reverse-engineering plan before deep analysis.\n"
        "Break work into ordered phases with concrete objectives and expected evidence.\n\n"
        f"Target request:\n{user_input}"
    )

def build_code_analysis_prompt(user_input: str, planning_output: str = "") -> str:
    if planning_output:
        return (
            "Use the plan below to drive a structured reverse-engineering analysis.\n"
            "Focus on control flow, data flow, key components, and behavior reconstruction.\n\n"
            f"Plan:\n{planning_output}\n\n"
            f"Target:\n{user_input}"
        )

    return (
        "Perform direct reverse-engineering analysis for the target.\n"
        "Focus on structure, logic flow, and inferred behavior.\n\n"
        f"Target:\n{user_input}"
    )

def build_vulnerability_detection_prompt(user_input: str, analysis_output: str = "") -> str:
    if analysis_output:
        return (
            "Assess vulnerabilities using the analysis below as primary evidence.\n"
            "Highlight exploitability, impact, and mitigation guidance.\n\n"
            f"Analysis:\n{analysis_output}\n\n"
            f"Target:\n{user_input}"
        )

    return (
        "Perform vulnerability assessment for the target directly.\n"
        "Report likely weakness classes, attack vectors, and mitigations.\n\n"
        f"Target:\n{user_input}"
    )
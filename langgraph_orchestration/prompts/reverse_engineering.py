from langgraph_orchestration.prompts import render_prompt
from langgraph_orchestration.prompts.shared import build_tooling_block
from langgraph_orchestration.prompts.ipsw_skill import load_ipsw_skill_context, get_ipsw_skill_source

REVERSE_ENGINEERING_TASKS = ["planning", "firmware_analysis", "code_analysis", "vulnerability_detection", "firmware_categorization"]
ROUTER_SYSTEM_PROMPT, _ROUTER_BODY = render_prompt(
    "reverse_engineering/task_router.md",
    user_input="",
)

def build_re_task_router_prompt(user_input: str) -> str:
    """Build routing prompt for selecting the reverse engineering plan"""
    _, body = render_prompt(
        "reverse_engineering/task_router.md",
        user_input=user_input,
    )
    return body

def _prepend_tooling_block(user_input: str, task_focus: str, body: str) -> str:
    tooling_block = build_tooling_block(
        domain="reverse_engineering",
        user_input=user_input,
        task_focus=task_focus,
    )
    return f"{tooling_block}\n\n{body}"

def build_planning_prompt(user_input: str) -> str:
    _, body = render_prompt(
        "reverse_engineering/planning.md",
        user_input=user_input,
    )
    return _prepend_tooling_block(
        user_input=user_input,
        task_focus="Plan an evidence-driven analysis and request missing decompilation, disassembly, or metadata before deeper work.",
        body=body,
    )

def build_code_analysis_prompt(user_input: str, planning_output: str = "", generated_code: str = "") -> str:
    if generated_code and planning_output:
        intro = (
            "Analyze this GENERATED code using the structured plan below.\n"
            "Identify structural issues, logic flaws, security considerations, and design problems."
        )
    elif generated_code:
        intro = (
            "Analyze this GENERATED code for structural issues, logic flaws, and security concerns.\n"
            "Examine control flow, data handling, error scenarios, and potential vulnerabilities."
        )
    elif planning_output:
        intro = (
            "Use the plan below to drive a structured reverse-engineering analysis.\n"
            "Focus on control flow, data flow, key components, and behavior reconstruction."
        )
    else:
        intro = (
            "Perform direct reverse-engineering analysis for the target.\n"
            "Focus on structure, logic flow, and inferred behavior."
        )

    planning_block = f"Structured Plan:\n{planning_output}\n\n" if planning_output else ""
    generated_block = f"Generated Code to Analyze:\n{generated_code}\n\n" if generated_code else ""
    analysis_block = "Additional Context:\n" if generated_code else ""

    _, body = render_prompt(
        "reverse_engineering/code_analysis.md",
        intro=intro,
        planning_block=planning_block,
        generated_block=generated_block,
        analysis_block=analysis_block,
        user_input=user_input,
    )
    return _prepend_tooling_block(
        user_input=user_input,
        task_focus="Trace control flow, data flow, and surrounding evidence before finalizing conclusions.",
        body=body,
    )

def build_vulnerability_detection_prompt(user_input: str, analysis_output: str = "") -> str:
    if analysis_output:
        intro = (
            "Assess vulnerabilities using the analysis below as primary evidence.\n"
            "Highlight exploitability, impact, and mitigation guidance."
        )
        analysis_block = f"Analysis:\n{analysis_output}\n\n"
    else:
        intro = (
            "Perform vulnerability assessment for the target directly.\n"
            "Report likely weakness classes, attack vectors, and mitigations."
        )
        analysis_block = ""

    _, body = render_prompt(
        "reverse_engineering/vulnerability_detection.md",
        intro=intro,
        analysis_block=analysis_block,
        user_input=user_input,
    )
    return _prepend_tooling_block(
        user_input=user_input,
        task_focus="Validate exploitability with direct evidence and request additional binary context when needed.",
        body=body,
    )

def build_firmware_analysis_prompt(user_input: str, planning_output: str = "") -> str:
    planning_block = f"Structured Plan:\n{planning_output}\n\n" if planning_output else ""
    ipsw_skill_block = load_ipsw_skill_context()
    ipsw_skill_source = get_ipsw_skill_source()
    _, body = render_prompt(
        "reverse_engineering/firmware_analysis.md",
        user_input=user_input,
        planning_block=planning_block,
    )
    if ipsw_skill_block:
        body = (
            f"{body}\n\n"
            "## IPSW Skill Pack (Loaded)\n"
            "Use the following instructions and references as canonical command guidance.\n\n"
            f"Source: {ipsw_skill_source or 'unknown'}\n\n"
            f"{ipsw_skill_block}"
        )
    return _prepend_tooling_block(
        user_input=user_input,
        task_focus=(
            "Use ipsw tools to collect concrete firmware evidence (download/extract/diff), "
            "then prioritize IDA disassembly targets before concluding."
        ),
        body=body,
    )

def build_firmware_categorization_prompt(user_input: str, retrieved_methods: str = "") -> str:
    intro = (
        "You are an expert iOS Reverse Engineer. Analyze the provided firmware diff evidence for a specific component and categorize its reverse-engineering priority.\n\n"
        "Assess research interest based on behavioural changes in binary metadata and strings.\n\n"
        "First, assign a Behavioural Class based on the evidence (especially CStrings):\n"
        "1. SECURITY/PRIVACY: Changes involving credentials, entitlements, Sandbox, or PII. Look for framework removals (Accounts/Contacts), OIDs, or sensitive logging masks (e.g., '%{sensitive}').\n"
        "2. DATA/IPC/SYNC: Changes involving XPC, serialization, data syncing logic, databases, or file parsing.\n"
        "3. UI/LOGGING: Purely UI text updates, standard non-sensitive logging, or version bumps.\n"
        "4. METADATA: Minimal metadata changes (only UUID/size changes with no semantic strings).\n\n"
        "Second, assign an AI Prioritisation Score (Interest Score):\n"
        "- TIER_1: Critical/High Interest. Strong indicators of security boundaries, privacy-sensitive framework changes, or IPC protocol updates.\n"
        "- TIER_2: Medium Interest. Core logic updates, data sync changes, or new internal logging for complex features.\n"
        "- TIER_3: Low Interest/Noise. Proceed only if investigating a specific UI/logging bug.\n\n"
        "OUTPUT INSTRUCTIONS: You MUST output a JSON array containing EXACTLY ONE object representing the component provided. Do NOT output an empty array. No conversational filler.\n"
        "Schema:\n"
        "]\n\n"
        '  {"method": "<component_name_or_summary>", "category": "<SECURITY/AUTH|DATA/IPC|UI/BOILERPLATE|IGNORE>", "tier": "<TIER_1|TIER_2|TIER_3>", "reason": "<brief justification based on strings/evidence>"}\n'        "]\n\n"
        "Important: If there are changes to CStrings related to data syncing or privacy masks (e.g., '%{sensitive}'), do NOT ignore them; categorize as TIER_2 or higher."
    )
    method_block = f"Diff Evidence to Analyze:\n{retrieved_methods}\n\n" if retrieved_methods else ""
    
    body = f"{intro}\n\n{method_block}\n\nUser Request: {user_input}"
    return _prepend_tooling_block(
        user_input=user_input,
        task_focus="Analyze the provided diff evidence and prioritize the component strictly into JSON format.",
        body=body,
    )

def build_unified_feature_analysis_prompt(user_input: str, component_evidence: str, component_name: str, has_tool_results: bool = False, at_limit: bool = False) -> str:
    """Builds a unified prompt for deep-dive analysis, summarization, and prioritization"""
    intro = (
        "You are an expert reverse engineer performing a comprehensive analysis of a single modified binary component from a firmware update. "
        "Your mission is to use decompiler tools to understand the code's function, document your findings, and assign a priority score."
    )

    workflow = """
    **Workflow:**
    1.  **Analyze Initial Evidence**: Review the provided metadata diff to understand the initial changes (e.g., new symbols, modified strings, version bumps).
    2.  **Formulate an Investigative Hypothesis**: Based on the metadata, what is the likely purpose of this change?
    3.  **Gather Decompilation Evidence with Tools** (you have multiple rounds):

        **TOOL SELECTION GUIDE — READ CAREFULLY:**
        *   **`lookup_symbol`**: Use this ONLY for **exported function symbols** that start with an underscore (e.g., `_IMSharedHelperPayloadByStrippingServerBagKeys`). These are entries in the binary's symbol table.
        *   **`search_string`**: Use this for **C strings, Objective-C method names, selector names, and any quoted text** from the diff (e.g., `"getNumberOfTimesRespondedToThread"`, `"MessageGroupController-strip-payload-keys"`, `"_shouldAcceptGroupMessagePayloadWithExistingChat:isKnownSender:type:"`). These are raw byte sequences embedded in the binary's `__cstring` or `__objc_methname` sections.

        **MULTI-ROUND INVESTIGATION — Follow this chain:**
        *   **Round 1**: Use `lookup_symbol` for exported symbols AND `search_string` for C strings / method names from the diff. This gives you memory addresses.
        *   **Round 2**: Use `get_xrefs_to` on the addresses you found. This tells you which functions reference those symbols/strings.
        *   **Round 3**: Use `decompile_function` on the function addresses returned by `get_xrefs_to`. This gives you the actual C-like pseudo-code. You **MUST** attempt to decompile at least one function.

        **CRITICAL:** The diff only provides names, NOT addresses. You CANNOT guess addresses. You must use `lookup_symbol` or `search_string` first to get addresses.
        **FALLBACK**: If all decompiler tool calls fail with connection errors, state that the decompiler was unavailable and analyze based only on the metadata diff.

    4.  **Synthesize a Comprehensive Report**: Based on the decompiled code and metadata, generate a complete analysis with these sections:
        *   `## What this feature does`: High-level summary based on decompilation findings.
        *   `## How is it implemented`: Detailed code logic. Reference decompiled functions, algorithms, and data structures.
        *   `## How to trigger this feature`: Infer trigger conditions from function names, strings, or framework usage.
        *   `## Evidence`: Critical evidence — strings, symbol names, decompiled pseudo-code, addresses.
    5.  **Provide AI Prioritisation Score**: After the sections, add `---AI_PRIORITISATION_SCORE---` followed by a JSON object with `method`, `category` (SECURITY/PRIVACY, DATA/IPC/SYNC, UI/LOGGING, METADATA), `tier` (TIER_1, TIER_2, TIER_3), and `reason`.
    """
    if not has_tool_results:
        output_format_instructions = """
        **CURRENT STATE: GATHERING EVIDENCE (STAGE 1)**
        You have not used any tools yet. You CANNOT write the final report yet.
        You MUST output ONLY `<tool_call>` blocks. DO NOT output any markdown headers, conversational filler, or the final report.

        **YOUR FIRST ACTION**: Look at the diff evidence. For each item in the "Symbols:" section (names starting with `_`), use `lookup_symbol`. For each item in the "CStrings:" section (quoted strings), use `search_string`. Do both in this round.
        """
    else:
        if at_limit:
            output_format_instructions = """
        **CURRENT STATE: FINAL REPORT (STAGE 3)**
        **NO MORE TOOL CALLS ALLOWED.** You MUST output the final report now based on all evidence gathered.
        
        Your response MUST be a single markdown document containing the four analysis sections, followed by `---AI_PRIORITISATION_SCORE---` and the JSON score. No conversational filler.
        """
        else:
            output_format_instructions = """
        **CURRENT STATE: CONTINUE INVESTIGATION (STAGE 2)**
        Review the tool results above. You should continue the investigation chain:
        - If you have **addresses** from `lookup_symbol` or `search_string` but haven't called `get_xrefs_to` yet, call `get_xrefs_to` on those addresses now.
        - If you have **function addresses** from `get_xrefs_to` but haven't decompiled them, call `decompile_function` on those function addresses now.
        - If you still have symbols/strings you haven't looked up, look them up now.

        Output ONLY `<tool_call>` blocks if you need more evidence.
        If you have gathered enough evidence (including at least one decompiled function), output the final report starting with `## What this feature does`.
        """
    _, body = render_prompt(
        "reverse_engineering/unified_analysis.md", 
        intro=intro,
        workflow=workflow,
        output_format_instructions=output_format_instructions,
        component_name=component_name,
        component_evidence=component_evidence,
        user_input=user_input,
    )
    return _prepend_tooling_block(
        user_input=user_input,
        task_focus=(
            "Perform a full feature analysis by decompiling the binary to understand its purpose, implementation, and trigger conditions, then provide a final prioritization score."
        ),
        body=body,
    )
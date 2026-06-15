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
        "[\n"
        '  {"method": "<component_name_or_summary>", "category": "<SECURITY/AUTH|DATA/IPC|UI/BOILERPLATE|IGNORE>", "tier": "<TIER_1|TIER_2|TIER_3>", "confidence": <0-100>, "decompile": <true|false>, "reason": "<brief justification based on strings/evidence>"}\n'
        "]\n\n"
        "Important: If there are changes to CStrings related to data syncing or privacy masks (e.g., '%{sensitive}'), do NOT ignore them; categorize as TIER_2 or higher. Only TIER_1 should default to decompile=true unless you specifically require deep code analysis."
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

    **STAGE 0: PRE-DECOMPILATION TRIAGE GATE**
    Evaluate the diff evidence against the following rules.
    *High-Signal Indicators:* Added/Removed symbols or ObjC selectors, new CStrings, new entitlements, function count changes, security/privacy/IPC/database terminology.
    *Low-Signal Indicators:* UUID changes only, version bumps only, __const/__got size changes, small section drift, no symbol/string count changes.
    
    *AUTO-PROMOTE RULES:* Elevate to TIER_1 if you see: added exported symbols, security/privacy strings, authentication logic, payload filtering, XPC interfaces, server bags, cryptography, or migration logic.
    *AUTO-IGNORE RULES:* Classify as TIER_3 if only UUID/version/GOT/section-sizes changed with NO new symbols or strings.
    
    If AUTO-IGNORE applies: DO NOT decompile. Output the final metadata-only assessment immediately with `decompile: false`.
    If HIGH-SIGNAL applies: Proceed to Stage 1.

    **STAGE 1: CANDIDATE SELECTION (TOOL BUDGET LIMITS)**
    You MUST NOT exhaustively search every string/symbol. Observe these strict limits per component:
    - Max 20 symbol lookups
    - Max 20 string lookups
    *Selection Priority:* 1. Added symbols, 2. Removed symbols, 3. Added strings, 4. Security/privacy/IPC strings.

    **TOOL SELECTION GUIDE — READ CAREFULLY:**
    *   **`find_address`**: Use this to find the memory address of ANY entry listed under **`Symbols:`** or **`CStrings:`** in the diff. Pass the raw string from the diff as the `query`.
    *   **`get_xrefs_to`**: Finds code that references a specific DATA address. Use this on addresses returned by `find_address` when the result type is `string_data`.
    *   **`decompile_function`**: Decompile a CODE address to get C-like pseudo-code. Use this on addresses returned by `find_address` when the result type is `symbol`, or on xref addresses.
    *   **`resolve_objc_dispatch`**: When you see `objc_msgSend(v4, "doSomething")` and need to resolve `v4`'s class.
    *   **`trace_variable_source`**: If a function takes an untrusted pointer, use this to trace its initialization.
    *   **`rename_local_variable` & `set_comment`**: Document the binary as you decipher variables.
    *   **`save_ida_database`**: Persist the `.i64` file after annotating.

    **STAGE 2: LIMITED DECOMPILATION (TOOL BUDGET LIMITS)**
    - Max 20 xref lookups
    - Max 20 decompiled functions
    Focus only on the most critical cross-references that map to high-signal indicators.

    **STAGE 3: REPORTING & CORRELATION**
    Synthesize findings into these sections:
    *   `## What this feature does`: High-level summary based on evidence.
    *   `## How is it implemented`: Detailed code logic if decompiled. You MUST include decompiled pseudocode snippets, call chain context, and data flow tracing.

    *   `## How to trigger this feature`: Infer trigger conditions.
    *   `## Evidence`: Critical evidence (strings, symbols, addresses, entitlements).
    *   `---AI_PRIORITISATION_SCORE---`: Provide the JSON object with `method`, `category`, `tier`, `confidence`, `decompile`, and `reason`.
    If the evidence contains multiple related binaries (e.g. sharing a subsystem or version bump), synthesize them as a single cohesive feature change.
    """ 
    if not has_tool_results:
        output_format_instructions = """
        **CURRENT STATE: PRE-DECOMPILATION TRIAGE (STAGE 0) & CANDIDATE SELECTION (STAGE 1)**
        You have not used any tools yet. First, evaluate the diff against the AUTO-IGNORE rules.
        - **IF AUTO-IGNORE APPLIES (TIER_3)**: Do NOT use any tools. Immediately output the final report starting with `## What this feature does` (which will be a metadata-only assessment) and conclude with the `---AI_PRIORITISATION_SCORE---` JSON object with `"decompile": false`.
        - **IF HIGH-SIGNAL APPLIES (TIER_1/2)**: You MUST use tools to gather evidence. Do NOT output the final report. Output ONLY `<tool_call>` blocks. 
        
        **CRITICAL INSTRUCTION FOR LOCAL MODELS**: Ignore any previous general instructions that say "DO NOT include `<tool_call>` JSON". Right now, you are NOT writing the final response. You MUST include the full, valid JSON body inside EVERY `<tool_call>` block!

        **STAGE 1 TOOL MAPPING RULES (follow exactly):**
        - For ANY item listed under `Symbols:` or `CStrings:` that you want to investigate, call `find_address` (max 20 calls).
        - Pass the exact text from the diff as the `query` parameter.
        - Prioritize strings/symbols related to security, privacy, IPC, authentication, or added functionality.
        Do all applicable calls in this single round.
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
        **CURRENT STATE: LIMITED DECOMPILATION (STAGE 2)**
        Review the tool results above. You MUST strictly adhere to the tool budget limits:
        - Max 20 `get_xrefs_to` calls total.
        - Max 20 `decompile_function` calls total.
        
        Continue the investigation chain carefully:
        - If you have **data addresses** but haven't called `get_xrefs_to` yet, call it on the most critical addresses (up to the limit).
        - If you have **function addresses** from `get_xrefs_to`, call `decompile_function` on the most promising ones (up to the limit).
        - If you see a function taking an untrusted pointer, trace it using `trace_variable_source`.
        - If you see an `objc_msgSend` block you want to resolve, use `resolve_objc_dispatch`.
        - If you understand a variable or function block, use `rename_local_variable` and `set_comment` to annotate the binary, followed by `save_ida_database`.

        Output ONLY `<tool_call>` blocks if you need more evidence and haven't hit your budget.
        
        **CRITICAL INSTRUCTION FOR LOCAL MODELS**: Ignore any previous general instructions that say "DO NOT include `<tool_call>` JSON". Right now, you are NOT writing the final response. You MUST include the full, valid JSON body inside EVERY `<tool_call>` block!
        
        If you have gathered enough evidence, or if you have hit your tool budget limits, transition to STAGE 3. Output the final report starting with `## What this feature does` and conclude with the `---AI_PRIORITISATION_SCORE---` JSON object with `"decompile": true`.
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
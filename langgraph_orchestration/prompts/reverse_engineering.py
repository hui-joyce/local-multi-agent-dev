"""Prompt builders for the reverse-engineering graph.

build_unified_feature_analysis_prompt embeds a read-only "ground truth"
decompilation block (_format_ground_truth_decompilation): the model describes that
code in prose, while the graph pastes real code into the report."""

from __future__ import annotations

from langgraph_orchestration.prompts import render_prompt
from langgraph_orchestration.prompts.shared import build_tooling_block
from langgraph_orchestration.prompts.utils import _truncate

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
    return body

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
    return body

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
    return body

def build_firmware_categorization_prompt(user_input: str, retrieved_methods: str = "") -> str:
    method_block = f"Diff Evidence to Analyze:\n{retrieved_methods}\n\n" if retrieved_methods else ""
    _, body = render_prompt(
        "reverse_engineering/firmware_categorization.md",
        method_block=method_block,
        user_input=user_input,
    )
    return _prepend_tooling_block(
        user_input=user_input,
        task_focus="Analyze the provided diff evidence and prioritize the component strictly into JSON format.",
        body=body,
    )

def _format_ground_truth_decompilation(
    decompilations: list[dict] | None, per_cap: int = 3000
) -> str:
    """Render real IDA output as a ground-truth block for the model.
    Returns "" when there is nothing to ground on"""
    if not decompilations:
        return ""
    blocks: list[str] = []
    for d in decompilations:
        code = (d.get("code") or "").strip()
        if not code:
            continue
        header = d.get("symbol") or d.get("address") or "function"
        blocks.append(f"// {header}  ({d.get('address', '?')})\n{_truncate(code, per_cap)}")
    if not blocks:
        return ""
    return (
        "\n### Verified Decompilation (ground truth — real IDA output)\n"
        "This is the ACTUAL decompiled code for this component's most security-relevant "
        "functions. Base `## How is it implemented` and `## Vulnerability Assessment` on THIS "
        "code — its control flow, calls, and data handling — not on guesses from symbol names. "
        "Do NOT paste it into the report (the system re-inserts the full output for you) and do "
        "NOT state anything that contradicts it.\n"
        "```c\n" + "\n\n".join(blocks) + "\n```\n"
    )


def build_unified_feature_analysis_prompt(
    user_input: str,
    component_evidence: str,
    component_name: str,
    has_tool_results: bool = False,
    at_limit: bool = False,
    security_notes_match: str | None = None,
    security_indicators: list[str] | None = None,
    decompilations: list[dict] | None = None,
) -> str:
    notes_block = ""
    if security_notes_match:
        notes_block = (
            f"\n**MATCHED IN APPLE SECURITY NOTES (component: {security_notes_match})**\n"
            "Apple's security notes name this component as changed in this release, so it is a "
            "high-priority target. Determine what security-relevant change the diff implements and "
            "document it with specific evidence from the decompiled output.\n"
        )

    indicators_block = ""
    if security_indicators:
        indicators_block = (
            f"\n**Security-relevant patterns detected in diff**: {', '.join(security_indicators)}\n"
            "Prioritise decompiling functions that contain these patterns.\n"
        )

    intro = (
        "You are an expert reverse engineer performing a comprehensive analysis of a single modified binary component from a firmware update. "
        "This component has already been selected for deep analysis by a deterministic triage system. "
        "Your mission is to use decompiler tools to understand the code's function, document your findings in full detail, and assign a priority score."
        + notes_block
        + indicators_block
    )

    workflow = """
    **Workflow:**

    **STAGE 1: CANDIDATE SELECTION (TOOL BUDGET LIMITS)**
    You MUST NOT exhaustively search every string/symbol. Observe these strict limits per component:
    - Max 20 symbol lookups
    - Max 20 string lookups
    *Selection Priority:* 1. Added symbols, 2. Removed symbols, 3. Added strings, 4. Security/privacy/IPC strings.

    **TOOL SELECTION GUIDE — READ CAREFULLY:**
    *   **`find_address`**: Use this to find the memory address of ANY entry listed under **`Symbols:`** or **`CStrings:`** in the diff. Pass the raw string from the diff as the `query`.
        *CRITICAL*: If a symbol/string is marked with `-` (minus sign) in the diff, it means it was REMOVED in the new version. The `find_address` tool runs against the NEW binary, so it WILL NOT find removed items. If a feature was entirely removed, document its removal thoroughly in the final report — do NOT skip the component.
    *   **`get_xrefs_to`**: Finds code that references a specific DATA address. Use this on addresses returned by `find_address` when the result type is `string_data`. (Args: `address`)
    *   **`decompile_function`**: Decompile a CODE address to get C-like pseudo-code. Use this on addresses returned by `find_address` when the result type is `symbol`, or on xref addresses. (Args: `address`)
    *   **`resolve_objc_dispatch`**: When you see `objc_msgSend(v4, "doSomething")` and need to resolve `v4`'s class. (Args: `func_ea`, `call_ea`)
    *   **`trace_variable_source`**: If a function takes an untrusted pointer, use this to trace its initialization. (Args: `func_ea`, `var_name`)
    *   **`rename_local_variable`**: Document the binary as you decipher variables. (Args: `func_address`, `old_name`, `new_name`)
    *   **`set_comment`**: Add a comment to a specific assembly address. (Args: `address`, `comment`)
    *   **`save_ida_database`**: Persist the `.i64` file after annotating.

    **STAGE 2: LIMITED DECOMPILATION & DB ANNOTATION (TOOL BUDGET LIMITS)**
    - Max 20 xref lookups
    - Max 20 decompiled functions
    Focus only on the most critical cross-references that map to high-signal indicators.
    *Recursive Decompilation:* Perform further/recursive decompilation when a called/calling function is critical to understanding the implementation of a feature.
    *Database Annotation (MANDATORY):* For each binary opened, you MUST utilize the `set_comment` tool to document data flow, call traces, and important entry points. Rename variables with `rename_local_variable` when you decipher them, and call `save_ida_database` to persist annotations.

    **STAGE 3: REPORTING & CORRELATION**
    If a `### Verified Decompilation (ground truth)` block is provided above, it is the AUTHORITATIVE source for this component's implementation — ground your `How is it implemented` and `Vulnerability Assessment` claims in that real code and never contradict it.
    Synthesize findings into these sections:
    *   `## What this feature does`: High-level summary based on evidence.
    *   `## How is it implemented`: Explain the implementation logic in PROSE. CRITICAL: do NOT write, paste, paraphrase, or invent any `c`/pseudocode code block here — the system automatically inserts the real `decompile_function` output into this section for you, so hand-written code is never needed and will be discarded. Your job is: (1) during Stage 2, actually call `decompile_function` on the key addresses; (2) here, describe in words what that decompiled code does (control flow, key calls, data handling). If you did NOT call `decompile_function`, say so plainly and describe the implementation from binary-level diff evidence (section size changes, removed dylib dependencies, symbol/function count changes) and string evidence. NEVER fabricate a function body or a decompilation.
    *   `## How to trigger this feature`: Infer trigger conditions.
    *   `## Vulnerability Assessment`: Analyze structural changes (new bounds checks, locking mechanisms, changed parameter types, memory management) to determine if this is a security patch. If it is a potential vulnerability fix, identify the likely vulnerability class (e.g., Use-After-Free, Out-of-Bounds, Privilege Escalation, Race Condition), how the old code was exploitable, how the new code mitigates it, and the potential impact if left unpatched. Be highly accurate and base this strictly on the evidence.
    *   `## Evidence`: Critical evidence (strings, symbols, addresses, entitlements, binary diff).
    *   `---AI_PRIORITISATION_SCORE---`: Provide the JSON object with `method`, `category`, `tier`, and `reason`. Use this rubric to assign `tier` — the value MUST be exactly one of these three strings, no substitutions:
        - `TIER_1`: Critical/high interest. Security boundaries, privilege changes, crypto/auth logic, IPC protocol updates, entitlement changes, privacy-sensitive framework changes, or any memory-safety fix (UAF, OOB, race).
        - `TIER_2`: Medium interest. Core business-logic updates, data-sync or serialisation changes, new internal subsystem logging, daemon lifecycle changes (e.g. observer registration/removal), or refactors with clear functional impact.
        - `TIER_3`: Low interest/noise. Pure UI text, version bumps, asset-table expansions with no code logic change, or telemetry jitter with no privacy implication.
        Assign `TIER_1` or `TIER_2` for any component whose change has observable runtime behaviour or security relevance.
    If the evidence contains multiple related binaries (e.g. sharing a subsystem or version bump), synthesize them as a single cohesive feature change.
    """
    # Four cases based on tool state and IDA availability:
    # 1. No tools used yet + IDA available      → Stage 1: must call find_address first
    # 2. No tools used yet + IDA unavailable    → Stage 3: write report from evidence only
    # 3. Has tool results  + budget exhausted   → Stage 3: final report now
    # 4. Has tool results  + budget remaining   → Stage 2: continue decompilation
    if not has_tool_results and at_limit:
        # IDA unavailable — write the report from binary diff + string/symbol evidence
        output_format_instructions = """
        **CURRENT STATE: FINAL REPORT FROM EVIDENCE (STAGE 3 — IDA UNAVAILABLE)**
        The decompiler could not be started for this component. You MUST still write a thorough report using the binary-level diff evidence provided above (section size changes, removed/added dylib dependencies, function count changes, symbol/string changes).

        Your response MUST be a single markdown document starting EXACTLY with `## What this feature does`.
        DO NOT include any `<tool_call>` tags.
        End with `---AI_PRIORITISATION_SCORE---` and the JSON score.
        In `## How is it implemented`, describe what the binary diff reveals about the change — removed classes, dropped dependencies, text section shrinkage, etc.
        No conversational filler. No skipping sections.
        """
    elif not has_tool_results:
        # IDA available and no tools used yet — must call tools before writing the report
        output_format_instructions = """
        **CURRENT STATE: CANDIDATE SELECTION (STAGE 1)**
        You have not used any tools yet. You MUST call tools to gather evidence before writing the final report.
        DO NOT output the final report in this turn. Output ONLY `<tool_call>` blocks.

        **CRITICAL INSTRUCTION FOR TOOL CALLS**: Output a fully valid JSON object wrapped exactly in `<tool_call>...</tool_call>` tags.

        **STAGE 1 TOOL MAPPING RULES (follow exactly):**
        - For items listed under `Symbols:` or `CStrings:`, call `find_address` (max 20 calls total).
        - Pass the exact text from the diff as the `query` parameter.
        - Prioritize added symbols, security/privacy strings, and IPC/authentication identifiers.
        - Issue all applicable `find_address` calls in this single round — do not stop after one.
        """
    elif at_limit:
        output_format_instructions = """
        **CURRENT STATE: FINAL REPORT (STAGE 3)**
        **NO MORE TOOL CALLS ALLOWED.** You MUST output the final report now based on all evidence gathered.

        Your response MUST be a single markdown document. You MUST start your response EXACTLY with `## What this feature does`. DO NOT include any `<tool_call>` tags. End your report with `---AI_PRIORITISATION_SCORE---` and the JSON score. No conversational filler.

        **PSEUDOCODE RULE**: Do NOT paste, paraphrase, or invent any code block in `## How is it implemented` — the system inserts the real `decompile_function` output there for you, and any code you write will be discarded. Write only a prose explanation of what the decompiled code does. Never fabricate a function body.
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
        - You MUST use `set_comment` to document data flow and call traces for each binary opened.
        - Use `rename_local_variable` to give meaningful names to variables as you decipher them.
        - Always run `save_ida_database` after renaming variables or setting comments to persist your work.

        Output ONLY `<tool_call>` blocks if you need more evidence and haven't hit your budget.

        **CRITICAL INSTRUCTION FOR TOOL CALLS**: Output a fully valid JSON object wrapped exactly in `<tool_call>...</tool_call>` tags. Do not output conversational text.

        If you have gathered enough evidence, or if you have hit your tool budget limits, transition to STAGE 3. Output the final report starting EXACTLY with `## What this feature does` and concluding with the `---AI_PRIORITISATION_SCORE---` JSON object.

        **PSEUDOCODE RULE**: In `## How is it implemented`, write only a prose explanation — do NOT paste or invent any code block. The system automatically inserts the real `decompile_function` output for you. Never fabricate a function body.
        """
    if security_notes_match:
        workflow += (
            f"\n    **SECURITY-NOTES CORRELATION REQUIREMENT (MANDATORY when matched in Apple Security Notes)**\n"
            f"    Apple's security notes name '{security_notes_match}' as changed this release. "
            f"The `## Vulnerability Assessment` section MUST explicitly answer:\n"
            f"    1. **Security-relevant change**: What did the diff actually change in this component?\n"
            f"    2. **Patch mechanism**: Explain exactly how the decompiled/diff code achieves it "
            f"(e.g., added size check before memcpy, introduced lock around shared state access).\n"
            f"    3. **Evidence**: Justify your conclusion with specific evidence from the decompiled output. "
            f"If you cannot find a security-relevant change, say so and assign a lower tier.\n"
        )

    _, body = render_prompt(
        "reverse_engineering/unified_analysis.md",
        intro=intro,
        workflow=workflow,
        output_format_instructions=output_format_instructions,
        component_name=component_name,
        component_evidence=component_evidence,
        ground_truth_decompilation=_format_ground_truth_decompilation(decompilations),
        user_input=user_input,
    )
    return _prepend_tooling_block(
        user_input=user_input,
        task_focus=(
            "Perform a full feature analysis by decompiling the binary to understand its purpose, implementation, and trigger conditions, then provide a final prioritization score."
        ),
        body=body,
    )
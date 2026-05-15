"""
Reverse-engineering graph for handling IPSW analysis tasks.
resolution -> download -> extraction -> semantic analysis -> synthesis.
"""

from __future__ import annotations

import json
import os
import re

from langgraph.graph import END, StateGraph

from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.core.state_utils import StateManager
from langgraph_orchestration.prompts.shared import get_allowed_tools
from langgraph_orchestration.retrievers.config import RAGConfigManager
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.tooling.executor import get_tool_executor
from langgraph_orchestration.tooling.tool import ToolRequest, ToolResult


def build_reverse_engineering_graph(factory: MLXAgentFactory = None):
    if factory is None or isinstance(factory, dict):
        factory = MLXAgentFactory()

    analysis_agent = factory.create_code_analysis_agent()
    full_download_timeout = 4 * 60 * 60
    dyld_extract_timeout = 4 * 60 * 60
    kernel_extract_timeout = 60 * 60

    graph = StateGraph(AgentState)

    def _parse_firmware_targets(user_input: str) -> list[dict[str, str]]:
        targets: list[dict[str, str]] = []
        seen: set[tuple[str, str, str]] = set()

        ipsw_pattern = r"([\w,]+)_(\d+\.\d+(?:\.\d+)?)_([A-Za-z0-9]+)_Restore\.ipsw"
        for device, version, build in re.findall(ipsw_pattern, user_input):
            key = (device, version, build)
            if key in seen:
                continue
            seen.add(key)
            targets.append({"device": device, "version": version, "build": build})

        if targets:
            return targets

        device_match = re.search(r"\b(iPhone\d+,\d+|iPad\d+,\d+|Watch\d+,\d+|AppleTV\d+,\d+)\b", user_input)
        versions = re.findall(r"\b\d+\.\d+(?:\.\d+)?\b", user_input)
        if device_match and versions:
            for version in versions[:2]:
                key = (device_match.group(1), version, "")
                if key in seen:
                    continue
                seen.add(key)
                targets.append({"device": device_match.group(1), "version": version, "build": ""})

        return targets

    def _run_tool_requests(state: AgentState, requests: list[ToolRequest]) -> tuple[list[ToolResult], list[str]]:
        executor = get_tool_executor("reverse_engineering", workspace_root=state.workspace_root)
        allowed = state.tool_policy.allowed_tools or []
        results: list[ToolResult] = []
        summary_lines: list[str] = []

        for req in requests:
            if allowed and req.tool_name not in allowed:
                result = ToolResult(
                    tool_name=req.tool_name,
                    success=False,
                    output="",
                    error=f"Tool not allowed: {req.tool_name}",
                )
            else:
                try:
                    result = executor.execute(req)
                except Exception as exc:
                    result = ToolResult(tool_name=req.tool_name, success=False, output="", error=str(exc))

            state.register_tool_request(req)
            state.register_tool_result(result)
            results.append(result)
            command = str(result.metadata.get("command", "")).strip()
            if result.success:
                command_info = f" | cmd={command}" if command else ""
                summary_lines.append(f"OK {req.tool_name}{command_info}: {(result.output or '')[:400]}")
            else:
                command_info = f" | cmd={command}" if command else ""
                summary_lines.append(f"ERR {req.tool_name}{command_info}: {result.error}")

        return results, summary_lines

    def _download_output_dir(state: AgentState) -> str:
        root = state.workspace_root or os.getcwd()
        return os.path.join(root, ".ipsw_downloads")

    def _is_download_extract_only_request(user_input: str) -> bool:
        lowered = (user_input or "").lower()
        if not ("download" in lowered and "extract" in lowered):
            return False
        if "only" in lowered and "do not perform" in lowered:
            return True
        blocked = ["compare", "diff", "vulnerable", "disassembly", "inference", "analysis"]
        return not any(token in lowered for token in blocked)

    def _collect_confirmed_local_artifacts(state: AgentState) -> list[str]:
        download_dir = _download_output_dir(state)
        if not os.path.isdir(download_dir):
            return []

        targets = _parse_firmware_targets(state.user_input)
        artifacts: list[str] = []

        for target in targets:
            device = target.get("device", "")
            version = target.get("version", "")
            build = target.get("build", "")

            if device and version and build:
                expected = f"{device}_{version}_{build}_Restore.ipsw"
                expected_path = os.path.join(download_dir, expected)
                if os.path.isfile(expected_path):
                    artifacts.append(expected_path)

        for name in os.listdir(download_dir):
            if not name.endswith(".ipsw"):
                continue
            full_path = os.path.join(download_dir, name)
            if os.path.isfile(full_path):
                artifacts.append(full_path)

        return sorted(set(artifacts))

    def _tool_observation_block(state: AgentState) -> str:
        if not state.tool_results:
            return ""
        recent = state.tool_results[-3:]
        lines = ["Recent execution evidence:"]
        for result in recent:
            if result.success:
                lines.append(f"- {result.tool_name}: {(result.output or '')[:1200]}")
            else:
                lines.append(f"- {result.tool_name} failed: {result.error}")
        return "\n".join(lines)

    def _analysis_prompt(state: AgentState, instruction: str) -> str:
        evidence = _tool_observation_block(state)
        if not evidence:
            return instruction
        return f"{instruction}\n\n{evidence}"

    def retrieve_re_context_node(state: AgentState) -> AgentState:
        RAGConfigManager.initialize()
        rag_manager = RAGConfigManager.get_rag_manager()
        config = RAGConfigManager.get_config()
        context = rag_manager.retrieve_reverse_engineering_context(
            query=state.user_input,
            top_k=config.default_top_k,
        )

        state.re_context = context
        state.selected_domain = "reverse_engineering"
        state.execution_domains = ["reverse_engineering"]
        state.re_task_plan = ["firmware_analysis"]
        state.split_tasks = {}
        state.tool_policy.allowed_tools = get_allowed_tools("reverse_engineering")
        state.max_tool_iterations = state.tool_policy.max_iterations
        return StateManager.add_retrieved_context(state, context)

    def firmware_locator_node(state: AgentState) -> AgentState:
        targets = _parse_firmware_targets(state.user_input)
        if not targets:
            payload = {
                "status": "unresolved",
                "error": "Unable to resolve firmware targets from input.",
            }
        else:
            payload = {
                "status": "resolved",
                "targets": targets,
            }
        return StateManager.add_intermediate_output(
            state,
            "firmware_locator",
            json.dumps(payload, ensure_ascii=True, indent=2),
        )

    def firmware_downloader_node(state: AgentState) -> AgentState:
        targets = _parse_firmware_targets(state.user_input)
        requests: list[ToolRequest] = []
        output_dir = _download_output_dir(state)
        os.makedirs(output_dir, exist_ok=True)

        for target in targets:
            base = ["download", "ipsw", "--device", target["device"]]
            if target.get("build"):
                base.extend(["--build", target["build"]])
            else:
                base.extend(["--version", target["version"]])

            requests.append(
                ToolRequest(
                    tool_name="ipsw_cli",
                    arguments={"args": base + ["--output", output_dir, "--resume-all"], "timeout": full_download_timeout},
                    target=f"{target['device']}:{target['version'] or target['build']}",
                    reason="Download firmware artifact.",
                )
            )

        _, summary = _run_tool_requests(state, requests)
        confirmed = _collect_confirmed_local_artifacts(state)
        summary.append(f"Confirmed local artifacts: {len(confirmed)}")
        for artifact in confirmed:
            summary.append(f"LOCAL_ARTIFACT {artifact}")

        if not requests:
            summary.append("No resolved targets; download stage skipped.")
        return StateManager.add_intermediate_output(state, "firmware_downloader", "\n".join(summary))

    def ipsw_extractor_node(state: AgentState) -> AgentState:
        local_ipsws = _collect_confirmed_local_artifacts(state)
        requests: list[ToolRequest] = []

        for ipsw in local_ipsws:
            requests.append(
                ToolRequest(
                    tool_name="ipsw_cli",
                    arguments={"args": ["extract", "--dyld", "--dyld-arch", "arm64e", ipsw], "timeout": dyld_extract_timeout},
                    target=ipsw,
                    reason="Extract dyld_shared_cache.",
                )
            )
            requests.append(
                ToolRequest(
                    tool_name="ipsw_cli",
                    arguments={"args": ["extract", "--kernel", ipsw], "timeout": kernel_extract_timeout},
                    target=ipsw,
                    reason="Extract kernelcache.",
                )
            )

        _, summary = _run_tool_requests(state, requests)
        if not requests:
            summary.append("No confirmed local artifacts available; extraction skipped.")
        return StateManager.add_intermediate_output(state, "ipsw_extractor", "\n".join(summary))

    def objc_class_analyzer_node(state: AgentState) -> AgentState:
        prompt = _analysis_prompt(
            state,
            "Analyze extracted firmware artifacts for Objective-C class-level changes and impacted frameworks.",
        )
        output = analysis_agent.invoke(user_input=prompt, context=state.re_context)
        return StateManager.add_intermediate_output(state, "objc_class_analyzer", output)

    def framework_diff_engine_node(state: AgentState) -> AgentState:
        prompt = _analysis_prompt(
            state,
            "Analyze framework-level deltas from extracted firmware artifacts and summarize concrete binary/resource changes.",
        )
        output = analysis_agent.invoke(user_input=prompt, context=state.re_context)
        return StateManager.add_intermediate_output(state, "framework_diff_engine", output)

    def entitlement_diff_engine_node(state: AgentState) -> AgentState:
        prompt = _analysis_prompt(
            state,
            "Analyze entitlement-level changes from extracted artifacts and identify security-relevant policy shifts.",
        )
        output = analysis_agent.invoke(user_input=prompt, context=state.re_context)
        return StateManager.add_intermediate_output(state, "entitlement_diff_engine", output)

    def symbol_diff_engine_node(state: AgentState) -> AgentState:
        prompt = _analysis_prompt(
            state,
            "Analyze symbol-level deltas from extracted kernel and dyld artifacts and prioritize high-signal changes.",
        )
        output = analysis_agent.invoke(user_input=prompt, context=state.re_context)
        return StateManager.add_intermediate_output(state, "symbol_diff_engine", output)

    def feature_inference_agent_node(state: AgentState) -> AgentState:
        prompt = _analysis_prompt(
            state,
            "Infer likely platform changes from observed firmware deltas and clearly separate confirmed vs likely inferences.",
        )
        output = analysis_agent.invoke(user_input=prompt, context=state.re_context)
        return StateManager.add_intermediate_output(state, "feature_inference_agent", output)

    def firmware_analysis_node(state: AgentState) -> AgentState:
        stage_keys = [
            "firmware_locator",
            "firmware_downloader",
            "ipsw_extractor",
            "objc_class_analyzer",
            "framework_diff_engine",
            "entitlement_diff_engine",
            "symbol_diff_engine",
            "feature_inference_agent",
        ]

        sections: list[str] = []
        for key in stage_keys:
            text = (state.intermediate_outputs.get(key) or "").strip()
            if text:
                sections.append(f"## {key}\n{text}")

        if state.tool_results:
            sections.append(StateManager.format_tool_activity(state))

        output = "\n\n".join(sections) if sections else "No IPSW execution output captured."
        return StateManager.add_intermediate_output(state, "firmware_analysis", output)

    def synthesize_output(state: AgentState) -> AgentState:
        final = state.intermediate_outputs.get("firmware_analysis", "")
        if not final:
            final = "IPSW execution pipeline completed without synthesized content."

        state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(final)
        state.agent_chain.append("reverse_engineering_synthesize")
        return state

    def route_after_extractor(state: AgentState) -> str:
        if _is_download_extract_only_request(state.user_input):
            return "firmware_analysis"
        return "objc_class_analyzer"

    graph.add_node("retrieve_re_context", retrieve_re_context_node)
    graph.add_node("firmware_locator", firmware_locator_node)
    graph.add_node("firmware_downloader", firmware_downloader_node)
    graph.add_node("ipsw_extractor", ipsw_extractor_node)
    graph.add_node("objc_class_analyzer", objc_class_analyzer_node)
    graph.add_node("framework_diff_engine", framework_diff_engine_node)
    graph.add_node("entitlement_diff_engine", entitlement_diff_engine_node)
    graph.add_node("symbol_diff_engine", symbol_diff_engine_node)
    graph.add_node("feature_inference_agent", feature_inference_agent_node)
    graph.add_node("firmware_analysis", firmware_analysis_node)
    graph.add_node("synthesize", synthesize_output)

    graph.add_edge("retrieve_re_context", "firmware_locator")
    graph.add_edge("firmware_locator", "firmware_downloader")
    graph.add_edge("firmware_downloader", "ipsw_extractor")
    graph.add_conditional_edges(
        "ipsw_extractor",
        route_after_extractor,
        {
            "firmware_analysis": "firmware_analysis",
            "objc_class_analyzer": "objc_class_analyzer",
        },
    )
    graph.add_edge("objc_class_analyzer", "framework_diff_engine")
    graph.add_edge("framework_diff_engine", "entitlement_diff_engine")
    graph.add_edge("entitlement_diff_engine", "symbol_diff_engine")
    graph.add_edge("symbol_diff_engine", "feature_inference_agent")
    graph.add_edge("feature_inference_agent", "firmware_analysis")
    graph.add_edge("firmware_analysis", "synthesize")
    graph.add_edge("synthesize", END)

    graph.set_entry_point("retrieve_re_context")

    compiled = graph.compile()
    compiled.name = "Reverse Engineering IPSW Pipeline"
    compiled.description = "Deterministic IPSW execution pipeline for firmware reverse engineering"
    return compiled
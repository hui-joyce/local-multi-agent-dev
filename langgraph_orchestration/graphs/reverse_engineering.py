"""
Reverse-engineering graph for handling IPSW analysis tasks.
resolution -> download -> extraction -> diff -> synthesis.
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
from ipsw_service.agents.ipsw_extractor import IpswExtractorAgent
from ipsw_service.cli import build_download_args
from ipsw_service.firmware_diff_service import FirmwareDiffService
from ipsw_service.models import FirmwareDiffRequest
from ipsw_service.utils import read_text
from ipsw_service.firmware_catalog import FirmwareCatalogService


def build_reverse_engineering_graph(factory: MLXAgentFactory = None):
    if factory is None or isinstance(factory, dict):
        factory = MLXAgentFactory()

    full_download_timeout = 4 * 60 * 60

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

    def _extract_output_dir(state: AgentState) -> str:
        root = state.workspace_root or os.getcwd()
        return os.path.join(root, ".ipsw_extracted")

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
                continue

            if device and version:
                prefix = f"{device}_{version}_"
                for name in os.listdir(download_dir):
                    if name.startswith(prefix) and name.endswith("_Restore.ipsw"):
                        full_path = os.path.join(download_dir, name)
                        if os.path.isfile(full_path):
                            artifacts.append(full_path)

        if targets:
            return sorted(set(artifacts))

        for name in os.listdir(download_dir):
            if not name.endswith(".ipsw"):
                continue
            full_path = os.path.join(download_dir, name)
            if os.path.isfile(full_path):
                artifacts.append(full_path)

        return sorted(set(artifacts))

    def _parse_version_tuple(version: str) -> tuple[int, ...]:
        return tuple(int(part) for part in version.split(".") if part.isdigit())

    def _order_ipsw_paths(paths: list[str]) -> list[str]:
        def key(path: str) -> tuple[tuple[int, ...], str]:
            name = os.path.basename(path)
            match = re.search(r"_(\d+\.\d+(?:\.\d+)?)_([A-Za-z0-9]+)_Restore\.ipsw", name)
            if not match:
                return ((), name)
            return (_parse_version_tuple(match.group(1)), match.group(2))

        return sorted(paths, key=key)

    def _select_diff_pair(paths: list[str]) -> tuple[str | None, str | None]:
        if len(paths) < 2:
            return None, None
        ordered = _order_ipsw_paths(paths)
        return ordered[0], ordered[-1]

    def _format_version_from_ipsw(path: str) -> str | None:
        name = os.path.basename(path)
        match = re.search(r"_(\d+\.\d+(?:\.\d+)?)_([A-Za-z0-9]+)_Restore\.ipsw", name)
        if not match:
            return None
        version, build = match.group(1), match.group(2)
        return f"{version} ({build})"

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
        if not targets and os.getenv("IPSW_DOWNLOADS_API_ENABLE") == "1":
            catalog = FirmwareCatalogService()
            identifier = catalog.resolve_by_model_hint(state.user_input)
            if identifier:
                resolved = catalog.resolve_latest_ipsw(identifier)
                if resolved:
                    targets = [{"device": resolved.get("device", ""), "version": resolved.get("version", ""), "build": resolved.get("build", "")}]
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
            base = build_download_args(
                device=target["device"],
                version=target.get("version") or None,
                build=target.get("build") or None,
                output_dir=output_dir,
                resume_all=True,
            )

            requests.append(
                ToolRequest(
                    tool_name="ipsw_cli",
                    arguments={"args": base, "timeout": full_download_timeout},
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
        extractor = IpswExtractorAgent(workspace_root=state.workspace_root)
        output_dir = _extract_output_dir(state)
        payload = extractor.extract(local_ipsws, output_dir)
        if not local_ipsws:
            payload["note"] = "No confirmed local artifacts available; extraction skipped."
        return StateManager.add_intermediate_output(state, "ipsw_extractor", json.dumps(payload, ensure_ascii=True, indent=2))

    def firmware_diff_service_node(state: AgentState) -> AgentState:
        local_ipsws = _collect_confirmed_local_artifacts(state)
        old_ipsw, new_ipsw = _select_diff_pair(local_ipsws)
        if not old_ipsw or not new_ipsw:
            payload = {"status": "skipped", "reason": "Need two IPSW artifacts for firmware diff."}
            return StateManager.add_intermediate_output(state, "firmware_diff_report", json.dumps(payload, ensure_ascii=True, indent=2))

        dyld_map: dict[str, str | None] = {}
        kernel_map: dict[str, str | None] = {}
        extractor_output = state.intermediate_outputs.get("ipsw_extractor", "")
        if extractor_output:
            try:
                data = json.loads(extractor_output)
                for entry in data.get("extractions", []):
                    ipsw = entry.get("ipsw")
                    if ipsw:
                        dyld_paths = entry.get("dyld_paths", [])
                        kernel_paths = entry.get("kernel_paths", [])
                        dyld_map[ipsw] = dyld_paths[0] if dyld_paths else None
                        kernel_map[ipsw] = kernel_paths[0] if kernel_paths else None
            except Exception:
                pass

        request = FirmwareDiffRequest(
            old_ipsw=old_ipsw,
            new_ipsw=new_ipsw,
            old_dyld=dyld_map.get(old_ipsw),
            new_dyld=dyld_map.get(new_ipsw),
            old_kernelcache=kernel_map.get(old_ipsw),
            new_kernelcache=kernel_map.get(new_ipsw),
            old_version=_format_version_from_ipsw(old_ipsw),
            new_version=_format_version_from_ipsw(new_ipsw),
        )
        service = FirmwareDiffService(workspace_root=state.workspace_root)
        result = service.run(request)

        report_text = read_text(result.artifacts.report_markdown)
        return StateManager.add_intermediate_output(state, "firmware_diff_report", report_text)

    def firmware_analysis_node(state: AgentState) -> AgentState:
        stage_keys = [
            "firmware_locator",
            "firmware_downloader",
            "ipsw_extractor",
            "firmware_diff_report",
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
        report = state.intermediate_outputs.get("firmware_diff_report", "")
        if report:
            state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(report)
            state.agent_chain.append("reverse_engineering_synthesize")
            return state

        final = state.intermediate_outputs.get("firmware_analysis", "")
        if not final:
            final = "IPSW execution pipeline completed without synthesized content."

        state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(final)
        state.agent_chain.append("reverse_engineering_synthesize")
        return state

    def route_after_extractor(state: AgentState) -> str:
        if _is_download_extract_only_request(state.user_input):
            return "firmware_analysis"
        return "firmware_diff_service"

    graph.add_node("retrieve_re_context", retrieve_re_context_node)
    graph.add_node("firmware_locator", firmware_locator_node)
    graph.add_node("firmware_downloader", firmware_downloader_node)
    graph.add_node("ipsw_extractor", ipsw_extractor_node)
    graph.add_node("firmware_diff_service", firmware_diff_service_node)
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
            "firmware_diff_service": "firmware_diff_service",
        },
    )
    graph.add_edge("firmware_diff_service", "firmware_analysis")
    graph.add_edge("firmware_analysis", "synthesize")
    graph.add_edge("synthesize", END)

    graph.set_entry_point("retrieve_re_context")

    compiled = graph.compile()
    compiled.name = "Reverse Engineering IPSW Pipeline"
    compiled.description = "Deterministic IPSW execution pipeline for firmware reverse engineering"
    return compiled
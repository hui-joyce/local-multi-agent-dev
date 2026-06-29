"""
Reverse-engineering graph for handling IPSW analysis tasks
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
from langgraph_orchestration.triage.rules import triage_evidence_explained
from langgraph_orchestration.tooling.executor import get_tool_executor, tool_executor_node, should_continue_tool_loop
from langgraph_orchestration.tooling.tool import ToolRequest, ToolResult
from langgraph_orchestration.inference.inference_engine import GenerationConfig
from ipsw_service.agents.ipsw_extractor import IpswExtractorAgent
from ipsw_service.cli import build_download_args
from ipsw_service.security_notes_service import SecurityNotesService
from ipsw_service.firmware_diff_service import FirmwareDiffService
from ipsw_service.models import FirmwareDiffRequest
from ipsw_service.utils import ensure_dir, read_text, write_text
from ipsw_service.firmware_catalog import FirmwareCatalogService


def build_reverse_engineering_graph(factory: MLXAgentFactory = None):
    if factory is None or isinstance(factory, dict):
        factory = MLXAgentFactory()

    feature_engine = None
    def _get_feature_engine():
        nonlocal feature_engine
        if feature_engine is None:
            feature_engine = factory.ensure_loaded()
        return feature_engine

    def _sanitize_model_output(text: str) -> str:
        if not isinstance(text, str):
            try:
                text = str(text)
            except Exception:
                return ""
        return text.strip()

    full_download_timeout = 4 * 60 * 60

    graph = StateGraph(AgentState)

    def _parse_firmware_targets(state: AgentState) -> list[dict[str, str]]:
        if "parsed_firmware_targets" in state.intermediate_outputs:
            try:
                return json.loads(state.intermediate_outputs["parsed_firmware_targets"])
            except Exception:
                pass

        user_input = state.user_input
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
            state.intermediate_outputs["parsed_firmware_targets"] = json.dumps(targets)
            return targets

        device_match = re.search(r"\b(iPhone\d+,\d+|iPad\d+,\d+|Watch\d+,\d+|AppleTV\d+,\d+)\b", user_input)
        versions_and_builds = re.findall(r"(?<![\w\.])(\d+\.\d+(?:\.\d+)?)(?:_([A-Za-z0-9]+))?(?![\w\.])", user_input)
        if device_match and versions_and_builds:
            for version, build in versions_and_builds[:2]:
                key = (device_match.group(1), version, build)
                if key in seen:
                    continue
                seen.add(key)
                targets.append({"device": device_match.group(1), "version": version, "build": build})

        state.intermediate_outputs["parsed_firmware_targets"] = json.dumps(targets)
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
        blocked = ["compare", "diff", "vulnerable", "disassembly", "inference", "analysis"]
        has_blocked = any(token in lowered for token in blocked)
        if has_blocked:
            if "only" in lowered and "do not perform" in lowered:
                return True
            return False
        return True

    def _collect_confirmed_local_artifacts(state: AgentState) -> list[str]:
        if "confirmed_local_ipsws" in state.intermediate_outputs:
            try:
                return json.loads(state.intermediate_outputs["confirmed_local_ipsws"])
            except Exception:
                pass

        download_dir = _download_output_dir(state)
        if not os.path.isdir(download_dir):
            return []

        targets = _parse_firmware_targets(state)
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
                continue
                
            if version and build:
                suffix = f"_{version}_{build}_Restore.ipsw"
                for name in os.listdir(download_dir):
                    if name.endswith(suffix):
                        full_path = os.path.join(download_dir, name)
                        if os.path.isfile(full_path):
                            artifacts.append(full_path)

        if targets:
            artifacts = sorted(set(artifacts))
            state.intermediate_outputs["confirmed_local_ipsws"] = json.dumps(artifacts)
            return artifacts

        for name in os.listdir(download_dir):
            if not name.endswith(".ipsw"):
                continue
            full_path = os.path.join(download_dir, name)
            if os.path.isfile(full_path):
                artifacts.append(full_path)

        artifacts = sorted(set(artifacts))
        state.intermediate_outputs["confirmed_local_ipsws"] = json.dumps(artifacts)
        return artifacts

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

    def _select_diff_pair(state: AgentState, paths: list[str]) -> tuple[str | None, str | None]:
        if "diff_pair_old" in state.intermediate_outputs and "diff_pair_new" in state.intermediate_outputs:
            old = state.intermediate_outputs["diff_pair_old"] or None
            new = state.intermediate_outputs["diff_pair_new"] or None
            return old, new

        if len(paths) < 2:
            return None, None
        ordered = _order_ipsw_paths(paths)
        old, new = ordered[0], ordered[-1]
        state.intermediate_outputs["diff_pair_old"] = old or ""
        state.intermediate_outputs["diff_pair_new"] = new or ""
        return old, new

    def _format_version_from_ipsw(path: str) -> str | None:
        name = os.path.basename(path)
        match = re.search(r"_(\d+\.\d+(?:\.\d+)?)_([A-Za-z0-9]+)_Restore\.ipsw", name)
        if not match:
            return None
        version, build = match.group(1), match.group(2)
        return f"{version} ({build})"

    def _slugify_feature(text: str) -> str:
        cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("._-")
        return cleaned or "feature"

    _SECURITY_INDICATOR_RES = [
        (re.compile(r'\b(malloc|calloc|realloc|free)\b'), "heap allocation"),
        (re.compile(r'\bos_unfair_lock\b'), "lock primitive"),
        (re.compile(r'\bpanic\b|\babort\b|\b__stack_chk_fail\b'), "bounds/stack guard"),
        (re.compile(r'valueForEntitlement:', re.IGNORECASE), "entitlement check"),
        (re.compile(r'\b(UAF|use.after.free|out.of.bounds|OOB|buffer overflow|race condition)\b', re.IGNORECASE), "vulnerability class"),
        (re.compile(r'\bcom\.apple\.security\b|\bentitlements\b', re.IGNORECASE), "security entitlement"),
    ]

    def _extract_security_indicators(evidence: str) -> list[str]:
        """Scan diff evidence for memory-safety and security-boundary patterns"""
        found: list[str] = []
        for pattern, label in _SECURITY_INDICATOR_RES:
            for line in evidence.splitlines():
                stripped = line.strip()
                if stripped.startswith(("+", "-")) and pattern.search(stripped):
                    if label not in found:
                        found.append(label)
                    break
        return found

    def _infer_feature_type(name: str, source: str) -> str:
        lowered = name.lower()
        if lowered.endswith(".framework"):
            return "framework"
        if lowered.endswith(".dylib"):
            return "dylib"
        if lowered.endswith(".kext"):
            return "kext"
        if lowered.endswith(".bundle"):
            return "bundle"
        if source == "launchd_changes":
            return "launchd"
        if source.startswith("firmware") or source.startswith("iboot"):
            return "firmware"
        return "component"

    def _resolve_feature_output_dir(report_path: str, workspace_root: str | None) -> str:
        normalized = os.path.normpath(report_path)
        parts = normalized.split(os.sep)
        if "firmware_diff" in parts:
            idx = parts.index("firmware_diff")
            if idx + 1 < len(parts):
                base = os.sep.join(parts[: idx + 2])
                return ensure_dir(os.path.join(base, "feature_analysis"))

        root = workspace_root or os.getcwd()
        return ensure_dir(os.path.join(root, "artifacts", "firmware_diff", "feature_analysis"))

    def _build_feature_targets(report_json_str: str, limit: int = 6) -> list[dict[str, str]]:
        try:
            data = json.loads(report_json_str)
        except json.JSONDecodeError:
            return []

        binary_map: dict[str, dict[str, str]] = {}
        
        def extract_paths(obj: dict | list | str, source_name: str) -> None:
            if isinstance(obj, list):
                for item in obj:
                    if isinstance(item, str) and item.startswith("/"):
                        name = os.path.basename(item)
                        binary_map[name] = {"path": item, "source": source_name}
            elif isinstance(obj, dict):
                for k, v in obj.items():
                    extract_paths(v, k if k not in ["updated", "added", "modified", "dylibs", "frameworks", "standard_binaries"] else source_name)

        extract_paths(data.get("kernel", {}), "kernel")
        extract_paths(data.get("macho", {}), "macho")
        extract_paths(data.get("dsc", {}), "dsc")
        extract_paths(data.get("boundary_changes", {}), "boundary_changes")
        extract_paths(data.get("userland_changes", {}), "userland_changes")

        evidence_map: dict[str, dict[str, list[str]]] = {}
        
        for line in data.get("cstring_context", []):
            parts = line.split(":", 1)
            if len(parts) == 2:
                name = parts[0].strip()
                if name not in evidence_map:
                    evidence_map[name] = {"cstrings": [], "symbols": []}
                evidence_map[name]["cstrings"].append(parts[1].strip())
                
        for line in data.get("symbol_context", []):
            parts = line.split(":", 1)
            if len(parts) == 2:
                name = parts[0].strip()
                if name not in evidence_map:
                    evidence_map[name] = {"cstrings": [], "symbols": []}
                evidence_map[name]["symbols"].append(parts[1].strip())

        targets: list[dict[str, str]] = []
        for name, ev_dict in evidence_map.items():
            ev_lines = []
            if ev_dict["cstrings"]:
                ev_lines.append("CStrings:")
                ev_lines.extend(ev_dict["cstrings"])
            if ev_dict["symbols"]:
                if ev_lines:
                    ev_lines.append("")
                ev_lines.append("Symbols:")
                ev_lines.extend(ev_dict["symbols"])
                
            evidence = "\n".join(ev_lines)
            binary_info = binary_map.get(name, {})
            source = binary_info.get("source", "component")
            
            target_entry = {
                "name": name,
                "feature_type": _infer_feature_type(name, source),
                "source": source,
                "evidence": evidence,
                "allowed_tool_names": [
                    "find_address",
                    "decompile_function",
                    "get_xrefs_to",
                    "rename_local_variable",
                    "get_local_variables",
                    "set_comment",
                    "get_entitlements",
                    "resolve_objc_dispatch",
                    "trace_variable_source",
                    "save_ida_database",
                ]
            }
            if binary_info.get("path"):
                target_entry["binary_path"] = binary_info["path"]
                
            targets.append(target_entry)

        # attach the deterministic triage signal to every target; filtering happens in
        # feature_analysis_select_node *after* Apple Security Notes matching, so an
        # advisory-named component can be promoted before the LOW_SIGNAL drop.
        for t in targets:
            result = triage_evidence_explained(t.get("evidence", ""))
            t["_triage_signal"] = result.signal
            t["_triage_reason"] = result.reason
            if result.evidence_line:
                t["_triage_evidence_line"] = result.evidence_line
        return targets

    def retrieve_re_context_node(state: AgentState) -> AgentState:
        lowered_input = (state.user_input or "").lower()
        if "categorize" in lowered_input or "dsdump" in lowered_input:
            state.re_context = []
            state.selected_domain = "reverse_engineering"
            state.execution_domains = ["reverse_engineering"]
            state.re_task_plan = ["firmware_categorization"]
            state.split_tasks = {}
            state.tool_policy.allowed_tools = get_allowed_tools("reverse_engineering")
            state.max_tool_iterations = state.tool_policy.max_iterations
            return state

        report_path = state.intermediate_outputs.get("firmware_diff_report_path")
        report_text = state.intermediate_outputs.get("firmware_diff_report")
        if report_path and report_text:
            state.re_context = []
            state.selected_domain = "reverse_engineering"
            state.execution_domains = ["reverse_engineering"]
            state.re_task_plan = ["feature_analysis"]
            state.split_tasks = {}
            state.tool_policy.allowed_tools = get_allowed_tools("reverse_engineering")
            state.max_tool_iterations = state.tool_policy.max_iterations
            return state

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
        targets = _parse_firmware_targets(state)
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
        targets = _parse_firmware_targets(state)
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

    def _find_dsc_for_ipsw(ipsw_path: str, workspace_root: str | None) -> str | None:
        """Scan .ipsw_extracted/<stem>/ for the base dyld_shared_cache_arm64e file"""
        import glob as _glob
        stem = os.path.basename(ipsw_path).replace(".ipsw", "")
        extracted_root = os.path.join(workspace_root or os.getcwd(), ".ipsw_extracted")
        pattern = os.path.join(extracted_root, stem, "**", "dyld_shared_cache_arm64e")
        matches = sorted(_glob.glob(pattern, recursive=True))
        if matches:
            return matches[0]
        # fallback: any subdirectory whose name starts with the build ID
        build_id = stem.split("_")[0] if "_" in stem else stem
        pattern2 = os.path.join(extracted_root, f"*{build_id}*", "**", "dyld_shared_cache_arm64e")
        matches2 = sorted(_glob.glob(pattern2, recursive=True))
        return matches2[0] if matches2 else None

    def _find_kernelcache_for_ipsw(ipsw_path: str, workspace_root: str | None) -> str | None:
        """Scan .ipsw_extracted/<stem>/ for the kernelcache release file"""
        import glob as _glob
        stem = os.path.basename(ipsw_path).replace(".ipsw", "")
        extracted_root = os.path.join(workspace_root or os.getcwd(), ".ipsw_extracted")
        pattern = os.path.join(extracted_root, stem, "**", "kernelcache*")
        matches = sorted(p for p in _glob.glob(pattern, recursive=True) if "release" in os.path.basename(p))
        if matches:
            return matches[0]
        return None

    def firmware_diff_service_node(state: AgentState) -> AgentState:
        local_ipsws = _collect_confirmed_local_artifacts(state)
        old_ipsw, new_ipsw = _select_diff_pair(state, local_ipsws)
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

        # fallback: Scan .ipsw_extracted/ directly if extractor state missed DSC/kernel paths
        workspace_root = state.workspace_root
        for ipsw_path in (old_ipsw, new_ipsw):
            if not dyld_map.get(ipsw_path):
                found = _find_dsc_for_ipsw(ipsw_path, workspace_root)
                if found:
                    dyld_map[ipsw_path] = found
            if not kernel_map.get(ipsw_path):
                found = _find_kernelcache_for_ipsw(ipsw_path, workspace_root)
                if found:
                    kernel_map[ipsw_path] = found

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

        # use structured report.json as the diff report for the LLM
        report_json_path = result.artifacts.report_json
        diff_report_text = read_text(report_json_path) if report_json_path and os.path.isfile(report_json_path) else ""

        framework_diff_path = result.artifacts.framework_diff
        if framework_diff_path and os.path.isfile(framework_diff_path):
            diff_report_path = framework_diff_path
        else:
            diff_report_path = ""
            raw_dir = result.artifacts.raw_diff_dir
            if raw_dir and os.path.isdir(raw_dir):
                for root, _, files in os.walk(raw_dir):
                    if "README.md" in files:
                        diff_report_path = os.path.join(root, "README.md")
                        break
        state = StateManager.add_intermediate_output(state, "firmware_diff_report", diff_report_text)
        state.intermediate_outputs["firmware_diff_report_path"] = diff_report_path
        if result.artifacts.raw_diff_dir:
            state.intermediate_outputs["firmware_raw_diff_dir"] = result.artifacts.raw_diff_dir
        return state


    def _diff_report_has_evidence(report_json_str: str) -> bool:
        """True when the report JSON carries the per-component evidence that feature
        targets are built from. A diff that was skipped emits a status stub with no evidence 
        and must not be treated as a usable report"""
        if not report_json_str:
            return False
        try:
            data = json.loads(report_json_str)
        except (json.JSONDecodeError, ValueError):
            return False
        if not isinstance(data, dict):
            return False
        return bool(data.get("cstring_context") or data.get("symbol_context"))

    def _find_report_json_on_disk(state: AgentState) -> str:
        """Recover the structured report.json from disk when the in-graph payload is
        missing/empty/a skip-stub"""
        search_dirs: list[str] = []
        report_path = state.intermediate_outputs.get("firmware_diff_report_path", "")
        if report_path:
            directory = os.path.dirname(report_path)
            for _ in range(4):  # README is a few levels below the diff output root
                search_dirs.append(directory)
                parent = os.path.dirname(directory)
                if parent == directory:
                    break
                directory = parent
        raw_dir = state.intermediate_outputs.get("firmware_raw_diff_dir", "")
        if raw_dir:
            search_dirs.extend([raw_dir, os.path.dirname(raw_dir)])

        seen: set[str] = set()
        for directory in search_dirs:
            if not directory or directory in seen:
                continue
            seen.add(directory)
            candidate = os.path.join(directory, "report.json")
            if os.path.isfile(candidate):
                try:
                    text = read_text(candidate)
                except Exception:
                    continue
                if _diff_report_has_evidence(text):
                    return text
        return ""

    def _resolve_diff_report_json(state: AgentState) -> str:
        """Single resilient source for the diff report JSON used by feature analysis"""
        inline = state.intermediate_outputs.get("firmware_diff_report", "")
        if _diff_report_has_evidence(inline):
            return inline
        recovered = _find_report_json_on_disk(state)
        if recovered:
            state.intermediate_outputs["firmware_diff_report"] = recovered
            state.record_analysis_note(
                "feature_analysis: in-graph diff report was empty/stub; recovered report.json from disk."
            )
            return recovered
        return inline

    def _extract_readme_diff_for_component(component_name: str, readme_text: str, max_lines: int = 200) -> str:
        """Return the diff block for component_name from the README, capped at max_lines"""
        if not readme_text or not component_name:
            return ""
        lines = readme_text.splitlines()
        in_section = False
        in_code_block = False
        result: list[str] = []
        for line in lines:
            stripped = line.strip()
            if stripped == f"#### {component_name}" or stripped.startswith(f"#### {component_name} "):
                in_section = True
                continue
            if in_section:
                if stripped.startswith("#### ") or stripped.startswith("### ") or stripped.startswith("## "):
                    break
                if stripped == "```diff":
                    in_code_block = True
                    result.append(line)
                    continue
                if in_code_block and stripped == "```":
                    result.append(line)
                    break
                if in_code_block or stripped.startswith(">"):
                    result.append(line)
                    if len(result) >= max_lines:
                        result.append("... (truncated)")
                        break
        return "\n".join(result)

    def _find_readme_for_state(state: AgentState) -> str:
        """Return README text from the diff artifact directory, or '' if not found"""
        report_path = state.intermediate_outputs.get("firmware_diff_report_path", "")
        if report_path and report_path.endswith("README.md") and os.path.isfile(report_path):
            try:
                return read_text(report_path)
            except Exception:
                pass
        # else derive from raw_diff_dir
        raw_dir = state.intermediate_outputs.get("firmware_raw_diff_dir", "")
        if raw_dir and os.path.isdir(raw_dir):
            for root, _dirs, files in os.walk(raw_dir):
                if "README.md" in files:
                    try:
                        return read_text(os.path.join(root, "README.md"))
                    except Exception:
                        pass
        return ""

    def _resolve_target_version(state: AgentState) -> str | None:
        report_path = state.intermediate_outputs.get("firmware_diff_report_path", "") or ""

        # 1. 
        if report_path.endswith("README.md") and os.path.isfile(report_path):
            try:
                first_line = read_text(report_path).splitlines()[0]
                versions = re.findall(r"\d+\.\d+(?:\.\d+)?", first_line)
                if versions:
                    return versions[-1]
            except Exception:
                pass

        # 2. diff directory name
        m = re.search(r"_vs_(\d+(?:_\d+)*)_\d+[A-Za-z]\d+", report_path)
        if m:
            return m.group(1).replace("_", ".")

        # 3. the newer of the two local IPSW artifacts
        try:
            _, new_ipsw = _select_diff_pair(state, _collect_confirmed_local_artifacts(state))
            if new_ipsw:
                m = re.search(r"_(\d+\.\d+(?:\.\d+)?)_", os.path.basename(new_ipsw))
                if m:
                    return m.group(1)
        except Exception:
            pass
        return None

    def feature_analysis_select_node(state: AgentState) -> AgentState:
        if not state.feature_analysis_queue and not state.feature_analysis_targets:
            report_json_str = _resolve_diff_report_json(state)

            if not _diff_report_has_evidence(report_json_str):
                state.feature_analysis_targets = []
                state.feature_analysis_queue = []
                state.feature_analysis_current = None
                state.record_analysis_note(
                    "feature_analysis skipped: no diff report with component evidence "
                    "(checked in-graph payload and on-disk report.json)."
                )
                return state

            targets = _build_feature_targets(report_json_str)

            readme_text = _find_readme_for_state(state)
            if readme_text:
                for t in targets:
                    readme_diff = _extract_readme_diff_for_component(t["name"], readme_text)
                    if readme_diff:
                        t["evidence"] = t["evidence"] + "\n\nBinary diff (from README):\n" + readme_diff

            for t in targets:
                indicators = _extract_security_indicators(t.get("evidence", ""))
                if indicators:
                    t["security_indicators"] = indicators

            target_version = _resolve_target_version(state)
            notes_service = SecurityNotesService.for_version(target_version)
            matched = 0
            promoted = 0
            if notes_service.has_entries():
                for t in targets:
                    matched_component = notes_service.match_component(t["name"])
                    if not matched_component:
                        continue
                    t["security_notes_match"] = matched_component
                    matched += 1
                    if t.get("_triage_signal") != "HIGH_SIGNAL":
                        t["_triage_signal"] = "HIGH_SIGNAL"
                        t["_triage_reason"] = (
                            f"Apple Security Notes name this component ({matched_component}) "
                            "as changed this release"
                        )
                        promoted += 1
                note = (
                    f"Apple Security Notes (iOS {target_version}) matched {matched} of "
                    f"{len(targets)} component(s) by name"
                )
                if promoted:
                    note += f" ({promoted} promoted from LOW_SIGNAL)"
                state.record_analysis_note(note + ".")
            else:
                state.record_analysis_note(
                    "Apple Security Notes matching skipped: could not fetch advisory for "
                    f"version {target_version or 'unknown'}."
                )

            # keep only HIGH_SIGNAL components 
            high_signal = [t for t in targets if t.get("_triage_signal") == "HIGH_SIGNAL"]
            for t in targets:
                if t.get("_triage_signal") != "HIGH_SIGNAL":
                    print(f"[TRIAGE] Skipping {t.get('name', '?')} — LOW_SIGNAL ({t.get('_triage_reason', '')})")

            state.feature_analysis_targets = high_signal
            state.feature_analysis_queue = list(high_signal)
            if high_signal:
                state.record_analysis_note(f"feature_analysis targets: {len(high_signal)} HIGH_SIGNAL component(s).")
            else:
                state.record_analysis_note(
                    "feature_analysis: diff report parsed but all components were LOW_SIGNAL "
                    "(metadata/timestamp churn only)."
                )

        # pop next feature from queue, resetting tool state for each new component
        if state.feature_analysis_queue:
            state.feature_analysis_current = state.feature_analysis_queue.pop(0)
            # reset tool state so each component gets a fresh tool budget
            state.tool_iteration = 0
            state.tool_requests = []
            state.tool_results = []
            state.agent_chain = []
            # clear previous component's analysis output
            state.intermediate_outputs.pop("unified_feature_analysis", None)
        else:
            state.feature_analysis_current = None
        return state

    def _is_macho_binary(filepath: str) -> bool:
        MACHO_MAGICS = {b'\xfe\xed\xfa\xce', b'\xfe\xed\xfa\xcf', b'\xce\xfa\xed\xfe', b'\xcf\xfa\xed\xfe', b'\xca\xfe\xba\xbe'}
        try:
            with open(filepath, 'rb') as f:
                magic = f.read(4)
            return magic in MACHO_MAGICS
        except (OSError, IOError):
            return False

    def prepare_decompiler_node(state: AgentState) -> AgentState:
        feature = state.feature_analysis_current
        if not feature:
            return state

        from langgraph_orchestration.tooling.decompiler_tools import start_ida_server_for_binary
        import subprocess

        def _find_macho_in_dir(directory: str, target_name: str) -> str | None:
            matches: list[str] = []
            for root, dirs, files in os.walk(directory):
                dirs.sort()
                for file in sorted(files):
                    if file == target_name:
                        candidate = os.path.join(root, file)
                        if _is_macho_binary(candidate):
                            matches.append(candidate)
            return sorted(matches)[0] if matches else None

        component_name = feature.get("name")
        if not component_name:
            return state

        feature_binary_path = feature.get("binary_path", "")
        output_dir = os.path.join(state.workspace_root or os.getcwd(), ".ipsw_features")
        os.makedirs(output_dir, exist_ok=True)
        target_basename = os.path.basename(feature_binary_path) if feature_binary_path else component_name
        extracted_binary = None

        _dsc_path_prefixes = (
            "/System/Library/Frameworks/",
            "/System/Library/PrivateFrameworks/",
            "/usr/lib/",
        )

        # Strategy 1: recursive scan of .ipsw_features/ to avoid re-extracting on every component
        if os.path.isdir(output_dir):
            extracted_binary = _find_macho_in_dir(output_dir, target_basename)
            if extracted_binary:
                state.record_analysis_note(f"Re-using cached binary from .ipsw_features/: {extracted_binary}")

        # Strategy 2: extract from DSC / IPSW if not already cached
        if not extracted_binary:
            import glob
            local_ipsws = _collect_confirmed_local_artifacts(state)
            _, new_ipsw = _select_diff_pair(state, local_ipsws)

            # Strategy 2a: DSC dylib extraction (only if DSC already in .ipsw_extracted/)
            if feature_binary_path:
                dsc_path = None
                if new_ipsw:
                    dsc_path = _find_dsc_for_ipsw(new_ipsw, state.workspace_root)

                if dsc_path:
                    try:
                        subprocess.run(
                            ["ipsw", "dyld", "extract", dsc_path, feature_binary_path, "-o", output_dir],
                            check=True,
                            capture_output=True
                        )
                    except subprocess.CalledProcessError as e:
                        stderr = e.stderr.decode(errors='replace') if isinstance(e.stderr, bytes) else str(e.stderr)
                        if "not found in cache" in stderr:
                            state.record_analysis_note("Component not found in DSC (proceeding to filesystem extraction fallback).")
                        else:
                            error_line = [line for line in stderr.split('\n') if '⨯' in line or 'Error' in line]
                            short_err = error_line[0] if error_line else stderr[:100]
                            state.record_analysis_note(f"DSC extract failed ({os.path.basename(dsc_path)}): {short_err}")

                    extracted_binary = _find_macho_in_dir(output_dir, target_basename)

            # Strategy 2b: Check existing DMG mounts (left by ipsw diff)
            if not extracted_binary and feature_binary_path:
                for mount_dir in sorted(glob.glob("/private/tmp/*.mount")):
                    if os.path.isdir(mount_dir):
                        mounted_file = os.path.join(mount_dir, feature_binary_path.lstrip("/"))
                        if os.path.isfile(mounted_file):
                            import shutil
                            dest_path = os.path.join(output_dir, target_basename)
                            shutil.copy2(mounted_file, dest_path)
                            extracted_binary = dest_path
                            state.record_analysis_note(f"Copied binary from existing mount: {mount_dir}")
                            break

            # Strategy 2c: Direct file extraction from IPSW archive (fallback for daemons/apps only)
            _is_dsc_binary = feature_binary_path and any(
                feature_binary_path.startswith(p) for p in _dsc_path_prefixes
            )
            if not extracted_binary and new_ipsw and not _is_dsc_binary:
                pattern = f".*{re.escape(target_basename)}$"
                try:
                    subprocess.run(
                        ["ipsw", "extract", new_ipsw, "--files", "--pattern", pattern, "-o", output_dir],
                        check=True,
                        capture_output=True
                    )
                except subprocess.CalledProcessError as e:
                    stderr = e.stderr.decode(errors='replace') if isinstance(e.stderr, bytes) else str(e.stderr)
                    if "hdiutil: attach failed" in stderr or "Permission denied" in stderr:
                        state.record_analysis_note(
                            "Environment restricted from mounting DMGs. Skipping filesystem extraction for this non-DSC binary."
                        )
                    else:
                        error_line = [line for line in stderr.split('\n') if '⨯' in line or 'Error' in line]
                        short_err = error_line[0] if error_line else stderr[:100]
                        state.record_analysis_note(f"Failed to extract {component_name} from {new_ipsw}: {short_err}")

                if not extracted_binary:
                    extracted_binary = _find_macho_in_dir(output_dir, target_basename)
            elif _is_dsc_binary and not extracted_binary:
                state.record_analysis_note(
                    f"{component_name} is DSC-resident; Strategy 2c (--files) skipped. Extraction requires DSC to be present in .ipsw_extracted/."
                )

            if not extracted_binary and not feature_binary_path:
                state.record_analysis_note(
                    f"No binary_path in feature entry for {component_name}; "
                    "cannot attempt extraction. Decompiler unavailable."
                )

        if extracted_binary:
            feature["decompiler_available"] = True
            state.record_analysis_note(f"Decompiler target: {extracted_binary}")
            result = start_ida_server_for_binary.invoke({"binary_path": extracted_binary})
            state.record_analysis_note(f"Decompiler prepare: {result}")
        else:
            feature["decompiler_available"] = False
            state.record_analysis_note(f"Could not locate Mach-O binary for {component_name}. Decompiler unavailable for this component.")
        return state

    def cleanup_decompiler_node(state: AgentState) -> AgentState:
        import time as _time
        from langgraph_orchestration.tooling.decompiler_tools import save_ida_database, stop_ida_server
        # retry save up to 3 times to guarantee .i64 is written before shutdown
        save_result = "Not attempted"
        for attempt in range(3):
            save_result = save_ida_database.invoke({})
            if "successfully" in save_result.lower():
                break
            state.record_analysis_note(f"Decompiler save attempt {attempt + 1} failed: {save_result}")
            _time.sleep(2)
        state.record_analysis_note(f"Decompiler save: {save_result}")
        stop_result = stop_ida_server.invoke({})
        state.record_analysis_note(f"Decompiler cleanup: {stop_result}")
        return state

    def unified_feature_analysis_node(state: AgentState) -> AgentState:
        feature = state.feature_analysis_current
        if not feature:
            return state
        from langgraph_orchestration.prompts.reverse_engineering import build_unified_feature_analysis_prompt

        ida_available = feature.get("decompiler_available", True)
        stage1_tools = {"find_address"}
        stage2_tools = {"get_xrefs_to", "decompile_function"}
        used_tool_names = {r.tool_name for r in state.tool_results}
        has_stage1_results = bool(used_tool_names & stage1_tools)
        has_stage2_results = bool(used_tool_names & stage2_tools)
        hard_at_limit = state.tool_iteration >= state.max_tool_iterations
        # Stage 1 (find_address) is always allowed, doesn't require IDA
        # Stage 2 (decompile_function, get_xrefs_to) requires IDA to be loaded
        ida_at_limit = hard_at_limit or not ida_available

        prompt = build_unified_feature_analysis_prompt(
            user_input=state.user_input,
            component_evidence=feature.get("evidence", ""),
            component_name=feature.get("name", "Unknown Component"),
            has_tool_results=bool(state.tool_results),
            at_limit=ida_at_limit,
            security_notes_match=feature.get("security_notes_match"),
            security_indicators=feature.get("security_indicators"),
        )
        context_blocks = []
        if state.tool_results:
            context_blocks.append(StateManager.format_tool_activity(state))

        if context_blocks:
            prompt += "\n\n=== RECENT TOOL EXECUTION CONTEXT ===\n" + "\n\n".join(context_blocks) + "\n=====================================\n"

            if hard_at_limit:
                # tool budget fully exhausted
                prompt += (
                    "\n**CRITICAL FINAL INSTRUCTION**: You have reached the absolute tool call limit. "
                    "You MUST NOT output any more `<tool_call>` blocks. "
                    "Output the final report NOW starting EXACTLY with `## What this feature does`."
                )
            elif has_stage1_results and not has_stage2_results:
                # collect addresses from Stage 1 tool results to guide the model
                symbol_addrs = []
                string_addrs = []
                for r in state.tool_results:
                    if r.tool_name == "find_address" and r.success and r.output.strip():
                        # extract the JSON part before the NOTE: string
                        json_part = r.output.split("\n\nNOTE:")[0]
                        try:
                            data = json.loads(json_part)
                            if data.get("type") == "symbol":
                                symbol_addrs.append(data.get("address"))
                                prompt += "\n**HINT**: You have found a CODE symbol address. To investigate its logic, you MUST call `decompile_function` on that address now."
                            elif data.get("type") == "string_data":
                                addrs = data.get("addresses", [])
                                string_addrs.append(", ".join(addrs))
                            elif data.get("type") == "data_symbol":
                                # e.g. an ObjC class pointer _OBJC_CLASS_$_CDPDUnlockListener
                                string_addrs.append(data.get("address"))
                        except Exception:
                            pass
                addr_block = ""
                if symbol_addrs:
                    addr_block += f"- **Exported symbol addresses** (use `decompile_function`): {', '.join(symbol_addrs)}\n"
                if string_addrs:
                    addr_block += f"- **String data addresses** (use `get_xrefs_to` FIRST): {'; '.join(string_addrs)}\n"
                prompt += (
                    f"\n**CRITICAL STAGE 2 INSTRUCTION — MANDATORY DECOMPILATION**: "
                    f"You have completed Stage 1 and obtained these memory addresses:\n"
                    f"{addr_block}\n"
                    f"You MUST now proceed to Stage 2. You are NOT allowed to write the final report yet.\n"
                    f"**Execute in this exact order** (to avoid IDA stream timeouts):\n"
                    f"  STEP A — Call `get_xrefs_to` for EACH string data address above (all xrefs first, before any decompile).\n"
                    f"  STEP B — Call `decompile_function` on the exported symbol address.\n"
                    f"  STEP C — Call `decompile_function` on the most interesting CALLER functions found in Step A.\n"
                    f"  STEP D — Trace the full data flow: caller → function → what it does with the data.\n"
                    f"Output ONLY `<tool_call>` blocks in this order. Do NOT write the report yet."
                )
            elif has_stage2_results:
                # stage 2: Allow annotations and iterative decompilation
                prompt += (
                    "\n**CRITICAL STAGE 2 INSTRUCTION**: You have obtained decompilation results. "
                    "Before writing the final report, you MUST use `rename_local_variable` and `set_comment` to annotate the code. "
                    "When you decipher variables or understand the data flow, document them. "
                    "Run `save_ida_database` to persist your annotations. "
                    "If you need to trace more code, use `get_xrefs_to` or `decompile_function`. "
                    "If you have fully analyzed and annotated the feature, transition to STAGE 3 and write the final report. "
                    "To write the report, start EXACTLY with `## What this feature does`. Include decompiled pseudocode and caller chains in `## How is it implemented`. "
                    "End with `---AI_PRIORITISATION_SCORE---` and the JSON score."
                )
            else:
                # intermediate state: continue gathering evidence
                prompt += (
                    "\n**INSTRUCTION**: Evaluate the tool results. If you need more data, output ONLY `<tool_call>` blocks. "
                    "Do NOT write the final report until Stage 2 decompilation is complete."
                )

        print(f"\n\n[DEBUG STATE] tool_iteration={state.tool_iteration}/{state.max_tool_iterations} "
              f"stage1={has_stage1_results} stage2={has_stage2_results} hard_at_limit={hard_at_limit}")
        print(f"\n\n[DEBUG PROMPT]\n{prompt}\n[END DEBUG PROMPT]\n\n")

        engine = _get_feature_engine()
        chat_prompt = engine.build_prompt(user_input=prompt, system_prompt="")
        output = engine.generate(
            chat_prompt,
            config=GenerationConfig(max_tokens=3000, temperature=0.0),
            stream=False,
        )

        # parse and handle limit logic/broken output
        from langgraph_orchestration.tooling.parser import parse_agent_output
        parsed = parse_agent_output(output)
        
        is_forcing_report = hard_at_limit or not ida_available
        output_has_report = "## What this feature does" in output
        output_has_tools = parsed.has_tool_calls() or "<tool_call>" in output
        needs_retry = False
        error_msg = ""

        if is_forcing_report:
            # Must write a final report — no tool calls allowed, and report header is mandatory
            if output_has_tools or not output_has_report:
                needs_retry = True
                error_msg = (
                    "**SYSTEM ERROR**: You MUST write the final markdown report NOW using the evidence provided. "
                    "Tool calls are NOT accepted in this state. "
                    "Start your response EXACTLY with `## What this feature does`."
                )
        elif not output_has_tools and not output_has_report:
            # Model produced neither tool calls nor a report — force it to call tools
            needs_retry = True
            error_msg = (
                "**SYSTEM ERROR**: Your response did not contain any `<tool_call>` blocks. "
                "You MUST call `find_address` on the key symbols and strings from the diff before writing the report. "
                "Output ONLY `<tool_call>` blocks now. Do NOT write a report in this turn."
            )
        elif not parsed.has_tool_calls() and "<tool_call>" in output:
            needs_retry = True
            error_msg = (
                "**SYSTEM ERROR**: Your `<tool_call>` block was incomplete or contained invalid JSON. "
                "Ensure you include the closing `</tool_call>` tag and valid JSON. "
                "If you were trying to output a final report, DO NOT include `<tool_call>` blocks at all."
            )
            
        if needs_retry:
            prompt += f"\n\n{output}\n\n{error_msg}"
            chat_prompt_retry = engine.build_prompt(user_input=prompt, system_prompt="")
            output = engine.generate(
                chat_prompt_retry,
                config=GenerationConfig(max_tokens=3000, temperature=0.0),
                stream=False,
            )
            parsed = parse_agent_output(output)

        output = _sanitize_model_output(output)
        return StateManager.add_intermediate_output(state, "unified_feature_analysis", output)

    def route_after_unified_analysis(state: AgentState) -> str:
        if should_continue_tool_loop(state):
            return "execute_tools"
        return "cleanup_decompiler"

    def feature_analysis_compile_node(state: AgentState) -> AgentState:
        feature = state.feature_analysis_current
        if not feature:
            return state

        raw_output = state.intermediate_outputs.get("unified_feature_analysis", "")
        print(f"\n\n[DEBUG RAW OUTPUT]\n{raw_output}\n[END DEBUG RAW OUTPUT]\n\n")
        parts = raw_output.split("---AI_PRIORITISATION_SCORE---")
        
        markdown_report = StateManager.sanitize_output(parts[0].strip())
        # extract the core report starting from the primary header
        match = re.search(r'(## What this feature does[\s\S]*)', markdown_report, re.IGNORECASE)
        if match:
            markdown_report = match.group(1).strip()
            
        # strip any hallucinated tool logs that might be embedded anywhere
        _anchor = r'## What this feature does|## How is it implemented|## How to trigger this feature|## Vulnerability Assessment|## Evidence|---AI_PRIORITISATION_SCORE---|$'
        markdown_report = re.sub(r'## TOOL ACTIVITY[\s\S]*?(?=' + _anchor + ')', '', markdown_report, flags=re.IGNORECASE)
        markdown_report = re.sub(r'### Requested Tools[\s\S]*?(?=' + _anchor + ')', '', markdown_report, flags=re.IGNORECASE)
        markdown_report = re.sub(r'### Tool Results[\s\S]*?(?=' + _anchor + ')', '', markdown_report, flags=re.IGNORECASE)
        markdown_report = re.sub(r'<tool_call>[\s\S]*?(?:</tool_call>|(?=' + _anchor + '))', '', markdown_report, flags=re.IGNORECASE)
        
        markdown_report = markdown_report.strip()
        
        # If the report is completely empty after stripping (e.g. model only hallucinated an unclosed tool call)
        if not markdown_report:
            markdown_report = (
                "## What this feature does\n(Model failed to generate report content)\n\n"
                "## How is it implemented\n(No data)\n\n"
                "## How to trigger this feature\n(No data)\n\n"
                "## Vulnerability Assessment\n(No data)\n\n"
                "## Evidence\n(No data)"
            )
            
        score_json = parts[1].strip() if len(parts) > 1 else ""
        should_save = True

        # prepend auditable provenance header so every report explains why it exists
        triage_reason = feature.get("_triage_reason", "passed HIGH_SIGNAL triage")
        triage_line = feature.get("_triage_evidence_line", "")
        analysis_mode = "decompiled" if feature.get("decompiler_available", False) else "evidence_only"
        provenance = (
            "## Triage Provenance\n"
            f"- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)\n"
            f"- **Reason**: {triage_reason}\n"
        )
        if triage_line:
            provenance += f"- **Deciding evidence**: `{triage_line}`\n"
        provenance += f"- **Analysis mode**: {analysis_mode}\n"
        notes_match = feature.get("security_notes_match")
        if notes_match:
            provenance += (
                f"- **Apple Security Notes**: matches advisory component `{notes_match}` "
                "— Apple confirms a security-relevant change here; this analysis examines the "
                "likely vulnerability patch.\n"
            )
        provenance += "\n"
        markdown_report = provenance + markdown_report

        if score_json:
            json_match = re.search(r'\{.*\}', score_json, re.DOTALL)
            if json_match:
                try:
                    parsed_score = json.loads(json_match.group(0))
                    state.categorized_methods.append(parsed_score)

                    tier = parsed_score.get("tier", "Unknown Tier")
                    # normalise any free-form tier value 
                    _tier_aliases = {
                        # numeric / shorthand
                        "1": "TIER_1", "tier1": "TIER_1", "tier 1": "TIER_1",
                        "2": "TIER_2", "tier2": "TIER_2", "tier 2": "TIER_2",
                        "3": "TIER_3", "tier3": "TIER_3", "tier 3": "TIER_3",
                        # descriptive words
                        "high": "TIER_1", "critical": "TIER_1", "high interest": "TIER_1",
                        "medium": "TIER_2", "medium interest": "TIER_2",
                        "low": "TIER_3", "low interest": "TIER_3", "noise": "TIER_3",
                    }
                    if isinstance(tier, str) and tier.lower() in _tier_aliases:
                        tier = _tier_aliases[tier.lower()]
                        parsed_score["tier"] = tier

                    if isinstance(tier, str) and tier.upper() in ("TIER_3", "TIER3"):
                        state.record_analysis_note(
                            f"{feature.get('name', 'component')} scored {tier} after full analysis — saved with advisory tier."
                        )

                    markdown_report += "\n\n## AI Prioritisation Scoring System\n\n"
                    method = parsed_score.get("method", "Unknown Method")
                    category = parsed_score.get("category", "Unknown Category")
                    reason = parsed_score.get("reason", "No reason provided")
                    markdown_report += f"- **{method}**\n  - **Tier**: {tier}\n  - **Category**: {category}\n  - **Reasoning**: {reason}\n\n"
                except json.JSONDecodeError:
                    state.record_analysis_note("Failed to parse JSON score from unified analysis output.")
                    markdown_report += "\n\n## AI Prioritisation Scoring System\n\n*(Failed to parse JSON score)*\n"
        else:
            markdown_report += "\n\n## AI Prioritisation Scoring System\n\nNo actionable methods or prioritisation targets identified for this component.\n\n"

        report_path = state.intermediate_outputs.get("firmware_diff_report_path", "")
        slug = _slugify_feature(feature.get("name", "feature"))

        if should_save:
            output_dir = _resolve_feature_output_dir(report_path, state.workspace_root)
            output_path = os.path.join(output_dir, f"{slug}_analysis.md")
            write_text(output_path, markdown_report)
            
            state.feature_analysis_reports[feature.get("name", slug)] = output_path
            state.intermediate_outputs["feature_analysis_reports"] = json.dumps(
                state.feature_analysis_reports,
                ensure_ascii=True,
                indent=2,
            )
        
        state.feature_analysis_current = None
        state.tool_requests.clear()
        state.tool_results.clear()
        state.tool_iteration = 0
        state.intermediate_outputs.pop("unified_feature_analysis", None)
        
        return state

    def route_after_feature_select(state: AgentState) -> str:
        """All items in the queue are already HIGH_SIGNAL (filtered at build time)"""
        if state.feature_analysis_current:
            return "prepare_decompiler"
        return "done"

    def parse_firmware_methods_node(state: AgentState) -> AgentState:
        raw_methods = []
        strict_methods = []
        IGNORE_PREFIXES = ("-[UIView", "-[UIResponder", "-[UIViewController", "-[NSObject")
        
        methods_text = state.intermediate_outputs.get("raw_methods", "")
        if not methods_text:
            methods_text = state.user_input 
        
        for line in methods_text.splitlines():
            line = line.strip()
            if not line or line.startswith(IGNORE_PREFIXES):
                continue
            
            raw_methods.append(line)
            if "-[" in line or "+[" in line:
                strict_methods.append(line)
                
        # use strict Obj-C methods if found, otherwise fallback to all valid lines
        final_methods = strict_methods if strict_methods else raw_methods
        chunk_size = 50
        chunks = [final_methods[i:i + chunk_size] for i in range(0, len(final_methods), chunk_size)]
        state.firmware_methods_queue = chunks
        state.record_analysis_note(f"Parsed {len(final_methods)} methods into {len(chunks)} chunks.")
        return state

    def categorize_firmware_node(state: AgentState) -> AgentState:
        if not state.firmware_methods_queue:
            return state
            
        chunk = state.firmware_methods_queue.pop(0)
        state.firmware_methods_current_chunk = chunk
        
        try:
            engine = _get_feature_engine()
            from langgraph_orchestration.prompts.reverse_engineering import build_firmware_categorization_prompt
            
            methods_str = "\n".join(chunk)
            prompt = build_firmware_categorization_prompt(state.user_input, methods_str)
            
            output = engine.generate(
                prompt,
                config=GenerationConfig(max_tokens=2048, temperature=0.0),
                stream=False,
            )
            
            sanitized = _sanitize_model_output(output)
            json_match = re.search(r'\[.*\]', sanitized, re.DOTALL)
            if json_match:
                try:
                    parsed_json = json.loads(json_match.group(0))
                    if isinstance(parsed_json, list):
                        state.categorized_methods.extend(parsed_json)
                except json.JSONDecodeError:
                    state.record_analysis_note("Failed to parse JSON from categorization output.")
        except Exception as e:
            state.record_analysis_note(f"Categorization error: {e}")
            
        return state

    def route_after_categorize(state: AgentState) -> str:
        if state.firmware_methods_queue:
            return "categorize_firmware"
        return "synthesize"

    def firmware_analysis_node(state: AgentState) -> AgentState:
        stage_keys = [
            "firmware_locator",
            "firmware_downloader",
            "ipsw_extractor",
            "firmware_diff_report",
            "feature_analysis_reports",
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
        is_categorization = state.re_task_plan and "firmware_categorization" in state.re_task_plan
        if is_categorization:
            final = "## Firmware Categorization Targets\n\n"
            if getattr(state, "categorized_methods", None):
                final += f"```json\n{json.dumps(state.categorized_methods, indent=2)}\n```\n"
            elif state.intermediate_outputs.get("raw_categorization"):
                final += "*(Failed to extract structured JSON. Showing raw model output)*\n\n"
                final += state.intermediate_outputs.get("raw_categorization", "")
            else:
                final += "No methods were parsed or categorized from the input."
            state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(final)
            state.agent_chain.append("reverse_engineering_synthesize")
            return state

        final = state.intermediate_outputs.get("firmware_analysis", "")
        if final:
            state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(final)
            state.agent_chain.append("reverse_engineering_synthesize")
            return state

        report = state.intermediate_outputs.get("firmware_diff_report", "")
        if report:
            state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(report)
            state.agent_chain.append("reverse_engineering_synthesize")
            return state

        final = "IPSW execution pipeline completed without synthesized content."

        state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(final)
        state.agent_chain.append("reverse_engineering_synthesize")
        return state

    def route_after_extractor(state: AgentState) -> str:
        if _is_download_extract_only_request(state.user_input):
            return "firmware_analysis"
        return "firmware_diff_service"

    def route_after_context(state: AgentState) -> str:
        if state.re_task_plan and "firmware_categorization" in state.re_task_plan:
            return "parse_firmware_methods"
        if (
            state.intermediate_outputs.get("firmware_diff_report_path")
            and state.intermediate_outputs.get("firmware_diff_report")
        ):
            return "feature_analysis_select"
        return "firmware_locator"

    graph.add_node("retrieve_re_context", retrieve_re_context_node)
    graph.add_node("firmware_locator", firmware_locator_node)
    graph.add_node("firmware_downloader", firmware_downloader_node)
    graph.add_node("ipsw_extractor", ipsw_extractor_node)
    graph.add_node("firmware_diff_service", firmware_diff_service_node)
    graph.add_node("feature_analysis_select", feature_analysis_select_node)
    graph.add_node("prepare_decompiler", prepare_decompiler_node)
    graph.add_node("unified_feature_analysis", unified_feature_analysis_node)
    graph.add_node("feature_analysis_tool_executor", tool_executor_node)
    graph.add_node("cleanup_decompiler", cleanup_decompiler_node)
    graph.add_node("feature_analysis_compile", feature_analysis_compile_node)
    graph.add_node("firmware_analysis", firmware_analysis_node)
    graph.add_node("synthesize", synthesize_output)
    graph.add_node("parse_firmware_methods", parse_firmware_methods_node)
    graph.add_node("categorize_firmware", categorize_firmware_node)

    graph.add_conditional_edges(
        "retrieve_re_context",
        route_after_context,
        {
            "feature_analysis_select": "feature_analysis_select",
            "firmware_locator": "firmware_locator",
            "parse_firmware_methods": "parse_firmware_methods",
        },
    )
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
    graph.add_edge("firmware_diff_service", "feature_analysis_select")
    graph.add_conditional_edges(
        "feature_analysis_select",
        route_after_feature_select,
        {
            "prepare_decompiler": "prepare_decompiler",
            "done": "firmware_analysis",
        },
    )

    graph.add_edge("prepare_decompiler", "unified_feature_analysis")
    graph.add_conditional_edges(
        "unified_feature_analysis",
        route_after_unified_analysis,
        {
            "execute_tools": "feature_analysis_tool_executor",
            "cleanup_decompiler": "cleanup_decompiler",
        }
    )
    graph.add_edge("feature_analysis_tool_executor", "unified_feature_analysis")
    graph.add_edge("cleanup_decompiler", "feature_analysis_compile")
    graph.add_edge("feature_analysis_compile", "feature_analysis_select")
    graph.add_edge("firmware_analysis", "synthesize")
    graph.add_edge("parse_firmware_methods", "categorize_firmware")
    graph.add_conditional_edges(
        "categorize_firmware",
        route_after_categorize,
        {
            "categorize_firmware": "categorize_firmware",
            "synthesize": "synthesize",
        },
    )
    graph.add_edge("synthesize", END)

    graph.set_entry_point("retrieve_re_context")

    compiled = graph.compile()
    compiled.name = "Reverse Engineering IPSW Pipeline"
    compiled.description = "Deterministic IPSW execution pipeline for firmware reverse engineering"
    return compiled
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
from langgraph_orchestration.inference.inference_engine import GenerationConfig
from ipsw_service.agents.ipsw_extractor import IpswExtractorAgent
from ipsw_service.cli import build_download_args
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
        import re
        if not isinstance(text, str):
            try:
                text = str(text)
            except Exception:
                return ""

        text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
        lines = []
        for line in text.splitlines():
            if re.search(r"\b(tool|tool_call|tool_result|metrics|trace|langgraph)\b", line, flags=re.IGNORECASE):
                continue
            lines.append(line)
        return "\n".join(lines).strip()

    def _extract_report_title(report_text: str) -> str:
        for line in (report_text or "").splitlines():
            if line.startswith("# "):
                return line[2:].strip()
        return ""

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

    def _slugify_feature(text: str) -> str:
        cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("._-")
        return cleaned or "feature"

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

    def _build_feature_targets(report_text: str, limit: int = 6) -> list[dict[str, str]]:
        targets: list[dict[str, str]] = []
        seen: set[str] = set()

        current_section = ""
        current_change = ""
        lines = (report_text or "").splitlines()
        idx = 0

        while idx < len(lines):
            line = lines[idx].strip()
            if line.startswith("## "):
                current_section = line[3:].strip().lower()
                current_change = ""
                idx += 1
                continue
            if line.startswith("### "):
                title = line[4:].strip().lower()
                if any(token in title for token in ("updated", "modified", "changed")):
                    current_change = "updated"
                elif any(token in title for token in ("added", "new")):
                    current_change = "added"
                else:
                    current_change = ""
                idx += 1
                continue
            if not line.startswith("#### "):
                idx += 1
                continue

            heading = line[5:].strip().lower()
            if any(token in heading for token in ("updated", "modified", "changed")):
                current_change = "updated"
                idx += 1
                continue
            if any(token in heading for token in ("added", "new")):
                current_change = "added"
                idx += 1
                continue

            if current_change not in {"updated", "added"}:
                idx += 1
                continue

            name = line[5:].strip()
            if not name:
                idx += 1
                continue

            key = name.lower()
            if key in seen:
                idx += 1
                continue
            seen.add(key)

            evidence_lines: list[str] = []
            peek = idx + 1
            while peek < len(lines):
                next_line = lines[peek].strip()
                if next_line.startswith(("#### ", "### ", "## ")):
                    break
                evidence_lines.append(lines[peek])
                peek += 1

            evidence = "\n".join(evidence_lines).strip() or name
            source = current_section or current_change
            targets.append(
                {
                    "name": name,
                    "feature_type": _infer_feature_type(name, source),
                    "source": source or "component",
                    "evidence": evidence,
                }
            )
            if len(targets) >= limit:
                break

            idx = peek

        return targets

    def _invoke_feature_llm(role: str, feature: dict[str, str], report_text: str) -> str:
        try:
            engine = _get_feature_engine()
        except Exception as exc:
            return f"LLM unavailable: {exc}"

        name = feature.get("name", "unknown")
        feature_type = feature.get("feature_type", "component")
        evidence = feature.get("evidence", "")
        if len(evidence) > 2000:
            evidence = f"{evidence[:2000]}..."

        report_title = _extract_report_title(report_text)
        context = []
        if report_title:
            context.append(f"Diff Report: {report_title}")
        if evidence:
            context.append(f"Evidence:\n{evidence}")

        if role == "function_relation":
            system_prompt = (
                "You are a reverse engineering analyst specializing in call graph context. "
                "Summarize likely callers, entry points, and connected components. "
                "If evidence is insufficient, state what is missing. Be concise. "
                "CRITICAL: Do not echo your role, task, or instructions. Output ONLY the final analysis."            
                )
            user_input = (
                "Describe how this feature is implemented and its call graph context. "
                "Be concise and evidence-based.\n"
                f"Feature: {name}\n"
                f"Type: {feature_type}"
            )
        elif role == "trigger":
            system_prompt = (
                "You are a reverse engineering analyst focusing on trigger conditions. "
                "Describe how the feature is activated (IPC, launchd, user actions, configs). "
                "If unknown, state that clearly. Be concise. "
                "CRITICAL: Do not echo your role, task, or instructions. Output ONLY the final analysis."
            )
            user_input = (
                "Explain how this feature is triggered. Be concise and evidence-based. "
                f"Feature: {name}\n"
                f"Type: {feature_type}"
            )
        else:
            system_prompt = (
                "You are a reverse engineering analyst specializing in semantic extraction. "
                "Infer the high-level purpose from the diff evidence in 1-3 sentences. "
                "If uncertain, state the confidence and missing evidence. "
                "CRITICAL: Do not echo your role, task, or instructions. Output ONLY the final analysis."            
            )
            user_input = (
                "Summarize what this feature does at a high level. Be concise and evidence-based. "
                f"Feature: {name}\n"
                f"Type: {feature_type}"
            )

        prompt = engine.build_prompt(
            user_input=user_input,
            context=context,
            system_prompt=system_prompt,
        )
        output = engine.generate(
            prompt,
            config=GenerationConfig(max_tokens=600, temperature=0.2),
            stream=False,
        )
        return _sanitize_model_output(output)

    def _render_feature_report(feature: dict[str, str]) -> str:
        def _strip_thinking(text: str) -> str:
            if not text:
                return ""
            
            cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
            cleaned = re.sub(r"<tool_call>.*?(?:</tool_call>|$)", "", cleaned, flags=re.DOTALL)
            
            if "<think>" in cleaned:
                parts = cleaned.split("<think>", 1)
                before = parts[0]
                after = parts[1]
                match = re.search(r"(\n\s*#|\n\s*\d+\.\s+\*\*|\n\s*\*\*)", after)
                if match:
                    cleaned = before + after[match.start():]
                else:
                    cleaned = cleaned.replace("<think>", "")

            lines = []
            
            meta_keywords = [
                "Role:", "Task:", "Constraint:", "Input:", 
                "Target Feature:", "Type:", "Path:", "Thinking Process:",
                "Analyze the Request:", "Analyze the Evidence:", "Synthesize Findings:"
            ]
            
            for line in cleaned.splitlines():
                stripped_line = line.lstrip(" \t-*").strip()
                if any(stripped_line.startswith(kw) for kw in meta_keywords):
                    continue
                if re.match(r"^\d+\.\s+(Synthesize|Determine|Analyze)", stripped_line):
                    continue
                if line.strip() in ["1.", "2.", "3.", "-", "*"]:
                    continue
                    
                lines.append(line)
            
            result = "\n".join(lines).strip()
            result = re.sub(r"\n{3,}", "\n\n", result)
            return result if result else ""

        relation = _strip_thinking(feature.get("relation", ""))
        decipher = _strip_thinking(feature.get("decipher", ""))
        trigger = _strip_thinking(feature.get("trigger", ""))
        lines = [
            f"# Feature Analysis: {feature.get('name', 'unknown')}",
            "",
            "## What this feature does",
            decipher or "No summary available.",
            "",
            "## How is it implemented",
            relation or "No implementation summary available.",
            "",
            "## How to trigger this feature",
            trigger or "No trigger summary available.",
            "",
            "## Evidence",
            f"- Source: {feature.get('source', 'unknown')}",
            f"- Evidence: {feature.get('evidence', '')}",
        ]
        return "\n".join(lines).strip() + "\n"

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
        state = StateManager.add_intermediate_output(state, "firmware_diff_report", report_text)
        state.intermediate_outputs["firmware_diff_report_path"] = result.artifacts.report_markdown
        return state

    def feature_analysis_select_node(state: AgentState) -> AgentState:
        # Initialize queue on first call
        if not state.feature_analysis_queue and not state.feature_analysis_targets:
            report_path = state.intermediate_outputs.get("firmware_diff_report_path", "")
            report_text = state.intermediate_outputs.get("firmware_diff_report", "")
            if not report_path or not report_text:
                state.feature_analysis_targets = []
                state.feature_analysis_queue = []
                state.feature_analysis_current = None
                state.record_analysis_note("feature_analysis skipped: missing diff report")
                return state
            targets = _build_feature_targets(report_text)
            state.feature_analysis_targets = targets
            state.feature_analysis_queue = list(targets)
            state.record_analysis_note(f"feature_analysis targets: {len(targets)}")
        # Pop next feature from queue
        if state.feature_analysis_queue:
            state.feature_analysis_current = state.feature_analysis_queue.pop(0)
        return state

    def feature_analysis_relation_node(state: AgentState) -> AgentState:
        feature = state.feature_analysis_current
        if not feature:
            return state
        updated = dict(feature)
        report_text = state.intermediate_outputs.get("firmware_diff_report", "")
        updated["relation"] = _invoke_feature_llm("function_relation", updated, report_text)
        state.feature_analysis_current = updated
        return state

    def feature_analysis_decipher_node(state: AgentState) -> AgentState:
        feature = state.feature_analysis_current
        if not feature:
            return state
        updated = dict(feature)
        report_text = state.intermediate_outputs.get("firmware_diff_report", "")
        updated["decipher"] = _invoke_feature_llm("decipher_function", updated, report_text)
        updated["trigger"] = _invoke_feature_llm("trigger", updated, report_text)
        state.feature_analysis_current = updated
        return state

    def feature_analysis_compile_node(state: AgentState) -> AgentState:
        feature = state.feature_analysis_current
        if not feature:
            return state
        report_path = state.intermediate_outputs.get("firmware_diff_report_path", "")
        output_dir = _resolve_feature_output_dir(report_path, state.workspace_root)
        slug = _slugify_feature(feature.get("name", "feature"))
        output_path = os.path.join(output_dir, f"{slug}_analysis.md")
        write_text(output_path, _render_feature_report(feature))
        state.feature_analysis_reports[feature.get("name", slug)] = output_path
        state.intermediate_outputs["feature_analysis_reports"] = json.dumps(
            state.feature_analysis_reports,
            ensure_ascii=True,
            indent=2,
        )
        state.feature_analysis_current = None
        return state

    def route_after_feature_select(state: AgentState) -> str:
        if state.feature_analysis_current:
            return "analyze"
        return "done"

    def parse_firmware_methods_node(state: AgentState) -> AgentState:
        raw_methods = []
        IGNORE_PREFIXES = ("-[UIView", "-[UIResponder", "-[UIViewController", "-[NSObject")
        
        methods_text = state.intermediate_outputs.get("raw_methods", "")
        if not methods_text:
            methods_text = state.user_input 
        
        for line in methods_text.splitlines():
            line = line.strip()
            if line and not line.startswith(IGNORE_PREFIXES) and ("-[" in line or "+[" in line):
                raw_methods.append(line)
                
        chunk_size = 50
        chunks = [raw_methods[i:i + chunk_size] for i in range(0, len(raw_methods), chunk_size)]
        state.firmware_methods_queue = chunks
        state.record_analysis_note(f"Parsed {len(raw_methods)} methods into {len(chunks)} chunks.")
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
                config=GenerationConfig(max_tokens=2048, temperature=0.1),
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
        if state.categorized_methods:
            final = f"## Firmware Categorization Targets\n\n```json\n{json.dumps(state.categorized_methods, indent=2)}\n```\n"
            state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(final)
            state.agent_chain.append("reverse_engineering_synthesize")
            return state

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
    graph.add_node("feature_analysis_relation", feature_analysis_relation_node)
    graph.add_node("feature_analysis_decipher", feature_analysis_decipher_node)
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
            "analyze": "feature_analysis_relation",
            "done": "firmware_analysis",
        },
    )
    graph.add_edge("feature_analysis_relation", "feature_analysis_decipher")
    graph.add_edge("feature_analysis_decipher", "feature_analysis_compile")
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
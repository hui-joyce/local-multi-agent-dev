from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.core.state_utils import StateManager
from langgraph_orchestration.graphs.orchestration import build_orchestration_graph
from langgraph_orchestration.graphs.reverse_engineering import build_reverse_engineering_graph
from langgraph_orchestration.schemas.state import AgentState

@dataclass
class IpswDiffCase:
    case_id: str
    description: str
    user_input: str

@dataclass
class IpswDiffResult:
    case_id: str
    description: str
    selected_domain: str | None
    execution_domains: list[str]
    agent_chain: list[str]
    latency_seconds: float
    output_chars: int
    output_text: str
    output_preview: str

def build_ipsw_diff_case() -> IpswDiffCase:
    return IpswDiffCase(
        case_id="RE-IPSW-DIFF-01",
        description="Download and extract artifacts for two iPhone17,1 IPSW versions.",
        user_input=(
            "Perform only these actions using IPSW skill guidance:\n"
            "1) Download Version 1 and Version 2 firmware artifacts.\n"
            "2) Extract dyld_shared_cache and kernelcache from both artifacts.\n"
            "Perform baseline comparison and feature inference.\n\n"
            # "Version 1: iPhone17,1_18.2_22C152_Restore.ipsw\n"
            # "Version 2: iPhone17,1_18.2.1_22C161_Restore.ipsw\n"
            # "Version 1: iPhone18,1_26.4.1_23E254_Restore.ipsw\n"
            # "Version 2: iPhone18,1_26.4.2_23E261_Restore.ipsw\n"
            "Version 1: iPhone17,1_18.2_22C152_Restore.ipsw\n"
            "Version 2: iPhone17,1_18.2.1_22C161_Restore.ipsw\n"
            "Perform a deep, static-only inspection of two provided dyld_shared_cache artifacts and produce a analysis of newly introduced classes and related changes.\n\n"
        ),
    )

def run_ipsw_diff_case(graph: Any, case: IpswDiffCase) -> tuple[IpswDiffResult, AgentState]:
    state = AgentState(user_input=case.user_input)

    start = time.perf_counter()
    raw_result = graph.invoke(state.model_dump())
    elapsed = time.perf_counter() - start

    final_state = AgentState(**raw_result)
    final_output = StateManager.sanitize_output(final_state.final_output or "")

    return IpswDiffResult(
            case_id=case.case_id,
            description=case.description,
            selected_domain=final_state.selected_domain,
            execution_domains=final_state.execution_domains,
            agent_chain=final_state.agent_chain,
            latency_seconds=round(elapsed, 3),
            output_chars=len(final_output),
            output_text=final_output,
            output_preview=final_output[:800],
    ), final_state

def write_result(result: IpswDiffResult, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    json_path = output_dir / f"test_ipsw_diff-{timestamp}.json"
    md_path = output_dir / f"test_ipsw_diff-{timestamp}.md"

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "result": asdict(result),
    }

    with json_path.open("w", encoding="utf-8") as file_handle:
        json.dump(payload, file_handle, indent=2)

    markdown = f"""# IPSW Diff Test
    ## Case
    - ID: {result.case_id}
    - Description: {result.description}

    ## Execution
    - Selected domain: {result.selected_domain}
    - Execution domains: {', '.join(result.execution_domains) if result.execution_domains else 'n/a'}
    - Agent chain: {', '.join(result.agent_chain) if result.agent_chain else 'n/a'}
    - Latency: {result.latency_seconds}s
    - Output chars: {result.output_chars}

    ## Output Preview
    ```text
    {result.output_preview}
    ```

    ## Full Output
    ```text
    {result.output_text}
    ```
    """
    with md_path.open("w", encoding="utf-8") as file_handle:
        file_handle.write(markdown)

    return json_path, md_path

def trigger_feature_analysis(diff_report_path: str | Path, factory: MLXAgentFactory) -> dict[str, str]:
    """Trigger feature analysis using the structured report.json payload"""
    diff_report_path = Path(diff_report_path)

    report_json_path: Path | None = None
    search_dir = diff_report_path.parent
    for _ in range(3):
        candidate = search_dir / "report.json"
        if candidate.exists():
            report_json_path = candidate
            break
        search_dir = search_dir.parent

    if report_json_path is None:
        print(f"Warning: report.json not found near {diff_report_path}, skipping feature analysis.")
        return {}

    report_text = report_json_path.read_text(encoding="utf-8")

    state = AgentState(user_input="Run feature analysis on generated diff report.")
    state.intermediate_outputs["firmware_diff_report_path"] = str(diff_report_path)
    state.intermediate_outputs["firmware_diff_report"] = report_text

    print(f"\nTriggering feature analysis on: {report_json_path}")
    start = time.perf_counter()

    re_graph = build_reverse_engineering_graph(factory=factory)
    raw_result = re_graph.invoke(state.model_dump())

    elapsed = time.perf_counter() - start
    final_state = AgentState(**raw_result)
    reports = final_state.feature_analysis_reports

    print(f"Feature analysis complete in {round(elapsed, 3)}s")
    print(f"Generated {len(reports)} feature analysis reports:")
    for name, path in reports.items():
        print(f"  - {name}: {path}")

    return reports


def main() -> None:
    load_dotenv()

    factory = MLXAgentFactory()
    factory.ensure_loaded() 
    graph = build_orchestration_graph(factory=factory)

    case = build_ipsw_diff_case()
    result, final_state_from_run = run_ipsw_diff_case(graph, case)

    output_dir = Path("benchmarks/results/test_ipsw_diff")
    json_path, md_path = write_result(result, output_dir)

    print(f"Case: {result.case_id}")
    print(f"JSON: {json_path}")

    raw_diff_dir = final_state_from_run.intermediate_outputs.get("firmware_raw_diff_dir")
    diff_report_path = None
    if raw_diff_dir and Path(raw_diff_dir).exists():
        for root, _, files in os.walk(raw_diff_dir):
            if "README.md" in files:
                diff_report_path = Path(root) / "README.md"
                break

    if not diff_report_path:
        diff_report_path = final_state_from_run.intermediate_outputs.get("firmware_diff_report_path")

    idiff_path = None
    if raw_diff_dir and Path(raw_diff_dir).exists():
        ent_dir = Path(raw_diff_dir).parent / "entitlements"
        if ent_dir.exists():
            for root, _, files in os.walk(ent_dir):
                for f in files:
                    if f.endswith(".idiff"):
                        idiff_path = Path(root) / f
                        break
                if idiff_path:
                    break
                
    if idiff_path:
        from ipsw_service.models import IDiffReport
        print(f"\nLoading idiff payload from: {idiff_path}")
        try:
            idiff_report = IDiffReport.from_file(str(idiff_path))
            print(f"Successfully loaded idiff report '{idiff_report.title}' with {len(idiff_report.machos)} binaries/dylibs tracked.")
        except Exception as e:
            print(f"Failed to load idiff report: {e}")

    if diff_report_path and Path(diff_report_path).exists():
        feature_reports = trigger_feature_analysis(diff_report_path, factory)
        if feature_reports:
            print(f"Feature analysis: {len(feature_reports)} reports")

if __name__ == "__main__":
    main()
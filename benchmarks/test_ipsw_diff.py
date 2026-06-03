from __future__ import annotations

import json
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
            # "Version 1: iPhone17,1_18.1_22B82_Restore.ipsw\n"
            # "Version 2: iPhone17,1_18.1.1_22B91_Restore.ipsw\n"
            # "Version 1: iPhone18,1_26.2_23C55_Restore.ipsw\n"
            # "Version 2: iPhone18,1_26.2.1_23C71_Restore.ipsw\n\n"
            # "Version 1: iPhone18,1_26.3_23D127_Restore.ipsw\n"
            # "Version 2: iPhone18,1_26.3.1_23D8133_Restore.ipsw\n\n"
            # "Version 1: iPhone18,1_26.4.1_23E254_Restore.ipsw\n"
            # "Version 2: iPhone18,1_26.4.2_23E261_Restore.ipsw\n"
            # "Version 1: iPhone16,2_17.6.1_21G101_Restore.ipsw\n"
            # "Version 2: iPhone16,2_17.7_21H16_Restore.ipsw\n"
            # "Version 1: iPhone17,1_18.6.1_22G90_Restore.ipsw\n"
            # "Version 2: iPhone17,1_18.6.2_22G100_Restore.ipsw\n"
            "Version 1: iPhone17,1_18.3.1_22D72_Restore.ipsw\n"
            "Version 2: iPhone17,1_18.3.2_22D82_Restore.ipsw\n"
            "Perform a deep, static-only inspection of two provided dyld_shared_cache artifacts and produce a analysis of newly introduced classes and related changes.\n\n"
        ),
    )

def run_ipsw_diff_case(graph: Any, case: IpswDiffCase) -> IpswDiffResult:
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
    )

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
    """Trigger feature analysis on the generated diff report"""
    diff_report_path = Path(diff_report_path)
    if not diff_report_path.exists():
        print(f"Warning: Diff report not found at {diff_report_path}, skipping feature analysis.")
        return {}
    
    report_text = diff_report_path.read_text(encoding="utf-8")
    
    state = AgentState(user_input="Run feature analysis on generated diff report.")
    state.intermediate_outputs["firmware_diff_report_path"] = str(diff_report_path)
    state.intermediate_outputs["firmware_diff_report"] = report_text
    
    print(f"\nTriggering feature analysis on: {diff_report_path}")
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
    graph = build_orchestration_graph(factory=factory)

    case = build_ipsw_diff_case()
    result = run_ipsw_diff_case(graph, case)

    output_dir = Path("benchmarks/results/test_ipsw_diff")
    json_path, md_path = write_result(result, output_dir)

    print("IPSW diff test complete.")
    print(f"Case: {result.case_id}")
    print(f"Selected domain: {result.selected_domain}")
    print(f"Execution domains: {', '.join(result.execution_domains) if result.execution_domains else 'n/a'}")
    print(f"Agent chain: {', '.join(result.agent_chain) if result.agent_chain else 'n/a'}")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")
    
    # Find and trigger feature analysis on the generated diff report
    artifacts_dir = Path("artifacts/firmware_diff")
    if artifacts_dir.exists():
        # Find the most recent diff report
        diff_dirs = sorted([d for d in artifacts_dir.iterdir() if d.is_dir()], reverse=True)
        for diff_dir in diff_dirs[:3]:  # Check last 3 timestamp directories
            diff_files = list(diff_dir.rglob("README.md"))
            if diff_files:
                diff_report = diff_files[0]
                print(f"\nFound diff report: {diff_report}")
                feature_reports = trigger_feature_analysis(diff_report, factory)
                if feature_reports:
                    print(f"✓ Feature analysis succeeded with {len(feature_reports)} reports")
                break

if __name__ == "__main__":
    main()
from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.graphs.reverse_engineering import build_reverse_engineering_graph
from langgraph_orchestration.schemas.state import AgentState
from ipsw_service.parsing import extract_cstring_diffs, strip_ansi
from ipsw_service.utils import write_json

REPORT_PATH = Path(
    "artifacts/firmware_diff/20260520-021825/diff/26_4_1_23E254_vs_26_4_2_23E261/README.md"
)

@dataclass
class FeatureAnalysisCase:
    case_id: str
    description: str
    report_path: Path
    user_input: str

@dataclass
class FeatureAnalysisResult:
    case_id: str
    description: str
    report_path: str
    agent_chain: list[str]
    latency_seconds: float
    report_count: int
    report_paths: dict[str, str]

def build_feature_case() -> FeatureAnalysisCase:
    return FeatureAnalysisCase(
        case_id="RE-FEATURE-ANALYSIS-26-4-2",
        description="Feature analysis on 26.4.1 vs 26.4.2 diff report.",
        report_path=REPORT_PATH,
        user_input=(
            "Run feature analysis on diff report: "
            "26.4.1 (23E254) vs 26.4.2 (23E261)."
        ),
    )

def run_case(graph, case: FeatureAnalysisCase) -> FeatureAnalysisResult:
    report_text = case.report_path.read_text(encoding="utf-8")
    _populate_symbol_metadata(case.report_path, report_text)
    state = AgentState(user_input=case.user_input)
    state.intermediate_outputs["firmware_diff_report_path"] = str(case.report_path)
    state.intermediate_outputs["firmware_diff_report"] = report_text

    start = time.perf_counter()
    raw_result = graph.invoke(state.model_dump())
    elapsed = time.perf_counter() - start

    final_state = AgentState(**raw_result)
    reports = final_state.feature_analysis_reports

    return FeatureAnalysisResult(
        case_id=case.case_id,
        description=case.description,
        report_path=str(case.report_path),
        agent_chain=final_state.agent_chain,
        latency_seconds=round(elapsed, 3),
        report_count=len(reports),
        report_paths=reports,
    )

def _populate_symbol_metadata(report_path: Path, report_text: str) -> None:
    changes = extract_cstring_diffs(report_text)
    for subdir in ("MACHOS", "DYLIBS"):
        dir_path = report_path.parent / subdir
        if not dir_path.is_dir():
            continue
        for path in sorted(dir_path.rglob("*.md")):
            try:
                changes.extend(extract_cstring_diffs(path.read_text(encoding="utf-8")))
            except OSError:
                continue

    deduped: list[str] = []
    seen: set[str] = set()
    for item in changes:
        key = strip_ansi(item).strip()
        if key and key not in seen:
            seen.add(key)
            deduped.append(item)

    metadata_path = report_path.parents[2] / "symbol_metadata.json"
    payload = {"dyld_changes": [], "kernel_changes": [], "cstring_changes": deduped}
    if metadata_path.exists():
        try:
            existing = json.loads(metadata_path.read_text(encoding="utf-8"))
            payload["dyld_changes"] = existing.get("dyld_changes", [])
            payload["kernel_changes"] = existing.get("kernel_changes", [])
        except Exception:
            pass

    write_json(str(metadata_path), payload)

def write_result(result: FeatureAnalysisResult, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    json_path = output_dir / f"test_feature_analysis-{timestamp}.json"
    md_path = output_dir / f"test_feature_analysis-{timestamp}.md"

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "result": asdict(result),
    }

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=True)

    report_lines = [f"- {name}: {path}" for name, path in result.report_paths.items()]
    report_list = "\n".join(report_lines) if report_lines else "- none"

    markdown = (
        "# Feature Analysis Benchmark\n\n"
        "## Case\n"
        f"- ID: {result.case_id}\n"
        f"- Description: {result.description}\n"
        f"- Diff report: {result.report_path}\n\n"
        "## Execution\n"
        f"- Latency: {result.latency_seconds}s\n"
        f"- Agent chain: {', '.join(result.agent_chain) if result.agent_chain else 'n/a'}\n"
        f"- Feature reports: {result.report_count}\n\n"
        "## Report Outputs\n"
        f"{report_list}\n"
    )

    with md_path.open("w", encoding="utf-8") as handle:
        handle.write(markdown)

    return json_path, md_path


def main() -> None:
    load_dotenv()

    case = build_feature_case()
    if not case.report_path.exists():
        raise FileNotFoundError(f"Missing diff report: {case.report_path}")

    factory = MLXAgentFactory(model_name="qwen-3.5-9b")
    factory.ensure_loaded()
    graph = build_reverse_engineering_graph(factory=factory)
    result = run_case(graph, case)

    output_dir = Path("benchmarks/results/test_feature_analysis")
    json_path, md_path = write_result(result, output_dir)

    print("Feature analysis benchmark complete.")
    print(f"Case: {result.case_id}")
    print(f"Reports: {result.report_count}")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")

if __name__ == "__main__":
    main()
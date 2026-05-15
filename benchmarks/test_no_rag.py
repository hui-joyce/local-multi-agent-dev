"""
This script runs a repeatable set of test cases against the current
orchestration graph while RAG retrieval is disabled in branch graphs.

Goals:
- Validate baseline LLM behavior with current prompt templates.
- Capture routing decisions, agent chain, latency, and output previews.
- Export structured benchmark artifacts for documentation.
"""


# TO-DO: add additional unit test for code analysis - analyse class object relation in repo codebase, purpose of certain functions etc 

from __future__ import annotations

import json
import os
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv

from langgraph_orchestration.graphs.orchestration import build_orchestration_graph
from langgraph_orchestration.core.state_utils import StateManager
from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.schemas.state import AgentState

@dataclass
class BenchmarkCase:
    """Single benchmark test case definition"""
    case_id: str
    domain_focus: str
    expected_execution_domains: list[str]
    description: str
    user_input: str

@dataclass
class BenchmarkResult:
    """Captured output metadata from one benchmark execution"""
    case_id: str
    domain_focus: str
    expected_execution_domains: list[str]
    description: str
    user_input: str
    selected_domain: str | None
    execution_domains: list[str]
    routing_match: bool
    agent_chain: list[str]
    latency_seconds: float
    output_chars: int
    ttft_seconds: float
    prompt_tokens: int
    generated_tokens: int
    generation_speed_tok_s: float
    output_text: str
    output_preview: str

def get_benchmark_cases(single_domain_only: bool = False) -> list[BenchmarkCase]:
    cases = [
        BenchmarkCase(
            case_id="SD-01",
            domain_focus="software_dev",
            expected_execution_domains=["software_dev"],
            description="Feature implementation request with expected test generation.",
            user_input=(
                "Implement a Python rate limiter using token bucket logic and include "
                "unit tests for burst and refill behavior."
            ),
        ),
        BenchmarkCase(
            case_id="SD-02",
            domain_focus="software_dev",
            expected_execution_domains=["software_dev"],
            description="Architecture-oriented backend service design prompt.",
            user_input=(
                "Design and implement a minimal FastAPI service for project tasks with "
                "clear module boundaries and architectural rationale."
            ),
        ),
        BenchmarkCase(
            case_id="RE-01",
            domain_focus="reverse_engineering",
            expected_execution_domains=["reverse_engineering"],
            description="Code-behavior reconstruction request.",
            user_input=(
                "Reverse engineer the following pseudo-code and explain likely intent, "
                "state transitions, hidden assumptions, and possible abuse cases.\n\n"
                "Pseudo-code:\n"
                "function verify_and_execute(input, key):\n"
                "    state = INIT\n"
                "    idx = 0\n"
                "    checksum = 0\n"
                "    while idx < len(input):\n"
                "        b = input[idx]\n"
                "        checksum = (checksum + ((b XOR key[idx % len(key)]) * 17)) & 0xFFFF\n"
                "        if state == INIT and b == 0x7B:\n"
                "            state = HEADER\n"
                "        else if state == HEADER and b == 0x3A:\n"
                "            state = BODY\n"
                "        else if state == BODY and b == 0x7D:\n"
                "            state = DONE\n"
                "        idx = idx + 1\n"
                "\n"
                "    if state != DONE:\n"
                "        return ERR_FORMAT\n"
                "\n"
                "    if checksum == 0xBEEF:\n"
                "        call privileged_operation(input)\n"
                "        return OK\n"
                "\n"
                "    return ERR_AUTH\n"
            ),
        ),
        BenchmarkCase(
            case_id="RE-02",
            domain_focus="reverse_engineering",
            expected_execution_domains=["reverse_engineering"],
            description="Security-oriented binary triage request.",
            user_input=(
                "Analyze this decompiled parser routine for memory safety risks, likely exploit paths, "
                "and mitigation guidance.\n\n"
                "Decompiled parser routine:\n"
                "int parse_packet(unsigned char *buf, int len) {\n"
                "    char tmp[64];\n"
                "    int i = 0;\n"
                "    int payload_len;\n"
                "\n"
                "    if (len < 8) return -1;\n"
                "\n"
                "    payload_len = *(int *)(buf + 4);\n"
                "    if (payload_len > len) return -2;\n"
                "\n"
                "    while (i <= payload_len) {\n"
                "        tmp[i] = buf[8 + i];\n"
                "        i++;\n"
                "    }\n"
                "\n"
                "    if (tmp[0] == 'A') {\n"
                "        printf(tmp);\n"
                "    }\n"
                "\n"
                "    if (buf[1] == 0x42) {\n"
                "        memmove(buf, buf + 12, payload_len + 32);\n"
                "    }\n"
                "\n"
                "    return 0;\n"
                "}\n"
            ),
        ),
    ]
    
    if not single_domain_only:
        cases.extend([
            BenchmarkCase(
                case_id="MX-01",
                domain_focus="mixed",
                expected_execution_domains=["software_dev", "reverse_engineering"],
                description="Cross-domain request requiring implementation plus security review.",
                user_input=(
                    "Build a secure file upload handler in Python, then assess its design and "
                    "implementation for reverse-engineering and vulnerability concerns."
                ),
            ),
            BenchmarkCase(
                case_id="MX-02",
                domain_focus="mixed",
                expected_execution_domains=["software_dev", "reverse_engineering"],
                description="Documentation generation plus threat assessment behavior check.",
                user_input=(
                    "Generate code documentation for this authentication module and then perform "
                    "a vulnerability-oriented reverse engineering assessment of its flow.\n\n"
                    "Authentication module snippet:\n"
                    "def login(db, username, password, token_cache):\n"
                    "    user = db.find_user(username)\n"
                    "    if not user:\n"
                    "        return {'ok': False, 'msg': 'invalid'}\n"
                    "\n"
                    "    if sha1(password).hexdigest() != user.password_hash:\n"
                    "        return {'ok': False, 'msg': 'invalid'}\n"
                    "\n"
                    "    token = f'{username}:{int(time.time())}'\n"
                    "    token_cache[token] = {'user': username, 'exp': time.time() + 86400}\n"
                    "    return {'ok': True, 'token': token}\n"
                ),
            ),
        ])
    
    return cases

def run_case(graph: Any, case: BenchmarkCase, factory: Any = None) -> BenchmarkResult:
    initial_state = AgentState(user_input=case.user_input)

    start = time.perf_counter()
    result = graph.invoke(initial_state.model_dump())
    elapsed = time.perf_counter() - start

    final_state = AgentState(**result)
    clean_output = StateManager.sanitize_output(final_state.final_output)
    final_output=clean_output or ""
    expected = sorted(case.expected_execution_domains)
    actual = sorted(final_state.execution_domains)
    routing_match = expected == actual

    # Extract metrics from inference engine if available
    ttft_seconds = 0.0
    prompt_tokens = 0
    generated_tokens = 0
    generation_speed_tok_s = 0.0
    
    if factory is not None:
        try:
            supervisor = factory.create_supervisor_agent()
            if (supervisor.inference_engine and 
                hasattr(supervisor.inference_engine, 'last_metrics') and 
                supervisor.inference_engine.last_metrics):
                metrics = supervisor.inference_engine.last_metrics
                ttft_seconds = metrics.ttft_seconds
                prompt_tokens = metrics.prompt_tokens
                generated_tokens = metrics.generated_tokens
                generation_speed_tok_s = metrics.generation_speed_tok_s
        except Exception:
            pass
    
    if generation_speed_tok_s == 0.0 and generated_tokens > 0:
        if ttft_seconds > 0 and elapsed > ttft_seconds:
            generation_time = elapsed - ttft_seconds
        else:
            generation_time = elapsed
        if generation_time > 0:
            generation_speed_tok_s = round(generated_tokens / generation_time, 2)  

    return BenchmarkResult(
        case_id=case.case_id,
        domain_focus=case.domain_focus,
        expected_execution_domains=case.expected_execution_domains,
        description=case.description,
        user_input=case.user_input,
        selected_domain=final_state.selected_domain,
        execution_domains=final_state.execution_domains,
        routing_match=routing_match,
        agent_chain=final_state.agent_chain,
        latency_seconds=round(elapsed, 3),
        output_chars=len(final_output),
        ttft_seconds=ttft_seconds,
        prompt_tokens=prompt_tokens,
        generated_tokens=generated_tokens,
        generation_speed_tok_s=generation_speed_tok_s,
        output_text=final_output,
        output_preview=final_output[:500],
    )

def write_results(results: list[BenchmarkResult], output_dir: Path) -> tuple[Path, Path]:
    """Persist raw JSON and a markdown summary for reporting"""
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    json_path = output_dir / f"no-rag-results-{timestamp}.json"
    md_path = output_dir / f"no-rag-results-{timestamp}.md"

    payload = {
        "run_type": "no_rag_baseline",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "total_cases": len(results),
        "results": [asdict(item) for item in results],
    }

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    lines = [
        "# No-RAG Benchmark Results",
        "",
        "This run measures model behavior with retrieval disabled.",
        "",
        "## Performance Metrics Summary",
        "",
        "| Case | Route Match | Latency (s) | TTFT (s) | Prompt Tok | Gen Tok |  Gen Speed (tok/s) | ",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for row in results:
        lines.append(
            "| "
            f"{row.case_id} | {'YES' if row.routing_match else 'NO'} | {row.latency_seconds} | "
            f"{row.ttft_seconds} | {row.prompt_tokens} | {row.generated_tokens} | {row.generation_speed_tok_s} |"
        )

    lines.append("")
    lines.append("## Detailed Results")
    lines.append("")
    lines.append("| Case | Focus | Expected Domains | Selected Domain | Execution Domains | Route Match | Output Chars |")
    lines.append("|---|---|---|---|---|---|---:|")

    for row in results:
        lines.append(
            "| "
            f"{row.case_id} | {row.domain_focus} | {', '.join(row.expected_execution_domains)} | "
            f"{row.selected_domain} | {', '.join(row.execution_domains)} | "
            f"{'YES' if row.routing_match else 'NO'} | {row.output_chars} |"
        )

    lines.append("")
    lines.append("## Output Results (Full)")

    for row in results:
        lines.append("")
        lines.append(f"### {row.case_id} - {row.description}")
        lines.append("")
        lines.append("```text")
        lines.append(row.output_text)
        lines.append("```")

    with md_path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return json_path, md_path

def main() -> None:
    """Run the full no-RAG benchmark suite and export result artifacts."""
    import sys
    
    load_dotenv()

    # Check for command-line flags
    single_domain_only = "--single-domain-only" in sys.argv
    
    if single_domain_only:
        print("Running in SINGLE-DOMAIN-ONLY mode (excluding mixed-domain cases MX-01, MX-02)")
    else:
        print("Running full benchmark suite (including mixed-domain cases)")
    
    cases = get_benchmark_cases(single_domain_only=single_domain_only)
    factory = MLXAgentFactory()
    graph = build_orchestration_graph(factory=factory)

    print(f"Running no-RAG benchmark suite...")
    print(f"Total cases: {len(cases)}\n")

    results: list[BenchmarkResult] = []
    for idx, case in enumerate(cases, start=1):
        print(f"[{idx}/{len(cases)}] {case.case_id} - {case.description}")
        case_result = run_case(graph, case, factory=factory)
        results.append(case_result)
        print(
            "  "
            f"selected={case_result.selected_domain}, "
            f"execution={case_result.execution_domains}, "
            f"expected={case_result.expected_execution_domains}, "
            f"route_match={case_result.routing_match}, "
            f"latency={case_result.latency_seconds}s, "
            f"gen_speed={case_result.generation_speed_tok_s}tok/s "
        )

    routing_accuracy = (
        sum(1 for item in results if item.routing_match) / len(results)
        if results
        else 0.0
    )

    output_dir = Path(os.getenv("NO_RAG_RESULTS_DIR", "benchmarks/results"))
    json_path, md_path = write_results(results, output_dir)

    print("\nBenchmark complete.")
    print(f"JSON report: {json_path}")
    print(f"Markdown report: {md_path}")
    print(f"Routing accuracy: {routing_accuracy:.2%}")
    
    if single_domain_only:
        print("\nTip: Run without --single-domain-only to include mixed-domain test cases.")


if __name__ == "__main__":
    main()
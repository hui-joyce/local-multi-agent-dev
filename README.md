# Local Multi-Agent Development System

Local-first multi-agent system for analysing iOS firmware changes and assisting with software development workflows using on-device LLM inference.

## Overview

Apple security advisories describe what was fixed, but rarely explain where the vulnerable code changed or how the fix was implemented. Finding those details manually means comparing firmware images, filtering rebuild noise, reverse engineering binaries, and understanding the surrounding code.

This project automates that workflow. It compares iOS firmware releases, identifies meaningful binary changes, drives headless IDA Pro for analysis, and generates structured reports. The same runtime also supports software development tasks such as code generation, testing, and architecture review.

The design follows three principles:

- **Deterministic work stays in code.** Diffing, filtering, scoring, and advisory matching are implemented as tested code rather than delegated to the model.
- **The LLM interprets results.** Decompiled pseudocode comes directly from IDA Pro and is inserted into reports after generation.
- **Analysis stays local.** Runtime analysis operates on local binaries only. Aside from downloading models, firmware, or security advisories during setup, the system performs no network requests.

Two LangGraph domain graphs power the system, and a supervisor routes each request to the appropriate graph, or both when necessary:

- **Reverse engineering**, for firmware analysis.
- **Software development**, for code generation, testing, and architectural review.

## Architecture

| Layer | Responsibility |
|---|---|
| Interfaces | Gradio UI, FastAPI service, and Python API |
| `OrchestrationRuntime` | Owns the model and compiled LangGraph runtime |
| Supervisor | Routes requests and coordinates one or both domain graphs |
| Domain graphs | `software_dev` and `reverse_engineering` workflows |
| Tool executor | Executes filesystem, `ipsw`, and IDA Pro operations |
| Services | Firmware downloads and cached Apple Security Notes |

| Diagram | Description |
|---|---|
| <img src="assets/system-architecture.png" alt="System architecture" width="640"/> | Overall system architecture |
| <img src="assets/high-level-flow.png" alt="High-level flow" width="640"/> | Request lifecycle |
| <img src="assets/langgraph.png" alt="LangGraph flow" width="640"/> | Compiled LangGraph workflow |

### Runtime

MLX expects model state to remain on the thread that created it, so the runtime loads a single model instance on a dedicated worker thread. Every interface shares this runtime, meaning requests execute sequentially instead of concurrently.

### Agent State

Each node receives and returns a shared `AgentState` object. It tracks routing decisions, tool requests and results, report paths, firmware metadata, and execution history throughout the graph.

Using a structured state provides two practical benefits:

- Every run is fully traceable.
- Automated workflows, such as Jenkins, can inject resolved firmware metadata directly into the graph without relying on natural-language parsing.

### Tech Stack

| Component | Technology |
|---|---|
| Model | Qwen3.5-9B, 4-bit (`mlx-community/Qwen3.5-9B-MLX-4bit`) |
| Orchestration | LangGraph |
| LLM inference | MLX + MLX-LM |
| State management | Pydantic v2 |
| Vector database | Qdrant (embedded) |
| Embeddings | Qwen3-Embedding-0.6B |
| Binary analysis | IDA Pro 9.1 headless, over RPyC |
| Firmware tooling | `ipsw` CLI |
| Interfaces | FastAPI, Gradio |
| Runtime | Python 3.11+, macOS on Apple Silicon |
| Testing and CI | pytest, ruff, Jenkins |

## How It Works

### Request Lifecycle

Every request follows the same execution flow:

1. The supervisor classifies the request and decides which domain graph(s) to run.
2. Each graph executes independently, calling tools as needed through a host-side executor.
3. The runtime combines the outputs into a single response, including execution metadata and any tool failures.

The software development graph plans its own workflow by selecting from code generation, unit testing, and architecture review. A generation step is only considered successful once files are written to disk. If the model returns prose instead of issuing a `create_file` tool call, the node retries until the iteration limit is reached.

### Firmware Analysis Pipeline

| Stage | Node | Purpose |
|---|---|---|
| 1 | `firmware_locator` | Resolve device identifiers and build numbers |
| 2 | `firmware_downloader` | Download IPSW files |
| 3 | `ipsw_extractor` | Extract `dyld_shared_cache` and `kernelcache` |
| 4 | `firmware_diff_service` | Generate a structured firmware diff |
| 5 | `feature_analysis_select` | Triage, scoring, and advisory matching |
| 6 | `prepare_decompiler` | Extract binaries and start IDA Pro |
| 7 | `unified_feature_analysis` | Analyse each selected component |
| 8 | `cleanup_decompiler` | Save annotations and close IDA |
| 9 | `feature_analysis_compile` | Generate per-component reports |
| 10 | `synthesize` | Produce the final report |

### Reducing Firmware Diffs

Raw `ipsw diff` output can reach hundreds of megabytes, so the diff service generates a compact `report.json` (typically ~11 KB) containing only the data needed for analysis.

It reduces the diff by:

- **Ignoring assets** that aren't useful for analysis, such as Metal shaders, ISP firmware, watch faces, and media bundles.
- **Filtering metadata-only changes**, including UUIDs, load commands, timestamps, version strings, and `__LINKEDIT` differences.
- **Grouping the remaining changes** into `userland_changes`, `boundary_changes`, and `base_firmware_changes`.

`report.json` is the interface between the diff and analysis stages.

### Scoring

After filtering, each component is assigned a priority score.

| Score | Meaning |
|---|---|
| **4** | Mentioned in Apple's security notes |
| **3** | Strong security indicators (heap, locks, stack guards, entitlement checks) |
| **2** | Security-related symbols or strings |
| **1** | Symbol changes only |
| **0** | Assets or metadata changes only |

If more than `FEATURE_ANALYSIS_BUDGET` (100 by default) components remain, anything scoring below **2** is dropped first. The highest-scoring components are analysed, while all components still appear in the triage summary.

Advisory matching is deterministic. Component names are normalised and matched against the cached Apple Security Notes without using the LLM.

## Installation

**Requirements**

- macOS on Apple Silicon
- Python 3.11+
- ~10 GB free disk space

Create the environment:

```bash
python3 -m venv venv
source venv/bin/activate

python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-dev.txt

cp .env.example .env
```

Configure `IDA_PATH` and `IDA_RPC_SCRIPT_PATH` if you plan to use decompilation.

Download the required models and cache Apple Security Notes:

```bash
python3 -m langgraph_orchestration.inference
python3 scripts/update_security_notes.py 26.4.2
```

Verify the installation and enable offline mode:

```bash
python3 -m langgraph_orchestration.inference --verify

echo "HF_HUB_OFFLINE=1" >> .env

python3 app.py
```

Existing model weights under `models/` or `~/.cache/huggingface` are reused automatically.

Firmware analysis additionally requires:

- `ipsw` CLI (`brew install blacktop/tap/ipsw`)
- IDA Pro 9.1+ with the Hex-Rays decompiler

## Usage

| Interface | Command | Address |
|---|---|---|
| Gradio chat UI | `python3 app.py` | `http://127.0.0.1:7860` |
| FastAPI service | `python3 api.py` | `http://127.0.0.1:8000` |
| Direct Python | `get_runtime().run(...)` | in process |

Gradio conversation history is stored locally for display and never used as model context.

### HTTP API

```bash
curl -X POST http://127.0.0.1:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"user_input":"Implement an API auth flow and inspect it for vulnerabilities"}'
```

Available endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /` | Health check |
| `GET /info` | Runtime information |
| `POST /invoke` | Execute a request |
| `POST /rag/add` | Add documents to the vector database |
| `POST /rag/search` | Semantic search |
| `GET /rag/stats` | Collection statistics |

CORS is restricted to localhost.

### Python API

```python
from langgraph_orchestration.runtime import get_runtime

state = get_runtime().run(
    "Generate a Python sorting function and assess security risks"
)

print(state.execution_domains)
print(state.agent_chain)
print(state.final_output)
```

### Firmware Comparison

A prompt such as `compare iPhone18,1 ios 26.4.1 and 26.4.2` runs the full firmware analysis pipeline. Output is written to a timestamped directory:

```text
artifacts/firmware_diff/20260712-141626/
├── report.json                     # structured payload, the only thing the model sees
├── artifacts/                      # raw ipsw dyld/kernel/launchd/kext/sandbox output
├── diff/26_4_1_23E254_vs_26_4_2_23E261/
│   └── README.md                   # raw ipsw diff markdown, deliberately withheld
├── entitlements/entitlements.idiff
└── feature_analysis/
    ├── 00_SUMMARY.md               # every component and its triage verdict
    └── <component>_analysis.md     # one file per analysed component
```

Example outputs from real firmware analyses are available under `artifacts/`.

IDA `.i64` databases are reused across runs, so annotations accumulate over time instead of being recreated.

### Scheduled Runs

[scripts/automation.py](scripts/automation.py) drives a four-stage Jenkins pipeline.

| Stage | Purpose |
|---|---|
| Check | Detect new firmware releases |
| Download | Fetch firmware and security advisories |
| Analyse | Execute the orchestration graph |
| Cleanup | Remove superseded IPSWs |

Each stage can be retried independently. The pipeline uses the same `OrchestrationRuntime.run()` entry point as the UI and API.

## Configuration

Configuration is managed through `.env`. See [.env.example](.env.example) for the full list. The settings below are the ones you'll most commonly change.

| Variable | Default | Purpose |
|---|---|---|
| `HF_HUB_OFFLINE` | unset | Disable model downloads after setup |
| `MODELS_DIR` | `./models` | Model storage directory |
| `SECURITY_NOTES_DIR` | `./data/security_notes` | Apple Security Notes cache |
| `IDA_PATH` | — | Path to `idat` |
| `IDA_RPC_SCRIPT_PATH` | — | Path to `ida_rpc_server.py` |
| `API_HOST` / `API_PORT` | `127.0.0.1` / `8000` | FastAPI bind address |
| `APP_HOST` / `APP_PORT` | `127.0.0.1` / `7860` | Gradio bind address |
| `IPSW_DOWNLOADS_API_ENABLE` | enabled | Enable firmware downloads |
| `IPSW_DIFF_LOW_MEMORY` | unset | Reduce memory usage during large diffs |
| `FEATURE_ANALYSIS_RESUME` | unset | Resume interrupted analysis |
| `RE_DEBUG` | unset | Save prompts and raw model output |
| `PIPELINE_DEVICES` | unset | Restrict scheduled analysis to selected devices |

### Offline Mode

For fully local execution, set:

- `HF_HUB_OFFLINE=1`
- `LANGSMITH_TRACING=false`

The offline compliance tests verify both settings.

Firmware downloads are the only network access required during analysis. Set `IPSW_DOWNLOADS_API_ENABLE=0` to analyse only firmware already available on disk.

## Development

Run the test suite and code quality checks:

```bash
source venv/bin/activate

pytest
ruff check .
ruff format --check .
```

The test suite focuses on two areas:

- **Offline compliance** (`tests/test_offline_compliance.py`) verifies that the runtime remains local-first, including network imports, loopback-only bindings, and runtime configuration.
- **Output contracts** (`tests/test_output_contracts.py`) ensure artifacts remain compatible across pipeline stages.

`Jenkinsfile.ci` runs dependency checks, Ruff, the test suite, offline compliance, and a non-blocking `pip-audit`.

### Benchmarks

The benchmark scripts require downloaded models, firmware images, and IDA Pro, so they run outside `pytest`.

```bash
python3 benchmarks/test_ipsw_diff.py
python3 benchmarks/test_feature_analysis.py
```

`test_feature_analysis.py` loads an existing `report.json`, making it useful for iterating on feature analysis without rerunning the firmware diff.

### LangGraph Studio

```bash
langgraph dev
```

Run Studio from the repository root and connect to `langgraph dev`. Since Qdrant runs in embedded mode, only one process can access the database at a time.

## Troubleshooting

| Problem | Solution |
|---|---|
| `No local copy of ...` | Download the models, then re-enable `HF_HUB_OFFLINE` |
| `Model type qwen3_5 not supported` | Activate the virtual environment and reinstall `mlx-lm` |
| GPU out of memory | Ensure `report.json` is passed to the model instead of the raw diff |
| `Qdrant database locked` | Stop any process using the embedded database |
| No security note matches | Run `update_security_notes.py` for the target release |
| `Port 18861 is still in use` | Terminate the stale IDA instance |
| `ipsw: command not found` | Ensure Homebrew's bin directory is on the Jenkins PATH |

## Limitations

- Runs only on macOS with Apple Silicon, and full decompilation requires IDA Pro 9.1+ with Hex-Rays.
- Requests execute sequentially using a single shared model instance.
- Diff filtering and scoring are tuned for iOS firmware.
- Qdrant retrieval is optional and requires indexed documents.

## Reference

### Repository Layout

| Path | Purpose |
|---|---|
| `app.py`, `api.py` | Gradio UI and FastAPI service |
| `langgraph_orchestration/` | Orchestration engine |
| `ipsw_service/` | Firmware tooling |
| `scripts/` | Automation and CLI utilities |
| `data/`, `models/`, `artifacts/` | Data, models, and generated output |
| `tests/`, `benchmarks/` | Tests and benchmarks |

> **Note:** `langgraph_orchestration/prompts_md/` contains runtime prompt templates, while `knowledge_base/` is an optional RAG corpus.

### Documentation

| Document | Purpose |
|---|---|
| `README.md` | Project overview, setup, and usage |
| `langgraph_orchestration/README.md` | Runtime architecture and internals |
| `scripts/README.md` | CLI utilities |
| `docs/jenkins_setup.md` | Jenkins setup |

### Further Reading

- [LangGraph](https://langchain-ai.github.io/langgraph/)
- [MLX](https://ml-explore.github.io/mlx/)
- [IDA Pro](https://hex-rays.com/ida-pro/)
- [ipsw CLI](https://blacktop.github.io/ipsw/)
- [Qdrant](https://qdrant.tech/documentation/)
# Local Multi-Agent Development System

Local-first, LangGraph-based orchestration for two domains: software development and reverse engineering. A supervisor routes requests to one or both branches and returns a unified result.

## What This Repository Provides
- Domain routing with optional dual-branch execution
- Software development workflow: code generation, testing loop, architecture review
- Reverse engineering workflow: firmware diffing, feature analysis, IDA Pro binary decompilation
- FastAPI service for local use and LangSmith Studio integration
- MLX-based local inference on Apple Silicon (Qwen3.5-9B-4bit)
- Embedded Qdrant retrieval with Qwen embeddings

## Tech Stack

| Component | Technology |
|---|---|
| Model | Qwen3.5-9B-4bit |
| Orchestration | LangGraph |
| LLM inference | MLX + MLX-LM |
| State management | Pydantic |
| Vector database | Qdrant (embedded) |
| Embeddings | Qwen3 Embeddings |
| Binary analysis | IDA Pro 9.1 (headless, via RPyC RPC) |
| Firmware tooling | `ipsw` CLI |
| API server | FastAPI |
| Runtime | Python 3.11+ |

## Architecture

### System Architecture
<img src="assets/system-architecture.png" alt="System Architecture" width="700"/>

### High-Level Flow
<img src="assets/high-level-flow.png" alt="High-Level Flow" width="700"/>

### LangGraph Flow
<img src="assets/langgraph.png" alt="LangGraph Flow" width="700"/>

---

## IPSW Firmware Analysis Pipeline

The reverse engineering domain includes a dedicated, stage-gated firmware analysis pipeline powered by the `ipsw` CLI and a headless IDA Pro 9.1 RPC server.

### Pipeline Stages

| Stage | Node | What it does |
|---|---|---|
| 1 | `firmware_locator` | Resolves device identifiers and build numbers |
| 2 | `firmware_downloader` | Downloads IPSW/OTA artifacts |
| 3 | `ipsw_extractor` | Extracts `dyld_shared_cache` and `kernelcache` |
| 4 | `firmware_diff_service` | Diffs old vs new firmware; writes structured `report.json` |
| 5 | `feature_analysis_select` → `prepare_decompiler` → `unified_feature_analysis` | LLM-driven per-component analysis with IDA decompilation |
| 6 | `cleanup_decompiler` | Saves IDA database (`.i64`) then shuts down IDA |
| 7 | `feature_analysis_compile` | Writes per-component markdown reports |
| 8 | `reverse_engineering_synthesize` | Aggregates all findings into a final report |

### Firmware Diff Service (`ipsw_service/`)

`FirmwareDiffService` generates a structured diff JSON and orchestrates all analysis steps:

- Runs `ipsw diff` to detect changes in Mach-O binaries, entitlements, launchd plists, sandbox profiles, and kernel extensions.
- Runs `ipsw dyld info --dylibs --diff` on `dyld_shared_cache_arm64e` pairs to capture DSC framework changes not covered by standard diffs.
- Classifies results by origin: filesystem binaries → `macho`, shared cache binaries → `dsc`.
- Applies `IGNORE_PATTERNS` to exclude non-analyzable artifacts (e.g. Metal shaders, microcode).
- Suppresses metadata-only diffs (e.g. UUID, `LC_*`, `__LINKEDIT`) to reduce noise.

**Artifact layout for a run (e.g. `20260705-095834`, iOS 26.4.1 → 26.4.2):**
```
artifacts/firmware_diff/20260705-095834/
├── report.json                        ← structured diff payload (fed to LLM)
├── artifacts/
│   ├── dyld_diff.txt                  ← raw ipsw dyld diff output + parsed items
│   ├── kernel_diff.txt
│   ├── launchd_diff.txt
│   ├── kext_diff.txt
│   └── sandbox_diff.txt
├── diff/26_4_1_23E254_vs_26_4_2_23E261/
│   └── README.md                      ← raw ipsw diff markdown (30KB+, not fed to LLM)
├── entitlements/
│   └── entitlements.idiff
└── feature_analysis/
    ├── 00_SUMMARY.md                  ← security-tiered summary of all analyzed components
    ├── iMessage_analysis.md
    ├── IMSharedUtilities_analysis.md
    └── <component>_analysis.md        ← one file per analyzed component
```

> **Note:** `report.json` (typically ~11KB) is what gets injected into the LLM's context for feature analysis. The raw `README.md` from `ipsw diff` (~30KB+) is intentionally excluded to avoid GPU OOM on local MLX inference.

### `report.json` Schema

```json
{
  "summary_metrics": { "total_cstring_changes": 74 },
  "kernel": {
    "kexts": ["..."],
    "firmware": ["..."]
  },
  "macho": {
    "updated": ["..."]
  },
  "dsc": {
    "dylibs": {
      "updated": ["..."]
    }
  },
  "feature_flags": [],
  "boundary_changes": {
    "entitlements": [],
    "sandbox": [],
    "launchd": ["..."]
  },
  "cstring_context": [
    "ComponentName: + \"<added_string>\"",
    "ComponentName: - \"<removed_string>\""
  ]
}
```

### IDA Pro Integration

The feature analysis pipeline connects to IDA Pro 9.1 via a headless RPyC RPC server (`langgraph_orchestration/tooling/ida_rpc_server.py`).

**How it works:**
1. `prepare_decompiler_node` extracts the target binary from the DSC using `ipsw dyld extract` into a per-comparison folder under `.ipsw_features/` (named for the firmware diff, e.g. `.ipsw_features/iPhone17,1__18_4_22E240_vs_18_4_1_22E252/`).
2. IDA is launched headlessly: `idat -A -c -S<rpc_server.py> <binary>`.
3. The LLM calls IDA tools during feature analysis: `find_address`, `get_xrefs_to`, `decompile_function`, `rename_local_variable`, `set_comment`.
4. `cleanup_decompiler_node` **always** calls `save_ida_database` before stopping IDA, guaranteeing the `.i64` is written regardless of LLM behaviour.

**IDA database files:**
```
.ipsw_features/
└── iPhone18,1__26_4_1_23E254_vs_26_4_2_23E261/   ← one folder per firmware comparison
    ├── MANIFEST.md             ← comparison metadata + list of .i64 databases
    ├── IMSharedUtilities       ← extracted Mach-O binary (from the NEW build)
    ├── IMSharedUtilities.i64   ← saved IDA database (written by cleanup_decompiler_node)
    ├── AppPredictionClient
    ├── AppPredictionClient.i64
    └── ...
```

The folder name is derived from the diff pair by `_comparison_dirname`, matching the
`artifacts/firmware_diff/.../diff/<old>_vs_<new>` naming so the two cross-reference.

> **Important:** If a `.i64` already exists for a binary, `start_ida_server_for_binary` will reload it (preserving prior annotations) instead of creating a fresh database. Only the unpacked working files (`.id0/.id1/.nam/.til`) from aborted runs are cleaned up on restart.

**Required `.env` variables for IDA integration:**
```
IDA_PATH=/Applications/IDA Professional 9.1.app/Contents/MacOS/idat
IDA_RPC_SCRIPT_PATH=/path/to/repo/langgraph_orchestration/tooling/ida_rpc_server.py
```

IDA listens on `localhost:18861`. The client uses a 360-second RPC timeout (larger than the server-side 300-second main-thread timeout).

### DSC Binary Extraction

The `prepare_decompiler_node` uses the following extraction strategy (in priority order):

1. **Pre-extracted binary** — checks this comparison's `.ipsw_features/<comparison>/` folder for an already-extracted Mach-O.
2. **DSC extraction** — `ipsw dyld extract <dsc_path> <binary_path> -o .ipsw_features/<comparison>/` (fastest, no DMG mount).
3. **Existing DMG mount** — scans `/private/tmp/*.mount` for binaries left by `ipsw diff`.
4. **IPSW archive extraction** — `ipsw extract <ipsw> --files --pattern <name>` (fallback for daemons and apps not in the DSC).

### Feature Analysis Targets

The pipeline does not analyze every changed binary. `_build_feature_targets` filters the diff report down to **high-signal components** — those that carry meaningful cstring or symbol evidence. Only these are queued for IDA-assisted decompilation.

Each feature analysis report (`<component>_analysis.md`) follows this structure:
```
## What this feature does
## How is it implemented      ← includes decompiled pseudocode and call chains
## How to trigger this feature
## Evidence                   ← addresses, symbols, strings, decompiled excerpts
## AI Prioritisation Scoring System
```

---

## Benchmark Harnesses

### `benchmarks/test_ipsw_diff.py` — Full pipeline benchmark

Runs the complete orchestration graph (firmware diff + feature analysis) end to end.

```bash
source venv/bin/activate
python3 benchmarks/test_ipsw_diff.py
```

- Builds an `IpswDiffCase` for a fixed pair of IPSWs.
- Runs `build_orchestration_graph` → invokes the full pipeline.
- On completion, calls `trigger_feature_analysis` on the generated `report.json`.
- Writes benchmark results to `benchmarks/results/test_ipsw_diff/`.

> **Note:** `trigger_feature_analysis` uses `report.json` (not the raw `README.md`) to avoid OOM on local MLX. It searches up to 3 directory levels from the README path to locate `report.json`.

### `benchmarks/test_feature_analysis.py` — Feature analysis only

Runs feature analysis directly against an existing diff report without re-running the firmware diff stage. Useful when the diff artifacts already exist and you want to iterate on the LLM analysis.

```bash
source venv/bin/activate
python3 benchmarks/test_feature_analysis.py
```

- Reads the README.md from a fixed path (edit `REPORT_PATH` at the top of the file).
- Pre-filters the report to dylib-relevant sections before injecting into state.
- Streams graph chunks and prints node-by-node progress.
- Writes results to `benchmarks/results/test_feature_analysis/`.

> **Note:** This benchmark directly seeds `firmware_diff_report` in state, so the graph routes straight to `feature_analysis_select_node`. The firmware diff stage is skipped entirely.

---

## Quickstart

Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Copy and fill in environment variables:
```bash
cp .env.example .env
# Edit .env — set IDA_PATH, IDA_RPC_SCRIPT_PATH, and optionally LANGSMITH_API_KEY
```

Run the example script:
```bash
source venv/bin/activate
python3 examples.py
```

API default address: `http://localhost:8000` (`API_HOST` and `API_PORT` are configurable via `.env`)

---

## How To Communicate With The Model

1. CLI via API (`curl` to FastAPI `POST /invoke`)
2. Direct Python graph invocation
3. Gradio chat interface (interactive local UI)

### 1) CLI via API endpoint

```bash
source venv/bin/activate
python3 api.py
```

```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"user_input":"Implement an API auth flow and inspect it for vulnerabilities"}'
```

Example response shape:
```json
{
  "selected_domain": "software_dev",
  "agent_chain": ["retrieve_dev_context", "code_generation", "unit_testing"],
  "final_output": "...",
  "intermediate_outputs": ["..."]
}
```

### 2) Direct Python graph invocation

All three interfaces (`examples.py`, `app.py`, `api.py`) route through a single
shared entry point — `OrchestrationRuntime` 

```python
from langgraph_orchestration.runtime import get_runtime

# Returns an AgentState; the runtime builds and caches the graph on first use
final_state = get_runtime().run(
    "Generate a Python sorting function and assess security risks"
)

print(final_state.selected_domain)
print(final_state.agent_chain)
print(final_state.final_output)
```

### 3) Gradio chat interface

```bash
source venv/bin/activate
python3 app.py
```

Open: `http://127.0.0.1:7860`

---

## API Surface
- `GET /` health check
- `GET /info` service metadata and configured agents
- `GET /domains` available domains and descriptions
- `POST /invoke` run orchestration with `user_input` and optional `domain`
- `GET /assistants` LangSmith Studio assistants list
- `POST /assistants/search` LangSmith Studio search endpoint
- `GET /assistants/{assistant_id}` assistant details
- `GET /assistants/{assistant_id}/schemas` input/output schemas
- `GET /graph` graph nodes and edges
- `GET /graph/schema` runnable schema
- `POST /langgraph` LangSmith invocation
- `GET /test-graph` LangSmith registration check
- `GET /threads` list threads placeholder
- `POST /threads/{thread_id}/messages` send a message

---

## Embedding Models And Retrieval

Embedding Model: [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)

| Purpose | Where It Is Active |
|---|---|
| General docs (base model) | Used during ingestion for shared knowledge base; used at runtime to embed `agents_shared` queries |
| Code retrieval (base model) | Used during ingestion for `agents_software_dev`; used at runtime for semantic code search |
| Reverse engineering (fine-tuned model) | Used during ingestion for RE corpus; used at runtime for `agents_reverse_engineering` queries |

Qdrant storage layout (embedded local DB):
```text
~/.local/share/qdrant/
├── agents_software_dev       (code retrieval)
├── agents_reverse_engineering (RE)
└── agents_shared             (general docs)
```

### Ingesting Documents

Use the helper script in `scripts/`:
- `scripts/load_documents_to_qdrant.py` — load `.md`, `.markdown`, `.txt`, or `.jsonl` files into a collection.

Chunking behaviour (defaults):
- Markdown-aware chunking: splits on headers and groups content into chunks.
- Word chunking: used for plain text files.
- JSONL ingestion: each line is treated as a pre-chunked record with `text` and optional `metadata`.

```bash
python scripts/load_documents_to_qdrant.py --file README.md --domain shared
python scripts/load_documents_to_qdrant.py --dir ./docs --domain software_dev --chunk-size 512 --overlap 100
python scripts/load_documents_to_qdrant.py --file chunks.jsonl --domain shared
```

What gets stored:
- Each chunk is embedded and written to the domain collection (`agents_<domain>`).
- Default metadata fields: `source_file`, `chunk_index`, `total_chunks`, `file_type`.
- JSONL chunks can carry custom metadata per line.
- Insertion is batched (default `batch_size=32`).

---

## Configuration Notes

- Inference uses MLX/MLX-LM and expects a compatible local model on Apple Silicon.
- LangSmith tracing is enabled when `LANGSMITH_TRACING=true`.
- API host and port are controlled by `API_HOST` and `API_PORT`.
- If you see `Model type qwen3_5 not supported`, upgrade `mlx-lm` or select a model supported by your current runtime.
- The firmware pipeline requires `ipsw` to be installed and on `PATH` (`brew install blacktop/tap/ipsw`).
- IDA Pro integration requires IDA 9.1+ with Hex-Rays decompiler and a valid license. The RPC server uses `rpyc` — install with `pip install rpyc`.
- GPU OOM crashes during MLX inference are caused by oversized context payloads. The pipeline is designed to pass `report.json` (~11KB) rather than the raw diff markdown to the LLM.

## Dev And Benchmarks

```bash
# Syntax check
python3 -m compileall langgraph_orchestration api.py

# Full pipeline benchmark (firmware diff + feature analysis)
python3 benchmarks/test_ipsw_diff.py

# Feature analysis only (requires existing diff artifacts)
python3 benchmarks/test_feature_analysis.py

# No-RAG benchmark
python3 benchmarks/test_no_rag.py
```

LangGraph local dev server with tracing UI:
1. Create a LangSmith account and generate an API key.
2. Set tracing env vars in `.env`:
   - `LANGSMITH_API_KEY=<your_key>`
   - `LANGSMITH_TRACING=true`
   - `LANGSMITH_PROJECT=local-multi-agent-dev`
3. Stop other local API servers first.
4. Start dev server from repo root: `langgraph dev`
5. Open the local LangGraph Studio URL printed in terminal.

---

## References
- LangGraph: https://langchain-ai.github.io/langgraph/
- ipsw CLI: https://blacktop.github.io/ipsw/
- IDA Pro: https://hex-rays.com/ida-pro/
- RPyC: https://rpyc.readthedocs.io/
- Pydantic: https://docs.pydantic.dev/
- Qdrant: https://qdrant.tech/documentation/
- Qwen3 Embeddings: https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
- MLX: https://ml-explore.github.io/mlx/
- FastAPI: https://fastapi.tiangolo.com/

Last updated: July 2026
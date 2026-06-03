# Local Multi-Agent Development System

Local-first, LangGraph-based orchestration for two domains: software development and reverse engineering. A supervisor routes requests to one or both branches and returns a unified result.

## What This Repository Provides
- Domain routing with optional dual-branch execution
- Software development workflow: code generation, testing loop, architecture review
- Reverse engineering workflow: planning, code analysis, vulnerability detection
- FastAPI service for local use and LangSmith Studio integration
- MLX-based local inference on Apple Silicon
- Embedded Qdrant retrieval with Qwen embeddings

## Tool Calling

Tool loop flow:
1. Agent requests a tool action.
2. Host executes the local tool.
3. Output is added to state and returned to the agent.
4. Repeat until completion or iteration limit.

## Tech Stack

| Component | Technology |
|---|---|
| Model | Qwen3.5-9B-4bit |
| Orchestration | LangGraph |
| LLM inference | MLX + MLX-LM |
| State management | Pydantic |
| Vector database | Qdrant (embedded) |
| Embeddings | Qwen3 Embeddings |
| API server | FastAPI |
| Runtime | Python 3.11+ |

## Architecture

### System Architecture
![System Architecture](assets/system-architecture.png)

### High-Level Flow
![High-Level Flow](assets/high-level-flow.png)

### LangGraph Flow
![LangGraph Flow](assets/langgraph.png)

## Quickstart

Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Run the example script:
```bash
source venv/bin/activate
python3 examples.py
```

API default address: `http://localhost:8000` (`API_HOST` and `API_PORT` are changeable)

## How To Communicate With The Model

1. Gradio chat interface (interactive local UI)
2. CLI via API (`curl` to FastAPI `POST /invoke`)
3. Direct Python graph invocation (run inside your own scripts/tests)

### 1) Gradio chat interface

Use this for quick local experimentation with a chat UX.

```bash
source venv/bin/activate
python3 app.py
```

The UI includes:
- Domain selector (`Software Dev` or `Reverse Engineering`)
- Optional `Enable RAG Context` toggle
- Chat interface with starter prompts

Open: `http://127.0.0.1:7860`

### 2) CLI via API endpoint

Use this for scriptable calls, shell workflows, and external tool integration.

First start the API server:
```bash
source venv/bin/activate
python3 api.py
```

Then invoke the model from CLI:
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

### 3) Direct Python graph invocation

Use this when you want the orchestration flow embedded directly in Python code.

```python
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.graphs.orchestration import build_orchestration_graph

graph = build_orchestration_graph()
state = AgentState(user_input="Generate a Python sorting function and assess security risks")
result = graph.invoke(state.model_dump())

print(result["selected_domain"])
print(result["agent_chain"])
print(result["final_output"])
```

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

## Embedding Models And Retrieval

Embedding Model: [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)

| Purpose | Where It Is Active |
|---|---|
| General docs (base model) | - Used during ingestion for shared knowledge base<br>- Used at runtime to embed `agents_shared` queries for retrieval |
| Code retrieval (base model) | - Used during ingestion for `agents_software_dev` code index<br>- Used at runtime to embed `agents_software_dev` queries for semantic code search |
| Reverse engineering (fine-tuned model) | - Used during ingestion for RE corpus<br>- Used at runtime to embed `agents_reverse_engineering` queries for program-understanding search |

Qdrant storage layout (embedded local DB):
```text
~/.local/share/qdrant/
├── agents_software_dev (code retrieval)
├── agents_reverse_engineering (RE)
└── agents_shared (general docs)
```

Ingesting documents & chunking
---------------------------------
Use the helper script in `scripts/`:

- `scripts/load_documents_to_qdrant.py` — load `.md`, `.markdown`, `.txt`, or `.jsonl` files into a collection.

Chunking behavior (defaults):
- Markdown-aware chunking: splits on headers and groups content into chunks.
- Word chunking: used for plain text files.
- JSONL ingestion: each line is treated as a pre-chunked record with `text` and optional `metadata`.

Example commands:
```bash
python scripts/load_documents_to_qdrant.py --file README.md --domain shared
python scripts/load_documents_to_qdrant.py --dir ./docs --domain software_dev --chunk-size 512 --overlap 100
python scripts/load_documents_to_qdrant.py --file chunks.jsonl --domain shared
```

What gets stored
- Each chunk is embedded and written to the domain collection (`agents_<domain>`).
- Default metadata fields: `source_file`, `chunk_index`, `total_chunks`, `file_type`.
- JSONL chunks can carry custom metadata per line.
- Insertion is batched (default `batch_size=32`) to balance memory and throughput.

Recommended ingestion policy
- Use markdown for documentation and notes.
- Use raw source files for code when you want retrieval on the code itself.
- Use JSONL only when you already have clean, pre-split chunks or need custom metadata per chunk.

## Configuration Notes
- Inference uses MLX/MLX-LM and expects a compatible local model
- LangSmith tracing is enabled when `LANGSMITH_TRACING=true`
- API host and port are controlled by `API_HOST` and `API_PORT`
- If you see `Model type qwen3_5 not supported`, upgrade `mlx-lm` or select a model supported by your current runtime

## Dev And Benchmarks
- Compile check: `python3 -m compileall langgraph_orchestration api.py`
- No-RAG benchmark harness: `python3 benchmarks/test_no_rag.py`
- Harness validation: `python3 benchmarks/test_validation.py`
- LangGraph local dev server with tracing UI:
  1. Create a LangSmith account and generate an API key.
  2. Set tracing env vars in `.env` (used by `langgraph.json`):
     - `LANGSMITH_API_KEY=<your_key>`
     - `LANGSMITH_TRACING=true`
     - `LANGSMITH_PROJECT=local-multi-agent-dev` 
  3. Stop other local API servers first (e.g. `python3 api.py`/other service bound to the same ports).
  4. Start dev server from repo root: `langgraph dev`
  5. Open the local LangGraph Studio URL printed in terminal to inspect traces and runs.

## References
- LangGraph: https://langchain-ai.github.io/langgraph/
- Pydantic: https://docs.pydantic.dev/
- Qdrant: https://qdrant.tech/documentation/
- Qwen3 Embeddings: https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
- MLX: https://ml-explore.github.io/mlx/
- FastAPI: https://fastapi.tiangolo.com/

Last updated: June 2026

# Local Multi-Agent Development System

Local-first, LangGraph-based orchestration for two domains: software development and reverse engineering. A supervisor model routes requests to one or both branches and produces a unified result.

## What This Provides
- Domain routing with optional dual-branch execution
- Software development workflow: code generation, testing loop, architecture review
- Reverse engineering workflow: planning, code analysis, vulnerability detection
- FastAPI service for local use and integration with LangSmith Studio
- MLX-based local inference on Apple Silicon

## Tech Stack

| Component | Technology |
|---|---|
| **Orchestration** | LangGraph |
| **LLM Inference** | MLX + MLX-LM |
| **State Management** | Pydantic |
| **Vector Database** | Qdrant (Embedded) |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) |
| **API Server** | FastAPI |
| **Runtime** | Python 3.11+ |

## Flow (High-Level)
![System Architecture](assets/system-architecture.png)
![LangGraph Flow](assets/langgraph.png)

**Supervisor**
- Classifies the request and selects execution domains
- Splits tasks when both domains are relevant

**Software Development Branch**
- `retrieve_dev_context` 
- `code_generation` → `unit_testing` (loop until pass or iteration cap)
- `architectural_review` → `synthesize`

**Reverse Engineering Branch**
- `retrieve_re_context`
- `planning` → `code_analysis` → `vulnerability_detection` → `synthesize`

**Final Synthesis**
- Merges branch outputs when both ran, otherwise returns the selected branch result

## Quick Start

Install:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Run examples:
```bash
source venv/bin/activate
python3 examples.py
```

Run API server:
```bash
source venv/bin/activate
python3 api.py
```

API default address: `http://localhost:8000`

## Python Usage
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
- `POST /langgraph` LangSmith-friendly invocation
- `GET /test-graph` LangSmith registration check
- `GET /threads` list threads (placeholder)
- `POST /threads/{thread_id}/messages` send a message

Example request:
```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Implement an API auth flow and inspect it for vulnerabilities"}'
```

## Configuration Notes
- Inference uses MLX/MLX-LM and expects a compatible local model
- LangSmith tracing is enabled when `LANGSMITH_TRACING=true`
- API host and port are controlled by `API_HOST` and `API_PORT`

If you see `Model type qwen3_5 not supported`, upgrade `mlx-lm` or select a model supported by your current runtime.

## Dev and Benchmarks
- Compile check: `python3 -m compileall langgraph_orchestration api.py`
- No-RAG benchmark harness: `python3 benchmarks/no_rag_harness.py`
- Harness validation: `python3 benchmarks/validate_harness.py`

## References
- **LangGraph**: https://langchain-ai.github.io/langgraph/
- **Pydantic**: https://docs.pydantic.dev/
- **Qdrant**: https://qdrant.tech/documentation/
- **Sentence Transformers**: https://www.sbert.net/
- **MLX**: https://ml-explore.github.io/mlx/
- **FastAPI**: https://fastapi.tiangolo.com/

Last updated: May 2026
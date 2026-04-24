# Local Multi-Agent Development System

A local-first, LangGraph-based multi-agent orchestration system with two specialized domains:
- Software Development
- Reverse Engineering

It uses an LLM-powered supervisor for dynamic routing, branch-specific retrieval, and structured synthesis across one or both branches.

## Architecture
![System Architecture](assets/system-architecture.png)

LangGraph flow:
![LangGraph Flow](assets/langgraph.png)

Software development branch:

1. `retrieve_dev_context`
2. `code_generation`
3. `unit_testing`
4. Conditional loop:
   - if tests fail and iteration limit not reached: back to `code_generation`
   - else: continue
5. `architectural_review`
6. `synthesize`

Reverse engineering branch:

1. `retrieve_re_context`
2. `planning`
3. `code_analysis`
4. `vulnerability_detection`
5. `synthesize`

## Tech Stack

| Component | Technology |
|---|---|
| Orchestration | LangGraph |
| LLM Inference | MLX + MLX-LM |
| State Model | Pydantic |
| Retrieval Layer | Qdrant Vector Database|
| API | FastAPI |
| Language | Python 3.9+ |

## Installation

```bash
git clone https://github.com/yourusername/local-multi-agent-dev.git
cd local-multi-agent-dev
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Quick Start

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

## Basic Python Usage

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

## API Endpoints

- `GET /` health check
- `GET /info` service metadata
- `GET /domains` available domains
- `POST /invoke` run orchestration
- `GET /graph` graph nodes and edges
- `GET /graph/schema` runnable schema
- `POST /langgraph` LangSmith-friendly invocation

Example request:

```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Implement an API auth flow and inspect it for vulnerabilities"}'
```

## Notes on Local Models

The project is configured for MLX-based local inference.

If you see an error like `Model type qwen3_5 not supported`, your installed `mlx-lm` version likely does not support the selected checkpoint architecture. In that case:

1. Upgrade `mlx-lm` to a version that supports your model, or
2. Switch to an MLX model repo compatible with your current `mlx-lm` install

## Development

Useful commands:

```bash
python3 -m compileall langgraph_orchestration api.py
python3 test_graph_tracing.py
```

## References

- LangGraph: https://langchain-ai.github.io/langgraph/
- Pydantic: https://docs.pydantic.dev/
- Qdrant: https://qdrant.tech/documentation/

Last updated: April 2026
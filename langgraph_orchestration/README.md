# `langgraph_orchestration` - Orchestration Engine

The core LangGraph engine for the multi-agent system. A **supervisor** classifies each
user request and routes it to one or both domain subgraphs (**software development** and
**reverse engineering**) then a **synthesizer** merges the branch outputs into a single
output.

Every interface in the repo (the CLI [`examples.py`](../examples.py), the Gradio chat
[`app.py`](../app.py), and the FastAPI service [`api.py`](../api.py)) drives this package
through one shared entry point: [`OrchestrationRuntime`](runtime.py).

> **Scope of this document.** This README explains the engine's *internals and extension
> points* for developers working inside the package. For installing dependencies, `.env`
> setup, running the app, the IPSW/IDA firmware pipeline, RAG ingestion, and benchmarks,
> see the [repository README](../README.md).

---

## Mental model

```
                    ┌──────────────────────────────────────────────┐
   user_input ──▶   │            OrchestrationRuntime              │
                    │ (single MLX thread · builds + caches graph)  │
                    └───────────────────────┬──────────────────────┘
                                             │ AgentState
                                             ▼
                                      ┌──────────────┐
                                      │  supervisor  │  label → domains + split_tasks
                                      └──────┬───────┘
                         software_dev  ┌─────┴─────┐  reverse_engineering
                                       ▼           ▼
                            ┌────────────────┐  ┌──────────────────────┐
                            │ software_dev   │  │ reverse_engineering  │
                            │ subgraph       │─▶│ subgraph             │
                            └────────────────┘  └──────────┬───────────┘
                                       │                   │
                                       └─────────┬─────────┘
                                                 ▼
                                       ┌──────────────────┐
                                       │ final_synthesis  │ ─▶ final_output
                                       └──────────────────┘
```

The supervisor may pick **one** domain or **both**. When both run, execution is
sequential (software development first, then reverse engineering) and `split_tasks`
carries a per-domain restatement of the request so each branch gets a focused prompt.
See [`graphs/orchestration.py`](graphs/orchestration.py) for the routing edges.

---

## Package layout

| Path | Responsibility |
|---|---|
| [`runtime.py`](runtime.py) | **Start here.** `OrchestrationRuntime` - single entry point every interface uses. Lazily builds the graph and pins all MLX work to one thread. |
| [`schemas/state.py`](schemas/state.py) | `AgentState` - Pydantic object that flows through every node (input, retrieved context, per-agent outputs, tool loop, final output, audit trail). |
| [`graphs/orchestration.py`](graphs/orchestration.py) | Top-level supervisor graph and domain routing. |
| [`graphs/software_dev.py`](graphs/software_dev.py) | Software-dev subgraph: code generation ⇄ testing loop → architectural review. |
| [`graphs/reverse_engineering.py`](graphs/reverse_engineering.py) | Reverse-engineering subgraph: the IPSW firmware-diff + IDA decompilation-injection pipeline. |
| [`agents/`](agents/) | Agent implementations. `base.py` (`SyncBaseAgent`), `supervisor.py`, `mlx_agents.py` (the six MLX task agents), `mlx_factory.py` (builds agents on a shared inference engine). |
| [`inference/`](inference/) | `MLXModelLoader` + `MLXInferenceEngine` - local model loading and generation on Apple Silicon. |
| [`prompts/`](prompts/) & [`prompts_md/`](prompts_md/) | Prompt builders (Python) and their Markdown templates, per domain plus shared. |
| [`tooling/`](tooling/) | Local agentic tool loop: `tool.py` (request/result schemas), `executor.py` (VS Code + IDA executors), `parser.py`, `decompiler_tools.py` + `ida_rpc_server.py` (headless IDA RPC). |
| [`retrievers/`](retrievers/) | RAG layer: `base.py`, `qdrant_client.py`, `embeddings.py`, `config.py` (`RAGConfigManager`). |
| [`triage/`](triage/) | `rules.py` - deterministic security triage/scoring for firmware-diff components. |
| [`synthesis/`](synthesis/) | `synthesizer.py` - merges branch outputs into the final report. |
| [`core/`](core/) | `state_utils.py` - `StateManager` helpers for recording outputs and sanitizing text. |

---

## Request lifecycle

1. **Entry.** A caller invokes `get_runtime().run(user_input)`. The runtime builds and
   caches the graph on first use and submits the invocation to its single MLX worker
   thread.
2. **Supervise.** [`SupervisorAgent`](agents/supervisor.py) emits a routing decision:
   `primary_domain`, `execution_domains` (`software_dev`, `reverse_engineering`, or both),
   and optional `split_tasks`. IPSW/firmware keywords take a deterministic fast-path
   straight to reverse engineering; decisions are cached per input.
3. **Run branch(es).** Each domain subgraph retrieves RAG context, plans its steps, runs
   its agents, and can enter a **tool loop** (request → host execution → observation)
   until it has enough evidence or hits `max_tool_iterations`. Each branch writes to
   `state.branch_outputs[<domain>]`.
4. **Synthesize.** [`synthesize_orchestration_output`](synthesis/synthesizer.py) combines
   the branch outputs (and any cross-domain findings) into `state.final_output`.
5. **Return.** The runtime returns the final `AgentState`; `run_text()` returns just the
   sanitized `final_output` string.

`state.agent_chain` records every node that executed (for auditable runs).

---

## Core concepts

### `OrchestrationRuntime` - the one entry point

All MLX model loading and inference run on a **single dedicated thread** so model arrays
and the GPU stream stay on one consistent thread. The model and graph are built only on the
first request and then reused, so that first call is slow (it loads the model) and every
call after it is fast.

```python
from langgraph_orchestration.runtime import get_runtime

# Returns a full AgentState; the runtime builds + caches the graph on first use.
final_state = get_runtime().run("Implement a token-bucket rate limiter with unit tests")

print(final_state.selected_domain)   # e.g. "software_dev"
print(final_state.agent_chain)       # ordered list of nodes that ran
print(final_state.final_output)      # synthesized answer

# Or, if you just want the text:
text = get_runtime().run_text("Analyze this decompiled parser for memory-safety bugs")
```

> Prefer `get_runtime()` over calling `build_orchestration_graph()` and `graph.invoke()`
> yourself - the runtime guarantees the model is loaded on, and inference runs on, the
> correct thread. Direct graph invocation exists mainly for tests and benchmarks.

### `AgentState`

A single Pydantic model ([`schemas/state.py`](schemas/state.py)) is the contract between
every node. Notable groups of fields:

- **Routing** - `user_input`, `selected_domain`, `execution_domains`, `split_tasks`.
- **Tool loop** - `tool_policy`, `tool_requests`, `tool_results`, `tool_iteration`,
  `max_tool_iterations`, `requires_tool_confirmation`, `workspace_root`.
- **Software dev** - `dev_context`, `dev_task_plan`, `dev_iteration`,
  `max_dev_iterations`, `dev_test_passed`.
- **Reverse engineering** - `re_context`, `re_task_plan`, plus the `feature_analysis_*`
  and `feature_triage_index` fields that drive the firmware pipeline.
- **Outputs** - `intermediate_outputs` (per agent), `branch_outputs` (per domain),
  `final_output`, and `agent_chain` (audit trail).

### Supervisor routing

[`SupervisorAgent.invoke()`](agents/supervisor.py) returns a dict. It:
- short-circuits to `reverse_engineering` on IPSW/firmware keywords;
- otherwise asks the model for exactly one label (`SOFTWARE_DEV` /
  `REVERSE_ENGINEERING` / `BOTH`), with a strict parser + a model-based resolver fallback;
- for `BOTH`, derives `split_tasks` (deterministic "…then…" splits first, else an
  LLM split), so each branch receives a focused sub-prompt;
- caches decisions per input (bounded cache).

### Domain subgraphs

**Software development** ([`graphs/software_dev.py`](graphs/software_dev.py)) - an LLM
router picks an ordered subset of `["code_generation", "unit_testing",
"architectural_review"]`. Code generation and testing form a retry loop: if tests read as
failing, code is regenerated up to `max_dev_iterations`. Each stage can request tools
before continuing.

**Reverse engineering** ([`graphs/reverse_engineering.py`](graphs/reverse_engineering.py)) -
the firmware-diff pipeline: locate → download → extract → diff → select high-signal
components → **decompile in IDA and inject the real pseudocode into the report** (the model
writes prose only) → compile per-component reports → synthesize. Full stage-by-stage
detail, IDA setup, and artifact layout live in the [repository README](../README.md).

### The tool loop

Agents don't call tools directly; they emit structured [`ToolRequest`](tooling/tool.py)
objects that a host-side executor fulfills, returning [`ToolResult`](tooling/tool.py)s that
are fed back as observations. [`tooling/executor.py`](tooling/executor.py) provides a
`VSCodeToolExecutor` (software dev) and an `IDAToolExecutor` (reverse engineering);
`should_continue_tool_loop()` gates iteration against `ToolPolicy` (allow-lists, write
confirmation, `max_iterations`). Allowed tools per domain are defined in
[`prompts/shared.py`](prompts/shared.py).

---

## Extending the engine

### Add a new agent

1. Implement the agent in [`agents/`](agents/), inheriting `SyncBaseAgent`.
2. Add a factory method on [`MLXAgentFactory`](agents/mlx_factory.py) so it shares the
   loaded inference engine.
3. Register a node for it in the relevant subgraph and wire its edges.

```python
from langgraph_orchestration.agents.base import SyncBaseAgent

class MyAgent(SyncBaseAgent):
    def __init__(self, inference_engine):
        super().__init__(name="my_agent", description="What this agent does")
        self.inference_engine = inference_engine

    def invoke(self, user_input: str, context=None) -> str:
        prompt = self.inference_engine.build_prompt(user_input=user_input, context=context)
        return self.inference_engine.generate(prompt=prompt)
```

### Add a node to a subgraph

Each node is `def node(state: AgentState) -> AgentState`. Record outputs via
`StateManager.add_intermediate_output(...)`, append to `state.agent_chain`, then register
with `graph.add_node(...)` and connect it with `add_edge` / `add_conditional_edges`. Follow
the routing patterns already in [`graphs/software_dev.py`](graphs/software_dev.py).

### Swap the retriever (e.g. Qdrant)

Retrieval goes through `RAGConfigManager` ([`retrievers/config.py`](retrievers/config.py)),
which nodes call as `retrieve_software_dev_context(...)` /
`retrieve_reverse_engineering_context(...)`. Implement the
[`BaseRetriever`](retrievers/base.py) interface and wire it in there (nodes don't
construct retrievers directly).

### Swap the model / inference backend

Agents depend only on the `MLXInferenceEngine` interface
([`inference/inference_engine.py`](inference/inference_engine.py)) they receive from the
factory. Point [`MLXAgentFactory`](agents/mlx_factory.py) at a different model (or a
different engine) and the graph is unchanged.

---

## Design invariants 

- **One thread for MLX.** Never invoke the graph off the runtime's worker thread - model
  arrays and the GPU stream must stay on the thread the model was loaded on.
- **Supervisor returns a dict.** `orchestration.py` validates `execution_domains` and
  `primary_domain`, raising an error if either is missing or invalid.
- **`report.json`, not raw markdown.** The RE branch feeds the compact `report.json`
  (~11 KB) to the model, not the multi-tens-of-KB `ipsw diff` markdown, to avoid GPU OOM on
  local inference.
- **IDA writes are guaranteed.** The RE cleanup node always saves the `.i64` database
  before shutting IDA down, regardless of what the model did.
- **Recursion limit.** Long RE runs need a high LangGraph `recursion_limit`; the runtime
  defaults to `1000` (see `DEFAULT_RECURSION_LIMIT` in [`runtime.py`](runtime.py)).
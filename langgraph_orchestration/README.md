# `langgraph_orchestration` Package Internals

Internal architecture and extension points. For installation, usage, and the firmware analysis pipeline, see the [repository README](../README.md).

## Package layout

| Path | Responsibility |
|---|---|
| [`runtime.py`](runtime.py) | `OrchestrationRuntime`, shared by every interface |
| [`state.py`](state.py) | `AgentState`, passed through every graph node |
| [`graphs/`](graphs/) | Orchestration, software development, and reverse engineering graphs |
| [`agents.py`](agents.py) | Agent definitions, factory, and supervisor |
| [`inference.py`](inference.py) | MLX inference and model management |
| [`prompts.py`](prompts.py), [`prompts_md/`](prompts_md/) | Prompt rendering and templates |
| [`tooling/`](tooling/) | Tool parsing, execution, and IDA integration |
| [`triage.py`](triage.py) | Deterministic firmware triage |
| [`retrievers.py`](retrievers.py) | Optional Qdrant retrieval |
| [`core.py`](core.py) | State helpers and runtime utilities |
| [`gemini.py`](gemini.py) | Benchmark-only cloud backend |

## Core Invariants

The test suite enforces four invariants:

1. **All MLX work runs on the runtime thread.** `OrchestrationRuntime` owns a dedicated worker for model loading and generation because MLX expects model state to remain on the thread that created it.
2. **Graph nodes accept and return `AgentState`.** Nodes communicate only through shared state, making runs traceable and allowing automation to inject resolved firmware metadata directly.
3. **Model downloads stay in `inference.py`.** Downloading is a setup step invoked only from main(), never during request handling.
4. **Runtime code stays local-first.** Only `inference.py` and the benchmark-only `gemini.py` are allowed to use network libraries.

## `AgentState`

Shared Pydantic model passed between every node.

| Group | Fields |
|---|---|
| Routing | `user_input`, `selected_domain`, `execution_domains`, `split_tasks` |
| Tools | `tool_policy`, `tool_requests`, `tool_results`, `tool_iteration`, `max_tool_iterations`, `workspace_root` |
| Software dev | `dev_context`, `dev_task_plan`, `dev_iteration`, `max_dev_iterations`, `dev_test_passed` |
| Reverse engineering | `re_context`, `re_task_plan`, `feature_analysis_targets`, `feature_analysis_queue`, `feature_analysis_current`, `feature_analysis_reports`, `feature_triage_index` |
| Output | `intermediate_outputs`, `branch_outputs`, `final_output`, `agent_chain`, `analysis_notes` |

`agent_chain` records every node that executes. New nodes should append their name so execution traces remain complete.

Where available, update state through `StateManager` or helper methods such as `register_tool_request` and `register_tool_result`.

## Routing

The supervisor returns a routing decision containing `primary_domain`, `execution_domains`, and optional `split_tasks`. Invalid decisions raise immediately instead of falling back to a default.

Firmware requests are routed deterministically. Other requests are classified by the model.

When both domains are selected, the software development graph runs first, followed by reverse engineering. `final_synthesis` combines both outputs.

## Tool Execution

Agents emit `<tool_call>` blocks which are parsed into `ToolRequest` objects and executed by the host. 
Results are returned as `ToolResult` objects, and the graph continues until
`should_continue_tool_loop()` returns false or the iteration limit is reached.

The model never executes code directly. Available tools are selected per domain and injected into the prompt.

## Extending the engine

### Adding an agent

Add an entry to `AGENT_SPECS` in [`agents.py`](agents.py):

```python
"my_agent": AgentSpec(
    description="What this agent is expert at. Becomes part of its system prompt.",
    max_tokens=4096,
    temperature=0.3,
),
```

Then create it with `factory.create_agent()` and add a corresponding graph node.

### Adding a graph node

```python
def my_node(state: AgentState) -> AgentState:
    output = my_agent.invoke(user_input=prompt, context=state.dev_context)
    return StateManager.add_intermediate_output(
        state=state, agent_name="my_node", output=output
    )

graph.add_node("my_node", my_node)
```

If the agent uses tools, pair the node with `tool_executor_node` and route through `should_continue_tool_loop()`.

### Changing prompts

Prompt templates live in [`prompts_md/`](prompts_md/) and are rendered by `prompts.py`. 
Updating a template changes model behaviour without modifying code.

### Replacing Retrieval

Retrieval is isolated behind `retrieve_context()` in [`retrievers.py`](retrievers.py).
Replace the backend there without changing the graph.

### Replacing the inference backend

Agents depend only on the inference engine interface (`build_prompt`, `generate`). A different backend 
can be substituted in [`inference.py`](inference.py) as long as the runtime thread model is preserved.

## Debugging

| Variable | Effect |
|---|---|
| `RE_DEBUG` | Save feature-analysis prompts and model output |
| `RE_AUTODECOMP_DEBUG` | Trace automatic decompiler selection |
| `RE_ANNOT_DEBUG` | Trace IDA annotation generation |
| `LOG_LEVEL` | Configure logging verbosity |

Run `langgraph dev` from the repository root to inspect the compiled graph in LangGraph Studio. Leave 
`LANGSMITH_TRACING` disabled unless you specifically need tracing, as it sends execution metadata off the machine and will fail the offline compliance tests.
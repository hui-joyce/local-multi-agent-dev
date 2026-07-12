"""
Single entry point used by every interface (Gradio chat, FastAPI service,
and the CLI examples) so that a prompt behaves identically regardless of how
it is submitted. Each caller wraps the user's text in an AgentState and
runs it through the same supervisor-routed orchestration graph.
"""

from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.core.state_utils import StateManager
from langgraph_orchestration.graphs.orchestration import build_orchestration_graph
from langgraph_orchestration.schemas.state import AgentState

DEFAULT_RECURSION_LIMIT = 1000


class OrchestrationRuntime:
    def __init__(
        self,
        factory: Optional[MLXAgentFactory] = None,
        recursion_limit: int = DEFAULT_RECURSION_LIMIT,
    ):
        self._factory_arg = factory
        self._recursion_limit = recursion_limit
        self._factory: Optional[MLXAgentFactory] = None
        self._graph = None
        self._ready = False
        self._build_lock = threading.Lock()
        # all MLX work (load + inference) runs on this single thread so that
        # model arrays and the GPU stream stay on one consistent thread
        self._executor = ThreadPoolExecutor(
            max_workers=1, thread_name_prefix="mlx-inference"
        )

    @property
    def factory(self) -> MLXAgentFactory:
        self.ensure_ready()
        return self._factory  # type: ignore[return-value]

    @property
    def graph(self):
        return self.ensure_ready()

    def _build(self):
        factory = self._factory_arg or MLXAgentFactory()
        factory.ensure_loaded()
        self._graph = build_orchestration_graph(factory=factory)
        self._factory = factory
        self._ready = True

    def ensure_ready(self):
        if not self._ready:
            with self._build_lock:
                if not self._ready:
                    # Build on the dedicated thread so the model is loaded on
                    # the same thread that will run inference
                    self._executor.submit(self._build).result()
        return self._graph

    def _invoke(
        self,
        user_input: str,
        seed_intermediate: Optional[dict[str, str]],
        recursion_limit: Optional[int],
        config: Optional[dict],
    ) -> AgentState:
        state = AgentState(user_input=user_input)
        if seed_intermediate:
            state.intermediate_outputs.update(seed_intermediate)

        run_config: dict = {"recursion_limit": recursion_limit or self._recursion_limit}
        if config:
            run_config.update(config)

        raw_result = self._graph.invoke(state.model_dump(), config=run_config)
        return AgentState(**raw_result)

    def run(
        self,
        user_input: str,
        *,
        seed_intermediate: Optional[dict[str, str]] = None,
        recursion_limit: Optional[int] = None,
        config: Optional[dict] = None,
    ) -> AgentState:
        self.ensure_ready()
        future = self._executor.submit(
            self._invoke, user_input, seed_intermediate, recursion_limit, config
        )
        return future.result()

    def run_text(self, user_input: str, **kwargs) -> str:
        final_state = self.run(user_input, **kwargs)
        return StateManager.sanitize_output(final_state.final_output or "")


_default_runtime: Optional[OrchestrationRuntime] = None
_default_lock = threading.Lock()


def get_runtime() -> OrchestrationRuntime:
    global _default_runtime
    if _default_runtime is None:
        with _default_lock:
            if _default_runtime is None:
                _default_runtime = OrchestrationRuntime()
    return _default_runtime
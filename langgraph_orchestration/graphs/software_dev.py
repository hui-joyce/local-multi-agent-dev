"""
Software development domain graph.
Defines the subgraph for code generation, testing, and architectural review
within the software development domain.
"""

import json
import re

from langgraph.graph import END, StateGraph

from langgraph_orchestration.agents import MLXAgentFactory
from langgraph_orchestration.core import StateManager
from langgraph_orchestration.inference import GenerationConfig
from langgraph_orchestration.prompts import (
    ROUTER_SYSTEM_PROMPT,
    SOFTWARE_DEV_TASKS,
    build_architectural_review_prompt,
    build_code_generation_prompt,
    build_dev_task_router_prompt,
    build_unit_testing_prompt,
    get_allowed_tools,
)
from langgraph_orchestration.retrievers import retrieve_context
from langgraph_orchestration.state import AgentState
from langgraph_orchestration.tooling.executor import (
    should_continue_tool_loop,
    tool_executor_node,
)


def build_software_dev_graph(factory: MLXAgentFactory = None):
    """
    Args:
        factory: MLXAgentFactory instance. If None, creates a new one.
    """
    if factory is None or isinstance(factory, dict):
        factory = MLXAgentFactory()

    code_gen_agent = factory.create_agent("code_generation")
    test_agent = factory.create_agent("unit_testing")
    arch_agent = factory.create_agent("architectural_review")
    inference_engine = factory.ensure_loaded()

    graph = StateGraph(AgentState)

    def _extract_json_block(raw_output: str) -> str:
        cleaned = raw_output.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()
        return cleaned

    def _select_dev_task_plan(user_input: str) -> list[str]:
        if inference_engine is None:
            return ["code_generation"]

        prompt = inference_engine.build_prompt(
            user_input=build_dev_task_router_prompt(user_input),
            context=None,
            system_prompt=ROUTER_SYSTEM_PROMPT,
        )

        try:
            raw = inference_engine.generate(
                prompt=prompt,
                config=GenerationConfig(max_tokens=120, temperature=0.0),
                stream=False,
            )
            parsed = json.loads(_extract_json_block(raw))
            selected = parsed.get("steps", [])
            if not isinstance(selected, list):
                selected = []
        except Exception:
            selected = []

        normalized = [step for step in SOFTWARE_DEV_TASKS if step in selected]
        if not normalized:
            return ["code_generation"]
        return normalized

    def _next_step_from_plan(plan: list[str], current_step: str) -> str:
        if current_step not in plan:
            return "synthesize"
        idx = plan.index(current_step)
        if idx + 1 >= len(plan):
            return "synthesize"
        return plan[idx + 1]

    def retrieve_dev_context_node(state: AgentState) -> AgentState:
        # Retrieval is optional. Missing Qdrant or embedding models return []
        context = retrieve_context(state.user_input, domain="software_dev")
        state.dev_context = context
        state.dev_task_plan = _select_dev_task_plan(state.user_input)
        state.tool_policy.allowed_tools = get_allowed_tools("software_dev")
        state.max_tool_iterations = state.tool_policy.max_iterations
        return StateManager.add_retrieved_context(state, context)

    def _tool_observation_block(state: AgentState) -> str:
        if not state.tool_results:
            return ""
        recent = state.tool_results[-2:]
        lines = ["Tool observations from prior step(s):"]
        for result in recent:
            if result.success:
                excerpt = (result.output or "")[:1200]
                lines.append(f"- {result.tool_name}: {excerpt}")
            else:
                lines.append(f"- {result.tool_name} failed: {result.error}")
        lines.append(
            "Use this evidence directly. Do not re-request the same tool unless data is missing."
        )
        return "\n".join(lines)

    def _augment_prompt_with_tools(prompt: str, state: AgentState) -> str:
        observation = _tool_observation_block(state)
        if not observation:
            return prompt
        return f"{prompt}\n\n{observation}"

    def _files_written(state: AgentState) -> list[str]:
        """Paths successfully written this run (proof codegen produced files, not prose)"""
        return [
            (result.metadata or {}).get("path") or result.output
            for result in state.tool_results
            if result.success and result.tool_name in ("create_file", "edit_file")
        ]

    # define node functions
    def code_generation_node(state: AgentState) -> AgentState:
        state.dev_iteration += 1
        prompt = build_code_generation_prompt(
            user_input=state.user_input,
            attempt=state.dev_iteration,
        )
        if state.dev_iteration > 1 and not _files_written(state):
            prompt += (
                "\n\nPREVIOUS ATTEMPT WROTE NO FILES. You described code in prose but emitted "
                "no create_file tool call. You MUST now emit a <tool_call> with create_file for "
                "every file, each containing the complete, runnable file contents."
            )
        output = code_gen_agent.invoke(
            user_input=_augment_prompt_with_tools(prompt, state),
            context=state.dev_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="code_generation",
            output=output,
        )

    def _tests_passed(test_output: str) -> bool:
        output_lower = test_output.lower()
        fail_markers = ["fail", "failed", "error", "exception", "not pass", "did not pass"]
        pass_markers = ["pass", "passed", "all tests green", "success"]
        has_fail = any(marker in output_lower for marker in fail_markers)
        has_pass = any(marker in output_lower for marker in pass_markers)
        if has_fail and not has_pass:
            return False
        if has_pass and not has_fail:
            return True
        return not has_fail

    def unit_testing_node(state: AgentState) -> AgentState:
        code_target = state.intermediate_outputs.get("code_generation") or state.user_input
        prompt = build_unit_testing_prompt(code_target)
        output = test_agent.invoke(
            user_input=_augment_prompt_with_tools(prompt, state),
            context=state.dev_context,
        )
        state.dev_test_passed = _tests_passed(output)
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="unit_testing",
            output=output,
        )

    def architectural_review_node(state: AgentState) -> AgentState:
        prompt = build_architectural_review_prompt(
            user_request=state.user_input,
            combined_outputs=StateManager.format_agent_outputs(state),
        )
        output = arch_agent.invoke(
            user_input=_augment_prompt_with_tools(prompt, state),
            context=state.dev_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="architectural_review",
            output=output,
        )

    def route_after_testing(state: AgentState) -> str:
        if state.dev_test_passed:
            return _next_step_from_plan(state.dev_task_plan, "unit_testing")
        if state.dev_iteration < state.max_dev_iterations:
            if "code_generation" in state.dev_task_plan:
                return "code_generation"
        return _next_step_from_plan(state.dev_task_plan, "unit_testing")

    def route_after_retrieve(state: AgentState) -> str:
        if not state.dev_task_plan:
            return "synthesize"
        return state.dev_task_plan[0]

    def route_after_codegen_tools(state: AgentState) -> str:
        if should_continue_tool_loop(state):
            return "code_generation"
        # A dev request is only "done" once files actually land on disk. If codegen
        # produced only prose, retry (bounded by max_dev_iterations) before moving on
        if (
            "code_generation" in state.dev_task_plan
            and not _files_written(state)
            and state.dev_iteration < state.max_dev_iterations
        ):
            return "code_generation"
        return _next_step_from_plan(state.dev_task_plan, "code_generation")

    def route_after_testing_tools(state: AgentState) -> str:
        if should_continue_tool_loop(state):
            return "unit_testing"
        return route_after_testing(state)

    def route_after_arch_tools(state: AgentState) -> str:
        if should_continue_tool_loop(state):
            return "architectural_review"
        return "synthesize"

    def synthesize_output(state: AgentState) -> AgentState:
        files = sorted(set(_files_written(state)))
        if "code_generation" not in state.dev_task_plan:
            file_status = "No code generation requested."
        elif files:
            file_status = "Files written: " + ", ".join(files)
        else:
            file_status = "WARNING: no files were written to the repository."
        final = (
            "### Generated Solutions\n"
            f"{StateManager.format_agent_outputs(state)}\n\n"
            "### Summary\n"
            f"- Development workflow completed in {state.dev_iteration} attempt(s).\n"
            f"- Latest test status: {'PASS' if state.dev_test_passed else 'N/A'}.\n"
            f"- {file_status}\n"
        )
        state.branch_outputs["software_dev"] = StateManager.sanitize_output(final)
        state.agent_chain.append("software_dev_synthesize")
        return state

    graph.add_node("retrieve_dev_context", retrieve_dev_context_node)
    graph.add_node("code_generation", code_generation_node)
    graph.add_node("code_generation_tools", tool_executor_node)
    graph.add_node("unit_testing", unit_testing_node)
    graph.add_node("unit_testing_tools", tool_executor_node)
    graph.add_node("architectural_review", architectural_review_node)
    graph.add_node("architectural_review_tools", tool_executor_node)
    graph.add_node("synthesize", synthesize_output)

    graph.add_conditional_edges(
        "retrieve_dev_context",
        route_after_retrieve,
        {
            "code_generation": "code_generation",
            "unit_testing": "unit_testing",
            "architectural_review": "architectural_review",
            "synthesize": "synthesize",
        },
    )
    graph.add_edge("code_generation", "code_generation_tools")
    graph.add_conditional_edges(
        "code_generation_tools",
        route_after_codegen_tools,
        {
            "code_generation": "code_generation",
            "unit_testing": "unit_testing",
            "architectural_review": "architectural_review",
            "synthesize": "synthesize",
        },
    )
    graph.add_edge("unit_testing", "unit_testing_tools")
    graph.add_conditional_edges(
        "unit_testing_tools",
        route_after_testing_tools,
        {
            "code_generation": "code_generation",
            "architectural_review": "architectural_review",
            "synthesize": "synthesize",
            "unit_testing": "unit_testing",
        },
    )
    graph.add_edge("architectural_review", "architectural_review_tools")
    graph.add_conditional_edges(
        "architectural_review_tools",
        route_after_arch_tools,
        {
            "architectural_review": "architectural_review",
            "synthesize": "synthesize",
        },
    )
    graph.add_edge("synthesize", END)

    graph.set_entry_point("retrieve_dev_context")

    compiled = graph.compile()
    compiled.name = "Software Development"
    compiled.description = "Code generation, testing, and architectural review workflow"
    return compiled

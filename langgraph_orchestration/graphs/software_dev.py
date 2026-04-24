"""
Software development domain graph.
Defines the subgraph for code generation, testing, and architectural review
within the software development domain.
"""

import json
import re

from langgraph.graph import StateGraph, END
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.inference.inference_engine import GenerationConfig
from langgraph_orchestration.retrievers.qdrant_client import QdrantRetriever
from langgraph_orchestration.core.state_utils import StateManager


def build_software_dev_graph(factory: MLXAgentFactory = None):
    """
    Args:
        factory: MLXAgentFactory instance. If None, creates a new one.
    """
    if factory is None or isinstance(factory, dict):
        factory = MLXAgentFactory()
    
    # Initialize agents using factory
    code_gen_agent = factory.create_code_generation_agent()
    test_agent = factory.create_unit_testing_agent()
    arch_agent = factory.create_architectural_review_agent()
    inference_engine = factory.inference_engine
    retriever = QdrantRetriever()
    
    # Create graph
    graph = StateGraph(AgentState)

    def _extract_json_block(raw_output: str) -> str:
        cleaned = raw_output.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()
        return cleaned

    def _select_dev_task_plan(user_input: str) -> list[str]:
        allowed = ["code_generation", "unit_testing", "architectural_review"]
        if inference_engine is None:
            return ["code_generation"]

        prompt = inference_engine.build_prompt(
            user_input=(
                "Select only the required software development tasks for this request.\n"
                f"Request: {user_input}\n\n"
                "Allowed tasks:\n"
                "- code_generation\n"
                "- unit_testing\n"
                "- architectural_review\n\n"
                "Return strict JSON only: {\"steps\": [\"...\"]}.\n"
                "Only include necessary tasks."
            ),
            context=None,
            system_prompt="You are a precise task router. Return JSON only.",
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

        normalized = [step for step in allowed if step in selected]
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
        context = retriever.retrieve(
            query=state.user_input,
            top_k=5,
            domain="software_dev",
        )
        state.dev_context = context
        state.dev_task_plan = _select_dev_task_plan(state.user_input)
        return StateManager.add_retrieved_context(state, context)
    
    # Define node functions
    def code_generation_node(state: AgentState) -> AgentState:
        state.dev_iteration += 1
        output = code_gen_agent.invoke(
            user_input=f"{state.user_input}\n\nGeneration attempt: {state.dev_iteration}",
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
        test_input = f"Code or component to test:\n{code_target}"
        output = test_agent.invoke(
            user_input=test_input,
            context=state.dev_context,
        )
        state.dev_test_passed = _tests_passed(output)
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="unit_testing",
            output=output,
        )
    
    def architectural_review_node(state: AgentState) -> AgentState:
        review_input = f"Code and tests generated:\n{StateManager.format_agent_outputs(state)}"
        output = arch_agent.invoke(
            user_input=review_input,
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

    def route_after_codegen(state: AgentState) -> str:
        return _next_step_from_plan(state.dev_task_plan, "code_generation")
    
    def synthesize_output(state: AgentState) -> AgentState:
        final = f"""# Software Development Analysis

## User Request
{state.user_input}

## Generated Solutions
{StateManager.format_agent_outputs(state)}

## Summary
Development workflow completed in {state.dev_iteration} attempt(s).
Latest test status: {'PASS' if state.dev_test_passed else 'N/A'}.
"""
        state.branch_outputs["software_dev"] = final
        state.agent_chain.append("software_dev_synthesize")
        return state
    
    # Add nodes
    graph.add_node("retrieve_dev_context", retrieve_dev_context_node)
    graph.add_node("code_generation", code_generation_node)
    graph.add_node("unit_testing", unit_testing_node)
    graph.add_node("architectural_review", architectural_review_node)
    graph.add_node("synthesize", synthesize_output)
    
    # Add edges
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
    graph.add_conditional_edges(
        "code_generation",
        route_after_codegen,
        {
            "unit_testing": "unit_testing",
            "architectural_review": "architectural_review",
            "synthesize": "synthesize",
        },
    )
    graph.add_conditional_edges(
        "unit_testing",
        route_after_testing,
        {
            "code_generation": "code_generation",
            "architectural_review": "architectural_review",
            "synthesize": "synthesize",
        },
    )
    graph.add_edge("architectural_review", "synthesize")
    graph.add_edge("synthesize", END)
    
    # Set entry point
    graph.set_entry_point("retrieve_dev_context")
    
    compiled = graph.compile()
    compiled.name = "Software Development"
    compiled.description = "Code generation, testing, and architectural review workflow"
    return compiled
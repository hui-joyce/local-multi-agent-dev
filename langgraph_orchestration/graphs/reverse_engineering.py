"""
Reverse engineering domain graph.
Defines the subgraph for planning, code analysis, and vulnerability detection
within the reverse engineering domain.
"""

import json
import re

from langgraph.graph import StateGraph, END
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.inference.inference_engine import GenerationConfig
from langgraph_orchestration.retrievers.config import RAGConfigManager
from langgraph_orchestration.core.state_utils import StateManager
from langgraph_orchestration.tooling.prompts import get_allowed_tools
from langgraph_orchestration.tooling.tool_executor_node import (
    should_continue_tool_loop,
    tool_executor_node,
)
from langgraph_orchestration.prompts.reverse_engineering import (
    REVERSE_ENGINEERING_TASKS,
    ROUTER_SYSTEM_PROMPT,
    build_re_task_router_prompt,
    build_planning_prompt,
    build_code_analysis_prompt,
    build_vulnerability_detection_prompt,
)


def build_reverse_engineering_graph(factory: MLXAgentFactory = None):
    """
    Args:
        factory: MLXAgentFactory instance. If None, creates a new one.
    """
    if factory is None or isinstance(factory, dict):
        factory = MLXAgentFactory()
    
    # Initialize agents using factory
    planning_agent = factory.create_planning_agent()
    analysis_agent = factory.create_code_analysis_agent()
    vuln_agent = factory.create_vulnerability_detection_agent()
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

    def _select_re_task_plan(user_input: str) -> list[str]:
        if inference_engine is None:
            return ["code_analysis"]

        prompt = inference_engine.build_prompt(
            user_input=build_re_task_router_prompt(user_input),
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

        normalized = [step for step in REVERSE_ENGINEERING_TASKS if step in selected]
        if not normalized:
            return ["code_analysis"]
        return normalized

    def _next_step_from_plan(plan: list[str], current_step: str) -> str:
        if current_step not in plan:
            return "synthesize"
        idx = plan.index(current_step)
        if idx + 1 >= len(plan):
            return "synthesize"
        return plan[idx + 1]

    def retrieve_re_context_node(state: AgentState) -> AgentState:
        RAGConfigManager.initialize()
        rag_manager = RAGConfigManager.get_rag_manager()
        config = RAGConfigManager.get_config()
        context = rag_manager.retrieve_reverse_engineering_context(
            query=state.user_input,
            top_k=config.default_top_k,
        )
        state.re_context = context
        
        # Skip planning when analyzing generated code from software_dev
        software_dev_output = state.branch_outputs.get("software_dev", "")
        if software_dev_output:
            state.re_task_plan = ["vulnerability_detection"]
        else:
            state.re_task_plan = _select_re_task_plan(state.user_input)

        state.tool_policy.allowed_tools = get_allowed_tools("reverse_engineering")
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
        lines.append("Use this evidence directly. Do not re-request the same tool unless data is missing.")
        return "\n".join(lines)

    def _augment_prompt_with_tools(prompt: str, state: AgentState) -> str:
        observation = _tool_observation_block(state)
        if not observation:
            return prompt
        return f"{prompt}\n\n{observation}"
    
    # Define node functions
    def planning_node(state: AgentState) -> AgentState:
        prompt = build_planning_prompt(state.user_input)
        plan = planning_agent.invoke(
            user_input=_augment_prompt_with_tools(prompt, state),
            context=state.re_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="planning",
            output=plan,
        )
    
    def code_analysis_node(state: AgentState) -> AgentState:
        planning_output = state.intermediate_outputs.get("planning", "")
        generated_code = state.branch_outputs.get("software_dev", "")
        prompt = build_code_analysis_prompt(
            user_input=state.user_input,
            planning_output=planning_output,
            generated_code=generated_code,
        )
        output = analysis_agent.invoke(
            user_input=_augment_prompt_with_tools(prompt, state),
            context=state.re_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="code_analysis",
            output=output,
        )
    
    def vulnerability_detection_node(state: AgentState) -> AgentState:
        analysis_output = state.intermediate_outputs.get("code_analysis", "")
        prompt = build_vulnerability_detection_prompt(
            user_input=state.user_input,
            analysis_output=analysis_output,
        )
        output = vuln_agent.invoke(
            user_input=_augment_prompt_with_tools(prompt, state),
            context=state.re_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="vulnerability_detection",
            output=output,
        )
    
    def synthesize_output(state: AgentState) -> AgentState:
        final = f"""# Reverse Engineering Analysis Report

## User Request
{state.user_input}

## Analysis Execution
{StateManager.format_agent_outputs(state)}

## Conclusion
Comprehensive reverse engineering analysis completed with planning,
structural analysis, and vulnerability assessment. All findings documented
with remediation recommendations where applicable.
"""
        state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(final)
        state.agent_chain.append("reverse_engineering_synthesize")
        return state

    def route_after_retrieve(state: AgentState) -> str:
        if not state.re_task_plan:
            return "synthesize"
        return state.re_task_plan[0]

    def route_after_planning(state: AgentState) -> str:
        return _next_step_from_plan(state.re_task_plan, "planning")

    def route_after_analysis(state: AgentState) -> str:
        return _next_step_from_plan(state.re_task_plan, "code_analysis")

    def route_after_planning_tools(state: AgentState) -> str:
        if should_continue_tool_loop(state):
            return "planning"
        return route_after_planning(state)

    def route_after_analysis_tools(state: AgentState) -> str:
        if should_continue_tool_loop(state):
            return "code_analysis"
        return route_after_analysis(state)

    def route_after_vuln_tools(state: AgentState) -> str:
        if should_continue_tool_loop(state):
            return "vulnerability_detection"
        return "synthesize"
    
    # Add nodes
    graph.add_node("retrieve_re_context", retrieve_re_context_node)
    graph.add_node("planning", planning_node)
    graph.add_node("planning_tools", tool_executor_node)
    graph.add_node("code_analysis", code_analysis_node)
    graph.add_node("code_analysis_tools", tool_executor_node)
    graph.add_node("vulnerability_detection", vulnerability_detection_node)
    graph.add_node("vulnerability_detection_tools", tool_executor_node)
    graph.add_node("synthesize", synthesize_output)
    
    # Add edges
    graph.add_conditional_edges(
        "retrieve_re_context",
        route_after_retrieve,
        {
            "planning": "planning",
            "code_analysis": "code_analysis",
            "vulnerability_detection": "vulnerability_detection",
            "synthesize": "synthesize",
        },
    )
    graph.add_edge("planning", "planning_tools")
    graph.add_conditional_edges(
        "planning_tools",
        route_after_planning_tools,
        {
            "planning": "planning",
            "code_analysis": "code_analysis",
            "vulnerability_detection": "vulnerability_detection",
            "synthesize": "synthesize",
        },
    )
    graph.add_edge("code_analysis", "code_analysis_tools")
    graph.add_conditional_edges(
        "code_analysis_tools",
        route_after_analysis_tools,
        {
            "code_analysis": "code_analysis",
            "vulnerability_detection": "vulnerability_detection",
            "synthesize": "synthesize",
        },
    )
    graph.add_edge("vulnerability_detection", "vulnerability_detection_tools")
    graph.add_conditional_edges(
        "vulnerability_detection_tools",
        route_after_vuln_tools,
        {
            "vulnerability_detection": "vulnerability_detection",
            "synthesize": "synthesize",
        },
    )
    graph.add_edge("synthesize", END)
    
    graph.set_entry_point("retrieve_re_context")
    
    compiled = graph.compile()
    compiled.name = "Reverse Engineering"
    compiled.description = "Planning, code analysis, and vulnerability detection workflow"
    return compiled
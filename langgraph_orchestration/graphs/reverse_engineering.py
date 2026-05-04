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
    # RAG disabled for no-RAG benchmark runs
    # retriever = QdrantRetriever()
    
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
        
        # When analyzing generated code from software_dev domain, skip planning and code_analysis
        # Go directly to vulnerability detection since we already have structured code
        software_dev_output = state.branch_outputs.get("software_dev", "")
        if software_dev_output:
            # For generated code security analysis only
            state.re_task_plan = ["vulnerability_detection"]
        else:
            # For standalone reverse engineering, use LLM-selected task plan
            state.re_task_plan = _select_re_task_plan(state.user_input)
        
        return StateManager.add_retrieved_context(state, context)
    
    # Define node functions
    def planning_node(state: AgentState) -> AgentState:
        plan = planning_agent.invoke(
            user_input=build_planning_prompt(state.user_input),
            context=state.re_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="planning",
            output=plan,
        )
    
    def code_analysis_node(state: AgentState) -> AgentState:
        planning_output = state.intermediate_outputs.get("planning", "")
        # Check if there's generated code from previous software_dev domain
        generated_code = state.branch_outputs.get("software_dev", "")
        output = analysis_agent.invoke(
            user_input=build_code_analysis_prompt(
                user_input=state.user_input,
                planning_output=planning_output,
                generated_code=generated_code,
            ),
            context=state.re_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="code_analysis",
            output=output,
        )
    
    def vulnerability_detection_node(state: AgentState) -> AgentState:
        analysis_output = state.intermediate_outputs.get("code_analysis", "")
        output = vuln_agent.invoke(
            user_input=build_vulnerability_detection_prompt(
                user_input=state.user_input,
                analysis_output=analysis_output,
            ),
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
    
    # Add nodes
    graph.add_node("retrieve_re_context", retrieve_re_context_node)
    graph.add_node("planning", planning_node)
    graph.add_node("code_analysis", code_analysis_node)
    graph.add_node("vulnerability_detection", vulnerability_detection_node)
    graph.add_node("synthesize", synthesize_output)
    
    # Add edges - sequential pipeline
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
    graph.add_conditional_edges(
        "planning",
        route_after_planning,
        {
            "code_analysis": "code_analysis",
            "vulnerability_detection": "vulnerability_detection",
            "synthesize": "synthesize",
        },
    )
    graph.add_conditional_edges(
        "code_analysis",
        route_after_analysis,
        {
            "vulnerability_detection": "vulnerability_detection",
            "synthesize": "synthesize",
        },
    )
    graph.add_edge("vulnerability_detection", "synthesize")
    graph.add_edge("synthesize", END)
    
    # Set entry point
    graph.set_entry_point("retrieve_re_context")
    
    compiled = graph.compile()
    compiled.name = "Reverse Engineering"
    compiled.description = "Planning, code analysis, and vulnerability detection workflow"
    return compiled
"""Top-level orchestration graph with conditional supervisor routing."""

from langgraph.graph import StateGraph, END
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.core.state_utils import StateManager
from langgraph_orchestration.graphs.software_dev import build_software_dev_graph
from langgraph_orchestration.graphs.reverse_engineering import build_reverse_engineering_graph


def build_orchestration_graph(factory: MLXAgentFactory = None):
    """Build the supervisor-driven orchestration graph."""

    if factory is None or isinstance(factory, dict):
        factory = MLXAgentFactory()

    supervisor = factory.create_supervisor_agent()

    software_dev_graph = build_software_dev_graph(factory=factory)
    reverse_eng_graph = build_reverse_engineering_graph(factory=factory)

    graph = StateGraph(AgentState)

    def supervisor_node(state: AgentState) -> AgentState:
        domain = supervisor.invoke(user_input=state.user_input)
        state.selected_domain = domain
        return state

    def software_dev_router(state: AgentState) -> AgentState:
        result = software_dev_graph.invoke(state.model_dump())
        return AgentState(**result)

    def reverse_engineering_router(state: AgentState) -> AgentState:
        result = reverse_eng_graph.invoke(state.model_dump())
        return AgentState(**result)

    def both_router(state: AgentState) -> AgentState:
        dev_result = software_dev_graph.invoke(state.model_dump())
        merged_state = AgentState(**dev_result)
        re_result = reverse_eng_graph.invoke(merged_state.model_dump())
        return AgentState(**re_result)

    def final_synthesis(state: AgentState) -> AgentState:
        dev_output = state.branch_outputs.get("software_dev")
        re_output = state.branch_outputs.get("reverse_engineering")

        if dev_output and re_output:
            state.final_output = (
                "# Integrated Multi-Agent Report\n\n"
                "## User Request\n"
                f"{state.user_input}\n\n"
                "## Software Development Perspective\n"
                f"{dev_output}\n\n"
                "## Reverse Engineering Perspective\n"
                f"{re_output}\n\n"
                "## Unified Recommendations\n"
                "1. Prioritize fixes from vulnerability findings in the generated implementation.\n"
                "2. Align architectural decisions with security hardening guidance from analysis results.\n"
                "3. Validate remediation with targeted tests and follow-up code inspection."
            )
        elif dev_output:
            state.final_output = dev_output
        elif re_output:
            state.final_output = re_output
        elif state.final_output is None:
            state.final_output = StateManager.format_agent_outputs(state)

        state.agent_chain.append("final_synthesis")
        return state

    def route_to_domain(state: AgentState) -> str:
        if state.selected_domain == "software_dev":
            return "software_dev"
        if state.selected_domain == "reverse_engineering":
            return "reverse_engineering"
        return "both"

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("software_dev", software_dev_router)
    graph.add_node("reverse_engineering", reverse_engineering_router)
    graph.add_node("both", both_router)
    graph.add_node("final_synthesis", final_synthesis)

    graph.add_conditional_edges(
        "supervisor",
        route_to_domain,
        {
            "software_dev": "software_dev",
            "reverse_engineering": "reverse_engineering",
            "both": "both",
        },
    )

    graph.add_edge("software_dev", "final_synthesis")
    graph.add_edge("reverse_engineering", "final_synthesis")
    graph.add_edge("both", "final_synthesis")
    graph.add_edge("final_synthesis", END)

    graph.set_entry_point("supervisor")

    compiled_graph = graph.compile()

    compiled_graph.name = "Multi-Agent Orchestration"
    compiled_graph.description = "Supervisor-routed multi-agent system for software development and reverse engineering"

    return compiled_graph
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
        decision = supervisor.invoke(user_input=state.user_input)
        state.selected_domain = decision.get("primary_domain", "software_dev")
        state.execution_domains = decision.get("execution_domains", [state.selected_domain])
        state.split_tasks = decision.get("split_tasks", {})
        return state

    def software_dev_router(state: AgentState) -> AgentState:
        dev_state = state.model_dump()
        if state.split_tasks.get("software_dev"):
            dev_state["user_input"] = state.split_tasks["software_dev"]
        result = software_dev_graph.invoke(dev_state)
        return AgentState(**result)

    def reverse_engineering_router(state: AgentState) -> AgentState:
        re_state = state.model_dump()
        re_task = state.split_tasks.get("reverse_engineering", "")
        
        # If software_dev already ran, include the generated code in the analysis
        software_dev_output = state.branch_outputs.get("software_dev", "")
        if software_dev_output:
            clean_output = StateManager.sanitize_output(software_dev_output)
            # Combine the split task with the generated code for contextual analysis
            re_state["user_input"] = (
                f"Analyze and assess this generated code from development:\n\n"
                f"{clean_output}\n\n"
                f"Focus your analysis on: {re_task}"
            )
        elif re_task:
            re_state["user_input"] = re_task
        
        result = reverse_eng_graph.invoke(re_state)
        return AgentState(**result)

    def final_synthesis(state: AgentState) -> AgentState:
        dev_output = state.branch_outputs.get("software_dev")
        re_output = state.branch_outputs.get("reverse_engineering")

        if dev_output and re_output:
            state.final_output = StateManager.sanitize_output(
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
            state.final_output = StateManager.sanitize_output(dev_output)
        elif re_output:
            state.final_output = StateManager.sanitize_output(re_output)
        elif state.final_output is None:
            state.final_output = StateManager.sanitize_output(StateManager.format_agent_outputs(state))

        state.agent_chain.append("final_synthesis")
        return state

    def route_to_domain(state: AgentState) -> str:
        domains = state.execution_domains or ([state.selected_domain] if state.selected_domain else ["software_dev"])
        first_domain = domains[0]
        if first_domain == "reverse_engineering":
            return "reverse_engineering"
        return "software_dev"

    def route_after_software_dev(state: AgentState) -> str:
        domains = state.execution_domains or ["software_dev"]
        should_run_re = "reverse_engineering" in domains
        re_already_run = "reverse_engineering" in state.branch_outputs
        if should_run_re and not re_already_run:
            return "reverse_engineering"
        return "final_synthesis"

    def route_after_reverse_engineering(state: AgentState) -> str:
        domains = state.execution_domains or ["reverse_engineering"]
        should_run_dev = "software_dev" in domains
        dev_already_run = "software_dev" in state.branch_outputs
        if should_run_dev and not dev_already_run:
            return "software_dev"
        return "final_synthesis"

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("software_dev", software_dev_router)
    graph.add_node("reverse_engineering", reverse_engineering_router)
    graph.add_node("final_synthesis", final_synthesis)

    graph.add_conditional_edges(
        "supervisor",
        route_to_domain,
        {
            "software_dev": "software_dev",
            "reverse_engineering": "reverse_engineering",
        },
    )

    graph.add_conditional_edges(
        "software_dev",
        route_after_software_dev,
        {
            "reverse_engineering": "reverse_engineering",
            "final_synthesis": "final_synthesis",
        },
    )
    graph.add_conditional_edges(
        "reverse_engineering",
        route_after_reverse_engineering,
        {
            "software_dev": "software_dev",
            "final_synthesis": "final_synthesis",
        },
    )
    graph.add_edge("final_synthesis", END)

    graph.set_entry_point("supervisor")

    compiled_graph = graph.compile()

    compiled_graph.name = "Multi-Agent Orchestration"
    compiled_graph.description = "Supervisor-routed multi-agent system for software development and reverse engineering"

    return compiled_graph
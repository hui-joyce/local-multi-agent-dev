"""Top-level orchestration graph with conditional supervisor routing."""

from langgraph.graph import StateGraph, END
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.core.state_utils import StateManager
from langgraph_orchestration.graphs.reverse_engineering import build_reverse_engineering_graph
from langgraph_orchestration.graphs.software_dev import build_software_dev_graph
from langgraph_orchestration.synthesis.synthesizer import synthesize_orchestration_output

def build_orchestration_graph(factory: MLXAgentFactory = None):
    """
    Build the supervisor-driven orchestration graph.
    
    Routes user requests to one or both domain-specific subgraphs:
    - software_dev: Code generation, testing, architecture review
    - reverse_engineering: Firmware analysis, binary diff, symbol analysis
    """

    if factory is None or isinstance(factory, dict):
        factory = MLXAgentFactory()

    supervisor = factory.create_supervisor_agent()

    dev_graph = build_software_dev_graph(factory=factory)
    re_graph = build_reverse_engineering_graph(factory=factory)

    graph = StateGraph(AgentState)

    def supervisor_node(state: AgentState) -> AgentState:
        decision = supervisor.invoke(user_input=state.user_input)
        
        if not isinstance(decision, dict):
            raise ValueError(f"Supervisor must return a dict, got {type(decision)}: {decision}")
        
        execution_domains = decision.get("execution_domains")
        if not execution_domains:
            raise ValueError(f"Supervisor decision missing execution_domains: {decision}")
        
        primary_domain = decision.get("primary_domain")
        if not primary_domain:
            raise ValueError(f"Supervisor decision missing primary_domain: {decision}")
        
        split_tasks = decision.get("split_tasks", {})
        
        valid_domains = {"software_dev", "reverse_engineering"}
        execution_domains = [d for d in execution_domains if d in valid_domains]
        
        if not execution_domains:
            raise ValueError(f"Supervisor decision has no valid domains. Got: {decision.get('execution_domains')}")
        if primary_domain not in valid_domains:
            raise ValueError(f"Supervisor decision has invalid primary_domain: {primary_domain}")
        
        state.execution_domains = execution_domains
        state.selected_domain = primary_domain
        state.split_tasks = split_tasks
        state.agent_chain.append("supervisor")
        
        return state

    def software_dev_router(state: AgentState) -> AgentState:
        dev_state = state.model_dump()
        dev_task = state.split_tasks.get("software_dev", "")
        if dev_task:
            dev_state["user_input"] = dev_task
        
        result = dev_graph.invoke(dev_state)
        updated = AgentState(**result)
        
        updated.execution_domains = state.execution_domains
        updated.selected_domain = state.selected_domain
        
        return updated

    def reverse_engineering_router(state: AgentState) -> AgentState:
        re_state = state.model_dump()
        re_task = state.split_tasks.get("reverse_engineering", "")
        if re_task:
            re_state["user_input"] = re_task
        
        result = re_graph.invoke(re_state)
        updated = AgentState(**result)
        
        updated.execution_domains = state.execution_domains
        updated.selected_domain = state.selected_domain
        
        return updated

    def final_synthesis(state: AgentState) -> AgentState:
        state.final_output = synthesize_orchestration_output(state)
        state.agent_chain.append("final_synthesis")
        return state

    def route_after_supervisor(state: AgentState) -> str:
        if "software_dev" in state.execution_domains and "reverse_engineering" in state.execution_domains:
            return "software_dev_and_re"
        elif "software_dev" in state.execution_domains:
            return "software_dev"
        else:
            return "reverse_engineering"

    def route_to_synthesis(state: AgentState) -> str:
        return "final_synthesis"

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("software_dev", software_dev_router)
    graph.add_node("reverse_engineering", reverse_engineering_router)
    graph.add_node("final_synthesis", final_synthesis)

    # add edges and routing
    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "software_dev": "software_dev",
            "reverse_engineering": "reverse_engineering",
            "software_dev_and_re": "software_dev",  # start with software dev, then flow to RE
        },
    )
    
    # after software dev, route to RE if needed, otherwise to synthesis
    def route_after_software_dev(state: AgentState) -> str:
        if "reverse_engineering" in state.execution_domains:
            return "reverse_engineering"
        return "final_synthesis"
    
    graph.add_conditional_edges(
        "software_dev",
        route_after_software_dev,
        {
            "reverse_engineering": "reverse_engineering",
            "final_synthesis": "final_synthesis",
        },
    )
    
    # after reverse engineering, always route to synthesis
    graph.add_edge("reverse_engineering", "final_synthesis")
    
    # final synthesis to end
    graph.add_edge("final_synthesis", END)

    graph.set_entry_point("supervisor")

    compiled_graph = graph.compile()

    compiled_graph.name = "Multi-Domain Orchestration Engine"
    compiled_graph.description = "Supervisor-routed orchestration supporting software development and reverse engineering domains"

    return compiled_graph
"""
Implements the Supervisor pattern for routing requests to appropriate domains
and coordinating the overall multi-agent workflow.
"""

from langgraph.graph import StateGraph, END
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.agents.supervisor import SupervisorAgent
from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.retrievers.qdrant_client import QdrantRetriever
from langgraph_orchestration.core.state_utils import StateManager
from langgraph_orchestration.graphs.software_dev import build_software_dev_graph
from langgraph_orchestration.graphs.reverse_engineering import build_reverse_engineering_graph


def build_orchestration_graph(factory: MLXAgentFactory = None):
    """
    This graph implements the high-level orchestration logic:
    1. Routes incoming request to appropriate domain via Supervisor
    2. Retrieves relevant context from RAG (Qdrant)
    3. Invokes domain-specific subgraph
    4. Returns final synthesized output
    
    The routing to either software_dev or reverse_engineering subgraph
    is handled via conditional edges.
    
    Args:
        factory: MLXAgentFactory instance for shared model loading.
                 If None, creates a new one.
    Returns:
        Compiled StateGraph for the complete orchestration system
    """
    
    # Initialize components
    if factory is None:
        factory = MLXAgentFactory()
    
    supervisor = SupervisorAgent()
    retriever = QdrantRetriever()
    
    # Build domain subgraphs (pass factory for model sharing)
    software_dev_graph = build_software_dev_graph(factory=factory)
    reverse_eng_graph = build_reverse_engineering_graph(factory=factory)
    
    # Create main graph
    graph = StateGraph(AgentState)
    
    # Node 1: Supervisor routing
    def supervisor_node(state: AgentState) -> AgentState:
        """
        Analyze user request and route to appropriate domain.
        
        The Supervisor uses heuristic-based keyword analysis to determine
        whether the request is for software development or reverse engineering. (TBC)
        """
        domain = supervisor.invoke(user_input=state.user_input)
        state.selected_domain = domain
        return state
    
    # Node 2: RAG retrieval
    def retrieve_context_node(state: AgentState) -> AgentState:
        """
        Retrieve relevant context from Qdrant knowledge base.

        Uses the selected domain as a filter to retrieve domain-specific
        knowledge that will inform the specialized agents.
        """
        context = retriever.retrieve(
            query=state.user_input,
            top_k=5,
            domain=state.selected_domain,
        )
        return StateManager.add_retrieved_context(state, context)
    
    # Node 3: Software development domain router
    def software_dev_router(state: AgentState) -> AgentState:
        """        
        This node executes the code generation, testing, and architectural
        review workflow for software development tasks.
        """
        result = software_dev_graph.invoke(state)
        return result
    
    # Node 4: Reverse engineering domain router
    def reverse_engineering_router(state: AgentState) -> AgentState:
        """
        This node executes the planning, analysis, and vulnerability detection
        workflow for reverse engineering tasks.
        """
        result = reverse_eng_graph.invoke(state)
        return result
    
    # Node 5: Final synthesis (if needed)
    def final_synthesis(state: AgentState) -> AgentState:
        """
        Ensure final output is properly formatted and complete.
        This is a safety node that guarantees a response even if
        subgraph synthesis was skipped.
        """
        if state.final_output is None:
            state.final_output = StateManager.format_agent_outputs(state)
        return state
    
    # Add all nodes
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("retrieve_context", retrieve_context_node)
    graph.add_node("software_dev", software_dev_router)
    graph.add_node("reverse_engineering", reverse_engineering_router)
    graph.add_node("final_synthesis", final_synthesis)
    
    # Add sequential edges for supervisor and retrieval
    graph.add_edge("supervisor", "retrieve_context")
    
    # Add conditional routing based on domain selection
    def route_to_domain(state: AgentState) -> str:
        """Route to appropriate domain subgraph based on supervisor decision."""
        if state.selected_domain == "reverse_engineering":
            return "reverse_engineering"
        else:
            return "software_dev"
    
    graph.add_conditional_edges(
        "retrieve_context",
        route_to_domain,
        {
            "software_dev": "software_dev",
            "reverse_engineering": "reverse_engineering",
        },
    )
    
    # Both domain paths converge to final synthesis
    graph.add_edge("software_dev", "final_synthesis")
    graph.add_edge("reverse_engineering", "final_synthesis")
    graph.add_edge("final_synthesis", END)
    
    # Set entry point
    graph.set_entry_point("supervisor")
    
    return graph.compile()
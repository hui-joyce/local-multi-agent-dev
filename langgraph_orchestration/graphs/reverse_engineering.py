"""
Reverse engineering domain graph.
Defines the subgraph for planning, code analysis, and vulnerability detection
within the reverse engineering domain.
"""

from langgraph.graph import StateGraph, END
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.core.state_utils import StateManager


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
    
    # Create graph
    graph = StateGraph(AgentState)
    
    # Define node functions
    def planning_node(state: AgentState) -> AgentState:
        """Create analysis plan for the reverse engineering task."""
        plan = planning_agent.invoke(
            user_input=state.user_input,
            context=state.retrieved_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="planning",
            output=plan,
        )
    
    def code_analysis_node(state: AgentState) -> AgentState:
        analysis_input = f"""Based on this plan:
{state.intermediate_outputs.get('planning', '')}

Now analyze: {state.user_input}"""
        
        output = analysis_agent.invoke(
            user_input=analysis_input,
            context=state.retrieved_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="code_analysis",
            output=output,
        )
    
    def vulnerability_detection_node(state: AgentState) -> AgentState:
        vuln_input = f"""Based on this analysis:
{state.intermediate_outputs.get('code_analysis', '')}

Perform vulnerability assessment for: {state.user_input}"""
        
        output = vuln_agent.invoke(
            user_input=vuln_input,
            context=state.retrieved_context,
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
        return StateManager.set_final_output(state, final)
    
    # Add nodes
    graph.add_node("planning", planning_node)
    graph.add_node("code_analysis", code_analysis_node)
    graph.add_node("vulnerability_detection", vulnerability_detection_node)
    graph.add_node("synthesize", synthesize_output)
    
    # Add edges - sequential pipeline
    graph.add_edge("planning", "code_analysis")
    graph.add_edge("code_analysis", "vulnerability_detection")
    graph.add_edge("vulnerability_detection", "synthesize")
    graph.add_edge("synthesize", END)
    
    # Set entry point
    graph.set_entry_point("planning")
    
    compiled = graph.compile()
    compiled.name = "Reverse Engineering"
    compiled.description = "Planning, code analysis, and vulnerability detection workflow"
    return compiled
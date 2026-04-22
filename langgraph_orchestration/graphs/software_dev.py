"""
Software development domain graph.

Defines the subgraph for code generation, testing, and architectural review
within the software development domain.
"""

from langgraph.graph import StateGraph, END
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.agents import (
    CodeGenerationAgent,
    UnitTestingAgent,
    ArchitecturalReviewAgent,
)
from langgraph_orchestration.core.state_utils import StateManager


def build_software_dev_graph():    
    # Initialize agents
    code_gen_agent = CodeGenerationAgent()
    test_agent = UnitTestingAgent()
    arch_agent = ArchitecturalReviewAgent()
    
    # Create graph
    graph = StateGraph(AgentState)
    
    # Define node functions
    def code_generation_node(state: AgentState) -> AgentState:
        """Generate code based on user request and retrieved context."""
        output = code_gen_agent.invoke(
            user_input=state.user_input,
            context=state.retrieved_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="code_generation",
            output=output,
        )
    
    def unit_testing_node(state: AgentState) -> AgentState:
        """Generate tests for the generated code."""
        # Use previous agent output as input
        test_input = f"Code to test:\n{state.intermediate_outputs.get('code_generation', '')}"
        output = test_agent.invoke(
            user_input=test_input,
            context=state.retrieved_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="unit_testing",
            output=output,
        )
    
    def architectural_review_node(state: AgentState) -> AgentState:
        """Review architectural fit and best practices."""
        # Review all generated outputs
        review_input = f"Code and tests generated:\n{StateManager.format_agent_outputs(state)}"
        output = arch_agent.invoke(
            user_input=review_input,
            context=state.retrieved_context,
        )
        return StateManager.add_intermediate_output(
            state=state,
            agent_name="architectural_review",
            output=output,
        )
    
    def synthesize_output(state: AgentState) -> AgentState:
        final = f"""# Software Development Analysis

## User Request
{state.user_input}

## Generated Solutions
{StateManager.format_agent_outputs(state)}

## Summary
All solutions have been reviewed for architectural fit and best practices.
Ready for integration and deployment.
"""
        return StateManager.set_final_output(state, final)
    
    # Add nodes
    graph.add_node("code_generation", code_generation_node)
    graph.add_node("unit_testing", unit_testing_node)
    graph.add_node("architectural_review", architectural_review_node)
    graph.add_node("synthesize", synthesize_output)
    
    # Add edges
    graph.add_edge("code_generation", "unit_testing")
    graph.add_edge("unit_testing", "architectural_review")
    graph.add_edge("architectural_review", "synthesize")
    graph.add_edge("synthesize", END)
    
    # Set entry point
    graph.set_entry_point("code_generation")
    
    return graph.compile()
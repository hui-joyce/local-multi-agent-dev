"""
Example execution and testing of the orchestration system.
"""

from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.graphs.orchestration import build_orchestration_graph


def run_orchestration_example(user_input: str) -> None:
    """
    Run the orchestration graph with a user input and display results.
    
    Args:
        user_input: The user's request to the multi-agent system
    """
    print("\n" + "="*80)
    print(f"USER REQUEST: {user_input}")
    print("="*80 + "\n")
    
    # Build the orchestration graph
    graph = build_orchestration_graph()
    
    # Create initial state
    initial_state = AgentState(user_input=user_input)
    
    # Execute the graph
    print("Executing orchestration graph...\n")
    result = graph.invoke(initial_state.model_dump())
    
    # Convert result dict back to AgentState for easier access
    final_state = AgentState(**result)
    
    # Display results
    print(f"✓ Selected Domain: {final_state.selected_domain.upper()}\n")
    
    print(f"Retrieved Context ({len(final_state.retrieved_context)} documents):")
    for i, doc in enumerate(final_state.retrieved_context[:3], 1):
        print(f"  {i}. {doc[:70]}...")
    
    print(f"\nAgents Executed: {' → '.join(final_state.agent_chain)}\n")
    
    print("="*80)
    print("FINAL OUTPUT")
    print("="*80)
    print(final_state.final_output)
    print("="*80 + "\n")


def run_all_examples() -> None:
    """Run multiple examples demonstrating different capabilities."""
    
    # Example 1: Software development request
    print("\n\nEXAMPLE 1: Software Development Assistant")
    run_orchestration_example(
        "I need to generate a Python function for sorting and then write unit tests for it. "
        "Also review the architecture."
    )
    
    # Example 2: Reverse engineering request
    print("\n\nEXAMPLE 2: Reverse Engineering Assistant")
    run_orchestration_example(
        "Analyze this binary for vulnerabilities and security issues. "
        "Perform a comprehensive reverse engineering assessment."
    )
    
    # Example 3: Code implementation request
    print("\n\nEXAMPLE 3: Code Generation Focus")
    run_orchestration_example(
        "Implement a REST API endpoint for user authentication with proper error handling"
    )
    
    # Example 4: Security analysis request
    print("\n\nEXAMPLE 4: Security Vulnerability Detection")
    run_orchestration_example(
        "I found suspicious assembly code with potential buffer overflow. "
        "Analyze it for security threats."
    )

if __name__ == "__main__":
    print("MULTI-AGENT ORCHESTRATION SYSTEM - EXAMPLES")
    
    run_all_examples()
    
    print("All examples completed successfully!")
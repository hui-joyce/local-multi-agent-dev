import os
from dotenv import load_dotenv
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.graphs.orchestration import build_orchestration_graph

# Load environment variables
load_dotenv()

# Enable LangSmith tracing if credentials are available
if os.getenv("LANGSMITH_API_KEY"):
    os.environ["LANGSMITH_TRACING"] = "true"
    print(f"✓ LangSmith tracing enabled")
    print(f"  Project: {os.getenv('LANGSMITH_PROJECT', 'default')}")
else:
    print("LangSmith not configured. Set LANGSMITH_API_KEY to enable tracing.")


def run_orchestration_example(user_input: str) -> None:
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
    if os.getenv("LANGCHAIN_TRACING_V2"):
        print("See LangSmith dashboard")
    # Run examples
    run_all_examples()
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
    # Software development - rate limiter with tests (SD-01)
    print("\n\nEXAMPLE 1: Software Development - Feature Implementation")
    run_orchestration_example(
        "Implement a Python rate limiter using token bucket logic and include "
        "unit tests for burst and refill behavior."
    )
    
    # Reverse engineering - code analysis (RE-01)
    print("\n\nEXAMPLE 2: Reverse Engineering - Code Behavior Analysis")
    run_orchestration_example(
        "Reverse engineer the following pseudo-code and explain likely intent, "
        "state transitions, hidden assumptions, and possible abuse cases.\n\n"
        "Pseudo-code:\n"
        "function verify_and_execute(input, key):\n"
        "    state = INIT\n"
        "    idx = 0\n"
        "    checksum = 0\n"
        "    while idx < len(input):\n"
        "        b = input[idx]\n"
        "        checksum = (checksum + ((b XOR key[idx % len(key)]) * 17)) & 0xFFFF\n"
        "        if state == INIT and b == 0x7B:\n"
        "            state = HEADER\n"
        "        else if state == HEADER and b == 0x3A:\n"
        "            state = BODY\n"
        "        else if state == BODY and b == 0x7D:\n"
        "            state = DONE\n"
        "        idx = idx + 1\n"
        "\n"
        "    if state != DONE:\n"
        "        return ERR_FORMAT\n"
        "\n"
        "    if checksum == 0xBEEF:\n"
        "        call privileged_operation(input)\n"
        "        return OK\n"
        "\n"
        "    return ERR_AUTH\n"
    )

if __name__ == "__main__":
    print("MULTI-AGENT ORCHESTRATION SYSTEM - EXAMPLES")
    if os.getenv("LANGCHAIN_TRACING_V2"):
        print("See LangSmith dashboard")
    # Run examples
    run_all_examples()
import sys
from pathlib import Path

import gradio as gr

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

from langgraph_orchestration.core.state_utils import StateManager
from langgraph_orchestration.runtime import get_runtime

load_dotenv()
get_runtime().ensure_ready()


def _format_routing(final_state) -> str:
    """Transparent footer to capture which domain(s) and agent chain were used to produce the final output"""
    domains = final_state.execution_domains or (
        [final_state.selected_domain] if final_state.selected_domain else []
    )
    domain_str = ", ".join(d for d in domains if d) or "n/a"
    chain_str = " → ".join(final_state.agent_chain) if final_state.agent_chain else "n/a"
    return f"\n\n---\n_routed: {domain_str} · {chain_str}_"

def respond(message, history):
    try:
        final_state = get_runtime().run(message)
        answer = StateManager.sanitize_output(final_state.final_output or "")
        if not answer:
            answer = "_(No output produced.)_"
        return answer + _format_routing(final_state)
    except Exception as e:
        return f"Error: {e}"

with gr.Blocks(title="Multi-Agent Orchestration Chat") as demo:
    gr.Markdown(
        "# Multi-Agent Orchestration Chat\n"
        "Prompts are routed by the supervisor to the software-development and/or "
        "reverse-engineering domains"
    )

    gr.ChatInterface(
        fn=respond,
        examples=[
            "Implement a Python rate limiter using token bucket logic and include unit tests for burst and refill behavior.",
            "Reverse engineer this pseudo-code and explain its likely intent and abuse cases.",
            "Analyze this decompiled parser routine for memory safety risks and exploit paths.",
            "Build a secure file upload handler in Python, then assess it for vulnerability concerns.",
        ],
        title="Chat with the agent",
        analytics_enabled=False,
    )

if __name__ == "__main__":
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)
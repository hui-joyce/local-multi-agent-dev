import logging
import os
import sys
from pathlib import Path

import gradio as gr

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

from langgraph_orchestration.chat_history import load_history, save_history
from langgraph_orchestration.core.state_utils import StateManager
from langgraph_orchestration.runtime import get_runtime
from langgraph_orchestration.security import is_loopback_host

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mad.app")
get_runtime().ensure_ready()

EXAMPLES = [
    "Implement a Python rate limiter using token bucket logic and include unit tests for burst and refill behavior.",
    "Reverse engineer this pseudo-code and explain its likely intent and abuse cases.",
    "Analyze this decompiled parser routine for memory safety risks and exploit paths.",
    "Build a secure file upload handler in Python, then assess it for vulnerability concerns.",
]


def _format_routing(final_state) -> str:
    """Transparent footer capturing which domain(s) and agent chain produced the output"""
    domains = final_state.execution_domains or (
        [final_state.selected_domain] if final_state.selected_domain else []
    )
    domain_str = ", ".join(d for d in domains if d) or "n/a"
    chain_str = " → ".join(final_state.agent_chain) if final_state.agent_chain else "n/a"
    return f"\n\n---\n_routed: {domain_str} · {chain_str}_"


def _run(message: str) -> str:
    try:
        final_state = get_runtime().run(message)
        answer = StateManager.sanitize_output(final_state.final_output or "")
        if not answer:
            return "_(No output produced.)_"
        return answer + _format_routing(final_state)
    except Exception:
        logger.exception("Orchestration run failed")
        return "_An internal error occurred while processing your request. Please try again._"


def _content_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for p in content:
            if isinstance(p, dict):
                parts.append(str(p.get("text", "")))
            elif isinstance(p, str):
                parts.append(p)
        return "\n".join(t for t in parts if t)
    return str(content or "")


def _normalize(history: list[dict]) -> list[dict]:
    return [
        {"role": m.get("role"), "content": _content_text(m.get("content"))}
        for m in history
        if isinstance(m, dict) and m.get("role")
    ]


def add_user_message(message: str, history: list[dict]):
    if not message or not message.strip():
        return "", history
    return "", history + [{"role": "user", "content": message}]


def generate_reply(history: list[dict]):
    """Answer the latest user message, then persist the full transcript to disk"""
    if not history or history[-1].get("role") != "user":
        return history
    user_msg = _content_text(history[-1].get("content", ""))
    if not user_msg.strip():
        return history
    answer = _run(user_msg)
    history = history + [{"role": "assistant", "content": answer}]
    save_history(_normalize(history))
    return history


def clear_history():
    """Wipe the saved transcript."""
    save_history([])
    return []


with gr.Blocks(title="Multi-Agent Orchestration Chat", analytics_enabled=False) as demo:
    gr.Markdown(
        "# Multi-Agent Orchestration Chat\n"
        "Prompts are routed by the supervisor to the software-development and/or "
        "reverse-engineering domains. Conversation is saved locally and reloaded "
        "on restart."
    )

    chatbot = gr.Chatbot(value=load_history(), label="Conversation", height=520)
    msg = gr.Textbox(
        placeholder="Ask something… (Enter to send)",
        label="Message",
        autofocus=True,
    )
    with gr.Row():
        send = gr.Button("Send", variant="primary")
        clear = gr.Button("Clear history")

    gr.Examples(examples=EXAMPLES, inputs=msg, label="Examples")
    demo.load(load_history, inputs=None, outputs=chatbot)

    msg.submit(add_user_message, [msg, chatbot], [msg, chatbot], queue=False).then(
        generate_reply, chatbot, chatbot
    )
    send.click(add_user_message, [msg, chatbot], [msg, chatbot], queue=False).then(
        generate_reply, chatbot, chatbot
    )
    clear.click(clear_history, None, chatbot, queue=False)


if __name__ == "__main__":
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "7860"))

    if not is_loopback_host(host):
        logger.warning(
            "Gradio chat bound to %s with no auth — anyone who can reach this port "
            "can use the model. Bind to 127.0.0.1 to keep it local only.",
            host,
        )

    demo.launch(
        server_name=host,
        server_port=port,
        share=False,       
        show_error=False,  # don't render raw tracebacks in the browser
    )
"""Gradio chat front end"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import gradio as gr  # noqa: E402

from langgraph_orchestration.core import StateManager, enforce_bind_policy  # noqa: E402
from langgraph_orchestration.runtime import get_runtime  # noqa: E402

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("mad.app")

EXAMPLES = [
    "Implement a Python rate limiter using token bucket logic and include unit tests "
    "for burst and refill behavior.",
    "Reverse engineer this pseudo-code and explain its likely intent and abuse cases.",
    "Analyze this decompiled parser routine for memory safety risks and exploit paths.",
    "Build a secure file upload handler in Python, then assess it for vulnerability concerns.",
]


def _format_routing(final_state) -> str:
    """Footer showing which domains and agents produced the answer"""
    domains = final_state.execution_domains or (
        [final_state.selected_domain] if final_state.selected_domain else []
    )
    domain_str = ", ".join(domain for domain in domains if domain) or "n/a"
    chain_str = " -> ".join(final_state.agent_chain) if final_state.agent_chain else "n/a"
    return f"\n\n---\n_routed: {domain_str} · {chain_str}_"


def _run(message: str) -> str:
    try:
        final_state = get_runtime().run(message)
    except Exception:
        logger.exception("Orchestration run failed")
        return "_An internal error occurred while processing your request. Please try again._"

    answer = StateManager.sanitize_output(final_state.final_output or "")
    if not answer:
        return "_(No output produced.)_"
    return answer + _format_routing(final_state)


def _content_text(content) -> str:
    """Flatten Gradio message content, which may be a string or a parts list"""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = [
            str(part.get("text", "")) if isinstance(part, dict) else part
            for part in content
            if isinstance(part, (dict, str))
        ]
        return "\n".join(text for text in parts if text)
    return str(content or "")


def _normalize(history: list[dict]) -> list[dict]:
    return [
        {"role": message.get("role"), "content": _content_text(message.get("content"))}
        for message in history
        if isinstance(message, dict) and message.get("role")
    ]


def add_user_message(message: str, history: list[dict]):
    if not message or not message.strip():
        return "", history
    return "", history + [{"role": "user", "content": message}]


_WORKING = (
    "_Working on it..._\n\n"
    "Firmware comparisons download and diff multi-gigabyte IPSWs and can run for "
    "hours; ordinary requests take under a minute."
)


def generate_reply(history: list[dict]):
    if not history or history[-1].get("role") != "user":
        yield history
        return
    user_message = _content_text(history[-1].get("content", ""))
    if not user_message.strip():
        yield history
        return

    yield history + [{"role": "assistant", "content": _WORKING}]

    history = history + [{"role": "assistant", "content": _run(user_message)}]
    save_history(_normalize(history))
    yield history


def clear_history():
    save_history([])
    return []


logger = logging.getLogger("mad.chat_history")

MAX_MESSAGES = 400

_DEFAULT_DIR = Path.home() / ".local" / "share" / "local-multi-agent-dev"


def history_path() -> Path:
    override = os.getenv("CHAT_HISTORY_FILE")
    if override:
        return Path(override).expanduser()
    base = os.getenv("CHAT_HISTORY_DIR")
    base_dir = Path(base).expanduser() if base else _DEFAULT_DIR
    return base_dir / "chat_history.json"


def _clean(history: list) -> list[dict]:
    out: list[dict] = []
    for m in history or []:
        if isinstance(m, dict) and "role" in m and "content" in m:
            out.append({"role": m["role"], "content": m["content"]})
    return out


def load_history() -> list[dict]:
    path = history_path()
    try:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return _clean(data)
    except Exception:
        logger.exception("Failed to load chat history from %s", path)
    return []


def save_history(history: list[dict]) -> None:
    path = history_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        clean = _clean(history)[-MAX_MESSAGES:]
        path.write_text(json.dumps(clean, ensure_ascii=False), encoding="utf-8")
    except Exception:
        logger.exception("Failed to save chat history to %s", path)


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Multi-Agent Orchestration Chat", analytics_enabled=False) as demo:
        gr.Markdown(
            "# Multi-Agent Orchestration Chat\n"
            "Prompts are routed by the supervisor to the software-development and/or "
            "reverse-engineering domains. Conversation is saved locally and reloaded "
            "on restart."
        )

        chatbot = gr.Chatbot(value=load_history(), label="Conversation", height=520)
        message_box = gr.Textbox(
            placeholder="Ask something... (Enter to send)", label="Message", autofocus=True
        )
        with gr.Row():
            send = gr.Button("Send", variant="primary")
            clear = gr.Button("Clear history")

        gr.Examples(examples=EXAMPLES, inputs=message_box, label="Examples")
        demo.load(load_history, inputs=None, outputs=chatbot)

        message_box.submit(
            add_user_message, [message_box, chatbot], [message_box, chatbot], queue=False
        ).then(generate_reply, chatbot, chatbot)
        send.click(
            add_user_message, [message_box, chatbot], [message_box, chatbot], queue=False
        ).then(generate_reply, chatbot, chatbot)
        clear.click(clear_history, None, chatbot, queue=False)

    return demo


def main() -> None:
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "7860"))

    enforce_bind_policy(host, surface="Gradio chat")

    logger.info("Loading model and building graph...")
    get_runtime().ensure_ready()
    logger.info("Ready")

    build_ui().launch(
        server_name=host,
        server_port=port,
        share=False,
        show_error=False,  # never render raw tracebacks in the browser
    )


if __name__ == "__main__":
    main()

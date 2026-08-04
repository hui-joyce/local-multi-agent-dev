from __future__ import annotations

import re

from langgraph_orchestration.state import AgentState

_THINK_BLOCK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)
_THINK_UNWRAP_RE = re.compile(r"<think>(.*?)</think>", re.DOTALL)
_THINKING_UNWRAP_RE = re.compile(r"<thinking>(.*?)</thinking>", re.DOTALL)
_TOOL_CALL_RE = re.compile(r"<tool_call>.*?</tool_call>", re.DOTALL)
_CONTEXT_COMPLETE_RE = re.compile(r"\[CONTEXT_COMPLETE\]")
_BLANK_RUN_RE = re.compile(r"\n\n\n+")

_FENCED_JSON_RE = re.compile(r"```json\s*(.*?)```", re.DOTALL | re.IGNORECASE)
_TOOL_ENVELOPE_KEY_RE = re.compile(r'"(?:tool_name|tool_result|tool_call)"\s*:')


def _coerce(text: object) -> str:
    if isinstance(text, str):
        return text
    try:
        return str(text or "")
    except Exception:
        return ""


def strip_reasoning(text: object) -> str:
    """Remove complete <think>...</think> blocks, content included"""
    return _THINK_BLOCK_RE.sub("", _coerce(text)).strip()


def _strip_echoed_tool_envelopes(text: str) -> str:
    def _replace(match: re.Match[str]) -> str:
        return "" if _TOOL_ENVELOPE_KEY_RE.search(match.group(1)) else match.group(0)

    return _FENCED_JSON_RE.sub(_replace, text)


def sanitize_agent_output(text: object) -> str:
    raw = _coerce(text)
    cleaned = _strip_echoed_tool_envelopes(strip_reasoning(raw)).strip()
    return cleaned or strip_reasoning(raw)


def sanitize_final_output(text: object) -> str:
    raw = _coerce(text)
    if not raw:
        return raw

    unwrapped = _THINK_UNWRAP_RE.sub(r"\1", raw)
    unwrapped = _THINKING_UNWRAP_RE.sub(r"\1", unwrapped)
    without_tools = _TOOL_CALL_RE.sub("", unwrapped)
    without_markers = _CONTEXT_COMPLETE_RE.sub("", without_tools)
    return _BLANK_RUN_RE.sub("\n\n", without_markers).strip()


_MAX_TOOL_BODY_CHARS = 4000
_TOOL_BODY_EDGE_CHARS = 2000


class StateManager:
    @staticmethod
    def sanitize_output(text: str) -> str:
        return sanitize_final_output(text)

    @staticmethod
    def add_intermediate_output(state: AgentState, agent_name: str, output: str) -> AgentState:
        state.intermediate_outputs[agent_name] = output
        state.agent_chain.append(agent_name)
        return state

    @staticmethod
    def add_retrieved_context(state: AgentState, context: list[str]) -> AgentState:
        state.retrieved_context.extend(context)
        return state

    @staticmethod
    def format_agent_outputs(state: AgentState) -> str:
        from langgraph_orchestration.tooling.tool import parse_agent_output

        outputs = []
        for agent_name, raw_output in state.intermediate_outputs.items():
            parsed = parse_agent_output(raw_output)
            formatted_text = parsed.assistant_message.strip() if parsed.assistant_message else ""

            for tool_call in parsed.tool_calls:
                if tool_call.tool_name in ("create_file", "edit_file"):
                    content = (
                        tool_call.arguments.get("content")
                        or tool_call.arguments.get("file_text")
                        or ""
                    )
                    path = tool_call.arguments.get("path") or tool_call.target or "Generated Code"
                    if content:
                        formatted_text += f"\n\n**File: `{path}`**\n```python\n{content}\n```\n"

            if parsed.parse_errors:
                formatted_text += (
                    "\n\n*(Parser encountered issues extracting tool calls. "
                    "Please check your workspace for the files.)*"
                )

            outputs.append(f"\n## {agent_name.upper()}\n{formatted_text.strip()}")

        if state.tool_results:
            outputs.append(StateManager.format_tool_activity(state))

        return "\n".join(outputs)

    @staticmethod
    def format_tool_activity(state: AgentState) -> str:
        if not state.tool_requests and not state.tool_results:
            return ""

        sections = ["\n## TOOL ACTIVITY"]

        if state.tool_requests:
            sections.append("\n### Requested Tools")
            for index, request in enumerate(state.tool_requests, start=1):
                sections.append(f"{index}. {request.tool_name} -> target={request.target or 'n/a'}")

        if state.tool_results:
            sections.append("\n### Tool Results")
            for index, result in enumerate(state.tool_results, start=1):
                status = "ok" if result.success else "error"
                command = result.metadata.get("command") if result.metadata else None
                command_line = f"\ncommand: {command}" if command else ""
                body = result.output or (result.error or "")

                if len(body) > _MAX_TOOL_BODY_CHARS:
                    body = (
                        body[:_TOOL_BODY_EDGE_CHARS]
                        + "\n\n...[CONTENT TRUNCATED FOR CONTEXT LENGTH]...\n\n"
                        + body[-_TOOL_BODY_EDGE_CHARS:]
                    )

                sections.append(f"{index}. {result.tool_name} [{status}]{command_line}\n{body}")

        return "\n".join(sections)


FIRMWARE_KEYWORDS: tuple[str, ...] = (
    "ipsw",
    "firmware",
    "dyld",
    "dyld_shared_cache",
    "kernelcache",
    "kernel cache",
    "ota",
    "restore.ipsw",
    "sepos",
    "iboot",
    "entitlement",
    "framework diff",
    "symbol analysis",
    "binary analysis",
)

FIRMWARE_HINT_RE = re.compile(
    r"\b(?:ios|ipados|macos|watchos|tvos|bridgeos)\b\s*v?\d+(?:\.\d+)+"
    r"|\b(?:iphone|ipad|appletv|watch)\d+,\d+\b",
    re.IGNORECASE,
)


def looks_like_firmware_request(user_input: str) -> bool:
    """True when the request is about firmware, decided without the model"""
    text = user_input or ""
    lowered = text.lower()
    if any(keyword in lowered for keyword in FIRMWARE_KEYWORDS):
        return True
    return bool(FIRMWARE_HINT_RE.search(text))


# Section: binary addresses


def parse_address(value: object) -> int | None:
    """Return *value* as an int address, or None if it is not one"""
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if not isinstance(value, str):
        return None

    text = value.strip()
    if not text:
        return None
    try:
        return int(text, 16) if text.lower().startswith("0x") else int(text)
    except ValueError:
        return None


def require_address(value: object) -> int:
    """Like :func:`parse_address`, but raises for an unusable value"""
    address = parse_address(value)
    if address is None:
        raise ValueError(f"Invalid address: {value!r}")
    return address


_LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1", ""}


def is_loopback_host(host: str | None) -> bool:
    return (host or "").strip().lower() in _LOOPBACK_HOSTS


def enforce_bind_policy(host: str, *, surface: str) -> None:
    if is_loopback_host(host):
        return
    raise RuntimeError(
        f"{surface} refusing to start: bound to non-loopback host {host!r}. "
        "This is a local-only tool with no request authentication; bind to "
        "127.0.0.1 (set API_HOST=127.0.0.1)."
    )

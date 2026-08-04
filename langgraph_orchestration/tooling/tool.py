from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field

ToolStatus = Literal["requested", "executed", "failed"]


class ToolRequest(BaseModel):
    type: Literal["tool_request"] = "tool_request"
    tool_name: str = Field(description="Official tool name requested from the host")
    arguments: dict[str, Any] = Field(default_factory=dict)
    target: str | None = Field(
        default=None,
        description="File, function, artifact, or other target of the request",
    )
    reason: str = Field(default="", description="Why this tool is needed before proceeding")
    status: ToolStatus = "requested"
    domain: Literal["software_dev", "reverse_engineering"] | None = None


class ToolResult(BaseModel):
    type: Literal["tool_result"] = "tool_result"
    tool_name: str = Field(description="Tool that produced this result")
    success: bool = True
    output: str = Field(description="Agent-visible tool output")
    error: str | None = None
    source: str | None = Field(
        default=None,
        description="Host subsystem that executed the tool, e.g. 'ida' or 'vscode'",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


class ToolPolicy(BaseModel):
    """What the active workflow is allowed to call, and how often."""

    max_iterations: int = 40
    allowed_tools: list[str] = Field(default_factory=list)


@dataclass()
class ToolCall:
    """A tool call as parsed out of raw model output."""

    tool_name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    target: str | None = None
    reason: str | None = None
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass()
class ParseError:
    error_type: Literal["invalid_json", "missing_required_field", "unexpected_format", ""]
    message: str
    context: str | None = None


@dataclass()
class ParsedAgentOutput:
    raw_output: str
    assistant_message: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    parse_errors: list[ParseError] = field(default_factory=list)

    def has_tool_calls(self) -> bool:
        return bool(self.tool_calls)

    def has_errors(self) -> bool:
        return bool(self.parse_errors)

    def error_summary(self) -> str:
        if not self.parse_errors:
            return ""
        lines = [f"Parse errors ({len(self.parse_errors)}):"]
        lines += [f"  - {err.error_type}: {err.message}" for err in self.parse_errors]
        return "\n".join(lines)


# =========================================================================
# Parsing
#
# Tolerant by design: models fence JSON, add prose around it, and
# occasionally emit two envelopes. All of that is recoverable.
# =========================================================================


_TOOL_CALL_RE = re.compile(r"<tool_call>\s*(.*?)\s*</tool_call>", re.DOTALL)
_JSON_OBJECT_RE = re.compile(r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}", re.DOTALL)
_CONTEXT_LIMIT = 120


def parse_agent_output(agent_output: str) -> ParsedAgentOutput:
    """Parse ``<tool_call>`` envelopes, falling back to bare JSON objects.

    The fallback exists because models routinely emit a well-formed tool-call
    object without wrapping it in the envelope.
    """
    if not agent_output:
        return ParsedAgentOutput(raw_output="", assistant_message="")

    matches = list(_TOOL_CALL_RE.finditer(agent_output))
    enveloped = bool(matches)

    if not matches:
        matches = [
            match
            for match in _JSON_OBJECT_RE.finditer(agent_output)
            if _is_tool_call_object(match.group(0))
        ]

    if not matches:
        return ParsedAgentOutput(
            raw_output=agent_output,
            assistant_message=agent_output.strip(),
        )

    tool_calls: list[ToolCall] = []
    parse_errors: list[ParseError] = []
    for match in matches:
        payload = match.group(1) if enveloped else match.group(0)
        tool_call, parse_error = _parse_envelope(payload.strip(), _trim(match.group(0)))
        if parse_error:
            parse_errors.append(parse_error)
        elif tool_call:
            tool_calls.append(tool_call)

    return ParsedAgentOutput(
        raw_output=agent_output,
        assistant_message=_extract_prose(agent_output, matches),
        tool_calls=tool_calls,
        parse_errors=parse_errors,
    )


def _is_tool_call_object(text: str) -> bool:
    try:
        obj = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return False
    return isinstance(obj, dict) and "tool_name" in obj


def _extract_prose(full_text: str, matches: list[re.Match[str]]) -> str:
    parts: list[str] = []
    last_end = 0
    for match in matches:
        start, end = match.span()
        if start > last_end:
            parts.append(full_text[last_end:start])
        last_end = end
    if last_end < len(full_text):
        parts.append(full_text[last_end:])
    return "".join(parts).strip()


def _parse_envelope(payload: str, context: str) -> tuple[ToolCall | None, ParseError | None]:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        message = f"Invalid JSON in tool_call envelope: {exc}"
        lines = payload.split("\n")
        if exc.lineno and exc.lineno <= len(lines):
            message += f" | Problem line: {lines[exc.lineno - 1].strip()[:60]}"
        return None, ParseError("invalid_json", message, context or None)

    if not isinstance(data, dict):
        return None, ParseError(
            "unexpected_format",
            f"Expected JSON object, got {type(data).__name__}",
            context or None,
        )

    if "tool_name" not in data:
        return None, ParseError(
            "missing_required_field",
            "tool_call envelope missing 'tool_name' field",
            context or None,
        )

    arguments = data.get("arguments", {})
    if not isinstance(arguments, dict):
        return None, ParseError(
            "unexpected_format",
            f"'arguments' must be an object, got {type(arguments).__name__}",
            context or None,
        )

    target = data.get("target")
    return (
        ToolCall(
            tool_name=str(data["tool_name"]),
            arguments=arguments,
            target=str(target) if target is not None else None,
            reason=data.get("reason"),
        ),
        None,
    )


def _trim(context: str) -> str:
    context = context.strip()
    if len(context) <= _CONTEXT_LIMIT:
        return context
    return context[:_CONTEXT_LIMIT] + "..."

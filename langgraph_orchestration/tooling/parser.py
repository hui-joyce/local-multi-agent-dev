from __future__ import annotations

import json
import re

from langgraph_orchestration.tooling.tool import ParseError, ParsedAgentOutput, ToolCall

TOOL_CALL_PATTERN = re.compile(r"<tool_call>\s*(.*?)\s*</tool_call>", re.DOTALL)
JSON_OBJECT_PATTERN = re.compile(r"\{(?:[^{}]|(?:\{[^{}]*\}))*\}", re.DOTALL)

def parse_agent_output(agent_output: str) -> ParsedAgentOutput:
    if not agent_output:
        return ParsedAgentOutput(
            raw_output="",
            assistant_message="",
            tool_calls=[],
            parse_errors=[],
            context_complete=False,
        )

    # Check for context completion signal
    context_complete = "[CONTEXT_COMPLETE]" in agent_output

    tool_call_matches = list(TOOL_CALL_PATTERN.finditer(agent_output))
    
    # fallback
    if not tool_call_matches:
        json_matches = list(JSON_OBJECT_PATTERN.finditer(agent_output))
        fallback_matches = []
        for match in json_matches:
            try:
                obj = json.loads(match.group(0))
                if isinstance(obj, dict) and "tool_name" in obj:
                    fallback_matches.append(match)
            except (json.JSONDecodeError, ValueError):
                continue
        
        if fallback_matches:
            tool_call_matches = fallback_matches
    
    if not tool_call_matches:
        return ParsedAgentOutput(
            raw_output=agent_output,
            assistant_message=agent_output.strip(),
            tool_calls=[],
            parse_errors=[],
            context_complete=context_complete,
        )

    assistant_message = _extract_prose(agent_output, tool_call_matches)

    tool_calls: list[ToolCall] = []
    parse_errors: list[ParseError] = []

    for match in tool_call_matches:
        try:
            envelope_content = match.group(1).strip()
        except IndexError:
            envelope_content = match.group(0).strip()
        
        envelope_context = _trim_context(match.group(0))
        tool_call, parse_err = _parse_single_envelope(
            envelope_content,
            envelope_context=envelope_context,
        )

        if parse_err:
            parse_errors.append(parse_err)
        elif tool_call:
            tool_calls.append(tool_call)

    return ParsedAgentOutput(
        raw_output=agent_output,
        assistant_message=assistant_message,
        tool_calls=tool_calls,
        parse_errors=parse_errors,
        context_complete=context_complete,
    )

def _extract_prose(full_text: str, tool_call_matches: list[re.Match[str]]) -> str:
    result = []
    last_end = 0
    for match in tool_call_matches:
        start, end = match.span()
        if start > last_end:
            result.append(full_text[last_end:start])
        last_end = end

    if last_end < len(full_text):
        result.append(full_text[last_end:])

    return "".join(result).strip()

def _parse_single_envelope(
    envelope_content: str,
    envelope_context: str = "",
) -> tuple[ToolCall | None, ParseError | None]:
    try:
        data = json.loads(envelope_content)
    except json.JSONDecodeError as exc:
        error_line = ""
        if exc.lineno and exc.colno:
            lines = envelope_content.split('\n')
            if exc.lineno <= len(lines):
                error_line = lines[exc.lineno - 1].strip()
        
        error_msg = f"Invalid JSON in tool_call envelope: {str(exc)}"
        if error_line:
            error_msg += f" | Problem line: {error_line[:60]}"
        
        return None, ParseError(
            error_type="invalid_json",
            message=error_msg,
            context=envelope_context or None,
            recoverable=True,
        )

    if not isinstance(data, dict):
        return None, ParseError(
            error_type="unexpected_format",
            message=f"Expected JSON object, got {type(data).__name__}",
            context=envelope_context or None,
            recoverable=True,
        )

    if "tool_name" not in data:
        return None, ParseError(
            error_type="missing_required_field",
            message="tool_call envelope missing 'tool_name' field",
            context=envelope_context or None,
            recoverable=True,
        )

    try:
        tool_call = ToolCall(
            tool_name=data["tool_name"],
            arguments=data.get("arguments", {}),
            target=data.get("target"),
            reason=data.get("reason"),
            needs_confirmation=data.get("needs_confirmation", False),
            expected_outcome=data.get("expected_outcome"),
        )
    except Exception as exc:
        return None, ParseError(
            error_type="unexpected_format",
            message=f"Invalid tool_call schema: {str(exc)}",
            context=envelope_context or None,
            recoverable=True,
        )

    return tool_call, None

def _trim_context(context: str, limit: int = 120) -> str:
    context = context.strip()
    if len(context) <= limit:
        return context
    return context[:limit] + "..."
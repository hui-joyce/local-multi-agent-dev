# STILL IN DEV
"""Tool executor node integration for LangGraph orchestration"""

import json
import re
from typing import Optional

from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.tooling.contracts import ToolRequest, ToolResult
from langgraph_orchestration.tooling.tool_executor import get_tool_executor


def parse_tool_request_from_output(output: str) -> Optional[ToolRequest]:
    """Extract a ToolRequest JSON block from agent output"""
    if not output:
        return None

    json_blocks = re.findall(r"```(?:json)?\s*(\{[^`]*\})\s*```", output)
    for block in json_blocks:
        try:
            data = json.loads(block)
            if data.get("type") == "tool_request":
                return ToolRequest(**data)
        except (json.JSONDecodeError, ValueError):
            continue

    in_string = False
    escape_next = False
    depth = 0
    json_start = -1
    
    for i, char in enumerate(output):
        if escape_next:
            escape_next = False
            continue
        if char == '\\':
            escape_next = True
            continue
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
        if not in_string:
            if char == '{':
                if depth == 0:
                    json_start = i
                depth += 1
            elif char == '}':
                depth -= 1
                if depth == 0 and json_start >= 0:
                    json_str = output[json_start:i+1]
                    try:
                        data = json.loads(json_str)
                        if data.get("type") == "tool_request":
                            return ToolRequest(**data)
                    except (json.JSONDecodeError, ValueError):
                        pass
                    json_start = -1

    if "TOOL REQUEST:" in output:
        try:
            start = output.index("TOOL REQUEST:") + len("TOOL REQUEST:")
            rest = output[start:]
            depth = 0
            in_json = False
            json_start = -1
            for i, char in enumerate(rest):
                if char == "{":
                    if not in_json:
                        in_json = True
                        json_start = i
                    depth += 1
                elif char == "}" and in_json:
                    depth -= 1
                    if depth == 0:
                        json_str = rest[json_start : i + 1]
                        data = json.loads(json_str)
                        if data.get("type") == "tool_request":
                            return ToolRequest(**data)
                        break
        except (json.JSONDecodeError, ValueError, IndexError):
            pass

    return None


def tool_executor_node(state: AgentState) -> AgentState:
    """Execute one tool request and record the result in state"""

    if state.tool_iteration >= state.max_tool_iterations:
        return state

    last_agent = state.agent_chain[-1] if state.agent_chain else None
    if not last_agent:
        return state

    last_output = state.intermediate_outputs.get(last_agent)
    if not last_output:
        return state

    tool_request = parse_tool_request_from_output(last_output)
    if not tool_request:
        return state

    if not tool_request.domain:
        tool_request.domain = state.selected_domain or "software_dev"

    # Validate against policy
    allowed_tools = state.tool_policy.allowed_tools or []
    if tool_request.tool_name not in allowed_tools:
        error_msg = (
            f"Tool '{tool_request.tool_name}' not allowed in "
            f"domain '{state.selected_domain}'. "
            f"Allowed: {', '.join(allowed_tools)}"
        )
        result = ToolResult(
            tool_name=tool_request.tool_name,
            success=False,
            error=error_msg,
            output="",
            source="policy_check",
        )
    elif state.requires_tool_confirmation and tool_request.needs_confirmation:
        result = ToolResult(
            tool_name=tool_request.tool_name,
            success=False,
            error="Tool requires confirmation and no approval callback is configured",
            output="",
            source="policy_check",
        )
    else:
        try:
            executor = get_tool_executor(
                domain=tool_request.domain or "software_dev",
                workspace_root=state.workspace_root,
            )
            result = executor.execute(tool_request)
        except Exception as e:
            result = ToolResult(
                tool_name=tool_request.tool_name,
                success=False,
                error=str(e),
                output="",
                source="executor",
            )

    tool_request.status = "executed" if result.success else "failed"
    state.register_tool_request(tool_request)
    state.register_tool_result(result)

    # One logical iteration per request/result pair.
    state.tool_iteration -= 1

    observation = (
        f"Tool '{tool_request.tool_name}' result: {result.output[:500]}"
        if result.success
        else f"Tool '{tool_request.tool_name}' failed: {result.error}"
    )
    state.analysis_notes.append(observation)
    return state


def should_continue_tool_loop(state: AgentState) -> bool:
    if state.tool_iteration >= state.max_tool_iterations:
        return False

    last_agent = state.agent_chain[-1] if state.agent_chain else None
    if not last_agent:
        return False

    last_output = state.intermediate_outputs.get(last_agent)
    if not last_output:
        return False

    has_tool_request = parse_tool_request_from_output(last_output) is not None
    return has_tool_request


def build_agent_with_tools_subgraph(
    graph: any,
    agent_node_name: str,
    agent_callable: callable,
    next_node_name: str = None,
) -> any:
    """Attach an executor node to an existing agent node in a graph.

    agent_callable is accepted for backwards compatibility but not used.
    The caller should add the agent node before calling this helper.
    """
    _ = agent_callable
    graph.add_node(f"{agent_node_name}__executor", tool_executor_node)

    graph.add_edge(agent_node_name, f"{agent_node_name}__executor")

    if next_node_name:
        graph.add_conditional_edges(
            f"{agent_node_name}__executor",
            should_continue_tool_loop,
            {
                True: agent_node_name,
                False: next_node_name,
            },
        )
    elif next_node_name is None:
        graph.add_edge(f"{agent_node_name}__executor", agent_node_name)

    return graph
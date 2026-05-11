# STILL IN DEV
"""Tooling package exports with lazy loading to avoid import cycles."""

from .contracts import ToolPolicy, ToolRequest, ToolResult
from .prompts import build_tooling_block, get_allowed_tools

__all__ = [
    "ToolPolicy",
    "ToolRequest",
    "ToolResult",
    "build_tooling_block",
    "get_allowed_tools",
    "BaseToolExecutor",
    "VSCodeToolExecutor",
    "IDAToolExecutor",
    "get_tool_executor",
    "tool_executor_node",
    "should_continue_tool_loop",
    "parse_tool_request_from_output",
    "build_agent_with_tools_subgraph",
]

def __getattr__(name: str):
    if name in {"BaseToolExecutor", "VSCodeToolExecutor", "IDAToolExecutor", "get_tool_executor"}:
        from .tool_executor import BaseToolExecutor, VSCodeToolExecutor, IDAToolExecutor, get_tool_executor

        mapping = {
            "BaseToolExecutor": BaseToolExecutor,
            "VSCodeToolExecutor": VSCodeToolExecutor,
            "IDAToolExecutor": IDAToolExecutor,
            "get_tool_executor": get_tool_executor,
        }
        return mapping[name]

    if name in {
        "tool_executor_node",
        "should_continue_tool_loop",
        "parse_tool_request_from_output",
        "build_agent_with_tools_subgraph",
    }:
        from .tool_executor_node import (
            build_agent_with_tools_subgraph,
            parse_tool_request_from_output,
            should_continue_tool_loop,
            tool_executor_node,
        )
        mapping = {
            "tool_executor_node": tool_executor_node,
            "should_continue_tool_loop": should_continue_tool_loop,
            "parse_tool_request_from_output": parse_tool_request_from_output,
            "build_agent_with_tools_subgraph": build_agent_with_tools_subgraph,
        }
        return mapping[name]

    raise AttributeError(f"module 'langgraph_orchestration.tooling' has no attribute {name}")
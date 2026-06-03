# STILL IN DEV
"""Shared prompt helpers for local tool-calling behavior"""

from __future__ import annotations
from typing import Iterable
from langgraph_orchestration.prompts import render_prompt

_SOFTWARE_DEV_ALLOWED_TOOLS = [
    "read_file",
    "read_many_files",
    "search_repository",
    "get_errors",
    "create_file",
    "edit_file",
]

_REVERSE_ENGINEERING_ALLOWED_TOOLS = [
    "read_file",
    "read_many_files",
    "read_decompilation",
    "read_disassembly",
    "xrefs_to",
    "xrefs_from",
    "lookup_funcs",
    "basic_blocks",
    "ipsw_cli",
    "ipsw_download",
    "ipsw_extract",
    "ipsw_diff",
]

def get_allowed_tools(domain: str) -> list[str]:
    if domain == "reverse_engineering":
        return list(_REVERSE_ENGINEERING_ALLOWED_TOOLS)
    return list(_SOFTWARE_DEV_ALLOWED_TOOLS)

def _format_tools(tool_names: Iterable[str]) -> str:
    return "\n".join(f"- {tool}" for tool in tool_names)

def build_tooling_block(domain: str, user_input: str, task_focus: str) -> str:
    if domain == "reverse_engineering":
        allowed_tools = _format_tools(_REVERSE_ENGINEERING_ALLOWED_TOOLS)
    else:
        allowed_tools = _format_tools(_SOFTWARE_DEV_ALLOWED_TOOLS)

    _, body = render_prompt(
        "shared/tooling.md",
        domain=domain,
        allowed_tools=allowed_tools,
        task_focus=task_focus,
        user_input=user_input,
    )
    return body
# STILL IN DEV
"""Provide a stable schema for IDE plugins"""

from __future__ import annotations
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field

ToolStatus = Literal["requested", "approved", "executed", "failed", "skipped"]

class ToolRequest(BaseModel):
    type: Literal["tool_request"] = "tool_request"
    tool_name: str = Field(description="Official tool name requested from the host")
    arguments: dict[str, Any] = Field(default_factory=dict)
    target: Optional[str] = Field(
        default=None,
        description="File, function, artifact, database object, or other target of the request",
    )
    reason: str = Field(description="Why this tool is needed before proceeding")
    needs_confirmation: bool = Field(
        default=False,
        description="Whether the host should require explicit approval before executing",
    )
    expected_outcome: Optional[str] = Field(
        default=None,
        description="What evidence or effect the agent expects from the tool",
    )
    status: ToolStatus = "requested"
    domain: Optional[Literal["software_dev", "reverse_engineering"]] = None
    repository_hint: Optional[str] = Field(
        default=None,
        description="Optional repo, workspace, or database identifier for the host to bind",
    )

class ToolResult(BaseModel):
    """Structured response returned by a host-side tool executor"""
    type: Literal["tool_result"] = "tool_result"
    tool_name: str = Field(description="Tool that produced this result")
    success: bool = True
    output: str = Field(description="User-visible or agent-visible tool output")
    error: Optional[str] = None
    source: Optional[str] = Field(
        default=None,
        description="Host source that executed the tool, for example IDA or VS Code",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)

class ToolPolicy(BaseModel):
    requires_context_before_write: bool = True
    confirm_destructive_actions: bool = True
    max_iterations: int = 8
    allowed_tools: list[str] = Field(default_factory=list)
    read_only_until_context_complete: bool = True
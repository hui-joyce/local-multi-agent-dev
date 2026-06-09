"""Shared state schema for LangGraph orchestration.

Defines the data structure that flows through the agent graph,
incl. user input, retrieved context, outputs from agents, and
tool-call history for local agentic workflows.
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal
from langgraph_orchestration.tooling.tool import ToolPolicy, ToolRequest, ToolResult

class AgentState(BaseModel):
    user_input: str = Field(description="The original user request/query")

    selected_domain: Optional[Literal["software_dev", "reverse_engineering"]] = Field(
        default=None,
        description="Primary domain selected by supervisor routing",
    )

    execution_domains: list[Literal["software_dev", "reverse_engineering"]] = Field(
        default_factory=list,
        description="Domain execution plan selected by supervisor",
    )

    split_tasks: dict[str, str] = Field(
        default_factory=dict,
        description="Optional domain-specific subtasks when request is split across domains",
    )

    tool_policy: ToolPolicy = Field(
        default_factory=ToolPolicy,
        description="Local-only tool policy used by the active workflow",
    )

    tool_requests: list[ToolRequest] = Field(
        default_factory=list,
        description="Structured tool requests emitted during the current run",
    )

    tool_results: list[ToolResult] = Field(
        default_factory=list,
        description="Structured tool results returned by the host-side executor",
    )

    tool_iteration: int = Field(
        default=0,
        description="Current count of tool-request and observation events",
    )

    max_tool_iterations: int = Field(
        default=40,
        description="Maximum tool loop iterations before forcing synthesis",
    )

    requires_tool_confirmation: bool = Field(
        default=True,
        description="Whether write/edit actions must be confirmed before execution",
    )

    workspace_root: Optional[str] = Field(
        default=None,
        description="Optional repository or IDA workspace root for host-side execution",
    )

    analysis_notes: list[str] = Field(
        default_factory=list,
        description="High-level analysis notes produced while gathering evidence",
    )

    retrieved_context: list[str] = Field(
        default_factory=list,
        description="Combined context documents retrieved across active branches",
    )

    dev_context: list[str] = Field(
        default_factory=list,
        description="Domain-specific context retrieved for software development branch",
    )

    dev_task_plan: list[str] = Field(
        default_factory=list,
        description="LLM-selected execution plan for software development branch",
    )

    re_context: list[str] = Field(
        default_factory=list,
        description="Domain-specific context retrieved for reverse engineering branch",
    )

    re_task_plan: list[str] = Field(
        default_factory=list,
        description="LLM-selected execution plan for reverse engineering branch",
    )

    feature_analysis_targets: list[dict[str, str]] = Field(
        default_factory=list,
        description="Feature analysis targets selected from diff report",
    )

    feature_analysis_queue: list[dict[str, str]] = Field(
        default_factory=list,
        description="Pending feature analysis targets",
    )

    feature_analysis_current: Optional[dict[str, str]] = Field(
        default=None,
        description="Active feature analysis target",
    )

    feature_analysis_reports: dict[str, str] = Field(
        default_factory=dict,
        description="Generated feature analysis reports keyed by feature name",
    )

    intermediate_outputs: dict[str, str] = Field(
        default_factory=dict,
        description="Outputs from individual agents {agent_name: output}",
    )

    branch_outputs: dict[str, str] = Field(
        default_factory=dict,
        description="Branch-level synthesized outputs keyed by branch name",
    )

    dev_test_passed: bool = Field(
        default=False,
        description="Latest unit testing status for software development branch",
    )

    dev_iteration: int = Field(
        default=0,
        description="Current software development regeneration iteration count",
    )

    max_dev_iterations: int = Field(
        default=3,
        description="Maximum code generation retry attempts when tests fail",
    )

    final_output: Optional[str] = Field(
        default=None,
        description="Final synthesized output for the user",
    )

    agent_chain: list[str] = Field(
        default_factory=list,
        description="Sequence of agents executed (for auditing)",
    )

    firmware_methods_queue: list[list[str]] = Field(
        default_factory=list,
        description="Queue of chunked method signatures for categorization",
    )

    firmware_methods_current_chunk: list[str] = Field(
        default_factory=list,
        description="Current chunk of methods being categorized",
    )

    categorized_methods: list[dict] = Field(
        default_factory=list,
        description="Accumulated strict JSON output of categorized methods",
    )

    def register_tool_request(self, request: ToolRequest) -> None:
        self.tool_requests.append(request)
        self.tool_iteration += 1

    def register_tool_result(self, result: ToolResult) -> None:
        self.tool_results.append(result)
        self.tool_iteration += 1

    def record_analysis_note(self, note: str) -> None:
        cleaned = note.strip()
        if cleaned:
            self.analysis_notes.append(cleaned)

    class Config:
        arbitrary_types_allowed = True
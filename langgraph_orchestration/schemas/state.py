"""
Shared state schema for LangGraph orchestration.

Defines the data structure that flows through the agent graph,
including user input, retrieved context, and outputs from agents.
"""

from typing import Literal, Optional
from pydantic import BaseModel, Field

class AgentState(BaseModel):
    user_input: str = Field(
        description="The original user request/query"
    )
    
    selected_domain: Optional[Literal["software_dev", "reverse_engineering"]] = Field(
        default=None,
        description="Primary domain selected by supervisor routing"
    )

    execution_domains: list[Literal["software_dev", "reverse_engineering"]] = Field(
        default_factory=list,
        description="Domain execution plan selected by supervisor"
    )

    split_tasks: dict[str, str] = Field(
        default_factory=dict,
        description="Optional domain-specific subtasks when request is split across domains"
    )
    
    retrieved_context: list[str] = Field(
        default_factory=list,
        description="Combined context documents retrieved across active branches"
    )

    dev_context: list[str] = Field(
        default_factory=list,
        description="Domain-specific context retrieved for software development branch"
    )

    dev_task_plan: list[str] = Field(
        default_factory=list,
        description="LLM-selected execution plan for software development branch"
    )

    re_context: list[str] = Field(
        default_factory=list,
        description="Domain-specific context retrieved for reverse engineering branch"
    )

    re_task_plan: list[str] = Field(
        default_factory=list,
        description="LLM-selected execution plan for reverse engineering branch"
    )
    
    intermediate_outputs: dict[str, str] = Field(
        default_factory=dict,
        description="Outputs from individual agents {agent_name: output}"
    )

    branch_outputs: dict[str, str] = Field(
        default_factory=dict,
        description="Branch-level synthesized outputs keyed by branch name"
    )

    dev_test_passed: bool = Field(
        default=False,
        description="Latest unit testing status for software development branch"
    )

    dev_iteration: int = Field(
        default=0,
        description="Current software development regeneration iteration count"
    )

    max_dev_iterations: int = Field(
        default=3,
        description="Maximum code generation retry attempts when tests fail"
    )
    
    final_output: Optional[str] = Field(
        default=None,
        description="Final synthesized output for the user"
    )
    
    agent_chain: list[str] = Field(
        default_factory=list,
        description="Sequence of agents executed (for auditing)"
    )

    class Config:
        arbitrary_types_allowed = True
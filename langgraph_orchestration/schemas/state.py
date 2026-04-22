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
        description="Domain selected by supervisor routing"
    )
    
    retrieved_context: list[str] = Field(
        default_factory=list,
        description="Context documents retrieved from Qdrant RAG"
    )
    
    intermediate_outputs: dict[str, str] = Field(
        default_factory=dict,
        description="Outputs from individual agents {agent_name: output}"
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
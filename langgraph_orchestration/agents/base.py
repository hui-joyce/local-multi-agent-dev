"""
Base agent class defining the interface for all agents.

All agents in the system implement this interface for consistency
and seamless integration with LangGraph.
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseAgent(ABC):
    """
    Abstract base class for all agents in the orchestration system.
    
    Each agent implements a single specialized capability and can be
    invoked independently or as part of a domain-specific workflow.
    """
    
    def __init__(self, name: str, description: str):
        """
        Initialize a base agent.
        
        Args:
            name: Unique identifier for this agent
            description: Human-readable description of agent capability
        """
        self.name = name
        self.description = description
    
    @abstractmethod
    async def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        """
        Execute the agent on the given input.
        
        Args:
            user_input: The task or query for this agent
            context: Optional retrieved context from RAG
            
        Returns:
            The agent's output/response
        """
        pass


class SyncBaseAgent(ABC):
    """Synchronous version of BaseAgent for simpler blocking calls."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        """
        Execute the agent on the given input (synchronous).
        
        Args:
            user_input: The task or query for this agent
            context: Optional retrieved context from RAG
            
        Returns:
            The agent's output/response
        """
        pass

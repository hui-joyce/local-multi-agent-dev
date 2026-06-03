"""Base agent interfaces for orchestration"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseAgent(ABC):
    """Async agent interface"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    async def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        """Execute the agent on the given input."""
        pass


class SyncBaseAgent(ABC):
    """Sync agent interface"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> str:
        """Execute the agent on the given input"""
        pass
"""Base retriever interface"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseRetriever(ABC):
    """Abstract base class for RAG retrievers"""
    
    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        domain: Optional[str] = None,
    ) -> list[str]:
        """Retrieve relevant context for a query"""
        pass
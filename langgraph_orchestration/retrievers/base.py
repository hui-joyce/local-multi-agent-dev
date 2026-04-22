"""Base retriever interface for RAG components."""

from abc import ABC, abstractmethod
from typing import Optional


class BaseRetriever(ABC):
    """
    Abstract base class for RAG retrievers.
    
    Defines the interface for retrieving relevant context from
    knowledge bases or vector databases.
    """
    
    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        domain: Optional[str] = None,
    ) -> list[str]:
        """
        Retrieve relevant documents/context for a query.
        
        Args:
            query: The search query
            top_k: Number of results to return
            domain: Optional domain filter (software_dev or reverse_engineering)
            
        Returns:
            List of retrieved context documents
        """
        pass

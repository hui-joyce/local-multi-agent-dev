from typing import Optional
from .base import BaseRetriever


class QdrantRetriever(BaseRetriever):
    """    
    In production, this would connect to a real Qdrant instance
    with embedded documents. Currently uses mock data for demonstration.
    """
    
    # Mock knowledge base organized by domain
    MOCK_KNOWLEDGE_BASE = {
        "software_dev": [
            "Design Pattern: Repository Pattern provides abstraction for data access",
            "Unit Testing Best Practice: Use mocking for external dependencies",
            "API Design: RESTful endpoints should use HTTP status codes correctly",
            "Python: List comprehensions are more efficient than explicit loops",
            "Architecture: Microservices should maintain loose coupling",
            "Testing Strategy: Aim for 80%+ code coverage in critical paths",
            "Refactoring: Extract methods when functions exceed 20 lines",
            "Clean Code: Variable names should be intention-revealing",
        ],
        "reverse_engineering": [
            "Security: Buffer overflows require careful bounds checking",
            "Analysis: Use static analysis tools before dynamic analysis",
            "Vulnerability: Stack-based overflows have predictable patterns",
            "Reverse Engineering: Function prologue/epilogue reveal stack frames",
            "Assembly: x86-64 calling conventions differ on Windows vs Linux",
            "Binary Analysis: Ghidra provides high-quality decompilation",
            "Security Testing: Fuzzing reveals edge cases in input handling",
            "Cryptography: Weak RNG leads to predictable security tokens",
        ],
    }
    
    def __init__(self):
        """Initialize Qdrant retriever with mock data."""
        self.knowledge_base = self.MOCK_KNOWLEDGE_BASE
        self.collection_name = "multi_agent_knowledge"
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        domain: Optional[str] = None,
    ) -> list[str]:
        """        
        In production, this would:
        1. Embed the query using a sentence transformer
        2. Search Qdrant vector database for nearest neighbors
        3. Return top-k results with scores
        
        For now, we use simple keyword-based retrieval on mock data.
        """
        # Select knowledge base for the domain
        if domain and domain in self.knowledge_base:
            kb = self.knowledge_base[domain]
        else:
            # Combine all knowledge if no domain specified
            kb = []
            for docs in self.knowledge_base.values():
                kb.extend(docs)
        
        # Simple keyword-based ranking (in production: semantic similarity via embeddings)
        query_terms = set(query.lower().split())
        
        scored_docs = []
        for doc in kb:
            doc_terms = set(doc.lower().split())
            overlap = len(query_terms & doc_terms)
            if overlap > 0:
                scored_docs.append((overlap, doc))
        
        # Sort by relevance score (descending) and return top-k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        results = [doc for _, doc in scored_docs[:top_k]]
        
        # If fewer results than requested, fill with general context
        if len(results) < top_k:
            remaining_kb = [doc for doc in kb if doc not in results]
            results.extend(remaining_kb[:top_k - len(results)])
        
        return results[:top_k]
    
    def add_documents(self, documents: list[str], domain: str) -> None:
        """
        Add documents to the knowledge base.
        
        In production, this would upload embeddings to Qdrant.
        Currently just extends mock data.
        
        Args:
            documents: List of documents to add
            domain: Domain to add documents to
        """
        if domain not in self.knowledge_base:
            self.knowledge_base[domain] = []
        self.knowledge_base[domain].extend(documents)
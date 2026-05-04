import logging
from typing import Optional
from functools import lru_cache

logger = logging.getLogger(__name__)

class RAGManager:    
    def __init__(self, retriever, cache_size: int = 128):
        self.retriever = retriever
        self.cache_size = cache_size
        self._setup_cache()
    
    def _setup_cache(self):
        # Create cached retrieve function
        @lru_cache(maxsize=self.cache_size)
        def _cached_retrieve(query: str, domain: Optional[str], top_k: int):
            return tuple(
                self.retriever.retrieve(query, top_k=top_k, domain=domain)
            )
        
        self._cached_retrieve = _cached_retrieve
    
    def retrieve_for_agent(
        self,
        query: str,
        domain: Optional[str] = None,
        top_k: int = 5,
        use_cache: bool = True,
    ) -> list[str]:
        if use_cache:
            results = self._cached_retrieve(query, domain, top_k)
            return list(results)
        else:
            return self.retriever.retrieve(query, top_k=top_k, domain=domain)
    
    def retrieve_for_router(
        self,
        query: str,
        top_k: int = 3,
    ) -> list[str]:
        return self.retrieve_for_agent(query, domain=None, top_k=top_k)
    
    def retrieve_software_dev_context(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[str]:
        return self.retrieve_for_agent(
            query,
            domain="software_dev",
            top_k=top_k,
        )
    
    def retrieve_reverse_engineering_context(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[str]:
        return self.retrieve_for_agent(
            query,
            domain="reverse_engineering",
            top_k=top_k,
        )
    
    def clear_cache(self):
        self._cached_retrieve.cache_clear()
        logger.info("RAG cache cleared")
    
    def get_cache_info(self) -> dict:
        cache_info = self._cached_retrieve.cache_info()
        return {
            "hits": cache_info.hits,
            "misses": cache_info.misses,
            "size": cache_info.currsize,
            "maxsize": cache_info.maxsize,
            "hit_rate": (
                cache_info.hits / (cache_info.hits + cache_info.misses)
                if (cache_info.hits + cache_info.misses) > 0
                else 0
            ),
        }
    
    def build_context_string(
        self,
        documents: list[str],
        format_type: str = "markdown",
    ) -> str:
        if not documents:
            return ""
        
        if format_type == "markdown":
            return "## Retrieved Context\n\n" + "\n\n".join(
                f"{i}. {doc}" for i, doc in enumerate(documents, 1)
            )
        elif format_type == "plain":
            return "\n".join(f"- {doc}" for doc in documents)
        elif format_type == "xml":
            return ("<context>\n" + 
                    "\n".join(f"  <document>{doc}</document>" for doc in documents) +
                    "\n</context>")
        else:
            raise ValueError(f"Unknown format type: {format_type}")


class AdaptiveRAGManager(RAGManager):    
    def __init__(self, retriever, cache_size: int = 128):
        super().__init__(retriever, cache_size)
        self.domain_weights = {
            "software_dev": {"top_k": 5, "score_threshold": 0.3},
            "reverse_engineering": {"top_k": 7, "score_threshold": 0.25},
        }
    
    def retrieve_adaptive(
        self,
        query: str,
        domain: Optional[str] = None,
    ) -> list[str]:
        # Analyze query complexity
        query_length = len(query.split())
        query_complexity = "high" if query_length > 20 else "medium" if query_length > 10 else "low"
        
        # Determine top_k based on complexity
        base_top_k = self.domain_weights.get(domain, {}).get("top_k", 5)
        
        if query_complexity == "high":
            top_k = base_top_k + 2
        elif query_complexity == "low":
            top_k = max(3, base_top_k - 1)
        else:
            top_k = base_top_k
        
        return self.retrieve_for_agent(query, domain=domain, top_k=top_k)
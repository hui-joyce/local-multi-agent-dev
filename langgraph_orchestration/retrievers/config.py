import os
import json
import logging
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict

class RAGManager:
    def __init__(self, retriever, cache_size: int = 128):
        self.retriever = retriever

    def retrieve_for_agent(
        self,
        query: str,
        domain: Optional[str] = None,
        top_k: int = 5,
        use_cache: bool = True,
    ) -> list[str]:
        return self.retriever.retrieve(query, top_k=top_k, domain=domain)

    def retrieve_for_router(self, query: str, top_k: int = 3) -> list[str]:
        return self.retrieve_for_agent(query, top_k=top_k)

    def retrieve_software_dev_context(self, query: str, top_k: int = 5) -> list[str]:
        return self.retrieve_for_agent(query, domain="software_dev", top_k=top_k)

    def retrieve_reverse_engineering_context(self, query: str, top_k: int = 5) -> list[str]:
        return self.retrieve_for_agent(query, domain="reverse_engineering", top_k=top_k)

class RAGAdminService:
    def __init__(self, retriever):
        self.retriever = retriever

    def add_document(
        self,
        text: str,
        domain: str,
        metadata: Optional[dict] = None,
    ) -> dict:
        if not text or not isinstance(text, str):
            return {"status": "error", "message": "Invalid text"}

        try:
            payload = dict(metadata or {})
            payload["added_at"] = datetime.utcnow().isoformat()
            self.retriever.add_documents([text], domain, metadata=[payload])

            return {
                "status": "success",
                "message": f"Document added to {domain}",
                "text": text[:100] + "..." if len(text) > 100 else text,
            }
        except Exception as e:
            logging.getLogger(__name__).error("Failed to add document: %s", e)
            return {"status": "error", "message": str(e)}

    def add_documents_batch(
        self,
        documents: list[dict],
        domain: str,
    ) -> dict:
        if not documents:
            return {"status": "error", "message": "No documents provided"}

        try:
            texts = []
            metadatas = []

            for doc in documents:
                if isinstance(doc, str):
                    texts.append(doc)
                    metadatas.append({"added_at": datetime.utcnow().isoformat()})
                elif isinstance(doc, dict):
                    texts.append(doc.get("text", ""))
                    payload = dict(doc.get("metadata", {}))
                    payload["added_at"] = datetime.utcnow().isoformat()
                    metadatas.append(payload)
                else:
                    logging.getLogger(__name__).warning("Skipping invalid document: %s", doc)

            texts = [text for text in texts if text]
            if not texts:
                return {"status": "error", "message": "No valid documents provided"}

            self.retriever.add_documents(texts, domain, metadata=metadatas)

            return {
                "status": "success",
                "message": f"Added {len(texts)} documents to {domain}",
                "count": len(texts),
            }
        except Exception as e:
            logging.getLogger(__name__).error("Batch add failed: %s", e)
            return {"status": "error", "message": str(e)}

    def delete_domain(self, domain: str) -> dict:
        try:
            self.retriever.delete_collection(domain)
            return {
                "status": "success",
                "message": f"Cleared all documents in {domain}",
            }
        except Exception as e:
            logging.getLogger(__name__).error("Delete domain failed: %s", e)
            return {"status": "error", "message": str(e)}

    def get_statistics(self) -> dict:
        try:
            stats = {}
            total_docs = 0

            for domain in ["software_dev", "reverse_engineering", "shared"]:
                info = self.retriever.get_collection_info(domain)
                stats[domain] = info
                if "document_count" in info:
                    total_docs += info["document_count"]

            return {
                "status": "success",
                "collections": stats,
                "total_documents": total_docs,
            }
        except Exception as e:
            logging.getLogger(__name__).error("Failed to get statistics: %s", e)
            return {"status": "error", "message": str(e)}

    def search_documents(
        self,
        query: str,
        domain: Optional[str] = None,
        top_k: int = 10,
    ) -> dict:
        try:
            results = self.retriever.retrieve(query, top_k=top_k, domain=domain)
            return {
                "status": "success",
                "query": query,
                "domain": domain,
                "results": results,
                "count": len(results),
            }
        except Exception as e:
            logging.getLogger(__name__).error("Search failed: %s", e)
            return {"status": "error", "message": str(e)}

@dataclass
class RAGConfig:
    db_path: str
    db_mode: str
    embedding_model: str
    embedding_device: str
    embedding_cache_dir: str
    default_top_k: int
    score_threshold: float
    enable_fallback: bool
    cache_size: int
    enable_logging: bool
    log_level: str
    
    db_url: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "RAGConfig":
        embedding_model = os.getenv("RAG_EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")
        return cls(
            db_path=os.getenv("RAG_DB_PATH", "~/.local/share/qdrant"),
            db_mode=os.getenv("RAG_DB_MODE", "embedded"),
            db_url=os.getenv("RAG_DB_URL"),
            embedding_model=embedding_model,
            embedding_device=os.getenv("RAG_EMBEDDING_DEVICE") or "",
            embedding_cache_dir=os.getenv("RAG_EMBEDDING_CACHE_DIR", "~/.cache/huggingface"),
            default_top_k=int(os.getenv("RAG_DEFAULT_TOP_K", "5")),
            score_threshold=float(os.getenv("RAG_SCORE_THRESHOLD", "0.3")),
            enable_fallback=os.getenv("RAG_ENABLE_FALLBACK", "true").lower() == "true",
            cache_size=int(os.getenv("RAG_CACHE_SIZE", "128")),
            enable_logging=os.getenv("RAG_ENABLE_LOGGING", "true").lower() == "true",
            log_level=os.getenv("RAG_LOG_LEVEL", "INFO"),
        )
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def validate(self) -> list[str]:
        errors = []
        if self.db_mode not in ["embedded", "remote"]:
            errors.append(f"Invalid db_mode: {self.db_mode}")
        
        if self.db_mode == "remote" and not self.db_url:
            errors.append("db_url required for remote mode")
        
        if self.default_top_k < 1:
            errors.append("default_top_k must be >= 1")
        
        if not (0 <= self.score_threshold <= 1):
            errors.append("score_threshold must be between 0 and 1")
        
        if self.cache_size < 0:
            errors.append("cache_size must be >= 0")
        
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            errors.append(f"Invalid log_level: {self.log_level}")
        
        return errors

class RAGConfigManager:
    _instance = None
    _config: Optional[RAGConfig] = None
    _retriever = None
    _rag_manager = None
    _admin_service = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def initialize(cls, config: Optional[RAGConfig] = None) -> None:
        manager = cls()
        
        if manager._retriever is not None and manager._config is not None:
            return
        
        if config is None:
            config = RAGConfig.from_env()
        
        errors = config.validate()
        if errors:
            raise ValueError(f"Configuration errors: {errors}")
        
        manager._config = config
        
        if config.enable_logging:
            import logging
            logging.basicConfig(level=config.log_level)
        
        manager._init_retriever()
    
    @classmethod
    def _init_retriever(cls):
        from langgraph_orchestration.retrievers.qdrant_client import QdrantRetriever
        
        manager = cls()
        
        # Prevent re-initialization if already exists
        if manager._retriever is not None:
            return
        
        config = manager._config
        
        if config is None:
            raise RuntimeError("RAGConfigManager not initialized. Call initialize() first.")
        
        if config.db_mode == "embedded":
            manager._retriever = QdrantRetriever(
                db_path=config.db_path,
                embedding_model=config.embedding_model,
                embedding_cache_dir=config.embedding_cache_dir,
                embedding_device=config.embedding_device or None,
                enable_fallback=config.enable_fallback,
            )
        else:
            raise NotImplementedError("Remote Qdrant mode not yet implemented")
    
    @classmethod
    def get_retriever(cls):
        manager = cls()
        if manager._retriever is None:
            manager._init_retriever()
        return manager._retriever
    
    @classmethod
    def get_rag_manager(cls):
        manager = cls()
        
        if manager._rag_manager is None:
            retriever = manager.get_retriever()
            config = manager._config
            manager._rag_manager = RAGManager(retriever, cache_size=config.cache_size)
        
        return manager._rag_manager
    
    @classmethod
    def get_admin_service(cls):
        manager = cls()
        
        if manager._admin_service is None:
            retriever = manager.get_retriever()
            manager._admin_service = RAGAdminService(retriever)
        
        return manager._admin_service
    
    @classmethod
    def get_config(cls) -> RAGConfig:
        manager = cls()
        if manager._config is None:
            manager._config = RAGConfig.from_env()
        return manager._config
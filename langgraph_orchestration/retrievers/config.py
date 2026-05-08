import os
from typing import Optional
from pathlib import Path
from dataclasses import dataclass, asdict

@dataclass
class RAGConfig:
    db_path: str
    db_mode: str
    embedding_model: str
    embedding_model_shared: str
    embedding_model_software_dev: str
    embedding_model_reverse_engineering: str
    embedding_device: str
    embedding_cache_dir: str
    default_top_k: int
    score_threshold: float
    enable_fallback: bool
    cache_size: int
    enable_adaptive_retrieval: bool
    enable_logging: bool
    log_level: str
    
    db_url: Optional[str] = None  # For remote mode
    
    @classmethod
    def from_env(cls) -> "RAGConfig":
        embedding_model = os.getenv(
            "RAG_EMBEDDING_MODEL",
            "mlx-community/Qwen3-Embedding-0.6B-4bit-DWQ",
        )
        return cls(
            db_path=os.getenv("RAG_DB_PATH", "~/.local/share/qdrant"),
            db_mode=os.getenv("RAG_DB_MODE", "embedded"),
            db_url=os.getenv("RAG_DB_URL"),
            embedding_model=embedding_model,
            embedding_model_shared=os.getenv("RAG_EMBEDDING_MODEL_SHARED", embedding_model),
            embedding_model_software_dev=os.getenv("RAG_EMBEDDING_MODEL_SOFTWARE_DEV", embedding_model),
            embedding_model_reverse_engineering=os.getenv(
                "RAG_EMBEDDING_MODEL_REVERSE_ENGINEERING",
                embedding_model,
            ),
            embedding_device=os.getenv("RAG_EMBEDDING_DEVICE") or "",  # Empty string for auto-detection
            embedding_cache_dir=os.getenv("RAG_EMBEDDING_CACHE_DIR", "~/.cache/huggingface"),
            default_top_k=int(os.getenv("RAG_DEFAULT_TOP_K", "5")),
            score_threshold=float(os.getenv("RAG_SCORE_THRESHOLD", "0.3")),
            enable_fallback=os.getenv("RAG_ENABLE_FALLBACK", "true").lower() == "true",
            cache_size=int(os.getenv("RAG_CACHE_SIZE", "128")),
            enable_adaptive_retrieval=os.getenv("RAG_ENABLE_ADAPTIVE", "false").lower() == "true",
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

    def get_embedding_model(self, domain: Optional[str] = None) -> str:
        if domain == "software_dev":
            return self.embedding_model_software_dev
        if domain == "reverse_engineering":
            return self.embedding_model_reverse_engineering
        if domain == "shared":
            return self.embedding_model_shared
        return self.embedding_model


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
        
        # Validate configuration
        errors = config.validate()
        if errors:
            raise ValueError(f"Configuration errors: {errors}")
        
        manager._config = config
        
        # Setup logging
        if config.enable_logging:
            import logging
            logging.basicConfig(level=config.log_level)
        
        # Initialize retriever
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
                domain_embedding_models={
                    "shared": config.embedding_model_shared,
                    "software_dev": config.embedding_model_software_dev,
                    "reverse_engineering": config.embedding_model_reverse_engineering,
                },
                embedding_cache_dir=config.embedding_cache_dir,
                embedding_device=config.embedding_device or None,
                enable_fallback=config.enable_fallback,
            )
        else:
            # Remote mode would require different client
            raise NotImplementedError("Remote Qdrant mode not yet implemented")
    
    @classmethod
    def get_retriever(cls):
        manager = cls()
        if manager._retriever is None:
            manager._init_retriever()
        return manager._retriever
    
    @classmethod
    def get_rag_manager(cls):
        from langgraph_orchestration.retrievers.rag_manager import RAGManager, AdaptiveRAGManager
        
        manager = cls()
        
        if manager._rag_manager is None:
            retriever = manager.get_retriever()
            config = manager._config
            
            if config.enable_adaptive_retrieval:
                manager._rag_manager = AdaptiveRAGManager(retriever, cache_size=config.cache_size)
            else:
                manager._rag_manager = RAGManager(retriever, cache_size=config.cache_size)
        
        return manager._rag_manager
    
    @classmethod
    def get_admin_service(cls):
        from langgraph_orchestration.retrievers.admin_service import RAGAdminService
        
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
"""
- Embedded Qdrant 
- Local semantic search
- Domain-specific collections
- Persistent storage
- Batch operations for efficiency
"""

import os
import time
from typing import Optional
from pathlib import Path
from datetime import datetime
import logging

from .base import BaseRetriever
from .embeddings import EmbeddingService

logger = logging.getLogger(__name__)

class QdrantRetriever(BaseRetriever):
    
    # Default Qdrant configuration
    DEFAULT_DB_PATH = "~/.local/share/qdrant"
    DEFAULT_COLLECTION_PREFIX = "agents_"
    
    # Known model vector dimensions (to avoid loading models during init)
    MODEL_VECTOR_SIZES = {
        "mlx-community/Qwen3-Embedding-0.6B-4bit-DWQ": 384,
        "sentence-transformers/all-MiniLM-L6-v2": 384,
        # Add more as needed
    }
    
    def __init__(
        self,
        db_path: Optional[str] = None,
        embedding_model: str = "mlx-community/Qwen3-Embedding-0.6B-4bit-DWQ",
        domain_embedding_models: Optional[dict[str, str]] = None,
        embedding_cache_dir: Optional[str] = None,
        embedding_device: Optional[str] = None,
        enable_fallback: bool = True,
    ):
        self.db_path = Path(db_path or self.DEFAULT_DB_PATH).expanduser()
        self.db_path.mkdir(parents=True, exist_ok=True)

        self.domain_embedding_models = domain_embedding_models or {
            "shared": embedding_model,
            "software_dev": embedding_model,
            "reverse_engineering": embedding_model,
        }
        self.embedding_cache_dir = embedding_cache_dir
        self.embedding_device = embedding_device
        self.embedding_services: dict[str, EmbeddingService] = {}
        self.enable_fallback = enable_fallback
        
        # Initialize Qdrant client
        self._init_qdrant_client()
        
        # Domain collections
        self.domain_collections = {
            "software_dev": f"{self.DEFAULT_COLLECTION_PREFIX}software_dev",
            "reverse_engineering": f"{self.DEFAULT_COLLECTION_PREFIX}reverse_engineering",
            "shared": f"{self.DEFAULT_COLLECTION_PREFIX}shared",
        }
        
        # Initialize collections
        for domain in self.domain_collections:
            self._ensure_collection(domain)

        # Backwards-compatible default service reference (lazy loaded)
        self._embedding_service = None
        self._embedding_dim = None
        
        logger.info(f"✓ Qdrant retriever initialized at {self.db_path}")

    def _get_embedding_service(self, domain: Optional[str] = None) -> EmbeddingService:
        domain_key = domain if domain in self.domain_collections else "shared"
        if domain_key not in self.embedding_services:
            model_name = self.domain_embedding_models.get(domain_key) or self.domain_embedding_models.get("shared")
            if not model_name:
                model_name = next(iter(self.domain_embedding_models.values()))
            self.embedding_services[domain_key] = EmbeddingService(
                model_name=model_name,
                cache_dir=self.embedding_cache_dir,
                device=self.embedding_device,
            )
        return self.embedding_services[domain_key]

    @property
    def embedding_dim(self) -> int:
        """Lazy-load embedding dimension on first access"""
        if self._embedding_dim is None:
            service = self._get_embedding_service("shared")
            self._embedding_dim = service.get_embedding_dimension()
        return self._embedding_dim

    @property
    def embedding_service(self) -> EmbeddingService:
        """Lazy-load embedding service on first access"""
        if self._embedding_service is None:
            self._embedding_service = self._get_embedding_service("shared")
        return self._embedding_service

    def _get_collection_name(self, domain: str) -> str:
        if domain not in self.domain_collections:
            raise ValueError(f"Unknown domain: {domain}")
        return self.domain_collections[domain]
    
    def _init_qdrant_client(self):
        try:
            from qdrant_client import QdrantClient
        except ImportError:
            raise ImportError(
                "qdrant-client is required. Install with: pip install qdrant-client"
            )
        
        max_retries = 5
        retry_delay = 0.5
        last_error = None
        
        for attempt in range(max_retries):
            try:
                self.client = QdrantClient(
                    path=str(self.db_path),
                    prefer_grpc=False,
                )
                logger.info("✓ Qdrant client initialized in embedded mode")
                return
            except Exception as e:
                last_error = e
                if "AlreadyLocked" in str(e) or "Resource temporarily unavailable" in str(e):
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2 ** attempt)
                        logger.warning(
                            f"Qdrant database locked (attempt {attempt + 1}/{max_retries}), "
                            f"retrying in {wait_time:.1f}s"
                        )
                        time.sleep(wait_time)
                        continue
                raise RuntimeError(f"Failed to initialize Qdrant: {e}")
        
        raise RuntimeError(f"Failed to initialize Qdrant after {max_retries} retries: {last_error}")

    def _ensure_collection(self, domain: str) -> None:
        collection_name = self._get_collection_name(domain)
        
        # Get vector size without loading the model
        embedding_model = self.domain_embedding_models.get(domain, self.domain_embedding_models.get("shared"))
        vector_size = self.MODEL_VECTOR_SIZES.get(embedding_model)
        
        if vector_size is None:
            # Only load model if we don't know the vector size
            vector_size = self._get_embedding_service(domain).get_embedding_dimension()
        
        try:
            collection_info = self.client.get_collection(collection_name)
        except Exception:
            # Collection doesn't exist, create it
            from qdrant_client.models import VectorParams, Distance
            
            try:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE,
                    ),
                )
                logger.info(f"Created collection: {collection_name}")
            except Exception as e:
                logger.error(f"Failed to create collection {collection_name}: {e}")
                raise
            return

        current_size = None
        try:
            current_size = collection_info.config.params.vectors.size
        except Exception:
            logger.debug(f"Could not inspect vector size for {collection_name}")

        if current_size is not None and current_size != vector_size:
            raise RuntimeError(
                f"Collection {collection_name} uses vector size {current_size}, "
                f"but {domain} requires {vector_size}. Rebuild the collection or use a matching model."
            )
    
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        domain: Optional[str] = None,
        score_threshold: float = 0.3,
    ) -> list[str]:
        if not query or not isinstance(query, str):
            logger.warning("Invalid query provided to retrieve")
            return []
        
        try:
            # Determine which domains to search
            domains = [domain] if domain and domain in self.domain_collections else list(self.domain_collections.keys())
            
            # Collect results from all relevant collections
            all_results = []
            
            for search_domain in domains:
                embedding_service = self._get_embedding_service(search_domain)
                query_embedding = embedding_service.embed_text(query)
                query_embedding_list = query_embedding.tolist()
                collection_name = self._get_collection_name(search_domain)

                try:
                    search_result = self.client.query_points(
                        collection_name=collection_name,
                        query=query_embedding_list,
                        limit=top_k * 2,
                        score_threshold=score_threshold,
                    )
                    
                    for hit in search_result:
                        all_results.append({
                            "text": hit.payload.get("text", ""),
                            "score": hit.score,
                            "collection": collection_name,
                            "metadata": hit.payload.get("metadata", {}),
                        })
                
                except Exception as e:
                    logger.warning(f"Search in {collection_name} failed: {e}")
            
            all_results.sort(key=lambda x: x["score"], reverse=True)
            results = [r["text"] for r in all_results[:top_k]]
            
            if not results and self.enable_fallback:
                logger.info("No semantic results found, attempting keyword fallback")
                results = self._keyword_fallback(query, top_k, domain)
            
            return results
        
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            if self.enable_fallback:
                return self._keyword_fallback(query, top_k, domain)
            return []
    
    def _keyword_fallback(
        self,
        query: str,
        top_k: int,
        domain: Optional[str],
    ) -> list[str]:
        query_terms = set(query.lower().split())        
        all_docs = []
        
        if domain and domain in self.domain_collections:
            collections = [self.domain_collections[domain]]
        else:
            collections = list(self.domain_collections.values())
        
        for collection_name in collections:
            try:
                scroll_result = self.client.scroll(
                    collection_name=collection_name,
                    limit=1000,
                )
                for point in scroll_result[0]:
                    all_docs.append(point.payload.get("text", ""))
            except Exception as e:
                logger.debug(f"Scroll failed for {collection_name}: {e}")
        
        # Simple keyword matching
        scored = []
        for doc in all_docs:
            doc_terms = set(doc.lower().split())
            overlap = len(query_terms & doc_terms)
            if overlap > 0:
                scored.append((overlap, doc))
        
        scored.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in scored[:top_k]]
    
    def add_documents(
        self,
        documents: list[str],
        domain: str,
        batch_size: int = 32,
        metadata: Optional[list[dict]] = None,
    ) -> None:
        """Add documents to the knowledge base."""
        if not documents:
            return
        
        if domain not in self.domain_collections:
            logger.warning(f"Unknown domain: {domain}. Using 'shared' instead.")
            domain = "shared"
        
        collection_name = self._get_collection_name(domain)
        embedding_service = self._get_embedding_service(domain)
        
        try:
            # Embed documents in batches
            embeddings = embedding_service.embed_batch(
                documents,
                batch_size=batch_size,
                normalize=True,
            )

            self._ensure_collection(domain)
            
            # Prepare points for insertion
            points = []
            for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
                point_id = self._generate_point_id(collection_name, doc)
                
                # Prepare metadata
                point_metadata = {
                    "text": doc,
                    "metadata": {
                        "timestamp": datetime.utcnow().isoformat(),
                        "domain": domain,
                        "source": "api",
                    }
                }
                
                if metadata and i < len(metadata):
                    point_metadata["metadata"].update(metadata[i])
                
                from qdrant_client.models import PointStruct
                
                points.append(
                    PointStruct(
                        id=point_id,
                        vector=embedding.tolist(),
                        payload=point_metadata,
                    )
                )
            
            # Upsert points (update if exists, insert if not)
            self.client.upsert(
                collection_name=collection_name,
                points=points,
            )
            
            logger.info(
                f"Added {len(documents)} documents to {collection_name} ({domain})"
            )
        
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    def delete_collection(self, domain: str) -> None:
        if domain not in self.domain_collections:
            logger.warning(f"Unknown domain: {domain}")
            return
        
        collection_name = self._get_collection_name(domain)
        try:
            self.client.delete_collection(collection_name)
            self._ensure_collection(domain)
            logger.info(f"Cleared collection: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
    
    def get_collection_info(self, domain: str) -> dict:
        if domain not in self.domain_collections:
            return {"error": f"Unknown domain: {domain}"}
        
        collection_name = self._get_collection_name(domain)
        try:
            collection_info = self.client.get_collection(collection_name)
            return {
                "name": collection_name,
                "domain": domain,
                "document_count": collection_info.points_count,
                "vector_size": self._get_embedding_service(domain).get_embedding_dimension(),
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {"error": str(e)}
    
    def _generate_point_id(self, collection_name: str, text: str) -> int:
        import hashlib
        # Use hash of text to create consistent IDs
        hash_value = int(
            hashlib.md5(f"{collection_name}:{text}".encode()).hexdigest(),
            16,
        ) % (2**31)  # Keep within 32-bit range
        return hash_value

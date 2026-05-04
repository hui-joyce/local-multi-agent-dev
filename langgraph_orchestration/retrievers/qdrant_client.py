"""
- Embedded Qdrant 
- Local semantic search with sentence-transformers
- Domain-specific collections
- Persistent storage
- Batch operations for efficiency
"""

import os
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
    
    def __init__(
        self,
        db_path: Optional[str] = None,
        embedding_model: str = "all-MiniLM-L6-v2",
        enable_fallback: bool = True,
    ):
        self.db_path = Path(db_path or self.DEFAULT_DB_PATH).expanduser()
        self.db_path.mkdir(parents=True, exist_ok=True)
        
        self.embedding_service = EmbeddingService(model_name=embedding_model)
        self.embedding_dim = self.embedding_service.get_embedding_dimension()
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
        for collection_name in self.domain_collections.values():
            self._ensure_collection(collection_name)
        
        logger.info(f"✓ Qdrant retriever initialized at {self.db_path}")
    
    def _init_qdrant_client(self):
        try:
            from qdrant_client import QdrantClient
        except ImportError:
            raise ImportError(
                "qdrant-client is required. Install with: pip install qdrant-client"
            )
        
        try:
            # Use embedded mode with local SQLite storage
            self.client = QdrantClient(
                path=str(self.db_path),
                prefer_grpc=False,  # Use HTTP for embedded mode
            )
            logger.info(f"✓ Qdrant client initialized in embedded mode")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Qdrant: {e}")
    
    def _ensure_collection(self, collection_name: str) -> None:
        try:
            self.client.get_collection(collection_name)
        except Exception:
            # Collection doesn't exist, create it
            from qdrant_client.models import VectorParams, Distance
            
            try:
                self.client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_dim,
                        distance=Distance.COSINE,
                    ),
                )
                logger.info(f"Created collection: {collection_name}")
            except Exception as e:
                logger.error(f"Failed to create collection {collection_name}: {e}")
                raise
    
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
            # Embed the query
            query_embedding = self.embedding_service.embed_text(query)
            query_embedding_list = query_embedding.tolist()
            
            # Determine which collections to search
            if domain and domain in self.domain_collections:
                collections = [self.domain_collections[domain]]
            else:
                # Search all domain collections + shared
                collections = list(self.domain_collections.values())
            
            # Collect results from all relevant collections
            all_results = []
            
            for collection_name in collections:
                try:
                    search_result = self.client.search(
                        collection_name=collection_name,
                        query_vector=query_embedding_list,
                        limit=top_k * 2,  # Get extra to account for filtering
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
                    if self.enable_fallback:
                        logger.info("Falling back to keyword search")
            
            # Sort by score and return top-k documents
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
        """Fallback keyword-based search."""
        query_terms = set(query.lower().split())
        
        # Get all documents from relevant collections
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
        
        collection_name = self.domain_collections[domain]
        
        try:
            # Embed documents in batches
            embeddings = self.embedding_service.embed_batch(
                documents,
                batch_size=batch_size,
                normalize=True,
            )
            
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
        
        collection_name = self.domain_collections[domain]
        try:
            self.client.delete_collection(collection_name)
            self._ensure_collection(collection_name)
            logger.info(f"Cleared collection: {collection_name}")
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
    
    def get_collection_info(self, domain: str) -> dict:
        """Get statistics for a collection"""
        if domain not in self.domain_collections:
            return {"error": f"Unknown domain: {domain}"}
        
        collection_name = self.domain_collections[domain]
        try:
            collection_info = self.client.get_collection(collection_name)
            return {
                "name": collection_name,
                "domain": domain,
                "document_count": collection_info.points_count,
                "vector_size": self.embedding_dim,
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {"error": str(e)}
    
    def _generate_point_id(self, collection_name: str, text: str) -> int:
        """Generate deterministic ID from text hash"""
        import hashlib
        # Use hash of text to create consistent IDs
        hash_value = int(
            hashlib.md5(f"{collection_name}:{text}".encode()).hexdigest(),
            16,
        ) % (2**31)  # Keep within 32-bit range
        return hash_value
"""
Provides operations for IDE plugins to manage documents and collections:
- Add/remove documents
- List documents by domain
- Bulk import/export
- Collection statistics
"""

import logging
import json
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

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
            if metadata is None:
                metadata = {}
            
            # Add source tracking
            metadata["added_at"] = datetime.utcnow().isoformat()
            
            self.retriever.add_documents([text], domain, metadata=[metadata])
            
            return {
                "status": "success",
                "message": f"Document added to {domain}",
                "text": text[:100] + "..." if len(text) > 100 else text,
            }
        except Exception as e:
            logger.error(f"Failed to add document: {e}")
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
                    metadata = doc.get("metadata", {})
                    metadata["added_at"] = datetime.utcnow().isoformat()
                    metadatas.append(metadata)
                else:
                    logger.warning(f"Skipping invalid document: {doc}")
            
            self.retriever.add_documents(texts, domain, metadata=metadatas)
            
            return {
                "status": "success",
                "message": f"Added {len(texts)} documents to {domain}",
                "count": len(texts),
            }
        except Exception as e:
            logger.error(f"Batch add failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def delete_domain(self, domain: str) -> dict:
        try:
            self.retriever.delete_collection(domain)
            return {
                "status": "success",
                "message": f"Cleared all documents in {domain}",
            }
        except Exception as e:
            logger.error(f"Delete domain failed: {e}")
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
            logger.error(f"Failed to get statistics: {e}")
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
            logger.error(f"Search failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def export_documents(self, domain: Optional[str] = None) -> dict:
        try:
            export_data = {
                "timestamp": datetime.utcnow().isoformat(),
                "domains": {},
            }
            
            domains = [domain] if domain else ["software_dev", "reverse_engineering", "shared"]
            
            for d in domains:
                collection_name = self.retriever.domain_collections.get(d)
                if not collection_name:
                    export_data["domains"][d] = {"error": f"Unknown domain: {d}"}
                    continue

                documents = []
                offset = None
                while True:
                    points, offset = self.retriever.client.scroll(
                        collection_name=collection_name,
                        limit=500,
                        offset=offset,
                        with_payload=True,
                    )
                    documents.extend([
                        {
                            "id": point.id,
                            "text": point.payload.get("text", ""),
                            "metadata": point.payload.get("metadata", {}),
                        }
                        for point in points
                    ])
                    if offset is None:
                        break

                export_data["domains"][d] = {
                    "collection": collection_name,
                    "document_count": len(documents),
                    "documents": documents,
                }
            
            return {"status": "success", "export": export_data}
        except Exception as e:
            logger.error(f"Export failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def import_documents_from_json(self, json_data: str) -> dict:
        try:
            data = json.loads(json_data)
            total_added = 0
            
            for domain, documents in data.items():
                if domain in ["software_dev", "reverse_engineering", "shared"]:
                    result = self.add_documents_batch(documents, domain)
                    if result["status"] == "success":
                        total_added += result.get("count", 0)
            
            return {
                "status": "success",
                "message": f"Imported {total_added} documents",
                "total": total_added,
            }
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            return {"status": "error", "message": f"Invalid JSON: {e}"}
        except Exception as e:
            logger.error(f"Import failed: {e}")
            return {"status": "error", "message": str(e)}
    
    def health_check(self) -> dict:
        try:
            stats = self.get_statistics()
            if stats["status"] == "success":
                return {
                    "status": "healthy",
                    "retriever": self.retriever.__class__.__name__,
                    "statistics": stats,
                }
            else:
                return {
                    "status": "degraded",
                    "message": stats.get("message", "Unknown error"),
                }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
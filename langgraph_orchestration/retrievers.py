"""Optional RAG scaffolding: embedded Qdrant plus local embeddings"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import numpy as np

from langgraph_orchestration.inference import in_hf_cache, models_dir, offline_mode

MODEL = "Qwen/Qwen3-Embedding-0.6B"

logger = logging.getLogger("mad.rag")

# Section: embedding model


def resolve_embedding_source(model_name: str = MODEL) -> str:
    """Local snapshot for *model_name* if downloaded, else its repo id"""
    explicit = os.getenv("RAG_EMBEDDING_PATH")
    if explicit:
        return str(Path(explicit).expanduser())
    local = models_dir() / model_name.replace("/", "__")
    return str(local) if (local / "config.json").is_file() else model_name


def _detect_default_device(preferred: str | None = None) -> str:
    if preferred:
        return preferred
    try:
        import torch

        if (
            hasattr(torch.backends, "mps")
            and torch.backends.mps.is_built()
            and torch.backends.mps.is_available()
        ):
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass
    return "cpu"


class EmbeddingService:
    _MODEL_CACHE: dict[tuple[str, str, str], tuple[object, object, int]] = {}

    def __init__(
        self,
        model_name: str = MODEL,
        cache_dir: str | None = None,
        device: str | None = None,
    ):
        self.model_name = model_name
        self.device = _detect_default_device(device)
        self.model = None
        self.tokenizer = None
        self.embedding_dim = None
        cache_dir = os.path.expanduser(cache_dir or "~/.cache/huggingface")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self._loaded = False

    @staticmethod
    def _is_mps_oom(error: Exception) -> bool:
        msg = str(error).lower()
        return "mps backend out of memory" in msg or ("mps" in msg and "out of memory" in msg)

    def _load_model(self):
        try:
            from transformers import AutoModel, AutoTokenizer
        except ImportError as e:
            raise ImportError(
                "transformers and torch are required for embeddings. "
                "Install with: pip install transformers torch"
            ) from e

        cache_key = (self.model_name, str(self.cache_dir), self.device)
        cached = self._MODEL_CACHE.get(cache_key)
        if cached is not None:
            self.tokenizer, self.model, self.embedding_dim = cached
            self._loaded = True
            return

        source = resolve_embedding_source(self.model_name)
        is_local = os.path.isdir(source)
        if offline_mode() and not is_local and not in_hf_cache(source, (str(self.cache_dir),)):
            raise RuntimeError(
                f"HF_HUB_OFFLINE=1 but the embedding model {self.model_name} is not "
                f"available locally (looked in {models_dir()}, {self.cache_dir} "
                "and the HuggingFace cache).\n"
                "Run: python -m langgraph_orchestration.inference --embeddings-only"
            )

        try:
            tokenizer = AutoTokenizer.from_pretrained(
                source,
                cache_dir=None if is_local else str(self.cache_dir),
                trust_remote_code=True,
                use_fast=False,
                local_files_only=is_local,
            )
            device_map = self.device if self.device != "cpu" else None
            model = AutoModel.from_pretrained(
                source,
                cache_dir=None if is_local else str(self.cache_dir),
                trust_remote_code=True,
                device_map=device_map,
                local_files_only=is_local,
            )
            if self.device == "cpu":
                model = model.to(self.device)
            model.eval()

            self.tokenizer = tokenizer
            self.model = model
            self._loaded = True

            inferred_dim = getattr(getattr(model, "config", None), "hidden_size", None)
            if not isinstance(inferred_dim, int) or inferred_dim <= 0:
                self.embedding_dim = int(self.embed_text("test", normalize=False).shape[-1])
            else:
                self.embedding_dim = int(inferred_dim)

            self._MODEL_CACHE[cache_key] = (self.tokenizer, self.model, self.embedding_dim)
        except Exception as e:
            if self.device == "mps" and self._is_mps_oom(e):
                logger.warning(
                    "MPS out of memory while loading %s; retrying on CPU", self.model_name
                )
                self.device = "cpu"
                self.model = None
                self.tokenizer = None
                self.embedding_dim = None
                self._loaded = False
                self._load_model()
                return
            self.model = None
            self.tokenizer = None
            self.embedding_dim = None
            self._loaded = False
            raise RuntimeError(f"Failed to load embedding model {self.model_name}: {e}") from e

    def _ensure_loaded(self):
        if not self._loaded:
            self._load_model()

    def embed_text(self, text: str, normalize: bool = True) -> np.ndarray:
        if not text or not isinstance(text, str):
            raise ValueError("Input must be a non-empty string")
        self._ensure_loaded()

        import torch

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        embeddings = outputs.last_hidden_state
        attention_mask = inputs["attention_mask"]
        mask_expanded = attention_mask.unsqueeze(-1).float()
        sum_embeddings = torch.sum(embeddings * mask_expanded, 1)
        sum_mask = torch.clamp(mask_expanded.sum(1), min=1e-9)
        mean_pooled = sum_embeddings / sum_mask

        embedding = mean_pooled.detach().cpu().numpy()[0]

        if normalize:
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm
        return np.asarray(embedding)

    def embed_batch(
        self,
        texts: list[str],
        batch_size: int = 32,
        normalize: bool = True,
    ) -> list[np.ndarray]:
        if not texts:
            return []

        self._ensure_loaded()

        import torch

        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]

            inputs = self.tokenizer(
                batch_texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)

            embeddings = outputs.last_hidden_state
            attention_mask = inputs["attention_mask"]
            mask_expanded = attention_mask.unsqueeze(-1).float()
            sum_embeddings = torch.sum(embeddings * mask_expanded, 1)
            sum_mask = torch.clamp(mask_expanded.sum(1), min=1e-9)
            mean_pooled = sum_embeddings / sum_mask

            batch_embeddings = mean_pooled.detach().cpu().numpy()

            if normalize:
                norms = np.linalg.norm(batch_embeddings, axis=1, keepdims=True)
                norms[norms == 0] = 1e-9
                batch_embeddings = batch_embeddings / norms

            all_embeddings.extend(batch_embeddings)

        return all_embeddings

    def get_embedding_dimension(self) -> int:
        """Get the dimensionality of embeddings produced by this model"""
        self._ensure_loaded()
        return int(self.embedding_dim)

    @staticmethod
    def similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Cosine similarity between two embeddings; 0.0 for degenerate input"""
        e1 = np.asarray(embedding1)
        e2 = np.asarray(embedding2)
        if e1.size == 0 or e2.size == 0:
            return 0.0
        norm1, norm2 = np.linalg.norm(e1), np.linalg.norm(e2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(e1, e2) / (norm1 * norm2))


# Section: vector store


class QdrantRetriever:
    DEFAULT_DB_PATH = "~/.local/share/qdrant"
    DEFAULT_COLLECTION_PREFIX = "agents_"

    MODEL_VECTOR_SIZES = {"Qwen/Qwen3-Embedding-0.6B": 1024}

    def __init__(
        self,
        db_path: str | None = None,
        embedding_model: str = "Qwen/Qwen3-Embedding-0.6B",
        embedding_cache_dir: str | None = None,
        embedding_device: str | None = None,
        enable_fallback: bool = True,
    ):
        self.db_path = Path(db_path or self.DEFAULT_DB_PATH).expanduser()
        self.db_path.mkdir(parents=True, exist_ok=True)

        self.embedding_model = embedding_model
        self.embedding_cache_dir = embedding_cache_dir
        self.embedding_device = embedding_device
        self._embedding_service: EmbeddingService | None = None
        self._embedding_dim: int | None = None
        self._collection_vector_sizes: dict[str, int] = {}
        self.enable_fallback = enable_fallback

        self._init_qdrant_client()

        self.domain_collections = {
            "software_dev": f"{self.DEFAULT_COLLECTION_PREFIX}software_dev",
            "reverse_engineering": f"{self.DEFAULT_COLLECTION_PREFIX}reverse_engineering",
            "shared": f"{self.DEFAULT_COLLECTION_PREFIX}shared",
        }

        for domain in self.domain_collections:
            self._ensure_collection(domain)

        logger.info(f"[OK] Qdrant retriever initialized at {self.db_path}")

    def _get_embedding_service(self, domain: str | None = None) -> EmbeddingService:
        if self._embedding_service is None:
            self._embedding_service = EmbeddingService(
                model_name=self.embedding_model,
                cache_dir=self.embedding_cache_dir,
                device=self.embedding_device,
            )
        return self._embedding_service

    @property
    def embedding_dim(self) -> int:
        if self._embedding_dim is None:
            service = self._get_embedding_service("shared")
            self._embedding_dim = service.get_embedding_dimension()
        return self._embedding_dim

    @property
    def embedding_service(self) -> EmbeddingService:
        if self._embedding_service is None:
            self._embedding_service = self._get_embedding_service("shared")
        return self._embedding_service

    def _get_collection_name(self, domain: str) -> str:
        if domain not in self.domain_collections:
            raise ValueError(f"Unknown domain: {domain}")
        return self.domain_collections[domain]

    def _coerce_vector_size(self, vector: np.ndarray | list[float], size: int) -> list[float]:
        array = np.asarray(vector, dtype=float).reshape(-1)
        if array.size == size:
            return array.tolist()
        if array.size > size:
            return array[:size].tolist()
        padded = np.zeros(size, dtype=float)
        padded[: array.size] = array
        return padded.tolist()

    def _init_qdrant_client(self):
        try:
            from qdrant_client import QdrantClient
        except ImportError as exc:
            raise ImportError(
                "qdrant-client is required. Install with: pip install qdrant-client"
            ) from exc

        max_retries = 5
        retry_delay = 0.5
        last_error = None

        for attempt in range(max_retries):
            try:
                self.client = QdrantClient(
                    path=str(self.db_path),
                    prefer_grpc=False,
                )
                logger.info("[OK] Qdrant client initialized in embedded mode")
                return
            except Exception as e:
                last_error = e
                if "AlreadyLocked" in str(e) or "Resource temporarily unavailable" in str(e):
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2**attempt)
                        logger.warning(
                            f"Qdrant database locked (attempt {attempt + 1}/{max_retries}), "
                            f"retrying in {wait_time:.1f}s"
                        )
                        time.sleep(wait_time)
                        continue
                raise RuntimeError(f"Failed to initialize Qdrant: {e}") from e

        raise RuntimeError(f"Failed to initialize Qdrant after {max_retries} retries: {last_error}")

    def _ensure_collection(self, domain: str) -> None:
        collection_name = self._get_collection_name(domain)

        vector_size = self.MODEL_VECTOR_SIZES.get(self.embedding_model)

        if vector_size is None:
            # only load model if we don't know the vector size
            vector_size = self.embedding_dim

        try:
            collection_info = self.client.get_collection(collection_name)
        except Exception:
            # collection doesn't exist, create it
            from qdrant_client.models import Distance, VectorParams

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

        if current_size is not None:
            if current_size != vector_size:
                logger.warning(
                    "Collection %s uses vector size %s, but model %s expects %s. "
                    "Using the existing collection size for compatibility.",
                    collection_name,
                    current_size,
                    self.embedding_model,
                    vector_size,
                )
            self._collection_vector_sizes[domain] = int(current_size)
        else:
            self._collection_vector_sizes[domain] = int(vector_size)

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        domain: str | None = None,
        score_threshold: float = 0.3,
    ) -> list[str]:
        if not query or not isinstance(query, str):
            logger.warning("Invalid query provided to retrieve")
            return []

        try:
            domains = (
                [domain]
                if domain and domain in self.domain_collections
                else list(self.domain_collections.keys())
            )
            query_embedding = self._get_embedding_service().embed_text(query).tolist()
            all_results = []

            for search_domain in domains:
                collection_name = self._get_collection_name(search_domain)
                target_size = self._collection_vector_sizes.get(search_domain)
                if target_size is None:
                    try:
                        target_size = int(
                            self.client.get_collection(collection_name).config.params.vectors.size
                        )
                        self._collection_vector_sizes[search_domain] = target_size
                    except Exception:
                        target_size = len(query_embedding)

                search_query = self._coerce_vector_size(query_embedding, target_size)

                try:
                    search_result = self.client.query_points(
                        collection_name=collection_name,
                        query=search_query,
                        limit=top_k * 2,
                        score_threshold=score_threshold,
                    )

                    for hit in search_result.points:
                        all_results.append(
                            {
                                "text": hit.payload.get("text", ""),
                                "score": hit.score,
                                "collection": collection_name,
                                "metadata": hit.payload.get("metadata", {}),
                            }
                        )

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
        domain: str | None,
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

        # simple keyword matching
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
        metadata: list[dict] | None = None,
    ) -> None:
        if not documents:
            return

        if domain not in self.domain_collections:
            logger.warning(f"Unknown domain: {domain}. Using 'shared' instead.")
            domain = "shared"

        collection_name = self._get_collection_name(domain)
        embedding_service = self._get_embedding_service(domain)

        try:
            embeddings = embedding_service.embed_batch(
                documents, batch_size=batch_size, normalize=True
            )

            self._ensure_collection(domain)
            target_size = self._collection_vector_sizes.get(
                domain, len(embeddings[0]) if embeddings else 0
            )

            points = []
            for i, (doc, embedding) in enumerate(zip(documents, embeddings, strict=True)):
                point_id = self._generate_point_id(collection_name, doc)

                point_metadata = {
                    "text": doc,
                    "metadata": {
                        "timestamp": datetime.utcnow().isoformat(),
                        "domain": domain,
                        "source": "api",
                    },
                }

                if metadata and i < len(metadata):
                    point_metadata["metadata"].update(metadata[i])

                from qdrant_client.models import PointStruct

                points.append(
                    PointStruct(
                        id=point_id,
                        vector=self._coerce_vector_size(embedding, target_size),
                        payload=point_metadata,
                    )
                )

            # upsert points (update if exists, insert if not)
            self.client.upsert(
                collection_name=collection_name,
                points=points,
            )

            logger.info(f"Added {len(documents)} documents to {collection_name} ({domain})")

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
            vector_size = None
            try:
                vector_size = collection_info.config.params.vectors.size
            except Exception:
                vector_size = self.MODEL_VECTOR_SIZES.get(self.embedding_model)

            return {
                "name": collection_name,
                "domain": domain,
                "document_count": collection_info.points_count,
                "vector_size": vector_size,
            }
        except Exception as e:
            logger.error(f"Failed to get collection info: {e}")
            return {"error": str(e)}

    def _generate_point_id(self, collection_name: str, text: str) -> int:
        import hashlib

        hash_value = int(
            hashlib.md5(f"{collection_name}:{text}".encode()).hexdigest(),
            16,
        ) % (2**31)
        return hash_value


# Section: public API

DOMAINS = ("software_dev", "reverse_engineering", "shared")


@dataclass(frozen=True)
class RAGConfig:
    db_path: str = "~/.local/share/qdrant"
    embedding_model: str = "Qwen/Qwen3-Embedding-0.6B"
    embedding_device: str = ""
    embedding_cache_dir: str = "~/.cache/huggingface"
    default_top_k: int = 5
    score_threshold: float = 0.3
    enable_fallback: bool = True

    @classmethod
    def from_env(cls) -> RAGConfig:
        config = cls(
            db_path=os.getenv("RAG_DB_PATH", cls.db_path),
            embedding_model=os.getenv("RAG_EMBEDDING_MODEL", cls.embedding_model),
            embedding_device=os.getenv("RAG_EMBEDDING_DEVICE", ""),
            embedding_cache_dir=os.getenv("RAG_EMBEDDING_CACHE_DIR", cls.embedding_cache_dir),
            default_top_k=_int_env("RAG_DEFAULT_TOP_K", cls.default_top_k),
            score_threshold=_float_env("RAG_SCORE_THRESHOLD", cls.score_threshold),
            enable_fallback=os.getenv("RAG_ENABLE_FALLBACK", "true").lower() == "true",
        )
        if config.default_top_k < 1:
            raise ValueError("RAG_DEFAULT_TOP_K must be >= 1")
        if not 0 <= config.score_threshold <= 1:
            raise ValueError("RAG_SCORE_THRESHOLD must be between 0 and 1")
        return config


def _int_env(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        logger.warning("%s is not an integer; using %s", name, default)
        return default


def _float_env(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except ValueError:
        logger.warning("%s is not a number; using %s", name, default)
        return default


_config: RAGConfig | None = None
_retriever = None
_retriever_failed = False


def get_config() -> RAGConfig:
    global _config
    if _config is None:
        _config = RAGConfig.from_env()
    return _config


def get_retriever():
    global _retriever, _retriever_failed
    if _retriever is not None or _retriever_failed:
        return _retriever

    try:
        from langgraph_orchestration.retrievers import QdrantRetriever

        config = get_config()
        _retriever = QdrantRetriever(
            db_path=config.db_path,
            embedding_model=config.embedding_model,
            embedding_cache_dir=config.embedding_cache_dir,
            embedding_device=config.embedding_device or None,
            enable_fallback=config.enable_fallback,
        )
    except Exception as exc:
        _retriever_failed = True
        logger.info(
            "RAG unavailable (%s: %s); continuing without retrieved context. "
            "This is expected until a corpus is ingested.",
            type(exc).__name__,
            exc,
        )
    return _retriever


def retrieve_context(query: str, domain: str | None = None, top_k: int | None = None) -> list[str]:
    retriever = get_retriever()
    if retriever is None:
        return []
    try:
        return retriever.retrieve(query, top_k=top_k or get_config().default_top_k, domain=domain)
    except Exception as exc:
        logger.warning("Retrieval failed (%s); continuing without context", exc)
        return []


def add_document(text: str, domain: str, metadata: dict | None = None) -> dict:
    """Ingest a single document. Used by the API and the loader script"""
    if not text or not isinstance(text, str):
        return {"status": "error", "message": "Invalid text"}
    if domain not in DOMAINS:
        return {"status": "error", "message": f"Unknown domain {domain!r}; expected {DOMAINS}"}

    retriever = get_retriever()
    if retriever is None:
        return {"status": "error", "message": "Vector database unavailable"}

    payload = dict(metadata or {})
    payload["added_at"] = datetime.now(UTC).isoformat()
    try:
        retriever.add_documents([text], domain, metadata=[payload])
    except Exception as exc:
        logger.error("Failed to add document: %s", exc)
        return {"status": "error", "message": str(exc)}

    return {"status": "success", "message": f"Document added to {domain}"}


def get_statistics() -> dict:
    """Per-domain collection sizes"""
    retriever = get_retriever()
    if retriever is None:
        return {"status": "error", "message": "Vector database unavailable"}

    try:
        collections = {domain: retriever.get_collection_info(domain) for domain in DOMAINS}
    except Exception as exc:
        logger.error("Failed to get statistics: %s", exc)
        return {"status": "error", "message": str(exc)}

    return {
        "status": "success",
        "collections": collections,
        "total_documents": sum(info.get("document_count", 0) for info in collections.values()),
    }

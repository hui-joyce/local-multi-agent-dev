"""
Local embedding service using sentence-transformers.
Provides semantic embeddings for RAG.
"""

import os
from typing import Optional
import numpy as np
from pathlib import Path
MODEL = "all-MiniLM-L6-v2"

def _detect_default_device(preferred: Optional[str] = None) -> str:
    if preferred:
        return preferred
    try:
        import torch
        if hasattr(torch, "has_mps") and torch.has_mps:
            return "mps"
        if torch.cuda.is_available():
            return "cuda"
    except Exception:
        pass
    return "cpu"


class EmbeddingService:
    def __init__(
        self,
        model_name: str = MODEL,
        cache_dir: Optional[str] = None,
        device: Optional[str] = None,
    ):
        self.model_name = model_name
        self.device = _detect_default_device(device)
        self.model = None
        self.embedding_dim = None
        # Set cache directory
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.cache/sentence-transformers")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self._loaded = False

    def preload(self) -> None:
        if not self._loaded:
            self._load_model()

    def _load_model(self):
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as e:
            raise ImportError(
                "sentence-transformers is required for embeddings. "
                "Install with: pip install sentence-transformers"
            ) from e

        try:
            self.model = SentenceTransformer(
                self.model_name,
                cache_folder=str(self.cache_dir),
                device=self.device,
            )
            # Determine embedding dimension by encoding a small test
            test_embedding = self.model.encode("test", convert_to_numpy=True)
            self.embedding_dim = int(np.asarray(test_embedding).shape[-1])
            self._loaded = True
            print(
                f"✓ Embedding model loaded: {self.model_name} "
                f"(dim={self.embedding_dim}, device={self.device})"
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to load embedding model {self.model_name}: {e}\n"
                "Ensure internet connection for first-time model download or pre-cache the model."
            ) from e

    def _ensure_loaded(self):
        if not self._loaded:
            self._load_model()

    def embed_text(self, text: str, normalize: bool = True) -> np.ndarray:
        if not text or not isinstance(text, str):
            raise ValueError("Input must be a non-empty string")
        self._ensure_loaded()
        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
        )
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
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=normalize,
            show_progress_bar=False,
        )

        embeddings = np.asarray(embeddings)
        if embeddings.ndim == 2:
            return [embeddings[i] for i in range(embeddings.shape[0])]
        return list(embeddings)

    def get_embedding_dimension(self) -> int:
        """Get the dimensionality of embeddings produced by this model"""
        self._ensure_loaded()
        return int(self.embedding_dim)

    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute cosine similarity between two normalized embeddings"""
        embedding1 = np.asarray(embedding1)
        embedding2 = np.asarray(embedding2)
        # If not normalized, normalize
        if embedding1.size == 0 or embedding2.size == 0:
            return 0.0
        # Use dot product (works for normalized vectors)
        sim = float(np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))
        return sim

    def batch_similarity(
        self,
        query_embedding: np.ndarray,
        embeddings_list: list[np.ndarray],
    ) -> list[float]:
        """Compute cosine similarity between query and multiple embeddings"""
        query_embedding = np.asarray(query_embedding)
        matrix = np.asarray(embeddings_list)
        # Normalize if necessary
        q_norm = np.linalg.norm(query_embedding)
        if q_norm == 0:
            return [0.0 for _ in range(len(matrix))]
        matrix_norms = np.linalg.norm(matrix, axis=1)
        dots = matrix.dot(query_embedding)
        sims = dots / (matrix_norms * q_norm + 1e-12)
        return [float(s) for s in sims]
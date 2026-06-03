import logging
import os
from pathlib import Path
from typing import Optional

import numpy as np

MODEL = "Qwen/Qwen3-Embedding-0.6B"
logger = logging.getLogger(__name__)

def _detect_default_device(preferred: Optional[str] = None) -> str:
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
        cache_dir: Optional[str] = None,
        device: Optional[str] = None,
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

    def preload(self) -> None:
        if not self._loaded:
            self._load_model()

    @staticmethod
    def _is_mps_oom(error: Exception) -> bool:
        msg = str(error).lower()
        return "mps backend out of memory" in msg or ("mps" in msg and "out of memory" in msg)

    def _load_model(self):
        try:
            from transformers import AutoTokenizer, AutoModel
            import torch
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

        try:
            tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=str(self.cache_dir),
                trust_remote_code=True,
                use_fast=False,
            )
            device_map = self.device if self.device != "cpu" else None
            model = AutoModel.from_pretrained(
                self.model_name,
                cache_dir=str(self.cache_dir),
                trust_remote_code=True,
                device_map=device_map,
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
                logger.warning("MPS out of memory while loading %s; retrying on CPU", self.model_name)
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

    def similarity(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        """Compute cosine similarity between two embeddings"""
        e1 = np.asarray(embedding1)
        e2 = np.asarray(embedding2)
        if e1.size == 0 or e2.size == 0:
            return 0.0
        norm1, norm2 = np.linalg.norm(e1), np.linalg.norm(e2)
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return float(np.dot(e1, e2) / (norm1 * norm2))

    def batch_similarity(
        self,
        query_embedding: np.ndarray,
        embeddings_list: list[np.ndarray],
    ) -> list[float]:
        """Compute cosine similarity between query and multiple embeddings"""
        query = np.asarray(query_embedding)
        matrix = np.asarray(embeddings_list)
        q_norm = np.linalg.norm(query)
        if q_norm == 0:
            return [0.0] * len(matrix)
        norms = np.linalg.norm(matrix, axis=1)
        return [float(s) for s in matrix.dot(query) / (norms * q_norm + 1e-12)]
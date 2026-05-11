"""
Local embedding service.
Provides semantic embeddings for RAG.
"""

import os
from typing import Optional
import numpy as np
from pathlib import Path

MODEL = "mlx-community/Qwen3-Embedding-0.6B-4bit-DWQ"

def _detect_default_device(preferred: Optional[str] = None) -> str:
    if preferred:
        return preferred
    try:
        import torch
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_built():
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
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.cache/huggingface")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self._loaded = False

    def preload(self) -> None:
        if not self._loaded:
            self._load_model()

    def _load_model(self):
        try:
            from transformers import AutoTokenizer, AutoModel
            import torch
        except ImportError as e:
            raise ImportError(
                "transformers and torch are required for embeddings. "
                "Install with: pip install transformers torch"
            ) from e

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=str(self.cache_dir),
                trust_remote_code=True,
                use_fast=False,
            )
            device_map = self.device if self.device != "cpu" else None
            self.model = AutoModel.from_pretrained(
                self.model_name,
                cache_dir=str(self.cache_dir),
                trust_remote_code=True,
                device_map=device_map,
            )
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            self.model.eval()
            
            test_embedding = self.embed_text("test", normalize=False)
            self.embedding_dim = int(test_embedding.shape[-1])
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
        
        # Mean-pool token embeddings
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
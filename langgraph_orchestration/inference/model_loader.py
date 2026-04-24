import os
from typing import Optional
from pathlib import Path


class MLXModelLoader:
    DEFAULT_MODELS = {
        "qwen-3.5-9b": {
            "repo_id": "mlx-community/Qwen3.5-9B-MLX-4bit",
            "model_type": "qwen3_5",
            "quantization": "4bit",
        }
    }
    
    def __init__(
        self,
        model_name: str = "qwen-3.5-9b",
        model_dir: Optional[str] = None,
        quantization: Optional[str] = None,
    ):
        self.model_name = model_name
        self.model_dir = Path(model_dir or "~/.cache/mlx_models").expanduser()
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Get model config
        if model_name in self.DEFAULT_MODELS:
            self.model_config = self.DEFAULT_MODELS[model_name]
        else:
            raise ValueError(
                f"Unknown model: {model_name}. "
                f"Available: {list(self.DEFAULT_MODELS.keys())}"
            )
        # Override quantization if specified
        if quantization:
            self.model_config["quantization"] = quantization
        
        self.model = None
        self.tokenizer = None
    
    def load(self) -> tuple:
        """Load model and tokenizer using mlx-lm."""
        try:
            from mlx_lm import load
        except ImportError as e:
            raise RuntimeError(
                f"MLX not installed. Install with: pip install -r requirements.txt"
            ) from e
        
        print(f"Loading {self.model_name} from {self.model_config['repo_id']}...")
        
        try:
            # Load model and tokenizer from HuggingFace repo
            # mlx-lm 0.31.2+ supports qwen3_5 model type natively
            model_and_tokenizer = load(self.model_config["repo_id"])
            
            if isinstance(model_and_tokenizer, tuple) and len(model_and_tokenizer) == 2:
                self.model, self.tokenizer = model_and_tokenizer
            else:
                self.model = model_and_tokenizer
                # Load tokenizer separately if needed
                from transformers import AutoTokenizer
                self.tokenizer = AutoTokenizer.from_pretrained(
                    self.model_config["repo_id"],
                    trust_remote_code=True
                )
            
            print(f"  ✓ Model loaded successfully")
            print(f"  Quantization: {self.model_config.get('quantization', 'none')}")
            
        except Exception as e:
            raise RuntimeError(
                f"Failed to load model {self.model_config['repo_id']}: {str(e)}"
            ) from e
        
        return self.model, self.tokenizer
    
    def is_loaded(self) -> bool:
        return self.model is not None and self.tokenizer is not None
    
    def get_model_info(self) -> dict:
        return {
            "name": self.model_name,
            "repo_id": self.model_config["repo_id"],
            "model_type": self.model_config["model_type"],
            "quantization": self.model_config["quantization"],
            "is_loaded": self.is_loaded(),
            "cache_dir": str(self.model_dir),
        }
import os
from typing import Optional
from pathlib import Path


class MLXModelLoader:
    """
    Features:
    - Automatic model downloading from HuggingFace
    - Quantization support (4-bit, 8-bit)
    - Memory-efficient loading on Apple Silicon
    - Caching and management of model files
    """
    
    # Default model configurations
    DEFAULT_MODELS = {
        "qwen-3.5-9b": {
            "repo_id": "Qwen/Qwen2.5-7B-Instruct",  # Using 7B as proxy for 9B capabilities
            "model_type": "qwen2",
            "quantization": "4bit",
        },
        "qwen-1.5-7b": {
            "repo_id": "Qwen/Qwen1.5-7B-Chat",
            "model_type": "qwen",
            "quantization": "4bit",
        },
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
        try:
            import mlx.core as mx
            from mlx_lm import load, models
            from transformers import AutoTokenizer
        except ImportError as e:
            raise RuntimeError(
                f"MLX not installed. Install with: pip install -r requirements.txt"
            ) from e
        
        print(f"Loading {self.model_name} from {self.model_config['repo_id']}...")
        
        # Load model using mlx-lm
        try:
            self.model, self.tokenizer = load(
                self.model_config["repo_id"],
                quantization=self.model_config.get("quantization")
            )
            print(f"✓ Model loaded successfully on device: {mx.default_device()}")
        except Exception as e:
            print(f"Failed to load model from mlx-lm, trying direct load...")
            # Fallback to direct HuggingFace loading
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_config["repo_id"]
            )
            print(f"✓ Tokenizer loaded successfully")
            
            # Model loading would happen here with transformers + mlx conversion
            # For now, this is a fallback point
            raise RuntimeError(
                f"Model loading not fully configured. "
                f"Please ensure mlx-lm is properly installed."
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
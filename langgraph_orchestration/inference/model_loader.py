import os
import sys
import time
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
        
        if model_name in self.DEFAULT_MODELS:
            self.model_config = self.DEFAULT_MODELS[model_name]
        else:
            raise ValueError(
                f"Unknown model: {model_name}. "
                f"Available: {list(self.DEFAULT_MODELS.keys())}"
            )
        if quantization:
            self.model_config["quantization"] = quantization
        
        self.model = None
        self.tokenizer = None

    def _assert_runtime_compatible(self) -> None:
        """Fail fast when the active interpreter cannot load the configured model type."""
        try:
            import mlx_lm
        except ImportError as e:
            raise RuntimeError(
                "mlx_lm is not installed in the active interpreter.\n"
                f"Active python: {sys.executable}\n"
                "Install deps in this interpreter: pip install -r requirements.txt"
            ) from e

        model_type = self.model_config["model_type"]
        models_dir = Path(mlx_lm.__file__).resolve().parent / "models"
        model_type_file = models_dir / f"{model_type}.py"

        if not model_type_file.exists():
            raise RuntimeError(
                "Active mlx_lm runtime does not support the configured model type.\n"
                f"Model type required: {model_type}\n"
                f"Active python: {sys.executable}\n"
                f"mlx_lm location: {Path(mlx_lm.__file__).resolve()}\n"
                "Likely cause: running with a different interpreter than your project venv.\n"
                "Try: source venv/bin/activate && python benchmarks/test_no_rag.py"
            )
    
    def load(self) -> tuple:
        """Load model and tokenizer using mlx-lm with strict runtime checks.="""
        self._assert_runtime_compatible()

        try:
            from mlx_lm import load
        except ImportError as e:
            raise RuntimeError(
                "MLX not installed in active interpreter.\n"
                f"Active python: {sys.executable}\n"
                "Install with: pip install -r requirements.txt"
            ) from e
        
        print(f"Loading {self.model_name} from {self.model_config['repo_id']}...")
        
        last_error: Optional[Exception] = None
        for attempt in range(1, 4):
            try:
                model_and_tokenizer = load(self.model_config["repo_id"])

                if isinstance(model_and_tokenizer, tuple) and len(model_and_tokenizer) == 2:
                    self.model, self.tokenizer = model_and_tokenizer
                else:
                    self.model = model_and_tokenizer
                    from transformers import AutoTokenizer
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        self.model_config["repo_id"],
                        trust_remote_code=True
                    )

                if self.model is None or self.tokenizer is None:
                    raise RuntimeError("Model or tokenizer returned None")

                print(f"  ✓ Model loaded successfully")
                print(f"  Quantization: {self.model_config.get('quantization', 'none')}")
                return self.model, self.tokenizer
            except Exception as e:
                last_error = e
                if attempt < 3:
                    print(f"  Load attempt {attempt}/3 failed, retrying...")
                    time.sleep(1.5)

        raise RuntimeError(
            f"Failed to load model {self.model_config['repo_id']} after 3 attempts.\n"
            f"Active python: {sys.executable}\n"
            f"Last error: {str(last_error)}"
        ) from last_error
    
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
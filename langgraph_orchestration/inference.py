from __future__ import annotations

import os
import shutil
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MODELS: dict[str, dict[str, str]] = {
    "qwen-3.5-9b": {
        "repo_id": "mlx-community/Qwen3.5-9B-MLX-4bit",
        "model_type": "qwen3_5",
        "quantization": "4bit",
    }
}

_DEFAULT_MODELS_DIR = Path(__file__).resolve().parents[1] / "models"

EMBEDDING_REPO = os.getenv("RAG_EMBEDDING_MODEL", "Qwen/Qwen3-Embedding-0.6B")

_DOWNLOAD_HINT = (
    "Download the weights first:\n"
    "  python -m langgraph_orchestration.inference\n"
    "then set HF_HUB_OFFLINE=1 in .env."
)

_REQUIRED_FILES = ("config.json",)
_WEIGHT_SUFFIXES = (".safetensors", ".bin", ".npz")


def models_dir() -> Path:
    override = os.getenv("MODELS_DIR")
    return Path(override).expanduser() if override else _DEFAULT_MODELS_DIR


def offline_mode() -> bool:
    return os.getenv("HF_HUB_OFFLINE", "").strip().lower() in ("1", "true", "yes")


def resolve_model_path(model_name: str = "qwen-3.5-9b") -> str:
    explicit = os.getenv("MODEL_PATH")
    if explicit:
        return str(Path(explicit).expanduser())

    repo_id = DEFAULT_MODELS[model_name]["repo_id"]
    local = models_dir() / repo_id.replace("/", "__")
    return str(local) if (local / "config.json").is_file() else repo_id


def local_dir_for(repo_id: str) -> Path:
    return models_dir() / repo_id.replace("/", "__")


def verify_snapshot(repo_id: str) -> tuple[bool, str]:
    target = local_dir_for(repo_id)
    if not target.is_dir():
        return False, f"missing directory {target}"

    missing = [name for name in _REQUIRED_FILES if not (target / name).is_file()]
    if missing:
        return False, f"missing {', '.join(missing)}"

    weights = [p for p in target.rglob("*") if p.is_file() and p.suffix in _WEIGHT_SUFFIXES]
    if not weights:
        return False, "no weight files (.safetensors/.bin/.npz)"

    total = sum(p.stat().st_size for p in weights)
    return True, f"{len(weights)} weight file(s), {total / 1024**3:.2f} GB"


def in_hf_cache(repo_id: str, extra_roots: tuple[str, ...] = ()) -> bool:
    hf_home = Path(os.getenv("HF_HOME", "~/.cache/huggingface")).expanduser()
    roots = [hf_home / "hub", hf_home, *(Path(r).expanduser() for r in extra_roots if r)]
    marker = f"models--{repo_id.replace('/', '--')}"
    return any((root / marker).is_dir() for root in roots)


_in_hf_cache = in_hf_cache


def ensure_downloaded(repo_id: str, *, label: str = "model") -> Path:
    target = local_dir_for(repo_id)
    present, detail = verify_snapshot(repo_id)
    if present:
        return target

    if offline_mode():
        raise RuntimeError(
            f"HF_HUB_OFFLINE=1 but the {label} is not available locally ({detail}).\n"
            f"Looked for: {target}\n"
            f"{_DOWNLOAD_HINT}"
        )

    try:
        from huggingface_hub import snapshot_download
    except ImportError as exc:
        raise RuntimeError(
            "huggingface_hub is required to fetch models. "
            "Install with: pip install -r requirements.txt"
        ) from exc

    free_gb = shutil.disk_usage(_existing_ancestor(target)).free / 1024**3
    print(f"Fetching {label} {repo_id}\n  -> {target}\n  free disk: {free_gb:.1f} GB")
    target.mkdir(parents=True, exist_ok=True)
    try:
        snapshot_download(repo_id=repo_id, local_dir=str(target), local_dir_use_symlinks=False)
    except TypeError:
        # huggingface_hub >= 1.0 dropped local_dir_use_symlinks; it is the default.
        snapshot_download(repo_id=repo_id, local_dir=str(target))

    present, detail = verify_snapshot(repo_id)
    if not present:
        raise RuntimeError(f"{label} download finished but looks incomplete: {detail}")
    print(f"  done -- {detail}")
    return target


def _existing_ancestor(path: Path) -> Path:
    while not path.exists() and path != path.parent:
        path = path.parent
    return path


class MLXModelLoader:
    def __init__(
        self,
        model_name: str = "qwen-3.5-9b",
        quantization: str | None = None,
    ):
        if model_name not in DEFAULT_MODELS:
            raise ValueError(f"Unknown model: {model_name}. Available: {sorted(DEFAULT_MODELS)}")
        self.model_name = model_name
        self.model_config = dict(DEFAULT_MODELS[model_name])
        if quantization:
            self.model_config["quantization"] = quantization

        self.model = None
        self.tokenizer = None

    def _assert_runtime_compatible(self) -> None:
        try:
            import mlx_lm
        except ImportError as exc:
            raise RuntimeError(
                "mlx_lm is not installed in the active interpreter.\n"
                f"Active python: {sys.executable}\n"
                "Install deps in this interpreter: pip install -r requirements.txt"
            ) from exc

        model_type = self.model_config["model_type"]
        models_path = Path(mlx_lm.__file__).resolve().parent / "models"
        if not (models_path / f"{model_type}.py").is_file():
            raise RuntimeError(
                "Active mlx_lm runtime does not support the configured model type.\n"
                f"Model type required: {model_type}\n"
                f"Active python: {sys.executable}\n"
                f"mlx_lm location: {Path(mlx_lm.__file__).resolve()}\n"
                "Likely cause: a different interpreter than the project venv.\n"
                "Try: source venv/bin/activate"
            )

    def _resolve_source(self) -> str:
        source = resolve_model_path(self.model_name)
        if os.path.isdir(source):
            return source
        if not _in_hf_cache(source):
            raise RuntimeError(
                f"No local copy of {self.model_name} ({source}).\n"
                f"Looked in: {models_dir() / source.replace('/', '__')}\n"
                f"and the HuggingFace cache.\n"
                f"{_DOWNLOAD_HINT}"
            )
        return source

    def load(self) -> tuple:
        self._assert_runtime_compatible()

        from mlx_lm import load

        source = self._resolve_source()
        print(f"Loading {self.model_name} from {source}...")

        try:
            self.model, self.tokenizer = load(source)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load model from {source}.\n"
                f"Active python: {sys.executable}\n"
                f"Cause: {type(exc).__name__}: {exc}\n"
                f"{_DOWNLOAD_HINT}"
            ) from exc

        if self.model is None or self.tokenizer is None:
            raise RuntimeError(f"mlx_lm.load({source}) returned no model or tokenizer")

        import mlx.core as mx

        # Cap the KV cache so long firmware prompts cannot exhaust Metal memory
        mx.set_cache_limit(2 * 1024 * 1024 * 1024)
        mx.clear_cache()

        print(f"  [OK] loaded ({self.model_config.get('quantization', 'none')})")
        return self.model, self.tokenizer

    def is_loaded(self) -> bool:
        return self.model is not None and self.tokenizer is not None


# Section: generation


@dataclass
class GenerationConfig:
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.95
    top_k: int = 50
    repeat_penalty: float = 1.0
    seed: int = 0

    def to_dict(self) -> dict:
        return {
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "repeat_penalty": self.repeat_penalty,
            "seed": self.seed,
        }

    @property
    def is_deterministic(self) -> bool:
        return self.temperature <= 0.0


class MLXInferenceEngine:
    DEFAULT_SYSTEM_PROMPT = (
        "You are a specialized AI assistant. "
        "Provide concise, actionable responses. "
        "Use provided context to inform your answers. "
        "Do not expose internal reasoning traces or <think> tags in your responses. "
        "Respond clearly and directly to the user's request."
    )

    def __init__(
        self,
        model,
        tokenizer,
        system_prompt: str | None = None,
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT

    def _build_generate_kwargs(self, config: GenerationConfig) -> dict:
        """Translate GenerationConfig into mlx_lm.generate kwargs.
        Seed RNG so runs are reproducible.
        """
        import mlx.core as mx

        mx.random.seed(config.seed)

        kwargs = {"max_tokens": config.max_tokens, "verbose": False}

        try:
            from mlx_lm.sample_utils import make_logits_processors

            kwargs["logits_processors"] = make_logits_processors(
                repetition_penalty=1.1,
                repetition_context_size=20,
            )
        except Exception:
            pass

        if config.temperature and config.temperature > 0.0:
            try:
                from mlx_lm.sample_utils import make_sampler

                kwargs["sampler"] = make_sampler(
                    temp=config.temperature,
                    top_p=config.top_p,
                    top_k=config.top_k,
                )
            except Exception:
                pass
        return kwargs

    def generate(
        self,
        prompt: str,
        config: GenerationConfig | None = None,
        stream: bool = False,
    ) -> str | Iterator[str]:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded. Call load() first.")

        config = config or GenerationConfig()

        try:
            import mlx.core as mx
            from mlx_lm import generate
        except ImportError as e:
            raise RuntimeError(
                "MLX not available. Install with: pip install -r requirements.txt"
            ) from e

        try:
            if stream:
                return self._generate_stream(prompt, config)
            generated_text = generate(
                self.model,
                self.tokenizer,
                prompt=prompt,
                **self._build_generate_kwargs(config),
            )
            mx.clear_cache()
            return generated_text

        except Exception as e:
            raise RuntimeError(f"Generation failed: {str(e)}") from e

    def _generate_stream(
        self,
        prompt: str,
        config: GenerationConfig,
    ) -> Iterator[str]:
        """Generate text in streaming mode"""
        try:
            from mlx_lm import generate
        except ImportError as exc:
            raise RuntimeError("MLX not installed") from exc

        full_text = generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            **self._build_generate_kwargs(config),
        )

        for word in full_text.split():
            yield word + " "

    def build_prompt(
        self,
        user_input: str,
        context: list[str] | None = None,
        system_prompt: str | None = None,
        enable_thinking: bool = True,
    ) -> str:
        system = system_prompt or self.system_prompt

        context_section = ""
        if context:
            context_section = "## Relevant Context\n"
            for i, doc in enumerate(context, 1):
                context_section += f"{i}. {doc}\n"
            context_section += "\n"

        parts = [
            "<|im_start|>system",
            f"{system}<|im_end|>",
            "<|im_start|>user",
            f"{context_section}{user_input}<|im_end|>",
            "<|im_start|>assistant",
        ]
        prompt = "\n".join(parts)

        if not enable_thinking:
            prompt += "\n<think>\n\n</think>\n\n"

        return prompt


# Section: command line


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Fetch or check the local model weights.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--llm-only", action="store_true", help="skip the embedding model")
    group.add_argument("--embeddings-only", action="store_true", help="skip the language model")
    parser.add_argument("--verify", action="store_true", help="report only, fetch nothing")
    parser.add_argument("--model", default="qwen-3.5-9b", choices=sorted(DEFAULT_MODELS))
    args = parser.parse_args(argv)

    jobs = []
    if not args.embeddings_only:
        jobs.append((DEFAULT_MODELS[args.model]["repo_id"], "language model"))
    if not args.llm_only:
        jobs.append((EMBEDDING_REPO, "embedding model"))

    print(f"Model directory: {models_dir()}")
    ok = True
    for repo_id, label in jobs:
        present, detail = verify_snapshot(repo_id)
        if present:
            print(f"  [OK] {label}: {repo_id} -- {detail}")
            continue
        if args.verify:
            print(f"  [MISSING] {label}: {repo_id} -- {detail}")
            ok = False
            continue
        try:
            ensure_downloaded(repo_id, label=label)
        except (RuntimeError, OSError) as exc:
            print(f"  [FAIL] {label}: {exc}", file=sys.stderr)
            ok = False

    if not ok:
        return 1
    if not args.verify:
        print("\nDone. Set HF_HUB_OFFLINE=1 in .env to forbid any further download:")
        print("  echo 'HF_HUB_OFFLINE=1' >> .env")
    return 0


if __name__ == "__main__":
    sys.exit(main())

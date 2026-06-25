import time
from typing import Optional, Iterator, Union
from dataclasses import dataclass

@dataclass
class GenerationConfig:
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.95
    top_k: int = 50
    repeat_penalty: float = 1.0
    seed: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary for MLX."""
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
        """A temperature of 0 selects greedy decoding (argmax), which is reproducible."""
        return self.temperature <= 0.0

@dataclass
class GenerationMetrics:
    """Metrics captured during text generation"""
    ttft_seconds: float  # time to first token
    prompt_tokens: int
    generated_tokens: int
    prompt_generation_speed_tok_s: float  # tokens/second for prompt building
    generation_speed_tok_s: float  # tokens/second for generation
    total_generation_seconds: float

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
        system_prompt: Optional[str] = None,
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.last_metrics: Optional[GenerationMetrics] = None

    def _build_generate_kwargs(self, config: GenerationConfig) -> dict:
        """Translate GenerationConfig into mlx_lm.generate kwargs.
        Seed RNG so runs are reproducible.
        """
        import mlx.core as mx

        mx.random.seed(config.seed)

        kwargs = {"max_tokens": config.max_tokens, "verbose": False}
        if config.temperature and config.temperature > 0.0:
            try:
                from mlx_lm.sample_utils import make_sampler

                kwargs["sampler"] = make_sampler(
                    temp=config.temperature,
                    top_p=config.top_p,
                    top_k=config.top_k,
                )
            except Exception:
                # If sampler construction fails, fall back to deterministic greedy
                # decoding rather than silently using an unknown default.
                pass
        # temperature <= 0 -> leave sampler unset; mlx_lm uses greedy argmax (deterministic).
        return kwargs
    
    def generate_with_metrics(
        self,
        prompt: str,
        config: Optional[GenerationConfig] = None,
    ) -> tuple[str, GenerationMetrics]:
        """Generate text and capture detailed metrics (TTFT, speeds)"""
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model not loaded. Call load() first.")
        
        config = config or GenerationConfig()
        
        try:
            import mlx.core as mx
            from mlx_lm import generate
            
            # Set cache limit to 2GB to prevent large KV caches from causing Metal OOMs
            mx.set_cache_limit(2 * 1024 * 1024 * 1024)

        except ImportError as e:
            raise RuntimeError(
                "MLX not available. Install with: pip install -r requirements.txt"
            ) from e
        
        try:
            tokenize_start = time.time()
            prompt_tokens = self.count_tokens(prompt)
            tokenize_end = time.time()
            prompt_tokenization_time = tokenize_end - tokenize_start
            
            prompt_generation_speed = prompt_tokens / prompt_tokenization_time if prompt_tokenization_time > 0 else 0
            
            gen_start = time.time()

            generated_text = generate(
                self.model,
                self.tokenizer,
                prompt=prompt,
                **self._build_generate_kwargs(config),
            )

            mx.clear_cache()

            gen_end = time.time()
            total_gen_time = gen_end - gen_start
            
            generated_tokens = self.count_tokens(generated_text)
            
            ttft = total_gen_time / max(generated_tokens, 1) if generated_tokens > 0 else total_gen_time
            
            generation_speed = generated_tokens / total_gen_time if total_gen_time > 0 else 0
            
            metrics = GenerationMetrics(
                ttft_seconds=round(ttft, 4),
                prompt_tokens=prompt_tokens,
                generated_tokens=generated_tokens,
                prompt_generation_speed_tok_s=round(prompt_generation_speed, 2),
                generation_speed_tok_s=round(generation_speed, 2),
                total_generation_seconds=round(total_gen_time, 3),
            )
            
            self.last_metrics = metrics
            return generated_text, metrics
        
        except Exception as e:
            raise RuntimeError(f"Generation failed: {str(e)}") from e
    
    def generate(
        self,
        prompt: str,
        config: Optional[GenerationConfig] = None,
        stream: bool = False,
    ) -> Union[str, Iterator[str]]:
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
        except ImportError:
            raise RuntimeError("MLX not installed")

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
        context: Optional[list[str]] = None,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Build formatted prompt with context."""
        system = system_prompt or self.system_prompt
        
        context_section = ""
        if context:
            context_section = "## Relevant Context\n"
            for i, doc in enumerate(context, 1):
                context_section += f"{i}. {doc}\n"
            context_section += "\n"
        
        prompt = f"""<|im_start|>system
{system}<|im_end|>
<|im_start|>user
{context_section}{user_input}<|im_end|>
<|im_start|>assistant"""
        
        return prompt
    
    def count_tokens(self, text: str) -> int:
        if self.tokenizer is None:
            raise RuntimeError("Tokenizer not loaded")
        
        tokens = self.tokenizer.encode(text)
        return len(tokens)
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        return {
            "has_model": self.model is not None,
            "has_tokenizer": self.tokenizer is not None,
            "system_prompt_length": len(self.system_prompt),
        }

class GeminiInferenceEngine:    
    DEFAULT_SYSTEM_PROMPT = (
        "You are a specialized AI assistant. "
        "Provide concise, actionable responses. "
        "Use provided context to inform your answers. "
        "Do not expose internal reasoning traces or <think> tags in your responses. "
        "Respond clearly and directly to the user's request."
    )
    
    def __init__(self, system_prompt: Optional[str] = None):
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        self.last_metrics: Optional[GenerationMetrics] = None
        
        import os
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
            
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is not set in .env")
            
        self.model_name = "gemini-3.1-flash-lite"

    def generate(
        self,
        prompt: str,
        config: Optional[GenerationConfig] = None,
        stream: bool = False,
    ) -> Union[str, Iterator[str]]:
        config = config or GenerationConfig()
        
        import urllib.request
        import urllib.error
        import json
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
        
        generation_config = {
            "maxOutputTokens": config.max_tokens,
            "temperature": config.temperature,
            "topP": config.top_p,
            "topK": config.top_k,
            "seed": config.seed,
        }
        if config.temperature <= 0.0:
            generation_config["temperature"] = 0.0
            generation_config["topK"] = 1

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": generation_config,
        }
        
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
        
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req, timeout=300) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    
                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            text = "".join(part.get("text", "") for part in candidate["content"]["parts"])
                            if stream:
                                return iter([text])
                            return text
                    return ""
            except urllib.error.HTTPError as e:
                error_body = e.read().decode('utf-8')
                if e.code in (503, 429) and attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                raise RuntimeError(f"Model generation failed: {e.code} - {error_body}") from e
            except Exception as e:
                if attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delay)
                    retry_delay *= 2
                    continue
                raise RuntimeError(f"Generation failed: {str(e)}") from e
            
    def generate_with_metrics(
        self,
        prompt: str,
        config: Optional[GenerationConfig] = None,
    ) -> tuple[str, GenerationMetrics]:
        start_time = time.time()
        text = self.generate(prompt, config)
        total_time = time.time() - start_time
        
        metrics = GenerationMetrics(
            ttft_seconds=0.0,
            prompt_tokens=0,
            generated_tokens=len(text.split()),
            prompt_generation_speed_tok_s=0.0,
            generation_speed_tok_s=0.0,
            total_generation_seconds=round(total_time, 3),
        )
        self.last_metrics = metrics
        return text, metrics

    def build_prompt(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
        system_prompt: Optional[str] = None,
    ) -> str:
        system = system_prompt or self.system_prompt
        
        context_section = ""
        if context:
            context_section = "## Relevant Context\n"
            for i, doc in enumerate(context, 1):
                context_section += f"{i}. {doc}\n"
            context_section += "\n"
        
        prompt = f"System: {system}\n\nUser Context:\n{context_section}\n\nUser Input: {user_input}"
        return prompt
        
    def get_model_info(self) -> dict:
        return {
            "has_model": True,
            "has_tokenizer": False,
            "system_prompt_length": len(self.system_prompt),
            "engine": "gemini"
        }
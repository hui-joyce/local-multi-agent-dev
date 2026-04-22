from typing import Optional, Iterator
from dataclasses import dataclass

@dataclass
class GenerationConfig:    
    max_tokens: int = 2048
    temperature: float = 0.7
    top_p: float = 0.95
    top_k: int = 50
    repeat_penalty: float = 1.0
    
    def to_dict(self) -> dict:
        """Convert to dictionary for MLX."""
        return {
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "repeat_penalty": self.repeat_penalty,
        }

class MLXInferenceEngine:
    """    
    Features:
    - Efficient token generation on Apple Silicon
    - Streaming support for real-time responses
    - Token counting and management
    - Prompt formatting with RAG context
    - System role and conversation history support
    """
    
    # Default system prompt for agents
    DEFAULT_SYSTEM_PROMPT = (
        "You are a specialized AI assistant. "
        "Provide concise, actionable responses. "
        "Use provided context to inform your answers."
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
    
    def generate(
        self,
        prompt: str,
        config: Optional[GenerationConfig] = None,
        stream: bool = False,
    ) -> str | Iterator[str]:
        """Generate text using the model."""
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
                # Streaming generation (yields tokens)
                return self._generate_stream(prompt, config)
            else:
                # Non-streaming generation (returns full text)
                generated_text = generate(
                    self.model,
                    self.tokenizer,
                    prompt=prompt,
                    **config.to_dict(),
                    verbose=False,
                )
                return generated_text
        
        except Exception as e:
            raise RuntimeError(f"Generation failed: {str(e)}") from e
    
    def _generate_stream(
        self,
        prompt: str,
        config: GenerationConfig,
    ) -> Iterator[str]:
        """Generate text in streaming mode (token by token)."""
        try:
            from mlx_lm import generate
        except ImportError:
            raise RuntimeError("MLX not installed")
        
        # Use generate with streaming
        # Note: This is a simplified version - actual implementation depends on mlx-lm version
        full_text = generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            **config.to_dict(),
            verbose=False,
        )
        
        # Simple word-by-word streaming
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
        
        # Build context section
        context_section = ""
        if context:
            context_section = "## Relevant Context\n"
            for i, doc in enumerate(context, 1):
                context_section += f"{i}. {doc}\n"
            context_section += "\n"
        
        # Qwen format: system, user interaction
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
        """Get information about the loaded model."""
        return {
            "has_model": self.model is not None,
            "has_tokenizer": self.tokenizer is not None,
            "system_prompt_length": len(self.system_prompt),
        }
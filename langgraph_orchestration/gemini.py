from __future__ import annotations

from collections.abc import Iterator

from langgraph_orchestration.agents import Agent, SupervisorAgent, create_agent
from langgraph_orchestration.inference import GenerationConfig

# Section: inference


class GeminiInferenceEngine:
    DEFAULT_SYSTEM_PROMPT = (
        "You are a specialized AI assistant. "
        "Provide concise, actionable responses. "
        "Use provided context to inform your answers. "
        "Do not expose internal reasoning traces or <think> tags in your responses. "
        "Respond clearly and directly to the user's request."
    )

    def __init__(self, system_prompt: str | None = None):
        self.system_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT

        import os

        try:
            from dotenv import load_dotenv

            load_dotenv()
        except ImportError:
            pass

        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY environment variable is not set in .env")

        self.model_name = "gemini-3.1-pro-preview"

    def generate(
        self,
        prompt: str,
        config: GenerationConfig | None = None,
        stream: bool = False,
    ) -> str | Iterator[str]:
        config = config or GenerationConfig()

        import json
        import urllib.error
        import urllib.request

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

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

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "x-goog-api-key": self.api_key},
        )

        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req, timeout=300) as response:
                    result = json.loads(response.read().decode("utf-8"))

                    if "candidates" in result and len(result["candidates"]) > 0:
                        candidate = result["candidates"][0]
                        if "content" in candidate and "parts" in candidate["content"]:
                            text = "".join(
                                part.get("text", "") for part in candidate["content"]["parts"]
                            )
                            if stream:
                                return iter([text])
                            return text
                    return ""
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8")
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

        prompt = f"System: {system}\n\nUser Context:\n{context_section}\n\nUser Input: {user_input}"
        return prompt

    def get_model_info(self) -> dict:
        return {
            "has_model": True,
            "has_tokenizer": False,
            "system_prompt_length": len(self.system_prompt),
            "engine": "gemini",
        }


# Section: factory
class GeminiAgentFactory:
    def __init__(self, model_name: str = "gemini-3.1-pro-preview"):
        self.model_name = model_name
        self.inference_engine: GeminiInferenceEngine | None = None

    def ensure_loaded(self) -> GeminiInferenceEngine:
        if self.inference_engine is None:
            self.load_model()
        if self.inference_engine is None:
            raise RuntimeError("Inference engine is unavailable after load attempt")
        return self.inference_engine

    def load_model(self) -> GeminiInferenceEngine:
        print(
            f"[WARN] Using hosted model {self.model_name}. Prompts and evidence "
            "leave this machine; this path is not offline."
        )
        self.inference_engine = GeminiInferenceEngine()
        self.inference_engine.model_name = self.model_name
        return self.inference_engine

    def create_agent(self, name: str) -> Agent:
        return create_agent(name, self.ensure_loaded())

    def create_supervisor_agent(self) -> SupervisorAgent:
        return SupervisorAgent(self.ensure_loaded())

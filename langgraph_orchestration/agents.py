"""Agent definitions and the factory that creates them"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from langgraph_orchestration.core import (
    looks_like_firmware_request,
    sanitize_agent_output,
    strip_reasoning,
)
from langgraph_orchestration.inference import (
    GenerationConfig,
    MLXInferenceEngine,
    MLXModelLoader,
)
from langgraph_orchestration.prompts import (
    build_label_routing_prompt,
    build_split_tasks_prompt,
)

# Section: agents
# Appended to every agent's system prompt; without it the model leaks tool traces and thinking
_OUTPUT_CONSTRAINTS = (
    "OUTPUT CONSTRAINTS:\n"
    "- Do NOT include any internal tool activity, JSON tool call traces, "
    "orchestration variables, or diagnostics.\n"
    "- Do NOT include internal monologue, chain-of-thought, or reasoning steps.\n"
    "- Use all provided context and produce a complete, final result.\n"
    "- When returning code, output only the code in a single fenced code block "
    "with the appropriate language.\n"
    "- When returning analysis, present only the final analysis in the "
    "requested format.\n"
)

_LABEL_TOKEN_RE = re.compile(r"\b(?:SOFTWARE_DEV|REVERSE_ENGINEERING|BOTH)\b")

_SPLIT_MARKER_RE = re.compile(r"\band then\b|\bthen\b", re.IGNORECASE)

_CODE_FENCE_RE = re.compile(r"```(?:\w+)?\n(.*?)```", re.DOTALL)


@dataclass(frozen=True)
class AgentSpec:
    description: str
    max_tokens: int
    temperature: float


AGENT_SPECS: dict[str, AgentSpec] = {
    "code_generation": AgentSpec(
        description=(
            "Generates production-ready code based on requirements. "
            "You are expert at Python, creating clean, well-documented code."
        ),
        max_tokens=4096,
        temperature=0.3,
    ),
    "unit_testing": AgentSpec(
        description=(
            "Generates comprehensive unit tests with high code coverage. "
            "You are expert at Python testing, using pytest and mocking."
        ),
        max_tokens=4096,
        temperature=0.2,
    ),
    "architectural_review": AgentSpec(
        description=(
            "Reviews code for architectural fitness and best practices. "
            "You are expert at software architecture and design patterns."
        ),
        max_tokens=3000,
        temperature=0.5,
    ),
    "planning": AgentSpec(
        description=(
            "Plans complex reverse engineering tasks. "
            "You create structured, methodical analysis plans."
        ),
        max_tokens=2048,
        temperature=0.5,
    ),
    "code_analysis": AgentSpec(
        description=(
            "Analyzes code structure, patterns, and logic flow. "
            "You are expert at reverse engineering and binary analysis."
        ),
        max_tokens=3000,
        temperature=0.4,
    ),
    "vulnerability_detection": AgentSpec(
        description=(
            "Detects security vulnerabilities and weaknesses. "
            "You are expert at security analysis, threat modeling, and CVEs."
        ),
        max_tokens=4096,
        temperature=0.3,
    ),
}


class Agent:
    def __init__(self, name: str, spec: AgentSpec, inference_engine):
        self.name = name
        self.spec = spec
        self.description = spec.description
        self.inference_engine = inference_engine

    def _build_prompt(self, user_input: str, context: list[str] | None = None) -> str:
        system_prompt = f"{self.description}\n\nBe concise and actionable.\n\n{_OUTPUT_CONSTRAINTS}"
        return self.inference_engine.build_prompt(
            user_input=user_input,
            context=context,
            system_prompt=system_prompt,
        )

    def invoke(self, user_input: str, context: list[str] | None = None) -> str:
        prompt = self._build_prompt(user_input, context)
        config = GenerationConfig(
            max_tokens=self.spec.max_tokens,
            temperature=self.spec.temperature,
        )
        return sanitize_agent_output(
            self.inference_engine.generate(prompt, config=config, stream=False)
        )


def create_agent(name: str, inference_engine) -> Agent:
    """Build the agent registered under *name*."""
    try:
        spec = AGENT_SPECS[name]
    except KeyError:
        raise ValueError(
            f"Unknown agent {name!r}. Available: {', '.join(sorted(AGENT_SPECS))}"
        ) from None
    return Agent(name=name, spec=spec, inference_engine=inference_engine)


# Section: supervisor


class SupervisorAgent:
    DOMAIN_OPTIONS = ("software_dev", "reverse_engineering")
    LABEL_OPTIONS = ("SOFTWARE_DEV", "REVERSE_ENGINEERING", "BOTH")
    _CACHE_MAX_SIZE = 1000

    def __init__(self, inference_engine=None):
        self.name = "supervisor"
        self.description = "Routes user requests to software_dev and/or reverse_engineering"
        self.inference_engine = inference_engine
        self._decision_cache: dict[str, dict] = {}

    # routing

    def invoke(self, user_input: str, context: list[str] | None = None) -> dict:
        if user_input in self._decision_cache:
            return self._decision_cache[user_input]

        if looks_like_firmware_request(user_input):
            return self._cache_decision(
                user_input,
                self._build_decision("reverse_engineering", ["reverse_engineering"]),
            )

        if self.inference_engine is None:
            raise RuntimeError(
                "Supervisor inference engine is unavailable. "
                "Model initialization must succeed before routing."
            )

        label = self._classify(user_input)
        if label == "REVERSE_ENGINEERING":
            decision = self._build_decision("reverse_engineering", ["reverse_engineering"])
        elif label == "BOTH":
            decision = self._build_decision(
                "software_dev",
                ["software_dev", "reverse_engineering"],
                self._extract_split_tasks(user_input),
            )
        else:
            decision = self._build_decision("software_dev", ["software_dev"])

        return self._cache_decision(user_input, decision)

    def _classify(self, user_input: str) -> str | None:
        """Ask the model for one routing label. Returns None if it never gives one"""
        prompt = build_label_routing_prompt(self.inference_engine, user_input)
        config = GenerationConfig(max_tokens=64, temperature=0.0)

        for attempt in range(2):
            attempt_prompt = prompt
            if attempt == 1:
                attempt_prompt += (
                    "\n\nIMPORTANT: Output one label only: "
                    "SOFTWARE_DEV or REVERSE_ENGINEERING or BOTH."
                )
            try:
                output = self.inference_engine.generate(
                    prompt=attempt_prompt, config=config, stream=False
                )
            except Exception:
                continue
            label = self._parse_label(sanitize_agent_output(output))
            if label:
                return label
        return None

    def _parse_label(self, text: str) -> str | None:
        """Accept a bare label, a label on its own line, or a single label token"""
        cleaned = strip_reasoning(text)
        if not cleaned:
            return None

        if cleaned.upper() in self.LABEL_OPTIONS:
            return cleaned.upper()

        line_labels = {
            stripped
            for line in cleaned.splitlines()
            if (stripped := line.strip().strip("`*_-. ")) in self.LABEL_OPTIONS
        }
        if len(line_labels) == 1:
            return line_labels.pop()

        tokens = set(_LABEL_TOKEN_RE.findall(cleaned.upper()))
        return tokens.pop() if len(tokens) == 1 else None

    # task splitting

    def _extract_split_tasks(self, user_input: str) -> dict[str, str]:
        """Split a two-domain request into a dev half and an RE half"""
        normalized = re.sub(r"\s+", " ", user_input).strip()

        match = _SPLIT_MARKER_RE.search(normalized)
        if match:
            software_part = normalized[: match.start()].strip(" ,;:-\n\t")
            reverse_part = normalized[match.end() :].strip(" ,;:-\n\t")
            if software_part and reverse_part:
                snippets = self._extract_code_blocks(user_input)
                if snippets:
                    software_part = f"{software_part}\n\n{snippets}"
                    reverse_part = f"{reverse_part}\n\n{snippets}"
                return {"software_dev": software_part, "reverse_engineering": reverse_part}

        if self.inference_engine is None:
            return {}

        try:
            output = self.inference_engine.generate(
                prompt=build_split_tasks_prompt(self.inference_engine, user_input),
                config=GenerationConfig(max_tokens=1200, temperature=0.0),
                stream=False,
            )
            parsed = self._parse_json_object(sanitize_agent_output(output))
        except Exception:
            return {}

        if not parsed:
            return {}
        return {
            domain: str(parsed[domain]).strip()
            for domain in self.DOMAIN_OPTIONS
            if parsed.get(domain)
        }

    @staticmethod
    def _extract_code_blocks(text: str) -> str:
        """Fenced code blocks from the request, in order, de-duplicated."""
        seen: set[str] = set()
        blocks: list[str] = []
        for match in _CODE_FENCE_RE.finditer(text):
            block = match.group(1).strip()
            if block and block not in seen:
                seen.add(block)
                blocks.append(block)
        return "\n\n".join(blocks)

    @staticmethod
    def _parse_json_object(text: str) -> dict | None:
        """First JSON object in *text*, tolerating prose and code fences."""
        stripped = strip_reasoning(text)
        stripped = re.sub(r"^```(?:json)?|```$", "", stripped.strip()).strip()

        decoder = json.JSONDecoder()
        for index, char in enumerate(stripped):
            if char != "{":
                continue
            try:
                obj, _ = decoder.raw_decode(stripped[index:])
            except ValueError:
                continue
            if isinstance(obj, dict):
                return obj
        return None

    # helpers

    @staticmethod
    def _build_decision(
        primary_domain: str,
        execution_domains: list[str],
        split_tasks: dict | None = None,
    ) -> dict:
        return {
            "primary_domain": primary_domain,
            "execution_domains": execution_domains,
            "split_tasks": split_tasks or {},
        }

    def _cache_decision(self, user_input: str, decision: dict) -> dict:
        if len(self._decision_cache) >= self._CACHE_MAX_SIZE:
            self._decision_cache.clear()
        self._decision_cache[user_input] = decision
        return decision


# Section: factory
class MLXAgentFactory:
    """Loads the model once and hands out agents that share it."""

    def __init__(
        self,
        model_name: str = "qwen-3.5-9b",
        quantization: str | None = "4bit",
    ):
        self.model_name = model_name
        self.quantization = quantization
        self.inference_engine: MLXInferenceEngine | None = None

    def ensure_loaded(self) -> MLXInferenceEngine:
        if self.inference_engine is None:
            self.load_model()
        if self.inference_engine is None:
            raise RuntimeError("Inference engine is unavailable after load attempt")
        return self.inference_engine

    def load_model(self) -> MLXInferenceEngine:
        print(f"Loading MLX model: {self.model_name}")
        loader = MLXModelLoader(model_name=self.model_name, quantization=self.quantization)
        model, tokenizer = loader.load()
        self.inference_engine = MLXInferenceEngine(model=model, tokenizer=tokenizer)
        print("[OK] MLX model loaded and ready")
        return self.inference_engine

    def create_agent(self, name: str) -> Agent:
        return create_agent(name, self.ensure_loaded())

    def create_supervisor_agent(self) -> SupervisorAgent:
        return SupervisorAgent(self.ensure_loaded())

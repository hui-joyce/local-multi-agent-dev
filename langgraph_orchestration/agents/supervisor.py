"""
Supervisor agent for domain routing and orchestration.

The Supervisor analyzes incoming requests and routes them to the
appropriate domain (software development or reverse engineering).
"""

import json
import re
from typing import Optional
from .base import SyncBaseAgent
from langgraph_orchestration.inference.inference_engine import (
    MLXInferenceEngine,
    GenerationConfig,
)
from langgraph_orchestration.prompts.supervisor import (
    build_label_routing_prompt,
    build_json_routing_prompt,
)

class SupervisorAgent(SyncBaseAgent):
    DOMAIN_OPTIONS = ("software_dev", "reverse_engineering")
    LABEL_OPTIONS = ("SOFTWARE_DEV", "REVERSE_ENGINEERING", "BOTH")

    def __init__(self, inference_engine: Optional[MLXInferenceEngine] = None):
        super().__init__(
            name="supervisor",
            description="Routes user requests to software_dev and/or reverse_engineering",
        )
        self.inference_engine = inference_engine
        self._decision_cache: dict[str, dict] = {}

    def _build_routing_prompt(self, user_input: str) -> str:
        """Build JSON-based routing prompt (legacy)."""
        return build_json_routing_prompt(self.inference_engine, user_input)

    def _build_label_prompt(self, user_input: str) -> str:
        """Build label-based routing prompt."""
        return build_label_routing_prompt(self.inference_engine, user_input)

    def _parse_label(self, raw_output: str) -> Optional[str]:
        cleaned = raw_output.strip()
        cleaned = re.sub(r"<think>.*?</think>", "", cleaned, flags=re.DOTALL).strip()
        cleaned_upper = cleaned.upper()

        # Exact match first.
        for label in self.LABEL_OPTIONS:
            if cleaned_upper == label:
                return label

        # Then line-based match
        for line in cleaned_upper.splitlines():
            token = line.strip().strip("`*_-. ")
            if token in self.LABEL_OPTIONS:
                return token

        # fallback to last mention in text (decision usually appears at the end).
        mentions: list[tuple[int, str]] = []
        for label in self.LABEL_OPTIONS:
            for m in re.finditer(rf"\b{re.escape(label)}\b", cleaned_upper):
                mentions.append((m.start(), label))
        if mentions:
            mentions.sort(key=lambda x: x[0])
            return mentions[-1][1]

        return None

    def _extract_decision(self, raw_output: str) -> Optional[dict]:
        cleaned = raw_output.strip()
        parsed = self._parse_json_from_text(cleaned)
        if parsed is not None:
            execution_domains = parsed.get("execution_domains")
            if execution_domains is None:
                return None
            if not isinstance(execution_domains, list):
                return None

            normalized_domains = [
                d for d in [str(x).strip().lower() for x in execution_domains]
                if d in self.DOMAIN_OPTIONS
            ]
            normalized_domains = list(dict.fromkeys(normalized_domains))
            if not normalized_domains:
                return None

            primary_domain = str(parsed.get("primary_domain", "")).strip().lower()
            if primary_domain not in self.DOMAIN_OPTIONS:
                primary_domain = normalized_domains[0]

            split_tasks = parsed.get("split_tasks", {})
            if not isinstance(split_tasks, dict):
                split_tasks = {}

            normalized_split_tasks = {
                domain: str(split_tasks.get(domain, "")).strip()
                for domain in self.DOMAIN_OPTIONS
                if str(split_tasks.get(domain, "")).strip()
            }

            if len(normalized_domains) == 2 and "software_dev" not in normalized_split_tasks:
                normalized_split_tasks["software_dev"] = "Implement and validate the requested software solution."
            if len(normalized_domains) == 2 and "reverse_engineering" not in normalized_split_tasks:
                normalized_split_tasks["reverse_engineering"] = "Analyze the request from security and reverse-engineering perspective."

            return {
                "primary_domain": primary_domain,
                "execution_domains": normalized_domains,
                "split_tasks": normalized_split_tasks,
            }

        return None
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> dict:
        if user_input in self._decision_cache:
            return self._decision_cache[user_input]

        if self.inference_engine is None:
            raise RuntimeError(
                "Supervisor inference engine is unavailable. "
                "Model initialization must succeed before routing."
            )

        prompt = self._build_label_prompt(user_input)
        config = GenerationConfig(max_tokens=1200, temperature=0.0)

        # Try twice before failing
        for attempt in range(2):
            try:
                attempt_prompt = prompt
                if attempt == 1:
                    attempt_prompt = (
                        prompt
                        + "\n\nIMPORTANT: Output one label only: SOFTWARE_DEV or REVERSE_ENGINEERING or BOTH."
                    )

                # Use generate_with_metrics for the first attempt to capture metrics
                if attempt == 0:
                    output, metrics = self.inference_engine.generate_with_metrics(
                        prompt=attempt_prompt,
                        config=config,
                    )
                else:
                    output = self.inference_engine.generate(
                        prompt=attempt_prompt,
                        config=config,
                        stream=False,
                    )
                    
                label = self._parse_label(output)
                if label == "SOFTWARE_DEV":
                    decision = {
                        "primary_domain": "software_dev",
                        "execution_domains": ["software_dev"],
                        "split_tasks": {},
                    }
                    self._decision_cache[user_input] = decision
                    return decision
                if label == "REVERSE_ENGINEERING":
                    decision = {
                        "primary_domain": "reverse_engineering",
                        "execution_domains": ["reverse_engineering"],
                        "split_tasks": {},
                    }
                    self._decision_cache[user_input] = decision
                    return decision
                if label == "BOTH":
                    decision = {
                        "primary_domain": "software_dev",
                        "execution_domains": ["software_dev", "reverse_engineering"],
                        "split_tasks": {
                            "software_dev": "Implement and validate the requested software solution.",
                            "reverse_engineering": "Analyze the request from security and reverse-engineering perspective.",
                        },
                    }
                    self._decision_cache[user_input] = decision
                    return decision
            except Exception:
                continue

        raise RuntimeError("Supervisor routing failed: could not obtain a valid route label from model")

    @staticmethod
    def _parse_json_from_text(text: str) -> Optional[dict]:
        candidates: list[str] = []
        stripped = text.strip()

        # Remove Qwen reasoning wrappers when present
        stripped = re.sub(r"<think>.*?</think>", "", stripped, flags=re.DOTALL).strip()

        if stripped.startswith("```"):
            stripped = re.sub(r"^```(?:json)?", "", stripped).strip()
            stripped = re.sub(r"```$", "", stripped).strip()
        candidates.append(stripped)

        block = SupervisorAgent._extract_first_braced_block(stripped)
        if block:
            candidates.append(block)

        reverse_block = SupervisorAgent._extract_last_braced_block(stripped)
        if reverse_block and reverse_block != block:
            candidates.append(reverse_block)

        for candidate in candidates:
            try:
                parsed = json.loads(candidate)
                if isinstance(parsed, dict):
                    return parsed
            except Exception:
                continue
        return None

    @staticmethod
    def _extract_first_braced_block(text: str) -> str:
        """Extract first balanced {...} block from text."""
        start = text.find("{")
        if start == -1:
            return ""
        depth = 0
        for idx in range(start, len(text)):
            char = text[idx]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
                if depth == 0:
                    return text[start : idx + 1]
        return ""

    @staticmethod
    def _extract_last_braced_block(text: str) -> str:
        """Extract last balanced {...} block from text."""
        end = text.rfind("}")
        if end == -1:
            return ""
        depth = 0
        for idx in range(end, -1, -1):
            char = text[idx]
            if char == "}":
                depth += 1
            elif char == "{":
                depth -= 1
                if depth == 0:
                    return text[idx : end + 1]
        return ""
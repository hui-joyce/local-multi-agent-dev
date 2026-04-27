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

class SupervisorAgent(SyncBaseAgent):
    DOMAIN_OPTIONS = ("software_dev", "reverse_engineering")

    def __init__(self, inference_engine: Optional[MLXInferenceEngine] = None):
        super().__init__(
            name="supervisor",
            description="Routes user requests to software_dev and/or reverse_engineering",
        )
        self.inference_engine = inference_engine
        self._decision_cache: dict[str, dict] = {}

    def _build_routing_prompt(self, user_input: str) -> str:
        system_prompt = (
            "You are a routing supervisor for a multi-agent system. "
            "Use intent-based routing with only two valid domains: software_dev and reverse_engineering. "
            "Return strict JSON only."
        )
        return self.inference_engine.build_prompt(
            user_input=(
                "Task:\n"
                f"{user_input}\n\n"
                "Classify using these steps:\n"
                "1) Identify implementation intent (build/generate/test/design) -> software_dev\n"
                "2) Identify analysis/security/decompilation intent -> reverse_engineering\n"
                "3) If both intents are present, return both domains and split_tasks for each domain\n"
                "4) If only one intent is present, return one domain only\n\n"
                "Return strict JSON with schema:\n"
                '{"execution_domains": ["software_dev"] | ["reverse_engineering"] | ["software_dev", "reverse_engineering"], '
                '"primary_domain": "software_dev|reverse_engineering", '
                '"split_tasks": {} | {"software_dev": "...", "reverse_engineering": "..."}, '
                '"rationale": "short reason"}'
            ),
            context=None,
            system_prompt=system_prompt,
        )

    def _extract_decision(self, raw_output: str) -> Optional[dict]:
        cleaned = raw_output.strip()
        parsed = self._parse_json_from_text(cleaned)
        if parsed is not None:
            execution_domains = parsed.get("execution_domains", [])
            if not isinstance(execution_domains, list):
                execution_domains = []

            normalized_domains = [
                d for d in [str(x).strip().lower() for x in execution_domains]
                if d in self.DOMAIN_OPTIONS
            ]
            normalized_domains = list(dict.fromkeys(normalized_domains))

            primary_domain = str(parsed.get("primary_domain", "")).strip().lower()
            if primary_domain not in self.DOMAIN_OPTIONS:
                primary_domain = normalized_domains[0] if normalized_domains else "software_dev"

            split_tasks = parsed.get("split_tasks", {})
            if not isinstance(split_tasks, dict):
                split_tasks = {}

            normalized_split_tasks = {
                domain: str(split_tasks.get(domain, "")).strip()
                for domain in self.DOMAIN_OPTIONS
                if str(split_tasks.get(domain, "")).strip()
            }

            if not normalized_domains:
                normalized_domains = [primary_domain]

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
            decision = {
                "primary_domain": "software_dev",
                "execution_domains": ["software_dev"],
                "split_tasks": {},
            }
            self._decision_cache[user_input] = decision
            return decision

        prompt = self._build_routing_prompt(user_input)
        config = GenerationConfig(max_tokens=140, temperature=0.0)

        try:
            output = self.inference_engine.generate(prompt=prompt, config=config, stream=False)
            decision = self._extract_decision(output)
            if decision is not None:
                self._decision_cache[user_input] = decision
                return decision
        except Exception:
            pass

        decision = {
            "primary_domain": "software_dev",
            "execution_domains": ["software_dev"],
            "split_tasks": {},
        }
        self._decision_cache[user_input] = decision
        return decision

    @staticmethod
    def _parse_json_from_text(text: str) -> Optional[dict]:
        """Parse JSON robustly from raw LLM text (supports fenced and prose-wrapped JSON)."""
        candidates: list[str] = []
        stripped = text.strip()

        if stripped.startswith("```"):
            stripped = re.sub(r"^```(?:json)?", "", stripped).strip()
            stripped = re.sub(r"```$", "", stripped).strip()
        candidates.append(stripped)

        block = SupervisorAgent._extract_first_braced_block(stripped)
        if block:
            candidates.append(block)

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
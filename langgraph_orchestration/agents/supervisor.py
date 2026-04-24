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

    def _build_routing_prompt(self, user_input: str) -> str:
        system_prompt = (
            "You are a routing supervisor for a multi-agent system. "
            "Decide whether to execute software_dev, reverse_engineering, or both domains. "
            "There are only two valid domains: software_dev and reverse_engineering. "
            "When both are needed, split the request into concise domain-specific subtasks. "
            "Return strict JSON only with this schema: "
            "{\"execution_domains\": [\"software_dev\", \"reverse_engineering\"], "
            "\"primary_domain\": \"software_dev|reverse_engineering\", "
            "\"split_tasks\": {\"software_dev\": \"...\", \"reverse_engineering\": \"...\"}, "
            "\"rationale\": \"short reason\"}."
        )
        return self.inference_engine.build_prompt(
            user_input=(
                "Decide route for this request:\n"
                f"{user_input}\n\n"
                "Guidance:\n"
                "- software_dev: implementation, testing, architecture, feature delivery\n"
                "- reverse_engineering: analysis, security/vulnerability, binary/behavior understanding\n"
                "- If both are needed, include both domains in execution_domains and split tasks clearly\n"
                "Output strict JSON only."
            ),
            context=None,
            system_prompt=system_prompt,
        )

    def _extract_decision(self, raw_output: str) -> Optional[dict]:
        cleaned = raw_output.strip()

        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()

        try:
            parsed = json.loads(cleaned)
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
        except Exception:
            pass

        lowered = cleaned.lower()

        matches = [
            option
            for option in self.DOMAIN_OPTIONS
            if re.search(rf"\b{re.escape(option)}\b", lowered)
        ]
        matches = list(dict.fromkeys(matches))
        if matches:
            return {
                "primary_domain": matches[0],
                "execution_domains": matches,
                "split_tasks": {},
            }

        return None
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> dict:
        if self.inference_engine is None:
            return {
                "primary_domain": "software_dev",
                "execution_domains": ["software_dev"],
                "split_tasks": {},
            }

        prompt = self._build_routing_prompt(user_input)
        config = GenerationConfig(max_tokens=220, temperature=0.0)

        try:
            output = self.inference_engine.generate(prompt=prompt, config=config, stream=False)
            decision = self._extract_decision(output)
            if decision is not None:
                return decision
        except Exception:
            pass

        return {
            "primary_domain": "software_dev",
            "execution_domains": ["software_dev"],
            "split_tasks": {},
        }
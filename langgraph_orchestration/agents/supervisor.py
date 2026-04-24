"""
Supervisor agent for domain routing and orchestration.

The Supervisor analyzes incoming requests and routes them to the
appropriate domain (software development or reverse engineering).
"""

import json
import re
from typing import Literal, Optional
from .base import SyncBaseAgent
from langgraph_orchestration.inference.inference_engine import (
    MLXInferenceEngine,
    GenerationConfig,
)


class SupervisorAgent(SyncBaseAgent):
    ROUTE_OPTIONS = ("software_dev", "reverse_engineering", "both")

    def __init__(self, inference_engine: Optional[MLXInferenceEngine] = None):
        super().__init__(
            name="supervisor",
            description="Routes user requests to software_dev, reverse_engineering, or both",
        )
        self.inference_engine = inference_engine

    def _build_routing_prompt(self, user_input: str) -> str:
        system_prompt = (
            "You are a routing supervisor for a multi-agent system. "
            "Your only task is to choose the best execution route. "
            "Available routes: software_dev, reverse_engineering, both. "
            "Return strict JSON only: {\"route\": \"software_dev|reverse_engineering|both\", \"rationale\": \"short reason\"}."
        )
        return self.inference_engine.build_prompt(
            user_input=(
                "Decide route for this request:\n"
                f"{user_input}\n\n"
                "Guidance:\n"
                "- software_dev: implementation, testing, architecture, feature delivery\n"
                "- reverse_engineering: analysis, security/vulnerability, binary/behavior understanding\n"
                "- both: request needs implementation and security/reverse-engineering perspectives\n"
                "Output strict JSON only."
            ),
            context=None,
            system_prompt=system_prompt,
        )

    def _extract_route(self, raw_output: str) -> Optional[Literal["software_dev", "reverse_engineering", "both"]]:
        cleaned = raw_output.strip()

        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()

        try:
            parsed = json.loads(cleaned)
            candidate = str(parsed.get("route", "")).strip().lower()
            if candidate in self.ROUTE_OPTIONS:
                return candidate
        except Exception:
            pass

        lowered = cleaned.lower()
        for option in self.ROUTE_OPTIONS:
            if re.search(rf"\b{re.escape(option)}\b", lowered):
                return option

        return None
    
    def invoke(
        self,
        user_input: str,
        context: Optional[list[str]] = None,
    ) -> Literal["software_dev", "reverse_engineering", "both"]:
        if self.inference_engine is None:
            return "both"

        prompt = self._build_routing_prompt(user_input)
        config = GenerationConfig(max_tokens=120, temperature=0.0)

        try:
            output = self.inference_engine.generate(prompt=prompt, config=config, stream=False)
            route = self._extract_route(output)
            if route is not None:
                return route
        except Exception:
            pass

        return "both"
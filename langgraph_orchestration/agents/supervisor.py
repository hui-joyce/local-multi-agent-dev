"""Supervisor agent for domain routing"""

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
    build_split_tasks_prompt,
)

class SupervisorAgent(SyncBaseAgent):
    DOMAIN_OPTIONS = ("software_dev", "reverse_engineering")
    LABEL_OPTIONS = ("SOFTWARE_DEV", "REVERSE_ENGINEERING", "BOTH")
    # Clear cache when it reaches this size to cap memory usage.
    _CACHE_MAX_SIZE = 1000

    def __init__(self, inference_engine: Optional[MLXInferenceEngine] = None):
        super().__init__(
            name="supervisor",
            description="Routes user requests to software_dev and/or reverse_engineering",
        )
        self.inference_engine = inference_engine
        self._decision_cache: dict[str, dict] = {}

    def _remove_thinking_blocks(self, text: str) -> str:
        """Remove internal reasoning blocks from text"""
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

    def _build_label_prompt(self, user_input: str) -> str:
        return build_label_routing_prompt(self.inference_engine, user_input)

    def _parse_label(self, raw_output: str) -> Optional[str]:
        cleaned_upper = self._remove_thinking_blocks(raw_output).upper()

        # Exact match first
        if cleaned_upper in self.LABEL_OPTIONS:
            return cleaned_upper

        # Line-based match
        for line in cleaned_upper.splitlines():
            token = line.strip().strip("`*_-. ")
            if token in self.LABEL_OPTIONS:
                return token

        # Fallback: return last mention (decision usually at end)
        last_match = None
        for label in self.LABEL_OPTIONS:
            if label in cleaned_upper:
                last_match = label
        return last_match

    def _extract_split_tasks(self, user_input: str) -> dict[str, str]:
        """Extract domain-specific subtasks from a multi-domain request"""
        normalized_input = re.sub(r"\s+", " ", user_input).strip()

        # Prefer deterministic splits for explicit "and then" requests.
        split_markers = (
            r"\band then\b",
            r"\bthen\b",
        )
        for marker in split_markers:
            match = re.search(marker, normalized_input, flags=re.IGNORECASE)
            if not match:
                continue

            software_part = normalized_input[: match.start()].strip(" ,;:-\n\t")
            reverse_part = normalized_input[match.end() :].strip(" ,;:-\n\t")

            if software_part and reverse_part:
                code_snippets = self._extract_code_blocks(user_input)
                
                if code_snippets:
                    software_part = f"{software_part}\n\n{code_snippets}"
                    reverse_part = f"{reverse_part}\n\n{code_snippets}"
                
                return {
                    "software_dev": software_part,
                    "reverse_engineering": reverse_part,
                }

        if self.inference_engine is None:
            return {}

        try:
            prompt = build_split_tasks_prompt(self.inference_engine, user_input)
            config = GenerationConfig(max_tokens=1200, temperature=0.0)
            output = self.inference_engine.generate(
                prompt=prompt,
                config=config,
                stream=False,
            )
            
            parsed = self._parse_json_from_text(output)
            if parsed is not None:
                split_tasks = {}
                if "software_dev" in parsed and parsed["software_dev"]:
                    split_tasks["software_dev"] = str(parsed["software_dev"]).strip()
                if "reverse_engineering" in parsed and parsed["reverse_engineering"]:
                    split_tasks["reverse_engineering"] = str(parsed["reverse_engineering"]).strip()
                return split_tasks
        except Exception:
            pass
        
        return {}
    
    def _extract_code_blocks(self, text: str) -> str:
        """Extract code blocks from text (markdown, labelled sections, indented blocks)"""
        seen = set()
        code_blocks = []
        
        for match in re.finditer(r"```(?:\w+)?\n(.*?)```", text, re.DOTALL):
            block = match.group(1).strip()
            if block and block not in seen:
                seen.add(block)
                code_blocks.append(block)
        
        for section in re.split(r"\n(?=[A-Z]|\Z)", text):
            if ":" in section:
                _, content = section.split(":", 1)
                content = content.strip()
                if content and ("\n" in content or any(c in content for c in "(){}[];")) and content not in seen:
                    seen.add(content)
                    code_blocks.append(content)
        
        lines = text.split("\n")
        indented_block = []
        for line in lines:
            if line.startswith(("    ", "\t")):
                indented_block.append(line)
            elif indented_block:
                block_text = "\n".join(indented_block).strip()
                if block_text and block_text not in seen:
                    seen.add(block_text)
                    code_blocks.append(block_text)
                indented_block = []
        
        if indented_block:
            block_text = "\n".join(indented_block).strip()
            if block_text and block_text not in seen:
                code_blocks.append(block_text)
        
        return "\n\n".join(code_blocks)

    def _build_decision(self, primary_domain: str, execution_domains: list, split_tasks: dict = None) -> dict:
        return {
            "primary_domain": primary_domain,
            "execution_domains": execution_domains,
            "split_tasks": split_tasks or {},
        }

    def _extract_decision(self, raw_output: str) -> Optional[dict]:
        cleaned = raw_output.strip()
        parsed = self._parse_json_from_text(cleaned)
        if parsed is None:
            return None
        
        execution_domains = parsed.get("execution_domains")
        if not isinstance(execution_domains, list) or not execution_domains:
            return None

        # Normalize and deduplicate domains
        normalized_domains = [
            str(d).strip().lower() for d in execution_domains if str(d).strip().lower() in self.DOMAIN_OPTIONS
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

        return self._build_decision(primary_domain, normalized_domains, split_tasks)
    
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

        for attempt in range(2):
            try:
                attempt_prompt = prompt
                if attempt == 1:
                    attempt_prompt = (
                        prompt
                        + "\n\nIMPORTANT: Output one label only: SOFTWARE_DEV or REVERSE_ENGINEERING or BOTH."
                    )

                # Capture generation metrics on the first attempt
                output = self.inference_engine.generate_with_metrics(
                    prompt=attempt_prompt,
                    config=config,
                )[0] if attempt == 0 else self.inference_engine.generate(
                    prompt=attempt_prompt,
                    config=config,
                    stream=False,
                )
                    
                label = self._parse_label(output)
                if label == "SOFTWARE_DEV":
                    decision = self._build_decision("software_dev", ["software_dev"])
                elif label == "REVERSE_ENGINEERING":
                    decision = self._build_decision("reverse_engineering", ["reverse_engineering"])
                elif label == "BOTH":
                    split_tasks = self._extract_split_tasks(user_input)
                    decision = self._build_decision("software_dev", ["software_dev", "reverse_engineering"], split_tasks)
                else:
                    continue
                
                if len(self._decision_cache) >= self._CACHE_MAX_SIZE:
                    self._decision_cache.clear()
                self._decision_cache[user_input] = decision
                return decision
            except Exception:
                continue

        raise RuntimeError("Supervisor routing failed: could not obtain a valid route label from model")

    def _parse_json_from_text(self, text: str) -> Optional[dict]:
        stripped = self._remove_thinking_blocks(text)

        if stripped.startswith("```"):
            stripped = re.sub(r"^```(?:json)?", "", stripped).strip()
            stripped = re.sub(r"```$", "", stripped).strip()
        
        candidates = [stripped]
        
        for block in [self._extract_braced_block(stripped), self._extract_braced_block(stripped, from_end=True)]:
            if block and block not in candidates:
                candidates.append(block)

        for candidate in candidates:
            if candidate:
                try:
                    parsed = json.loads(candidate)
                    if isinstance(parsed, dict):
                        return parsed
                except Exception:
                    continue
        return None

    @staticmethod
    def _extract_braced_block(text: str, from_end: bool = False) -> str:
        search_pos = text.rfind("}") if from_end else text.find("{")
        if search_pos == -1:
            return ""
        
        depth = 0
        step = -1 if from_end else 1
        range_iter = range(search_pos, -1 if from_end else len(text), step)
        
        for idx in range_iter:
            char = text[idx]
            if char == "}":
                depth += 1
            elif char == "{":
                depth -= 1
                if depth == 0:
                    return text[idx : search_pos + 1] if from_end else text[search_pos : idx + 1]
        
        return ""
"""Prompt templates for domain-specific orchestration flows."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any
import re

_PROMPT_ROOT = Path(__file__).resolve().parent.parent / "prompts_md"


@lru_cache(maxsize=128)
def load_prompt_file(relative_path: str) -> tuple[dict[str, str], str]:
	"""Load a markdown prompt file and return (frontmatter, body)."""
	prompt_path = _PROMPT_ROOT / relative_path
	content = prompt_path.read_text(encoding="utf-8")

	frontmatter: dict[str, str] = {}
	body = content

	if content.startswith("---"):
		end_idx = content.find("\n---", 3)
		if end_idx != -1:
			frontmatter_block = content[3:end_idx].strip("\n")
			body = content[end_idx + 4 :].lstrip("\n")

			for line in frontmatter_block.splitlines():
				if not line.strip():
					continue
				key, _, value = line.partition(":")
				if key and value is not None:
					frontmatter[key.strip()] = value.strip()

	return frontmatter, body


def render_prompt(relative_path: str, **kwargs: Any) -> tuple[str, str]:
	frontmatter, body = load_prompt_file(relative_path)
	system_prompt = frontmatter.get("system_prompt", "")

	# only replace simple identifier placeholders like {user_input}, {attempt}
	pattern = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")

	def _repl(match: re.Match) -> str:
		key = match.group(1)
		if key in kwargs:
			return str(kwargs[key])
		# leave unknown placeholders untouched to avoid accidental removal
		return match.group(0)

	rendered_body = pattern.sub(_repl, body)
	return system_prompt, rendered_body
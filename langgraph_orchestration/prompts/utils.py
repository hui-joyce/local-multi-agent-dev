from __future__ import annotations

def _truncate(text: str, limit: int) -> str:
    return text if len(text) <= limit else text[:limit].rstrip() + "\n\n[TRUNCATED]"
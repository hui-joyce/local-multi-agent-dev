from __future__ import annotations

import json
import logging
import os
from pathlib import Path

logger = logging.getLogger("mad.chat_history")

MAX_MESSAGES = 400

_DEFAULT_DIR = Path.home() / ".local" / "share" / "local-multi-agent-dev"

def history_path() -> Path:
    override = os.getenv("CHAT_HISTORY_FILE")
    if override:
        return Path(override).expanduser()
    base = os.getenv("CHAT_HISTORY_DIR")
    base_dir = Path(base).expanduser() if base else _DEFAULT_DIR
    return base_dir / "chat_history.json"

def _clean(history: list) -> list[dict]:
    out: list[dict] = []
    for m in history or []:
        if isinstance(m, dict) and "role" in m and "content" in m:
            out.append({"role": m["role"], "content": m["content"]})
    return out

def load_history() -> list[dict]:
    path = history_path()
    try:
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return _clean(data)
    except Exception:
        logger.exception("Failed to load chat history from %s", path)
    return []

def save_history(history: list[dict]) -> None:
    path = history_path()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        clean = _clean(history)[-MAX_MESSAGES:]
        path.write_text(json.dumps(clean, ensure_ascii=False), encoding="utf-8")
    except Exception:
        logger.exception("Failed to save chat history to %s", path)
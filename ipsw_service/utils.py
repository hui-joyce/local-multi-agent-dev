from __future__ import annotations

import json
import os
from typing import Any, Iterable, Optional

def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path

def write_text(path: str, content: str) -> None:
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)

def write_json(path: str, payload: Any) -> None:
    ensure_dir(os.path.dirname(path) or ".")
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=True)

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()

def find_first(paths: Iterable[str]) -> Optional[str]:
    for path in paths:
        if path and os.path.exists(path):
            return path
    return None

def list_files(root: str) -> list[str]:
    files: list[str] = []
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            files.append(os.path.join(dirpath, name))
    return files
from __future__ import annotations

import logging
from typing import Optional

logger = logging.getLogger("mad.security")

_LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1", ""}


def is_loopback_host(host: Optional[str]) -> bool:
    return (host or "").strip().lower() in _LOOPBACK_HOSTS


def enforce_bind_policy(host: str, *, surface: str) -> None:
    if is_loopback_host(host):
        return
    raise RuntimeError(
        f"{surface} refusing to start: bound to non-loopback host {host!r}. "
        "This is a local-only tool with no request authentication; bind to "
        "127.0.0.1 (set API_HOST=127.0.0.1)."
    )
"""Match binary names against Apple Security Release Notes"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

CACHE_SCHEMA_VERSION = 1
_DEFAULT_CACHE_DIR = Path(__file__).resolve().parent.parent / "data" / "security_notes"

# Suffixes that appear on binary/bundle names but not on Apple component names
_NAME_SUFFIXES = (".framework", ".dylib", ".bundle", ".kext", ".app")

# Trailing file version, e.g. "Foo.2.framework"
_VERSION_RE = re.compile(r"\.\d+(?=\.(?:framework|dylib|bundle|kext|app)$)")

_CAMEL_BOUNDARY_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")

_GENERIC_TOKENS = frozenset(
    {
        "service",
        "framework",
        "kit",
        "support",
        "ui",
        "core",
        "and",
        "for",
        "the",
        "of",
        "app",
        "os",
        "ios",
        "mac",
        "macos",
        "apple",
        "system",
        "private",
        "internal",
        "shared",
        "common",
        "lib",
        "daemon",
        "helper",
        "agent",
        "engine",
        "manager",
        "controller",
        "extension",
        "plugin",
        "feature",
        "api",
        "server",
        "client",
        "foundation",
        "util",
        "utils",
        "my",
    }
)

_ANCHOR_MIN_LEN = 7


def cache_dir() -> Path:
    """Directory holding cached advisories. Override with SECURITY_NOTES_DIR"""
    override = os.getenv("SECURITY_NOTES_DIR")
    return Path(override).expanduser() if override else _DEFAULT_CACHE_DIR


def cache_path(version: str) -> Path:
    return cache_dir() / f"ios-{version}.json"


def available_versions() -> list[str]:
    """Versions present in the local cache, newest first"""
    directory = cache_dir()
    if not directory.is_dir():
        return []
    versions = [
        path.stem[len("ios-") :]
        for path in directory.glob("ios-*.json")
        if path.stem.startswith("ios-")
    ]
    return sorted(versions, key=_version_key, reverse=True)


def _version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in version.split(".") if part.isdigit())


# Section: name normalisation


def _strip_suffix(name: str) -> str:
    base = os.path.basename(name.strip())
    base = _VERSION_RE.sub("", base)
    for suffix in _NAME_SUFFIXES:
        if base.lower().endswith(suffix):
            return base[: -len(suffix)]
    return base


def _normalize(name: str) -> str:
    # Collapse to alphanumerics so "Find My" == "FindMy"
    return re.sub(r"[^a-z0-9]+", "", _strip_suffix(name).lower())


def _singularize(token: str) -> str:
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def _significant_tokens(name: str) -> frozenset[str]:
    """Word tokens of a name: camelCase-split, singularized, generics removed"""
    words = _CAMEL_BOUNDARY_RE.sub(" ", _strip_suffix(name))
    tokens = {_singularize(token) for token in re.split(r"[^A-Za-z0-9]+", words.lower()) if token}
    return frozenset(token for token in tokens if token not in _GENERIC_TOKENS)


# Section: cache access


@lru_cache(maxsize=8)
def load_cached_components(version: str) -> tuple[str, ...]:
    """Advisory components for *version* from the local cache, or ()"""
    if not version:
        return ()
    path = cache_path(version)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return ()
    components = payload.get("components")
    if not isinstance(components, list):
        return ()
    return tuple(str(name) for name in components if isinstance(name, str))


@dataclass
class SecurityNotesService:
    """Matches binary names against one release's advisory components"""

    # normalized component name -> advisory component (exact, highest confidence)
    _index: dict[str, str] = field(default_factory=dict)
    # advisory component -> significant token set (token-subset fallback tier)
    _component_tokens: dict[str, frozenset[str]] = field(default_factory=dict)

    @classmethod
    def for_version(cls, version: str | None) -> SecurityNotesService:
        """Build from the local cache. Returns an empty service if absent"""
        return cls.from_components(load_cached_components(version or ""))

    @classmethod
    def from_components(cls, components) -> SecurityNotesService:
        service = cls()
        for component in components:
            service._index.setdefault(_normalize(component), component)
            service._component_tokens[component] = _significant_tokens(component)
        return service

    def has_entries(self) -> bool:
        return bool(self._index)

    def _match_by_tokens(self, component_name: str) -> str | None:
        """Match when every significant word of an advisory name is in the binary's"""
        binary_tokens = _significant_tokens(component_name)
        if not binary_tokens:
            return None
        best: tuple[int, int, str] | None = None  # (#tokens, anchor_len, name)
        for component, comp_tokens in sorted(self._component_tokens.items()):
            if not comp_tokens or not comp_tokens <= binary_tokens:
                continue
            anchor_len = max((len(token) for token in comp_tokens), default=0)
            if len(comp_tokens) < 2 and anchor_len < _ANCHOR_MIN_LEN:
                continue
            candidate = (len(comp_tokens), anchor_len, component)
            if best is None or candidate > best:
                best = candidate
        return best[2] if best else None

    def match_component(self, component_name: str) -> str | None:
        hit = self._index.get(_normalize(component_name))
        if hit:
            return hit

        # Retry using the final reverse-DNS segment, since advisories use component names
        if component_name.startswith(("com.", "org.", "io.")):
            last_segment = component_name.rsplit(".", 1)[-1]
            if last_segment:
                segment_hit = self._index.get(_normalize(last_segment))
                if segment_hit:
                    return segment_hit
                component_name = last_segment

        return self._match_by_tokens(component_name)

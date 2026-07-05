"""dynamic component-name matching against Apple Security Release Notes"""

from __future__ import annotations

import html as _html
import json
import os
import re
import urllib.request
from dataclasses import dataclass, field
from functools import lru_cache

_APPLE_SECURITY_RELEASES_URL = "https://support.apple.com/en-us/100100"
_HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X)"}
_HTTP_TIMEOUT = 15

_WAYBACK_INDEX_ORIGINAL = "support.apple.com/en-us/HT201222"
_WAYBACK_CDX_URL = (
    "http://web.archive.org/cdx/search/cdx?url={url}&output=json"
    "&fl=timestamp&collapse=timestamp:4&filter=statuscode:200"
)
_WAYBACK_SNAPSHOT_URL = "http://web.archive.org/web/{ts}id_/https://{url}"
_WAYBACK_TIMEOUT = 30

# suffixes that appear on binary/bundle names but not on Apple component names
_NAME_SUFFIXES = (".framework", ".dylib", ".bundle", ".kext", ".app")

# trailing file-version sitting
_VERSION_RE = re.compile(r"\.\d+(?=\.(?:framework|dylib|bundle|kext|app)$)")

_CAMEL_BOUNDARY_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")

_GENERIC_TOKENS = frozenset({
    "service", "framework", "kit", "support", "ui", "core", "and", "for", "the", "of",
    "app", "os", "ios", "mac", "macos", "apple", "system", "private", "internal",
    "shared", "common", "lib", "daemon", "helper", "agent", "engine", "manager",
    "controller", "extension", "plugin", "feature", "api", "server", "client",
    "foundation", "util", "utils", "my",
})

_ANCHOR_MIN_LEN = 7


def _strip_suffix(name: str) -> str:
    base = os.path.basename(name.strip())
    base = _VERSION_RE.sub("", base)
    for suffix in _NAME_SUFFIXES:
        if base.lower().endswith(suffix):
            return base[: -len(suffix)]
    return base


def _normalize(name: str) -> str:
    # collapse to alphanumerics so "Find My" == "FindMy"
    return re.sub(r"[^a-z0-9]+", "", _strip_suffix(name).lower())


def _singularize(token: str) -> str:
    if len(token) > 3 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def _significant_tokens(name: str) -> frozenset[str]:
    """Word tokens of a name, camelCase-split, singularized, minus generic words"""
    words = _CAMEL_BOUNDARY_RE.sub(" ", _strip_suffix(name))
    tokens = {
        _singularize(tok)
        for tok in re.split(r"[^A-Za-z0-9]+", words.lower())
        if tok
    }
    return frozenset(tok for tok in tokens if tok not in _GENERIC_TOKENS)

def _http_get(url: str, timeout: int = _HTTP_TIMEOUT, retries: int = 0) -> str | None:
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=_HTTP_HEADERS)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read().decode("utf-8", "replace")
        except Exception:
            if attempt == retries:
                return None
    return None


def _version_regexes(version: str) -> list[re.Pattern]:
    candidates = [version] + ([version[:-2]] if version.endswith(".0") else [])
    return [re.compile(r"(?<![A-Za-z])iOS\s+" + re.escape(v) + r"(?!\.?\d)") for v in candidates]


def _find_advisory_link(html_text: str, version_res: list[re.Pattern]) -> str | None:
    """Return the support.apple.com advisory URL for the given version.
    Handles live pages and Wayback snapshots"""
    for m in re.finditer(r'<a href="([^"]*support\.apple\.com/[^"]+)"[^>]*>([^<]+)</a>', html_text):
        text = _html.unescape(m.group(2))
        if not any(vr.search(text) for vr in version_res):
            continue
        real = re.search(r"https?://support\.apple\.com/.*$", m.group(1))
        if real:
            return real.group(0)
    return None


def _resolve_advisory_url(version: str) -> str | None:
    version_res = _version_regexes(version)

    index = _http_get(_APPLE_SECURITY_RELEASES_URL)
    if index:
        url = _find_advisory_link(index, version_res)
        if url:
            return url

    return _resolve_advisory_url_via_wayback(version_res)


@lru_cache(maxsize=1)
def _wayback_snapshot_timestamps() -> tuple[str, ...]:
    """Yearly Wayback capture timestamps of Apple's legacy index - oldest first"""
    cdx = _http_get(_WAYBACK_CDX_URL.format(url=_WAYBACK_INDEX_ORIGINAL),
                    timeout=_WAYBACK_TIMEOUT, retries=1)
    if not cdx:
        return ()
    try:
        rows = json.loads(cdx)
    except (ValueError, TypeError):
        return ()
    return tuple(r[0] for r in rows[1:] if r)  # rows[0] = CDX header


@lru_cache(maxsize=16)
def _wayback_snapshot_html(ts: str) -> str | None:
    return _http_get(_WAYBACK_SNAPSHOT_URL.format(ts=ts, url=_WAYBACK_INDEX_ORIGINAL),
                     timeout=_WAYBACK_TIMEOUT, retries=1)


def _resolve_advisory_url_via_wayback(version_res: list[re.Pattern]) -> str | None:
    # newest snapshot first: it lists everything up to its capture date, so a
    # recently-aged-off version is found on the first fetch
    for ts in reversed(_wayback_snapshot_timestamps()):
        html_text = _wayback_snapshot_html(ts)
        if not html_text:
            continue
        url = _find_advisory_link(html_text, version_res)
        if url:
            return url
    return None

def _parse_advisory_components(advisory_html: str) -> list[str]:
    """Extract component/feature names from an Apple advisory page"""
    components: list[str] = []
    seen: set[str] = set()
    headers = list(re.finditer(r"<h3[^>]*>(.*?)</h3>", advisory_html, re.S))
    for i, h in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(advisory_html)
        if "Available for" not in advisory_html[h.end():end]:
            continue
        name = _html.unescape(re.sub(r"<[^>]+>", "", h.group(1))).strip()
        if name and name not in seen:
            seen.add(name)
            components.append(name)
    return components

@lru_cache(maxsize=8)
def fetch_security_notes_components(version: str) -> tuple[str, ...]:
    if not version:
        return ()
    url = _resolve_advisory_url(version)
    if not url:
        return ()
    advisory = _http_get(url)
    if not advisory:
        return ()
    return tuple(_parse_advisory_components(advisory))


@dataclass
class SecurityNotesService:
    # normalized component name -> advisory component (exact, highest-confidence tier)
    _index: dict[str, str] = field(default_factory=dict)
    # advisory component -> its significant token set (token-subset fallback tier)
    _component_tokens: dict[str, frozenset[str]] = field(default_factory=dict)

    @classmethod
    def for_version(cls, version: str | None) -> "SecurityNotesService":
        return cls._from_components(fetch_security_notes_components(version or ""))

    @classmethod
    def _from_components(cls, components) -> "SecurityNotesService":
        service = cls()
        for component in components:
            service._index.setdefault(_normalize(component), component)
            service._component_tokens[component] = _significant_tokens(component)
        return service

    def has_entries(self) -> bool:
        return bool(self._index)

    def _match_by_tokens(self, component_name: str) -> str | None:
        """Match when the advisory component's significant words 
        are all present in the binary's tokens"""
        binary_tokens = _significant_tokens(component_name)
        if not binary_tokens:
            return None
        best: tuple[int, int, str] | None = None  # (#shared, anchor_len, name) for stable pick
        for component, comp_tokens in sorted(self._component_tokens.items()):
            if not comp_tokens or not comp_tokens <= binary_tokens:
                continue
            anchor_len = max((len(t) for t in comp_tokens), default=0)
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
        # Kext/bundle IDs are reverse-DNS (com.apple.security.sandbox)
        # Apple advisories name the component ("Sandbox")
        # Fall back to the final segment
        if component_name.startswith(("com.", "org.", "io.")):
            last_segment = component_name.rsplit(".", 1)[-1]
            if last_segment:
                seg_hit = self._index.get(_normalize(last_segment))
                if seg_hit:
                    return seg_hit
                component_name = last_segment
        # last resort: deterministic token-subset match
        return self._match_by_tokens(component_name)

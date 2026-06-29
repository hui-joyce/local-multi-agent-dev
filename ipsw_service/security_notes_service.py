"""dynamic component-name matching against Apple Security Release Notes"""

from __future__ import annotations

import html as _html
import os
import re
import urllib.request
from dataclasses import dataclass, field
from functools import lru_cache

_APPLE_SECURITY_RELEASES_URL = "https://support.apple.com/en-us/100100"
_HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X)"}
_HTTP_TIMEOUT = 15

# suffixes that appear on binary/bundle names but not on Apple component names
_NAME_SUFFIXES = (".framework", ".dylib", ".bundle", ".kext", ".app")

# trailing file-version sitting
_VERSION_RE = re.compile(r"\.\d+(?=\.(?:framework|dylib|bundle|kext|app)$)")

# apple advisory component name (non-derivable binary basename)
_COMPONENT_ALIASES: dict[str, list[str]] = {
    "Accessibility": ["AccessibilityUI"],
    "AirDrop": ["AirDropAsTCP"],
    "AppleGraphicsControl": ["GPUSupport"],
    "AVEVideoEncoder": ["AppleVideoEncoder"],
    "CommonCrypto": ["libcommonCrypto"],
    "FontParser": ["libFontParser"],
    "GPU Drivers": ["kernelcache"],
    "IOKit": ["kernelcache"],
    "Kernel": ["kernelcache"],
    "iCloud": ["CloudServices"],
    "Messages": ["MobileSMS"],
    "Notes": ["MobileNotes"],
    "Notifications": ["UserNotificationsCore"],
    "OpenSSL": ["libssl", "libcrypto"],
    "RPAC": ["libRPAC"],
    "Safari": ["MobileSafari"],
    "SQLite": ["libsqlite3"],
    "System Preferences": ["Preferences"],
    "WebKit": ["WebCore", "WebKitLegacy"],
    "Wi-Fi": ["WiFiKit"],
    "XPC": ["libxpc"],
    "zlib": ["libz"],
}

def _normalize(name: str) -> str:
    base = os.path.basename(name.strip()).lower()
    base = _VERSION_RE.sub("", base)
    for suffix in _NAME_SUFFIXES:
        if base.endswith(suffix):
            base = base[: -len(suffix)]
            break
    # collapse to alphanumerics so "Find My" == "FindMy"
    return re.sub(r"[^a-z0-9]+", "", base)

def _http_get(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, headers=_HTTP_HEADERS)
        with urllib.request.urlopen(req, timeout=_HTTP_TIMEOUT) as resp:
            return resp.read().decode("utf-8", "replace")
    except Exception:
        return None

def _resolve_advisory_url(version: str) -> str | None:
    """Find the Apple advisory URL for an iOS version via the releases index"""
    index = _http_get(_APPLE_SECURITY_RELEASES_URL)
    if not index:
        return None
    candidates = [version] + ([version[:-2]] if version.endswith(".0") else [])
    version_res = [
        re.compile(r"(?<![A-Za-z])iOS\s+" + re.escape(v) + r"(?!\.?\d)") for v in candidates
    ]
    for m in re.finditer(
        r'<a href="(https://support\.apple\.com/[^"]+)"[^>]*>([^<]+)</a>', index
    ):
        url, text = m.group(1), _html.unescape(m.group(2))
        if any(vr.search(text) for vr in version_res):
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
    _index: dict[str, str] = field(default_factory=dict)

    @classmethod
    def for_version(cls, version: str | None) -> "SecurityNotesService":
        return cls._from_components(fetch_security_notes_components(version or ""))

    @classmethod
    def _from_components(cls, components) -> "SecurityNotesService":
        service = cls()
        # index real component names first
        for component in components:
            service._index.setdefault(_normalize(component), component)
        for component in components:
            for alias in _COMPONENT_ALIASES.get(component, ()):
                service._index.setdefault(_normalize(alias), component)
        return service

    def has_entries(self) -> bool:
        return bool(self._index)

    def match_component(self, component_name: str) -> str | None:
        return self._index.get(_normalize(component_name))

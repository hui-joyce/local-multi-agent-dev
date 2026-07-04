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
    """Return the support.apple.com advisory URL whose anchor text names the version.

    Handles both the live page (direct https://support.apple.com/... hrefs) and
    Wayback snapshots"""
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
        hit = self._index.get(_normalize(component_name))
        if hit:
            return hit
        # Kext/bundle IDs are reverse-DNS (com.apple.security.sandbox)
        # Apple advisories name the component ("Sandbox")
        # Fall back to the final segment 
        if component_name.startswith(("com.", "org.", "io.")) and "." in component_name:
            last_segment = component_name.rsplit(".", 1)[-1]
            if last_segment:
                return self._index.get(_normalize(last_segment))
        return None

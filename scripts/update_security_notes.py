from __future__ import annotations

import argparse
import html
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ipsw_service.security_notes_service import (  # noqa: E402
    CACHE_SCHEMA_VERSION,
    available_versions,
    cache_dir,
    cache_path,
)

_RELEASES_INDEX_URL = "https://support.apple.com/en-us/100100"
_HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X)"}
_HTTP_TIMEOUT = 20

_ARCHIVE_INDEX_ORIGINAL = "support.apple.com/en-us/HT201222"
_ARCHIVE_CDX_URL = (
    "https://web.archive.org/cdx/search/cdx?url={url}&output=json"
    "&fl=timestamp&collapse=timestamp:4&filter=statuscode:200"
)
_ARCHIVE_SNAPSHOT_URL = "https://web.archive.org/web/{timestamp}id_/https://{url}"
_ARCHIVE_TIMEOUT = 45


def _http_get(url: str, timeout: int = _HTTP_TIMEOUT) -> str | None:
    try:
        request = urllib.request.Request(url, headers=_HTTP_HEADERS)
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", "replace")
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print(f"    fetch failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return None


def _find_advisory_url(index_html: str, version: str) -> str | None:
    candidates = [version] + ([version[:-2]] if version.endswith(".0") else [])
    patterns = [
        re.compile(r"(?<![A-Za-z])iOS\s+" + re.escape(candidate) + r"(?!\.?\d)")
        for candidate in candidates
    ]

    for match in re.finditer(
        r'<a href="([^"]*support\.apple\.com/[^"]+)"[^>]*>([^<]+)</a>', index_html
    ):
        text = html.unescape(match.group(2))
        if any(pattern.search(text) for pattern in patterns):
            absolute = re.search(r"https?://support\.apple\.com/.*$", match.group(1))
            if absolute:
                return absolute.group(0)
    return None


def _archive_snapshot_timestamps() -> list[str]:
    """Yearly Internet Archive captures of Apple's legacy index, newest first"""
    raw = _http_get(_ARCHIVE_CDX_URL.format(url=_ARCHIVE_INDEX_ORIGINAL), timeout=_ARCHIVE_TIMEOUT)
    if not raw:
        return []
    try:
        rows = json.loads(raw)
    except (ValueError, TypeError):
        return []
    return [row[0] for row in rows[1:] if row][::-1]  # rows[0] is the CDX header


def _find_advisory_url_via_archive(version: str) -> str | None:
    for timestamp in _archive_snapshot_timestamps():
        snapshot = _http_get(
            _ARCHIVE_SNAPSHOT_URL.format(timestamp=timestamp, url=_ARCHIVE_INDEX_ORIGINAL),
            timeout=_ARCHIVE_TIMEOUT,
        )
        if not snapshot:
            continue
        url = _find_advisory_url(snapshot, version)
        if url:
            return url
    return None


def parse_advisory_components(advisory_html: str) -> list[str]:
    """Component names from an Apple advisory page, in document order"""
    components: list[str] = []
    seen: set[str] = set()
    headers = list(re.finditer(r"<h3[^>]*>(.*?)</h3>", advisory_html, re.S))
    for index, header in enumerate(headers):
        end = headers[index + 1].start() if index + 1 < len(headers) else len(advisory_html)
        if "Available for" not in advisory_html[header.end() : end]:
            continue
        name = html.unescape(re.sub(r"<[^>]+>", "", header.group(1))).strip()
        if name and name not in seen:
            seen.add(name)
            components.append(name)
    return components


def _write_cache(version: str, url: str, components: list[str]) -> Path:
    path = cache_path(version)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": CACHE_SCHEMA_VERSION,
        "version": version,
        "source_url": url,
        "fetched_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "components": components,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def update_version(version: str, index_html: str, force: bool, use_archive: bool) -> bool:
    """Fetch and cache a security advisory"""
    path = cache_path(version)
    if path.exists() and not force:
        print(f"  [SKIP] iOS {version}: already cached ({path.name}); use --force to refresh")
        return True

    print(f"  [FETCH] iOS {version}")
    url = _find_advisory_url(index_html, version)
    if not url and use_archive:
        print("    not on the live index; searching the Internet Archive")
        url = _find_advisory_url_via_archive(version)
    if not url:
        hint = "" if use_archive else " (retry with --archive for aged-off releases)"
        print(
            f"    no advisory listed for iOS {version} on {_RELEASES_INDEX_URL}{hint}",
            file=sys.stderr,
        )
        return False

    advisory = _http_get(url)
    if not advisory:
        return False

    components = parse_advisory_components(advisory)
    if not components:
        print(f"    advisory at {url} listed no components", file=sys.stderr)
        return False

    written = _write_cache(version, url, components)
    print(f"    {len(components)} component(s) -> {written.relative_to(PROJECT_ROOT)}")
    return True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Download Apple Security Release Notes into the local cache.",
        epilog="The analysis pipeline reads only this cache and never goes online.",
    )
    parser.add_argument("versions", nargs="*", help="iOS versions, e.g. 26.4.1 26.4.2")
    parser.add_argument("--force", action="store_true", help="re-download versions already cached")
    parser.add_argument(
        "--archive",
        action="store_true",
        help=(
            "fall back to the Internet Archive for releases Apple has removed "
            "from its index (slower, third-party; acquisition only)"
        ),
    )
    parser.add_argument("--list", action="store_true", help="list cached versions and exit")
    args = parser.parse_args(argv)

    if args.list:
        cached = available_versions()
        print(f"Cache: {cache_dir()}")
        if not cached:
            print("  (empty)")
        for version in cached:
            print(f"  iOS {version}")
        return 0

    if not args.versions:
        parser.error("give at least one version, or use --list")

    print(f"Fetching from {_RELEASES_INDEX_URL}")
    index_html = _http_get(_RELEASES_INDEX_URL)
    if not index_html:
        print("Could not reach Apple's security releases index.", file=sys.stderr)
        return 1

    failed = [
        version
        for version in args.versions
        if not update_version(version, index_html, args.force, args.archive)
    ]
    if failed:
        print(f"\nFailed: {', '.join(failed)}", file=sys.stderr)
        return 1

    print(f"\nCache ready at {cache_dir()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

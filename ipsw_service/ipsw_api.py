"""Everything that talks to api.ipsw.me, and nothing else.

This is the only module in the project that opens a socket for analysis data,
which is why it is named for the API rather than for what it provides. Keeping
the raw HTTP client and the lookups built on it in one file means the offline
boundary is exactly one filename, and tests/test_offline_compliance.py can name
it without the exemption quietly covering anything else.

Downloading firmware itself goes through the `ipsw` CLI, not through here.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# ===========================================================================
# The raw client
#
# Four endpoints, no retries, no caching. If api.ipsw.me is unreachable the
# caller gets an exception and decides what that means -- for the nightly
# pipeline it means "try again tomorrow".
# ===========================================================================


@dataclass
class ApiResponse:
    data: Any
    status: int
    url: str


class IpswDownloadsClient:
    """Lightweight client for the IPSW Downloads API (api.ipsw.me)"""

    def __init__(self, base_url: str = "https://api.ipsw.me/v4", timeout: int = 15):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.user_agent = "local-multi-agent-dev/ipsw-client"

    def _get_json(self, path: str, params: dict[str, Any] | None = None) -> ApiResponse:
        params = params or {}
        query = f"?{urlencode(params)}" if params else ""
        url = f"{self.base_url}{path}{query}"
        req = Request(url, headers={"User-Agent": self.user_agent})
        with urlopen(req, timeout=self.timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            return ApiResponse(data=payload, status=resp.status, url=url)

    def get_devices(self) -> ApiResponse:
        return self._get_json("/devices")

    def get_device_firmwares(self, identifier: str, firmware_type: str = "ipsw") -> ApiResponse:
        params = {"type": firmware_type} if firmware_type else {}
        return self._get_json(f"/device/{identifier}", params=params)

    def get_version_firmwares(self, version: str) -> ApiResponse:
        return self._get_json(f"/ipsw/{version}")


# =========================================================================
# Catalog lookups
#
# The semantic layer: which device is newest, which build precedes this one,
# which identifier does 'iPhone 18 Pro' mean. All of it derived from the four
# endpoints above.
# =========================================================================


def _version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in str(version).split(".") if part.isdigit())


# iPhone18,1 -> family "iPhone", generation 18, model 1
_DEVICE_ID_RE = re.compile(r"^([A-Za-z]+)(\d+),(\d+)$")


class FirmwareCatalogService:
    """Use IPSW Downloads API to resolve firmware metadata"""

    def __init__(self, client: IpswDownloadsClient | None = None):
        self.client = client or IpswDownloadsClient()

    def list_ipsw_firmwares(self, identifier: str) -> list[dict]:
        """Every IPSW release for *identifier*, newest version first, [] on failure.

        Ordered by version, then release date so same-version rebuilds are
        deterministic.
        """
        try:
            response = self.client.get_device_firmwares(identifier, firmware_type="ipsw")
        except Exception:
            return []

        data = response.data
        if isinstance(data, dict):
            firmwares = data.get("firmwares") or data.get("firmware") or []
        elif isinstance(data, list):
            firmwares = data
        else:
            firmwares = []

        return sorted(
            (item for item in firmwares if isinstance(item, dict)),
            key=lambda item: (
                _version_tuple(item.get("version", "")),
                str(item.get("releasedate") or ""),
            ),
            reverse=True,
        )

    @staticmethod
    def _as_target(identifier: str, firmware: dict) -> dict:
        return {
            "device": identifier,
            "version": str(firmware.get("version", "")),
            "build": str(firmware.get("buildid", "")),
            "url": str(firmware.get("url") or ""),
            "released": str(firmware.get("releasedate") or ""),
            "signed": bool(firmware.get("signed")),
        }

    def resolve_latest_ipsw(self, identifier: str) -> dict | None:
        firmwares = self.list_ipsw_firmwares(identifier)
        return self._as_target(identifier, firmwares[0]) if firmwares else None

    def list_devices(self, family_prefix: str = "iPhone") -> list[str]:
        """Device identifiers in *family_prefix*, newest hardware first, [] on failure.

        Ordered by generation descending then model ascending: within a
        generation Apple assigns ``,1`` to the flagship that launches with it,
        and higher model numbers to the later, lower-tier variants (iPhone18,1
        is the 17 Pro; iPhone18,5 is the 17e).
        """
        try:
            response = self.client.get_devices()
        except Exception:
            return []

        ranked: list[tuple[int, int, str]] = []
        for item in response.data if isinstance(response.data, list) else []:
            if not isinstance(item, dict):
                continue
            identifier = str(item.get("identifier", ""))
            match = _DEVICE_ID_RE.match(identifier)
            if match and match.group(1) == family_prefix:
                ranked.append((-int(match.group(2)), int(match.group(3)), identifier))
        return [identifier for _, _, identifier in sorted(ranked)]

    def resolve_newest_device(self, family_prefix: str = "iPhone") -> str | None:
        """Newest device in *family_prefix* that has at least two releases to diff.

        Hardware released within the current OS cycle only has its launch
        build, so skipping to the next candidate keeps a diff pair available
        instead of stalling for a release cycle.
        """
        for identifier in self.list_devices(family_prefix):
            versions = {
                str(firmware.get("version", ""))
                for firmware in self.list_ipsw_firmwares(identifier)
            }
            if len(versions) >= 2:
                return identifier
        return None

    def resolve_previous_ipsw(self, identifier: str, version: str) -> dict | None:
        """Newest release for *identifier* older than *version*, or None.

        Compared by version rather than list position so it still resolves when
        *version* itself is absent from the catalog.
        """
        current = _version_tuple(version)
        if not current:
            return None
        for firmware in self.list_ipsw_firmwares(identifier):
            if _version_tuple(firmware.get("version", "")) < current:
                return self._as_target(identifier, firmware)
        return None

    def resolve_by_model_hint(self, user_input: str) -> str | None:
        match = re.search(
            r"\b(iPhone\d+,\d+|iPad\d+,\d+|Watch\d+,\d+|AppleTV\d+,\d+)\b", user_input
        )
        if match:
            return match.group(1)
        return None

    @staticmethod
    def family_prefix_for(user_input: str) -> str:
        """Device-identifier prefix implied by the OS/device family named in the request."""
        lowered = user_input.lower()
        if "ipad" in lowered:
            return "iPad"
        if "watch" in lowered:
            return "Watch"
        if "appletv" in lowered or "apple tv" in lowered or "tvos" in lowered:
            return "AppleTV"
        if "macos" in lowered or "mac " in lowered:
            return "Mac"
        return "iPhone"  # default, covers "ios"/"iphone"

    def resolve_targets_for_versions(
        self, versions: list[str], family_prefix: str = "iPhone"
    ) -> list[dict]:
        """Return build targets for the newest device covering all *versions*, or [] on failure"""
        builds_by_version: dict[str, dict[str, str]] = {}
        for version in versions:
            try:
                response = self.client.get_version_firmwares(version)
            except Exception:
                return []
            firmwares = response.data if isinstance(response.data, list) else []
            devices = {
                str(fw.get("identifier", "")): str(fw.get("buildid", ""))
                for fw in firmwares
                if re.fullmatch(rf"{family_prefix}\d+,\d+", str(fw.get("identifier", "")))
            }
            if not devices:
                return []
            builds_by_version[version] = devices

        common = set.intersection(*(set(d) for d in builds_by_version.values()))
        if not common:
            return []

        def rank(identifier: str) -> tuple:
            match = re.search(r"(\d+),(\d+)", identifier)
            return (int(match.group(1)), int(match.group(2))) if match else (0, 0)

        device = max(common, key=rank)
        return [
            {"device": device, "version": version, "build": builds_by_version[version][device]}
            for version in versions
        ]

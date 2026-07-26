from __future__ import annotations

import re
from typing import Optional

from ipsw_service.downloads_api import IpswDownloadsClient

class FirmwareCatalogService:
    """Use IPSW Downloads API to resolve firmware metadata"""

    def __init__(self, client: Optional[IpswDownloadsClient] = None):
        self.client = client or IpswDownloadsClient()

    def resolve_latest_ipsw(self, identifier: str) -> Optional[dict]:
        try:
            response = self.client.get_device_firmwares(identifier, firmware_type="ipsw")
        except Exception:
            return None

        data = response.data
        firmwares = []
        if isinstance(data, dict):
            firmwares = data.get("firmwares") or data.get("firmware") or []
        elif isinstance(data, list):
            firmwares = data

        if not firmwares:
            return None

        def version_key(item: dict) -> tuple:
            version = str(item.get("version", ""))
            return tuple(int(part) for part in version.split(".") if part.isdigit())

        latest = sorted(firmwares, key=version_key, reverse=True)[0]
        return {
            "device": identifier,
            "version": str(latest.get("version", "")),
            "build": str(latest.get("buildid", "")),
            "url": latest.get("url"),
        }

    def resolve_by_model_hint(self, user_input: str) -> Optional[str]:
        match = re.search(r"\b(iPhone\d+,\d+|iPad\d+,\d+|Watch\d+,\d+|AppleTV\d+,\d+)\b", user_input)
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

    def resolve_targets_for_versions(self, versions: list[str], family_prefix: str = "iPhone") -> list[dict]:
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
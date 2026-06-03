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
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import urlencode
from urllib.request import Request, urlopen

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

    def _get_json(self, path: str, params: Optional[dict[str, Any]] = None) -> ApiResponse:
        params = params or {}
        query = f"?{urlencode(params)}" if params else ""
        url = f"{self.base_url}{path}{query}"
        req = Request(url, headers={"User-Agent": self.user_agent})
        with urlopen(req, timeout=self.timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            return ApiResponse(data=payload, status=resp.status, url=url)

    def get_device_firmwares(self, identifier: str, firmware_type: str = "ipsw") -> ApiResponse:
        params = {"type": firmware_type} if firmware_type else {}
        return self._get_json(f"/device/{identifier}", params=params)
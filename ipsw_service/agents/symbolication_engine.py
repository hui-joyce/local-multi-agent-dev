from __future__ import annotations
from typing import Optional
from ipsw_service.cli import IpswCliRunner

class SymbolicationEngine:
    def __init__(self, runner: Optional[IpswCliRunner] = None):
        self.runner = runner or IpswCliRunner()

    def address_to_symbol(self, dsc_path: str, address: str) -> dict:
        result = self.runner.run(["dyld", "a2s", dsc_path, address])
        return self._build_result("address_to_symbol", result)

    def symbol_to_address(self, dsc_path: str, symbol: str, image: Optional[str] = None) -> dict:
        args = ["dyld", "symaddr", dsc_path, symbol]
        if image:
            args.extend(["--image", image])
        result = self.runner.run(args)
        return self._build_result("symbol_to_address", result)

    def xrefs(self, dsc_path: str, address: str, image: Optional[str] = None, all_images: bool = True) -> dict:
        args = ["dyld", "xref", dsc_path, address]
        if all_images:
            args.append("--all")
        if image:
            args.extend(["--image", image])
        result = self.runner.run(args)
        return self._build_result("xrefs", result)

    def _build_result(self, action: str, result) -> dict:
        return {
            "action": action,
            "success": result.success,
            "command": result.command,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
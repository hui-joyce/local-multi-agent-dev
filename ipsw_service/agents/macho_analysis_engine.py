from __future__ import annotations
from typing import Optional
from ipsw_service.cli import IpswCliRunner

class MachoAnalysisEngine:
    def __init__(self, runner: Optional[IpswCliRunner] = None):
        self.runner = runner or IpswCliRunner()

    def inspect(self, binary_path: str, json_output: bool = True) -> dict:
        args = ["macho", "info", binary_path]
        if json_output:
            args.append("--json")
        result = self.runner.run(args)
        return {
            "success": result.success,
            "command": result.command,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    def entitlements(self, binary_path: str) -> dict:
        result = self.runner.run(["macho", "info", "--ent", binary_path])
        return {
            "success": result.success,
            "command": result.command,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    def signature(self, binary_path: str) -> dict:
        result = self.runner.run(["macho", "info", "--sig", binary_path])
        return {
            "success": result.success,
            "command": result.command,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
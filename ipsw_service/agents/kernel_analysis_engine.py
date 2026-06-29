from __future__ import annotations

from typing import Optional

from ipsw_service.cli import IpswCliRunner

class KernelAnalysisEngine:
    def __init__(self, runner: Optional[IpswCliRunner] = None):
        self.runner = runner or IpswCliRunner()

    def diff_kexts(self, old_kernel: str, new_kernel: str) -> dict:
        args = ["kernel", "kexts", "--diff", old_kernel, new_kernel]
        result = self.runner.run(args, timeout=60 * 60)
        return {
            "success": result.success,
            "command": result.command,
            "diff": result.stdout,
            "stderr": result.stderr,
        }

    def diff_sandbox_ops(self, old_kernel: str, new_kernel: str) -> dict:
        args = ["sb", "opts", "--diff", old_kernel, new_kernel]
        result = self.runner.run(args, timeout=60 * 60)
        return {
            "success": result.success,
            "command": result.command,
            "diff": result.stdout,
            "stderr": result.stderr,
        }
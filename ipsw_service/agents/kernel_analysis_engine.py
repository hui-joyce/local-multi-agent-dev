from __future__ import annotations

from typing import Optional

from ipsw_service.cli import IpswCliRunner
from ipsw_service.parsing import parse_simple_list_output

class KernelAnalysisEngine:
    def __init__(self, runner: Optional[IpswCliRunner] = None):
        self.runner = runner or IpswCliRunner()

    def list_kexts(self, kernelcache_path: str, json_output: bool = False) -> dict:
        args = ["kernel", "kexts", kernelcache_path]
        if json_output:
            args.append("--json")
        result = self.runner.run(args)
        return {
            "success": result.success,
            "command": result.command,
            "kexts": parse_simple_list_output(result.stdout) if result.stdout else [],
            "stderr": result.stderr,
        }

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

    def syscalls(self, kernelcache_path: str) -> dict:
        args = ["kernel", "syscall", kernelcache_path]
        result = self.runner.run(args)
        return {
            "success": result.success,
            "command": result.command,
            "syscalls": parse_simple_list_output(result.stdout),
            "stderr": result.stderr,
        }
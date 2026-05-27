from __future__ import annotations
from typing import Optional
import os
import shlex
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

    def count_strings(
        self,
        binary_path: str,
        diff_report_root: Optional[str] = None,
        arch: Optional[str] = None,
        timeout: int = 300,
    ) -> dict:
        """Count statically embedded c-strings for a binary.
        - If the binary file exists and appears usable, run `ipsw macho info --strings <binary> | wc -l`.
        - Otherwise, if a dyld_shared_cache file is present under `diff_report_root`, route via
          `ipsw dyld macho <cache> <basename> --strings | wc -l` to avoid the DSC trap.
        - Uses shell pipeline to let `wc -l` count without buffering the full dump in Python.
        Returns a dict with keys: success, count, command, stdout, stderr.
        """
        def _parse_count(result) -> int:
            try:
                return int(result.stdout.strip()) if result.success and result.stdout.strip() else 0
            except ValueError:
                return 0

        def _run(command: str) -> dict:
            result = self.runner.run_shell(command, timeout=timeout)
            return {
                "success": result.success,
                "count": _parse_count(result),
                "command": result.command,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        def _find_dyld_cache() -> str:
            if not diff_report_root or not os.path.isdir(diff_report_root):
                return ""
            for root, _, files in os.walk(diff_report_root):
                for name in files:
                    if "dyld_shared_cache" in name:
                        return os.path.join(root, name)
            return ""

        base_name = os.path.basename(binary_path) if binary_path else ""
        cache_path = _find_dyld_cache()
        is_system_binary = any(segment in (binary_path or "") for segment in ("/System/Library/", "/usr/lib/"))
        arch_flag = f" --arch {shlex.quote(arch)}" if arch else ""

        if cache_path and (is_system_binary or not binary_path or not os.path.exists(binary_path) or os.path.getsize(binary_path) == 0):
            return _run(f"{shlex.quote(self.runner.executable)} dyld macho {shlex.quote(cache_path)} {shlex.quote(base_name)} --strings{arch_flag} | wc -l")

        if binary_path and os.path.exists(binary_path) and os.path.getsize(binary_path) > 0:
            direct = _run(f"{shlex.quote(self.runner.executable)} macho info --strings{arch_flag} {shlex.quote(binary_path)} | wc -l")
            if direct["count"] > 0 or not cache_path:
                return direct
            cached = _run(f"{shlex.quote(self.runner.executable)} dyld macho {shlex.quote(cache_path)} {shlex.quote(base_name)} --strings{arch_flag} | wc -l")
            return cached if cached["count"] > direct["count"] else direct

        if diff_report_root and os.path.isdir(diff_report_root):
            for root, _, files in os.walk(diff_report_root):
                for name in files:
                    if name == base_name:
                        return _run(f"{shlex.quote(self.runner.executable)} macho info --strings{arch_flag} {shlex.quote(os.path.join(root, name))} | wc -l")

        return {"success": False, "count": 0, "command": "", "stdout": "", "stderr": "could not locate binary or cache"}
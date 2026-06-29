from __future__ import annotations
from typing import Optional
import os
import shlex
from ipsw_service.cli import IpswCliRunner

class MachoAnalysisEngine:
    def __init__(self, runner: Optional[IpswCliRunner] = None):
        self.runner = runner or IpswCliRunner()

    def count_strings(
        self,
        binary_path: str,
        diff_report_root: Optional[str] = None,
        dyld_cache_path: Optional[str] = None,
        timeout: int = 300,
        arch: str = "arm64e",
    ) -> dict:
        """Count statically embedded c-strings for a binary.
        - If the binary file exists and appears usable, run `ipsw macho info --strings -a arm64e <binary> | wc -l`.
                - Otherwise, if a dyld_shared_cache file is present under `diff_report_root` or provided
                    explicitly via `dyld_cache_path`, route via
                    `ipsw dyld macho <cache> <path> --strings | wc -l` to avoid the DSC trap.
        - Uses shell pipeline to let `wc -l` count without buffering the full dump in Python.
        Returns a dict with keys: success, count, command, stdout, stderr.
        """

        def _run(command: str) -> dict:
            result = self.runner.run_shell(command, timeout=timeout)
            count = 0
            if result.stdout:
                try:
                    count = int(result.stdout.strip())
                except ValueError:
                    count = len([line for line in result.stdout.splitlines() if line.strip()])
            return {
                "success": result.success,
                "count": count,
                "command": result.command,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }

        binary_path = (binary_path or "").strip()
        base_name = os.path.basename(binary_path) if binary_path else ""
        cache_path = ""
        if dyld_cache_path and os.path.exists(dyld_cache_path):
            cache_path = dyld_cache_path
        elif diff_report_root:
            # fallback to look in the extracted diff root
            for root, _, files in os.walk(diff_report_root):
                for f in files:
                    if "dyld_shared_cache" in f:
                        cache_path = os.path.join(root, f)
                        break
                if cache_path:
                    break

        is_system_binary = any(segment in binary_path for segment in ("/System/Library/", "/usr/lib/"))
        arch_arg = f" -a {shlex.quote(arch)}" if arch else ""
        dyld_target = binary_path if (binary_path.startswith("/") or "/" in binary_path) else base_name

        if cache_path and (is_system_binary or not binary_path or not os.path.exists(binary_path) or os.path.getsize(binary_path) == 0):
            dyld_cmd = (
                f"{shlex.quote(self.runner.executable)} dyld macho {shlex.quote(cache_path)} "
                f"{shlex.quote(dyld_target)} --strings | wc -l"
            )
            return _run(dyld_cmd) 

        if binary_path and os.path.exists(binary_path) and os.path.getsize(binary_path) > 0:
            direct_cmd = f"{shlex.quote(self.runner.executable)} macho info --strings{arch_arg} {shlex.quote(binary_path)} | wc -l"
            direct = _run(direct_cmd) # <-- PASS RAW COMMAND
            if direct["count"] > 0 or not cache_path:
                return direct
            
            cached_cmd = (
                f"{shlex.quote(self.runner.executable)} dyld macho {shlex.quote(cache_path)} "
                f"{shlex.quote(dyld_target)} --strings | wc -l"
            )
            cached = _run(cached_cmd) # <-- PASS RAW COMMAND
            return cached if cached["count"] > direct["count"] else direct

        return {"success": False, "count": 0, "command": "", "stdout": "", "stderr": "could not locate binary or cache"}
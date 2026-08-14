from __future__ import annotations

import os
import shlex
import shutil

from ipsw_service.cli import (
    IpswCliRunner,
    build_diff_args,
    build_extract_args,
)
from ipsw_service.parsing import ensure_dir, extract_paths_by_keyword, list_files

class IpswExtractor:
    """Extracts dyld_shared_cache and kernelcache out of IPSW archives"""

    def __init__(self, runner: IpswCliRunner | None = None, workspace_root: str | None = None):
        self.runner = runner or IpswCliRunner(cwd=workspace_root)
        self.workspace_root = workspace_root or os.getcwd()

    def extract(self, ipsw_paths: list[str], output_dir: str, dyld_arch: str = "arm64e") -> dict:
        ensure_dir(output_dir)
        results: list[dict] = []
        overall_success = True

        for ipsw in ipsw_paths:
            ipsw_name = os.path.basename(ipsw)
            ipsw_dir = os.path.join(output_dir, ipsw_name.replace(".ipsw", ""))
            ensure_dir(ipsw_dir)
            commands: list[str] = []
            errors: list[str] = []

            existing_dyld_paths = self._find_extracted_paths(ipsw_dir, "dyld_shared_cache")
            existing_dyld_paths = [
                p
                for p in existing_dyld_paths
                if os.path.exists(p) and "." not in os.path.basename(p)
            ]
            if existing_dyld_paths:
                commands.append(f"[skipped] dyld already extracted to {ipsw_dir}")
                dyld_result_stdout = ""
                dyld_result_stderr = ""
                dyld_success = True
            else:
                dyld_args = build_extract_args(
                    ipsw,
                    output_dir=ipsw_dir,
                    dyld=True,
                    dyld_arch=dyld_arch,
                )
                dyld_result = self.runner.run(dyld_args, timeout=4 * 60 * 60)
                commands.append(dyld_result.command)
                dyld_result_stdout = dyld_result.stdout
                dyld_result_stderr = dyld_result.stderr
                dyld_success = dyld_result.success
                if not dyld_success:
                    errors.append(dyld_result.stderr or "dyld extraction failed")
                    overall_success = False

            existing_kernel_paths = self._find_extracted_paths(ipsw_dir, "kernelcache")
            existing_kernel_paths = [p for p in existing_kernel_paths if os.path.exists(p)]
            if existing_kernel_paths:
                commands.append(f"[skipped] kernelcache already extracted to {ipsw_dir}")
                kernel_result_stdout = ""
                kernel_result_stderr = ""
                kernel_success = True
            else:
                kernel_args = build_extract_args(
                    ipsw,
                    output_dir=ipsw_dir,
                    kernel=True,
                )
                kernel_result = self.runner.run(kernel_args, timeout=60 * 60)
                commands.append(kernel_result.command)
                kernel_result_stdout = kernel_result.stdout
                kernel_result_stderr = kernel_result.stderr
                kernel_success = kernel_result.success
                if not kernel_success:
                    errors.append(kernel_result.stderr or "kernel extraction failed")
                    overall_success = False

            # resolve paths: prefer paths surfaced by CLI output, then fall back to filesystem scan
            dyld_paths = extract_paths_by_keyword(
                dyld_result_stdout + "\n" + dyld_result_stderr, "dyld_shared_cache"
            )
            kernel_paths = extract_paths_by_keyword(
                kernel_result_stdout + "\n" + kernel_result_stderr, "kernelcache"
            )
            dyld_paths = [path for path in dyld_paths if os.path.exists(path)]
            kernel_paths = [path for path in kernel_paths if os.path.exists(path)]
            if not dyld_paths:
                dyld_paths = self._find_extracted_paths(ipsw_dir, "dyld_shared_cache")
                # only keep the base cache file (no subcache shard extensions like .01, .02…)
                dyld_paths = [p for p in dyld_paths if "." not in os.path.basename(p)]
            if not kernel_paths:
                kernel_paths = self._find_extracted_paths(ipsw_dir, "kernelcache")

            results.append(
                {
                    "ipsw": ipsw,
                    "output_dir": ipsw_dir,
                    "dyld_paths": dyld_paths,
                    "kernel_paths": kernel_paths,
                    "commands": commands,
                    "errors": errors,
                }
            )

        return {
            "success": overall_success,
            "extractions": results,
        }

    def _find_extracted_paths(self, root: str, keyword: str) -> list[str]:
        matches: list[str] = []
        for path in list_files(root):
            name = os.path.basename(path)
            if keyword in name:
                matches.append(path)
        return matches

class FrameworkDiffEngine:
    """``ipsw diff`` -- userland frameworks, launchd, strings, entitlements"""

    def __init__(self, runner: IpswCliRunner | None = None):
        self.runner = runner or IpswCliRunner()

    def diff_firmware(
        self,
        old_ipsw: str,
        new_ipsw: str,
        output_dir: str,
        include_fw: bool = True,
        include_launchd: bool = True,
        include_strs: bool = True,
        markdown: bool = True,
        low_memory: bool = False,
        clean: bool = False,
    ) -> dict:
        ensure_dir(output_dir)
        args = build_diff_args(
            old_ipsw=old_ipsw,
            new_ipsw=new_ipsw,
            output_dir=output_dir,
            markdown=markdown,
            include_fw=include_fw,
            include_launchd=include_launchd,
            include_strs=include_strs,
            low_memory=low_memory,
            clean=clean,
        )

        result = self.runner.run_with_sudo_fallback(args, timeout=4 * 60 * 60)

        files = list_files(output_dir)
        markdown_report = next(
            (path for path in files if path.replace("\\", "/").lower().endswith("/readme.md")), ""
        )
        if not markdown_report:
            markdown_report = next(
                (
                    path
                    for path in files
                    if path.lower().endswith(".md") and not path.lower().endswith("report.md")
                ),
                "",
            )
        json_report = next(
            (path for path in files if path.replace("\\", "/").lower().endswith("/report.json")), ""
        )
        if not json_report:
            json_report = next((path for path in files if path.lower().endswith("report.json")), "")

        return {
            "success": result.success,
            "command": result.command,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output_dir": output_dir,
            "markdown_report": markdown_report,
            "json_report": json_report,
            "files": files,
        }

    def entitlements_diff(
        self, old_ipsw: str, new_ipsw: str, output_dir: str, low_memory: bool = False
    ) -> dict:
        ensure_dir(output_dir)
        args = build_diff_args(
            old_ipsw=old_ipsw,
            new_ipsw=new_ipsw,
            output_dir=output_dir,
            markdown=False,
            include_fw=False,
            include_launchd=False,
            include_entitlements=True,
            include_sandbox=False,
            include_strs=False,
            low_memory=low_memory,
            json_output=True,
        )
        result = self.runner.run(args, timeout=4 * 60 * 60)

        for root, dirs, _ in os.walk(output_dir, topdown=False):
            for d in dirs:
                if d == "ENTITLEMENTS":
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except Exception:
                        pass

        files = list_files(output_dir)
        json_report = next((f for f in files if f.endswith(".json")), None)
        if json_report:
            idiff_path = os.path.join(output_dir, "entitlements.idiff")
            try:
                os.rename(json_report, idiff_path)
            except Exception:
                pass
            files = list_files(output_dir)

        return {
            "success": result.success,
            "command": result.command,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output_dir": output_dir,
            "files": files,
        }


class KernelAnalysisEngine:
    """``ipsw kernel`` and ``ipsw sb`` -- kext and sandbox-operation diffs."""

    def __init__(self, runner: IpswCliRunner | None = None):
        self.runner = runner or IpswCliRunner()

    def diff_kexts(self, old_kernel: str, new_kernel: str) -> dict:
        return self._diff(["kernel", "kexts", "--diff", old_kernel, new_kernel])

    def diff_sandbox_ops(self, old_kernel: str, new_kernel: str) -> dict:
        return self._diff(["sb", "opts", "--diff", old_kernel, new_kernel])

    def _diff(self, args: list[str]) -> dict:
        result = self.runner.run(args, timeout=60 * 60)
        return {
            "success": result.success,
            "command": result.command,
            "diff": result.stdout,
            "stderr": result.stderr,
        }

class MachoAnalysisEngine:
    """``ipsw macho`` / ``ipsw dyld macho`` -- static string counts"""

    def __init__(self, runner: IpswCliRunner | None = None):
        self.runner = runner or IpswCliRunner()

    def count_strings(
        self,
        binary_path: str,
        diff_report_root: str | None = None,
        dyld_cache_path: str | None = None,
        timeout: int = 300,
        arch: str = "arm64e",
    ) -> dict:
        """Count statically embedded c-strings for a binary.

        Uses ``ipsw macho info --strings`` for standalone binaries, or 
        ``ipsw dyld macho`` when the binary is inside a dyld shared cache. 
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

        is_system_binary = any(
            segment in binary_path for segment in ("/System/Library/", "/usr/lib/")
        )
        arch_arg = f" -a {shlex.quote(arch)}" if arch else ""
        dyld_target = (
            binary_path if (binary_path.startswith("/") or "/" in binary_path) else base_name
        )

        if cache_path and (
            is_system_binary
            or not binary_path
            or not os.path.exists(binary_path)
            or os.path.getsize(binary_path) == 0
        ):
            dyld_cmd = (
                f"{shlex.quote(self.runner.executable)} dyld macho {shlex.quote(cache_path)} "
                f"{shlex.quote(dyld_target)} --strings | wc -l"
            )
            return _run(dyld_cmd)

        if binary_path and os.path.exists(binary_path) and os.path.getsize(binary_path) > 0:
            direct_cmd = (
                f"{shlex.quote(self.runner.executable)} macho info --strings{arch_arg} "
                f"{shlex.quote(binary_path)} | wc -l"
            )
            direct = _run(direct_cmd)
            if direct["count"] > 0 or not cache_path:
                return direct

            cached_cmd = (
                f"{shlex.quote(self.runner.executable)} dyld macho {shlex.quote(cache_path)} "
                f"{shlex.quote(dyld_target)} --strings | wc -l"
            )
            cached = _run(cached_cmd)
            return cached if cached["count"] > direct["count"] else direct

        return {
            "success": False,
            "count": 0,
            "command": "",
            "stdout": "",
            "stderr": "could not locate binary or cache",
        }
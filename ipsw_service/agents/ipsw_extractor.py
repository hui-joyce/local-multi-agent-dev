from __future__ import annotations

import os
from typing import Optional

from ipsw_service.cli import IpswCliRunner, build_extract_args
from ipsw_service.parsing import extract_paths_by_keyword
from ipsw_service.utils import ensure_dir, list_files

class IpswExtractorAgent:
    def __init__(self, runner: Optional[IpswCliRunner] = None, workspace_root: Optional[str] = None):
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

            dyld_args = build_extract_args(
                ipsw,
                output_dir=ipsw_dir,
                dyld=True,
                dyld_arch=dyld_arch,
            )
            dyld_result = self.runner.run(dyld_args, timeout=4 * 60 * 60)
            commands.append(dyld_result.command)
            if not dyld_result.success:
                errors.append(dyld_result.stderr or "dyld extraction failed")
                overall_success = False

            kernel_args = build_extract_args(
                ipsw,
                output_dir=ipsw_dir,
                kernel=True,
            )
            kernel_result = self.runner.run(kernel_args, timeout=60 * 60)
            commands.append(kernel_result.command)
            if not kernel_result.success:
                errors.append(kernel_result.stderr or "kernel extraction failed")
                overall_success = False

            dyld_paths = extract_paths_by_keyword(dyld_result.stdout + "\n" + dyld_result.stderr, "dyld_shared_cache")
            kernel_paths = extract_paths_by_keyword(kernel_result.stdout + "\n" + kernel_result.stderr, "kernelcache")
            if not dyld_paths:
                dyld_paths = self._find_extracted_paths(ipsw_dir, "dyld_shared_cache")
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
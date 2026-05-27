from __future__ import annotations

import os
from typing import Optional

from ipsw_service.cli import IpswCliRunner, build_diff_args
from ipsw_service.utils import ensure_dir, list_files

class FrameworkDiffEngine:
    def __init__(self, runner: Optional[IpswCliRunner] = None):
        self.runner = runner or IpswCliRunner()

    def diff_firmware(
        self,
        old_ipsw: str,
        new_ipsw: str,
        output_dir: str,
        include_fw: bool = True,
        include_launchd: bool = True,
        markdown: bool = True,
        low_memory: bool = False,
    ) -> dict:
        ensure_dir(output_dir)
        args = build_diff_args(
            old_ipsw=old_ipsw,
            new_ipsw=new_ipsw,
            output_dir=output_dir,
            markdown=markdown,
            include_fw=include_fw,
            include_launchd=include_launchd,
            low_memory=low_memory,
        )

        result = self.runner.run(args, timeout=4 * 60 * 60)
        files = list_files(output_dir)
        markdown_report = next((path for path in files if path.replace("\\", "/").lower().endswith("/readme.md")), "")
        if not markdown_report:
            markdown_report = next((path for path in files if path.lower().endswith(".md") and not path.lower().endswith("report.md")), "")
        json_report = next((path for path in files if path.replace("\\", "/").lower().endswith("/report.json")), "")
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

    def entitlements_diff(self, old_ipsw: str, new_ipsw: str, output_dir: str, low_memory: bool = False) -> dict:
        ensure_dir(output_dir)
        args = build_diff_args(
            old_ipsw=old_ipsw,
            new_ipsw=new_ipsw,
            output_dir=output_dir,
            markdown=False,
            include_fw=False,
            include_launchd=False,
            include_entitlements=True,
            low_memory=low_memory,
        )
        result = self.runner.run(args, timeout=4 * 60 * 60)
        files = list_files(output_dir)
        return {
            "success": result.success,
            "command": result.command,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "output_dir": output_dir,
            "files": files,
        }
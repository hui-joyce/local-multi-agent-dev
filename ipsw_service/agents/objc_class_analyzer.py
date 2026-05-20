from __future__ import annotations

import os
from typing import Optional

from ipsw_service.cli import IpswCliRunner
from ipsw_service.utils import ensure_dir, list_files

class ObjcClassAnalyzer:
    def __init__(self, runner: Optional[IpswCliRunner] = None):
        self.runner = runner or IpswCliRunner()

    def dump_headers(self, dsc_path: str, image: str, output_dir: str, swift: bool = False) -> dict:
        ensure_dir(output_dir)
        command = "swift-dump" if swift else "class-dump"
        args = [command, dsc_path, image, "--headers", "-o", output_dir]
        result = self.runner.run(args, timeout=60 * 60)
        header_files = [path for path in list_files(output_dir) if path.endswith(".h")]
        return {
            "success": result.success,
            "command": result.command,
            "output_dir": output_dir,
            "header_count": len(header_files),
            "headers": header_files[:50],
            "stderr": result.stderr,
        }

    def list_classes(self, dsc_path: str, image: Optional[str] = None) -> dict:
        args = ["dyld", "objc", "--class", dsc_path]
        if image:
            args.extend(["--image", image])
        result = self.runner.run(args)
        classes = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        return {
            "success": result.success,
            "command": result.command,
            "class_count": len(classes),
            "classes": classes[:200],
            "stderr": result.stderr,
        }
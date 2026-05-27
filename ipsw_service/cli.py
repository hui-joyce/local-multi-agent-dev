from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from typing import Optional

@dataclass
class CommandResult:
    args: list[str]
    command: str
    stdout: str
    stderr: str
    exit_code: int
    duration_seconds: float
    success: bool

class IpswCliRunner:
    def __init__(self, executable: str = "ipsw", cwd: Optional[str] = None):
        self.executable = executable
        self.cwd = cwd

    def run(self, args: list[str], timeout: int = 600, cwd: Optional[str] = None) -> CommandResult:
        cmd = [self.executable, *args]
        started = time.perf_counter()
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd or self.cwd,
            )
            duration = time.perf_counter() - started
            stdout = (proc.stdout or "").strip()
            stderr = (proc.stderr or "").strip()
            return CommandResult(
                args=cmd,
                command=" ".join(cmd),
                stdout=stdout,
                stderr=stderr,
                exit_code=proc.returncode,
                duration_seconds=round(duration, 3),
                success=proc.returncode == 0,
            )
        except FileNotFoundError:
            duration = time.perf_counter() - started
            return CommandResult(
                args=cmd,
                command=" ".join(cmd),
                stdout="",
                stderr="ipsw CLI not found in PATH",
                exit_code=127,
                duration_seconds=round(duration, 3),
                success=False,
            )
        except subprocess.TimeoutExpired:
            duration = time.perf_counter() - started
            return CommandResult(
                args=cmd,
                command=" ".join(cmd),
                stdout="",
                stderr=f"ipsw command timed out after {timeout}s",
                exit_code=124,
                duration_seconds=round(duration, 3),
                success=False,
            )

    def run_shell(self, command: str, timeout: int = 600, cwd: Optional[str] = None) -> CommandResult:
        """Run a shell command string (supports pipes) and return a CommandResult.

        This is used for lightweight shell pipelines such as piping output to `wc -l` to avoid
        capturing extremely large stdout blobs in Python memory.
        """
        started = time.perf_counter()
        try:
            proc = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd or self.cwd,
            )
            duration = time.perf_counter() - started
            stdout = (proc.stdout or "").strip()
            stderr = (proc.stderr or "").strip()
            return CommandResult(
                args=[command],
                command=command,
                stdout=stdout,
                stderr=stderr,
                exit_code=proc.returncode,
                duration_seconds=round(duration, 3),
                success=proc.returncode == 0,
            )
        except FileNotFoundError:
            duration = time.perf_counter() - started
            return CommandResult(
                args=[command],
                command=command,
                stdout="",
                stderr="shell execution failed: command not found",
                exit_code=127,
                duration_seconds=round(duration, 3),
                success=False,
            )
        except subprocess.TimeoutExpired:
            duration = time.perf_counter() - started
            return CommandResult(
                args=[command],
                command=command,
                stdout="",
                stderr=f"shell command timed out after {timeout}s",
                exit_code=124,
                duration_seconds=round(duration, 3),
                success=False,
            )


def build_download_args(
    device: str,
    version: Optional[str] = None,
    build: Optional[str] = None,
    output_dir: Optional[str] = None,
    resume_all: bool = True,
    latest: bool = False,
    include_kernel: bool = False,
    include_dyld: bool = False,
) -> list[str]:
    args = ["download", "ipsw", "--device", str(device)]
    if build:
        args.extend(["--build", str(build)])
    elif version:
        args.extend(["--version", str(version)])
    elif latest:
        args.append("--latest")
    if include_kernel:
        args.append("--kernel")
    if include_dyld:
        args.append("--dyld")
    if output_dir:
        args.extend(["--output", str(output_dir)])
    if resume_all:
        args.append("--resume-all")
    return args


def build_extract_args(
    ipsw_path: str,
    output_dir: Optional[str] = None,
    dyld: bool = False,
    kernel: bool = False,
    dyld_arch: str = "arm64e",
    extra_args: Optional[list[str]] = None,
) -> list[str]:
    args = ["extract"]
    if dyld:
        args.extend(["--dyld", "--dyld-arch", dyld_arch])
    if kernel:
        args.append("--kernel")
    if extra_args:
        args.extend(extra_args)
    if output_dir:
        args.extend(["--output", str(output_dir)])
    args.append(str(ipsw_path))
    return args


def build_diff_args(
    old_ipsw: str,
    new_ipsw: str,
    output_dir: Optional[str] = None,
    markdown: bool = True,
    include_fw: bool = True,
    include_launchd: bool = True,
    include_entitlements: bool = False,
    low_memory: bool = False,
    json_output: bool = False,
) -> list[str]:
    args = ["diff", str(old_ipsw), str(new_ipsw)]
    if output_dir:
        args.extend(["--output", str(output_dir)])
    if markdown:
        args.append("--markdown")
    if include_fw:
        args.append("--fw")
    if include_launchd:
        args.append("--launchd")
    if include_entitlements:
        args.append("--ent")
    if low_memory:
        args.append("--low-memory")
    if json_output:
        args.append("--json")
    return args


def build_dyld_diff_args(
    old_dsc: str,
    new_dsc: str,
    json_output: bool = False,
) -> list[str]:
    args = ["dyld", "info", "--dylibs", "--diff", str(old_dsc), str(new_dsc)]
    if json_output:
        args.append("--json")
    return args
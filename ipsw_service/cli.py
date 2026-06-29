from __future__ import annotations

import os
import re
import subprocess
import time
from dataclasses import dataclass
from typing import Optional

_HDIUTIL_PERM_RE = re.compile(r"hdiutil:\s+attach\s+failed.*permission\s+denied", re.IGNORECASE)

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

    def _needs_sudo_retry(self, result: CommandResult) -> bool:
        """Return True if the result contains the SystemOS mount permission error"""
        combined = result.stdout + result.stderr
        return bool(_HDIUTIL_PERM_RE.search(combined))

    def run_with_sudo_fallback(
        self,
        args: list[str],
        timeout: int = 600,
        cwd: Optional[str] = None,
    ) -> CommandResult:
        """Run the command; if hdiutil permission denied is detected, retry with sudo.

        Sudo credential resolution order:
          1. ``IPSW_SUDO_PASSWORD`` environment variable — piped to ``sudo -S``.
          2. Passwordless sudo (``sudo -n``) — works if the user has a
             NOPASSWD entry for ``ipsw`` in sudoers
          3. Falls back to returning the original (non-sudo) result
        """
        result = self.run(args, timeout=timeout, cwd=cwd)
        if not self._needs_sudo_retry(result):
            return result

        # Attempt 1: passwordless sudo (-n flag — no password prompt)
        sudo_password = os.environ.get("IPSW_SUDO_PASSWORD", "")
        cmd_base = [self.executable, *args]

        if not sudo_password:
            sudo_cmd = ["sudo", "-n", *cmd_base]
            started = time.perf_counter()
            try:
                proc = subprocess.run(
                    sudo_cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=cwd or self.cwd,
                )
                duration = time.perf_counter() - started
                stdout = (proc.stdout or "").strip()
                stderr = (proc.stderr or "").strip()
                # If passwordless sudo also hit permission denied, fall through
                combined = stdout + stderr
                if proc.returncode == 0 or not _HDIUTIL_PERM_RE.search(combined):

                    return CommandResult(
                        args=sudo_cmd,
                        command=" ".join(sudo_cmd),
                        stdout=stdout,
                        stderr=stderr,
                        exit_code=proc.returncode,
                        duration_seconds=round(duration, 3),
                        success=proc.returncode == 0,
                    )
            except (FileNotFoundError, subprocess.TimeoutExpired):
                pass
            # Passwordless sudo unavailable, return original result with a note
            annotated = CommandResult(
                args=result.args,
                command=result.command,
                stdout=result.stdout,
                stderr=(
                    result.stderr
                    + "\n[sudo-retry] SystemOS volume requires sudo. "
                    "Set IPSW_SUDO_PASSWORD env var or grant NOPASSWD sudo for ipsw."
                ),
                exit_code=result.exit_code,
                duration_seconds=result.duration_seconds,
                success=result.success,
            )
            return annotated

        # Attempt 2: sudo -S (password via stdin)
        sudo_cmd = ["sudo", "-S", *cmd_base]
        started = time.perf_counter()
        try:
            proc = subprocess.run(
                sudo_cmd,
                input=sudo_password + "\n",
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd or self.cwd,
            )
            duration = time.perf_counter() - started
            stdout = (proc.stdout or "").strip()
            stderr = (proc.stderr or "").strip()
            return CommandResult(
                args=sudo_cmd,
                command="sudo -S " + " ".join(cmd_base),
                stdout=stdout,
                stderr=stderr,
                exit_code=proc.returncode,
                duration_seconds=round(duration, 3),
                success=proc.returncode == 0,
            )
        except FileNotFoundError:
            pass
        except subprocess.TimeoutExpired:
            duration = time.perf_counter() - started
            return CommandResult(
                args=sudo_cmd,
                command="sudo -S " + " ".join(cmd_base),
                stdout="",
                stderr=f"sudo ipsw command timed out after {timeout}s",
                exit_code=124,
                duration_seconds=round(duration, 3),
                success=False,
            )

        # return original
        return result

    def run_shell(self, command: str, timeout: int = 600, cwd: Optional[str] = None) -> CommandResult:
        """Run a shell command string (supports pipes) and return a CommandResult"""
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
    # ensure version and build are properly separated if a concatenated string is passed
    if version and not build and "_" in str(version):
        parts = str(version).split("_", 1)
        version = parts[0]
        build = parts[1]

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
    include_sandbox: bool = False,
    include_strs: bool = True,
    low_memory: bool = False,
    json_output: bool = False,
    clean: bool = False,
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
    if include_sandbox:
        args.append("--sandbox")
    if include_strs:
        args.append("--strs")
    if low_memory:
        args.append("--low-memory")
    if json_output:
        args.append("--json")
    if clean:
        args.append("--clean")
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
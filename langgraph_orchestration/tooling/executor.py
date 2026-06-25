from __future__ import annotations

import importlib
import json
import os
import re
import subprocess
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional

from langgraph_orchestration.tooling.parser import parse_agent_output
from langgraph_orchestration.tooling.tool import ToolRequest, ToolResult
from ipsw_service.cli import (
    IpswCliRunner,
    build_download_args,
    build_extract_args,
    build_diff_args,
    build_dyld_diff_args,
)

if TYPE_CHECKING:
    from langgraph_orchestration.schemas.state import AgentState

class BaseToolExecutor(ABC):
    """Abstract base for host-side tool execution"""

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = os.path.realpath(workspace_root or os.getcwd())

    @abstractmethod
    def execute(self, tool_request: ToolRequest) -> ToolResult:
        ...

    def _normalize_path(self, path: str) -> str:
        if os.path.isabs(path):
            return os.path.realpath(path)
        return os.path.realpath(os.path.join(self.workspace_root, path))

    def _validate_file_access(self, path: str) -> bool:
        try:
            normalized = self._normalize_path(path)
            return os.path.commonpath([normalized, self.workspace_root]) == self.workspace_root
        except (OSError, ValueError):
            return False

class VSCodeToolExecutor(BaseToolExecutor):
    """Tool executor for software dev workflows"""
    def execute(self, tool_request: ToolRequest) -> ToolResult:
        handlers = {
            "read_file": self._read_file,
            "read_many_files": self._read_many_files,
            "search_repository": self._search_repository,
            "get_errors": self._get_errors,
            "create_file": self._create_file,
            "edit_file": self._edit_file,
        }

        tool_name = tool_request.tool_name
        if tool_name not in handlers:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                output="",
                error=f"Unknown tool: {tool_name}",
                source="vscode",
            )

        try:
            result = handlers[tool_name](tool_request)
            result.source = "vscode"
            return result
        except Exception as exc:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                output="",
                error=str(exc),
                source="vscode",
            )

    def _read_file(self, req: ToolRequest) -> ToolResult:
        path = req.arguments.get("path") or req.target
        if not path:
            return ToolResult(tool_name="read_file", success=False, output="", error="No path provided")

        if not self._validate_file_access(path):
            return ToolResult(
                tool_name="read_file",
                success=False,
                output="",
                error=f"Access denied: {path}",
            )

        normalized = self._normalize_path(path)
        try:
            with open(normalized, "r", encoding="utf-8") as handle:
                content = handle.read()
            return ToolResult(
                tool_name="read_file",
                success=True,
                output=content,
                metadata={"path": path, "size_bytes": len(content)},
            )
        except FileNotFoundError:
            return ToolResult(
                tool_name="read_file",
                success=False,
                output="",
                error=f"File not found: {path}",
            )

    def _read_many_files(self, req: ToolRequest) -> ToolResult:
        paths = req.arguments.get("paths", [])
        if not isinstance(paths, list) or not paths:
            return ToolResult(
                tool_name="read_many_files",
                success=False,
                output="",
                error="No paths provided",
            )

        outputs: dict[str, str] = {}
        errors: list[str] = []
        for path in paths:
            if not isinstance(path, str):
                errors.append("Non-string path in request")
                continue
            if not self._validate_file_access(path):
                errors.append(f"Access denied: {path}")
                continue

            normalized = self._normalize_path(path)
            try:
                with open(normalized, "r", encoding="utf-8") as handle:
                    outputs[path] = handle.read()
            except Exception as exc:
                errors.append(f"{path}: {exc}")

        return ToolResult(
            tool_name="read_many_files",
            success=not errors,
            output=json.dumps(outputs, ensure_ascii=True, indent=2),
            error="; ".join(errors) if errors else None,
            metadata={"file_count": len(outputs), "error_count": len(errors)},
        )

    def _search_repository(self, req: ToolRequest) -> ToolResult:
        pattern = req.arguments.get("pattern") or req.target
        if not pattern:
            return ToolResult(
                tool_name="search_repository",
                success=False,
                output="",
                error="No search pattern provided",
            )

        include_glob = req.arguments.get("include_glob", "*")
        max_results = int(req.arguments.get("max_results", 50))
        is_regexp = bool(req.arguments.get("is_regexp", False))

        cmd = ["rg", "--line-number", "--with-filename", "--color", "never"]
        if not is_regexp:
            cmd.append("-F")
        cmd.extend(["-g", include_glob, str(pattern), self.workspace_root])

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if proc.returncode not in (0, 1):
                return ToolResult(
                    tool_name="search_repository",
                    success=False,
                    output="",
                    error=proc.stderr.strip() or "search_repository failed",
                )

            lines = [line for line in proc.stdout.splitlines() if line]
            limited = lines[:max_results]
            return ToolResult(
                tool_name="search_repository",
                success=True,
                output="\n".join(limited),
                metadata={"match_count": len(lines), "limited": len(lines) > max_results},
            )
        except FileNotFoundError:
            grep_cmd = ["grep", "-R", "-n", str(pattern), self.workspace_root]
            proc = subprocess.run(grep_cmd, capture_output=True, text=True, timeout=10)
            if proc.returncode not in (0, 1):
                return ToolResult(
                    tool_name="search_repository",
                    success=False,
                    output="",
                    error=proc.stderr.strip() or "search_repository failed",
                )
            lines = [line for line in proc.stdout.splitlines() if line]
            limited = lines[:max_results]
            return ToolResult(
                tool_name="search_repository",
                success=True,
                output="\n".join(limited),
                metadata={
                    "match_count": len(lines),
                    "limited": len(lines) > max_results,
                    "backend": "grep",
                },
            )

    def _get_errors(self, req: ToolRequest) -> ToolResult:
        path = req.arguments.get("path") or req.target
        if not path:
            return ToolResult(tool_name="get_errors", success=False, output="", error="No path provided")
        if not self._validate_file_access(path):
            return ToolResult(tool_name="get_errors", success=False, output="", error=f"Access denied: {path}")

        normalized = self._normalize_path(path)
        if not normalized.endswith(".py"):
            return ToolResult(
                tool_name="get_errors",
                success=False,
                output="",
                error="get_errors currently supports Python files only",
            )

        try:
            with open(normalized, "r", encoding="utf-8") as handle:
                code = handle.read()
            compile(code, path, "exec")
            return ToolResult(
                tool_name="get_errors",
                success=True,
                output="No syntax errors found",
                metadata={"path": path, "error_count": 0},
            )
        except SyntaxError as exc:
            snippet = (exc.text or "").strip()
            return ToolResult(
                tool_name="get_errors",
                success=False,
                output="",
                error=f"Line {exc.lineno}: {exc.msg}. {snippet}",
                metadata={"path": path, "line": exc.lineno, "error_type": "SyntaxError"},
            )

    def _validate_app_code_path(self, path: str) -> tuple[bool, Optional[str]]:
        if not path:
            return False, "File path cannot be empty"
        
        _, ext = os.path.splitext(path)
        if not ext:
            return False, f"File must have an extension (e.g., .py, .json, .md)"
        
        return True, None

    def _create_file(self, req: ToolRequest) -> ToolResult:
        path = req.arguments.get("path") or req.target
        content = req.arguments.get("content", "")

        if not path:
            return ToolResult(tool_name="create_file", success=False, output="", error="No path provided")
        if not self._validate_file_access(path):
            return ToolResult(tool_name="create_file", success=False, output="", error=f"Access denied: {path}")

        is_valid, validation_error = self._validate_app_code_path(path)
        if not is_valid:
            return ToolResult(
                tool_name="create_file",
                success=False,
                output="",
                error=validation_error,
            )

        normalized = self._normalize_path(path)
        try:
            os.makedirs(os.path.dirname(normalized), exist_ok=True)
            if os.path.exists(normalized):
                return ToolResult(
                    tool_name="create_file",
                    success=False,
                    output="",
                    error=f"File already exists: {path}",
                )
            with open(normalized, "w", encoding="utf-8") as handle:
                handle.write(content)
            return ToolResult(
                tool_name="create_file",
                success=True,
                output=f"Created {path}",
                metadata={"path": path, "size_bytes": len(content)},
            )
        except Exception as exc:
            return ToolResult(
                tool_name="create_file",
                success=False,
                output="",
                error=f"Failed to create file: {exc}",
            )

    def _edit_file(self, req: ToolRequest) -> ToolResult:
        path = req.arguments.get("path") or req.target
        old_string = req.arguments.get("old_string")
        new_string = req.arguments.get("new_string")

        if not path or old_string is None or new_string is None:
            return ToolResult(
                tool_name="edit_file",
                success=False,
                output="",
                error="Missing required arguments: path, old_string, new_string",
            )
        if not self._validate_file_access(path):
            return ToolResult(tool_name="edit_file", success=False, output="", error=f"Access denied: {path}")

        normalized = self._normalize_path(path)
        try:
            with open(normalized, "r", encoding="utf-8") as handle:
                content = handle.read()
            if old_string not in content:
                return ToolResult(
                    tool_name="edit_file",
                    success=False,
                    output="",
                    error="Old string not found in file",
                )
            updated = content.replace(old_string, new_string, 1)
            with open(normalized, "w", encoding="utf-8") as handle:
                handle.write(updated)
            return ToolResult(
                tool_name="edit_file",
                success=True,
                output=f"Edited {path}",
                metadata={"path": path, "old_len": len(content), "new_len": len(updated)},
            )
        except Exception as exc:
            return ToolResult(
                tool_name="edit_file",
                success=False,
                output="",
                error=f"Failed to edit file: {exc}",
            )


_TOOL_ERROR_SENTINELS = (
    "error:",
    "# error",
    "failed to",
    "failed.",
    "error saving",
    "request timed out",
    "not running",
    "connection to decompiler refused",
)


def _looks_like_error(text: Any) -> bool:
    """True when a decompiler tool returned an error string instead of real output.

    Several IDA RPC tools signal failure in-band by returning a human-readable
    error string while the Python call itself 'succeeds'. Without this check those
    errors were surfaced to the model as valid evidence (success=True), inviting
    hallucinated conclusions. This normalizes them back to failures.
    """
    if not isinstance(text, str):
        return False
    lowered = text.strip().lower()
    return any(lowered.startswith(s) or s in lowered[:60] for s in _TOOL_ERROR_SENTINELS)


class IDAToolExecutor(BaseToolExecutor):
    """Tool executor for RE workflows"""

    def __init__(self, workspace_root: Optional[str] = None, ida_instance: Optional[Any] = None):
        super().__init__(workspace_root)
        self.ida_instance = ida_instance

    def execute(self, tool_request: ToolRequest) -> ToolResult:
        handlers = {
            "read_file": self._read_file,
            "read_many_files": self._read_many_files,
            "ipsw_cli": self._ipsw_cli,
            "ipsw_download": self._ipsw_download,
            "ipsw_extract": self._ipsw_extract,
            "ipsw_diff": self._ipsw_diff,
            "decompile_function": self._remote_decompile_function,
            "get_xrefs_to": self._remote_get_xrefs_to,
            "find_address": self._remote_find_address,
            "rename_local_variable": self._remote_rename_local_variable,
            "set_comment": self._remote_set_comment,
            "start_ida_server_for_binary": self._remote_start_ida_server_for_binary,
            "stop_ida_server": self._remote_stop_ida_server,
            "save_ida_database": self._remote_save_ida_database,
            "get_entitlements": self._remote_get_entitlements,
            "resolve_objc_dispatch": self._remote_resolve_objc_dispatch,
            "trace_variable_source": self._remote_trace_variable_source,
        }

        tool_name = tool_request.tool_name
        if tool_name not in handlers:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                output="",
                error=f"Unknown IDA tool: {tool_name}",
                source="ida",
            )

        try:
            result = handlers[tool_name](tool_request)
            result.source = "ipsw" if tool_name.startswith("ipsw") else "ida"
            return result
        except Exception as exc:
            return ToolResult(
                tool_name=tool_name,
                success=False,
                output="",
                error=str(exc),
                source="ipsw" if tool_name.startswith("ipsw") else "ida",
            )

    def _read_file(self, req: ToolRequest) -> ToolResult:
        return VSCodeToolExecutor(self.workspace_root)._read_file(req)

    def _read_many_files(self, req: ToolRequest) -> ToolResult:
        return VSCodeToolExecutor(self.workspace_root)._read_many_files(req)

    def _remote_decompile_function(self, req: ToolRequest) -> ToolResult:
        from langgraph_orchestration.tooling.decompiler_tools import decompile_function
        address = req.arguments.get("address")
        if address is None:
            return ToolResult(tool_name="decompile_function", success=False, output="", error="Missing address argument")
        
        try:
            addr_int = self._parse_address(address)
        except (ValueError, TypeError):
            return ToolResult(tool_name="decompile_function", success=False, output="", error="Invalid address format")
        output = decompile_function.invoke({"address": addr_int})
        if isinstance(output, str) and output.startswith("# ERROR"):
            return ToolResult(tool_name="decompile_function", success=False, output="", error=output)
        return ToolResult(tool_name="decompile_function", success=True, output=str(output))
    
    def _remote_get_xrefs_to(self, req: ToolRequest) -> ToolResult:
        from langgraph_orchestration.tooling.decompiler_tools import get_xrefs_to
        import json
        address = req.arguments.get("address")
        if address is None:
            return ToolResult(tool_name="get_xrefs_to", success=False, output="", error="Missing address argument")
        
        try:
            addr_int = self._parse_address(address)
        except (ValueError, TypeError):
            return ToolResult(tool_name="get_xrefs_to", success=False, output="", error="Invalid address format")
        output = get_xrefs_to.invoke({"address": addr_int})
        if isinstance(output, list) and len(output) > 0 and "error" in output[0]:
            return ToolResult(tool_name="get_xrefs_to", success=False, output="", error=output[0]["error"])
        
        output_str = json.dumps(output, indent=2) if not isinstance(output, str) else output
        return ToolResult(tool_name="get_xrefs_to", success=True, output=output_str)
        
    def _remote_find_address(self, req: ToolRequest) -> ToolResult:
        from langgraph_orchestration.tooling.decompiler_tools import find_address
        import json
        query = req.arguments.get("query") or req.target
        if not query:
            return ToolResult(tool_name="find_address", success=False, output="", error="Missing query argument")
            
        output = find_address.invoke({"query": query})
        
        if isinstance(output, str) and output.startswith("error:"):
            return ToolResult(tool_name="find_address", success=False, output="", error=output)
            
        if isinstance(output, dict):
            # tell the agent exactly what it found so it can use the correct follow-up tool
            result_str = json.dumps(output, indent=2)
            if output["type"] in ("symbol", "symbol_fuzzy"):
                result_str += "\n\nNOTE: This is a CODE symbol. You MUST use `decompile_function` on this address."
            elif output["type"] in ("string_data", "data_symbol", "data_symbol_fuzzy"):
                result_str += "\n\nNOTE: This is a DATA or selector address. You MUST use `get_xrefs_to` on these addresses to find the code referencing it."
            return ToolResult(tool_name="find_address", success=True, output=result_str)
            
        return ToolResult(tool_name="find_address", success=False, output="", error=f"Unexpected response: {output}")
    
    def _remote_rename_local_variable(self, req: ToolRequest) -> ToolResult:
        from langgraph_orchestration.tooling.decompiler_tools import rename_local_variable
        func_address = req.arguments.get("func_address")
        old_name = req.arguments.get("old_name")
        new_name = req.arguments.get("new_name")
        
        if func_address is None or not old_name or not new_name:
            return ToolResult(tool_name="rename_local_variable", success=False, output="", error="Missing arguments")
            
        try:
            addr_int = self._parse_address(func_address)
        except (ValueError, TypeError):
            return ToolResult(tool_name="rename_local_variable", success=False, output="", error="Invalid func_address format")
        success = rename_local_variable.invoke({"func_address": addr_int, "old_name": old_name, "new_name": new_name})
        if success:
            return ToolResult(tool_name="rename_local_variable", success=True, output="Variable renamed successfully.")
        return ToolResult(tool_name="rename_local_variable", success=False, output="", error="Failed to rename variable.")
    
    def _remote_set_comment(self, req: ToolRequest) -> ToolResult:
        from langgraph_orchestration.tooling.decompiler_tools import set_comment
        address = req.arguments.get("address")
        comment = req.arguments.get("comment")
        
        if address is None or not comment:
            return ToolResult(tool_name="set_comment", success=False, output="", error="Missing arguments")
            
        try:
            addr_int = self._parse_address(address)
        except (ValueError, TypeError):
            return ToolResult(tool_name="set_comment", success=False, output="", error="Invalid address format")
        success = set_comment.invoke({"address": addr_int, "comment": comment})
        if success:
            return ToolResult(tool_name="set_comment", success=True, output="Comment set successfully.")
        return ToolResult(tool_name="set_comment", success=False, output="", error="Failed to set comment.")
    
    def _remote_start_ida_server_for_binary(self, req: ToolRequest) -> ToolResult:
        from langgraph_orchestration.tooling.decompiler_tools import start_ida_server_for_binary
        binary_path = req.arguments.get("binary_path")
        if not binary_path:
            return ToolResult(tool_name="start_ida_server_for_binary", success=False, output="", error="Missing binary_path argument")
        
        output = start_ida_server_for_binary.invoke({"binary_path": binary_path})
        if isinstance(output, str) and output.startswith("# ERROR"):
            return ToolResult(tool_name="start_ida_server_for_binary", success=False, output="", error=output)
        return ToolResult(tool_name="start_ida_server_for_binary", success=True, output=output)
    
    def _remote_stop_ida_server(self, req: ToolRequest) -> ToolResult:
        from langgraph_orchestration.tooling.decompiler_tools import stop_ida_server
        output = stop_ida_server.invoke({})
        return ToolResult(tool_name="stop_ida_server", success=True, output=output)

    def _remote_save_ida_database(self, req: ToolRequest) -> ToolResult:
        from langgraph_orchestration.tooling.decompiler_tools import save_ida_database
        output = str(save_ida_database.invoke({}))
        if _looks_like_error(output) or "failed to save" in output.lower():
            return ToolResult(tool_name="save_ida_database", success=False, output="", error=output)
        return ToolResult(tool_name="save_ida_database", success=True, output=output)

    def _remote_get_entitlements(self, req: ToolRequest) -> ToolResult:
        from langgraph_orchestration.tooling.decompiler_tools import get_entitlements
        binary_path = req.arguments.get("binary_path")
        if not binary_path:
            return ToolResult(tool_name="get_entitlements", success=False, output="", error="Missing binary_path argument")
        output = str(get_entitlements.invoke({"binary_path": binary_path}))
        if _looks_like_error(output):
            return ToolResult(tool_name="get_entitlements", success=False, output="", error=output)
        return ToolResult(tool_name="get_entitlements", success=True, output=output)

    def _remote_resolve_objc_dispatch(self, req: ToolRequest) -> ToolResult:
        from langgraph_orchestration.tooling.decompiler_tools import resolve_objc_dispatch
        func_ea = req.arguments.get("func_ea")
        call_ea = req.arguments.get("call_ea")
        if func_ea is None or call_ea is None:
            return ToolResult(tool_name="resolve_objc_dispatch", success=False, output="", error="Missing func_ea or call_ea")
        output = str(resolve_objc_dispatch.invoke({"func_ea": int(func_ea), "call_ea": int(call_ea)}))
        if _looks_like_error(output):
            return ToolResult(tool_name="resolve_objc_dispatch", success=False, output="", error=output)
        return ToolResult(tool_name="resolve_objc_dispatch", success=True, output=output)

    def _remote_trace_variable_source(self, req: ToolRequest) -> ToolResult:
        from langgraph_orchestration.tooling.decompiler_tools import trace_variable_source
        func_ea = req.arguments.get("func_ea")
        var_name = req.arguments.get("var_name")
        if func_ea is None or not var_name:
            return ToolResult(tool_name="trace_variable_source", success=False, output="", error="Missing func_ea or var_name")
        output = str(trace_variable_source.invoke({"func_ea": int(func_ea), "var_name": var_name}))
        if _looks_like_error(output):
            return ToolResult(tool_name="trace_variable_source", success=False, output="", error=output)
        return ToolResult(tool_name="trace_variable_source", success=True, output=output)

    def _parse_address(self, address: Any) -> int:
        if isinstance(address, int):
            return address
        val = str(address).strip()
        if val.lower().startswith("0x"):
            return int(val, 16)
        return int(val)

    def _run_ipsw(self, args: list[str], timeout: int = 120) -> ToolResult:
        if not args:
            return ToolResult(tool_name="ipsw_cli", success=False, output="", error="No ipsw arguments provided")
        runner = IpswCliRunner(cwd=self.workspace_root)
        result = runner.run(args, timeout=timeout)
        output = result.stdout if result.stdout else result.stderr
        return ToolResult(
            tool_name="ipsw_cli",
            success=result.success,
            output=output,
            error=None if result.success else (result.stderr or result.stdout or f"ipsw exited with code {result.exit_code}"),
            metadata={
                "command": result.command,
                "exit_code": result.exit_code,
                "duration_seconds": result.duration_seconds,
            },
        )

    def _ipsw_cli(self, req: ToolRequest) -> ToolResult:
        raw_args = req.arguments.get("args", [])
        timeout = int(req.arguments.get("timeout", 120))
        if not isinstance(raw_args, list) or not all(isinstance(item, str) for item in raw_args):
            return ToolResult(
                tool_name="ipsw_cli",
                success=False,
                output="",
                error="ipsw_cli requires arguments.args as a list of strings",
            )
        return self._run_ipsw(raw_args, timeout=timeout)

    def _ipsw_download(self, req: ToolRequest) -> ToolResult:
        device = req.arguments.get("device")
        version = req.arguments.get("version")
        build = req.arguments.get("build")
        latest = bool(req.arguments.get("latest", False))
        output_dir = req.arguments.get("output_dir")
        timeout = int(req.arguments.get("timeout", 600))
        include_kernel = bool(req.arguments.get("kernel", False))
        include_dyld = bool(req.arguments.get("dyld", False))

        if not device:
            return ToolResult(
                tool_name="ipsw_download",
                success=False,
                output="",
                error="ipsw_download requires a device identifier",
            )
        if not (version or build or latest):
            return ToolResult(
                tool_name="ipsw_download",
                success=False,
                output="",
                error="ipsw_download requires version, build, or latest flag",
            )

        args = build_download_args(
            device=str(device),
            version=str(version) if version else None,
            build=str(build) if build else None,
            output_dir=str(output_dir) if output_dir else None,
            resume_all=True,
            latest=latest,
            include_kernel=include_kernel,
            include_dyld=include_dyld,
        )

        base = self._run_ipsw(args, timeout=timeout)
        return ToolResult(
            tool_name="ipsw_download",
            success=base.success,
            output=base.output,
            error=base.error,
            metadata=base.metadata,
        )

    def _ipsw_extract(self, req: ToolRequest) -> ToolResult:
        ipsw_path = req.arguments.get("ipsw") or req.arguments.get("ipsw_path") or req.target
        artifact = req.arguments.get("artifact", "dyld")
        output_dir = req.arguments.get("output_dir")
        dyld_arch = req.arguments.get("dyld_arch", "arm64e")
        extra_args = req.arguments.get("extra_args", [])
        pattern = req.arguments.get("pattern")
        timeout = int(req.arguments.get("timeout", 300))

        if not ipsw_path:
            return ToolResult(
                tool_name="ipsw_extract",
                success=False,
                output="",
                error="ipsw_extract requires ipsw or ipsw_path",
            )

        dyld = artifact in ("dyld", "dsc")
        kernel = artifact == "kernel"
        normalized_extra: list[str] = []
        if isinstance(extra_args, list):
            normalized_extra = [str(item) for item in extra_args]
        if artifact == "files":
            normalized_extra = ["--files"]
            if pattern:
                normalized_extra.extend(["--pattern", str(pattern)])
        elif not dyld and not kernel and not normalized_extra and artifact:
            flag = str(artifact)
            normalized_extra = [flag if flag.startswith("--") else f"--{flag}"]
        if not output_dir:
            output_dir = os.path.join(self.workspace_root, ".ipsw_extracted")

        args = build_extract_args(
            ipsw_path=str(ipsw_path),
            output_dir=str(output_dir),
            dyld=dyld,
            kernel=kernel,
            dyld_arch=str(dyld_arch),
            extra_args=normalized_extra,
        )
        base = self._run_ipsw(args, timeout=timeout)
        return ToolResult(
            tool_name="ipsw_extract",
            success=base.success,
            output=base.output,
            error=base.error,
            metadata=base.metadata,
        )

    def _ipsw_diff(self, req: ToolRequest) -> ToolResult:
        old_dsc = req.arguments.get("old_dsc")
        new_dsc = req.arguments.get("new_dsc")
        old_ipsw = req.arguments.get("old_ipsw") or req.arguments.get("old_ipsw_path") or req.arguments.get("old")
        new_ipsw = req.arguments.get("new_ipsw") or req.arguments.get("new_ipsw_path") or req.arguments.get("new")
        json_output = bool(req.arguments.get("json", False))
        timeout = int(req.arguments.get("timeout", 180))

        # Auto-resolve: if the model omitted explicit paths (sent only a target label),
        # scan .ipsw_downloads/ for two IPSWs and pick old=first, new=last by mtime.
        if not old_dsc and not new_dsc and not old_ipsw and not new_ipsw:
            import glob as _glob
            downloads_dir = os.path.join(self.workspace_root, ".ipsw_downloads")
            candidates = sorted(
                _glob.glob(os.path.join(downloads_dir, "*.ipsw")),
                key=os.path.getmtime,
            )
            if len(candidates) >= 2:
                old_ipsw, new_ipsw = candidates[0], candidates[-1]
            # also accept pre-extracted DSC pairs from .ipsw_extracted/
            if not old_ipsw:
                dsc_candidates = sorted(
                    _glob.glob(os.path.join(self.workspace_root, ".ipsw_extracted", "**", "dyld_shared_cache_arm64e"), recursive=True),
                    key=os.path.getmtime,
                )
                if len(dsc_candidates) >= 2:
                    old_dsc, new_dsc = dsc_candidates[0], dsc_candidates[-1]

        if old_dsc and new_dsc:
            args = build_dyld_diff_args(str(old_dsc), str(new_dsc), json_output=json_output)
        elif old_ipsw and new_ipsw:
            args = build_diff_args(
                old_ipsw=str(old_ipsw),
                new_ipsw=str(new_ipsw),
                output_dir=req.arguments.get("output_dir"),
                markdown=bool(req.arguments.get("markdown", True)),
                include_fw=bool(req.arguments.get("fw", False)),
                include_launchd=bool(req.arguments.get("launchd", False)),
                include_entitlements=bool(req.arguments.get("ent", False)),
                include_strs=bool(req.arguments.get("strs", True)),
                low_memory=bool(req.arguments.get("low_memory", False)),
                json_output=json_output,
            )
        else:
            return ToolResult(
                tool_name="ipsw_diff",
                success=False,
                output="",
                error=(
                    "ipsw_diff requires old/new IPSW paths or old_dsc/new_dsc arguments. "
                    f"No IPSWs found in {os.path.join(self.workspace_root, '.ipsw_downloads')}."
                ),
            )

        base = self._run_ipsw(args, timeout=timeout)
        return ToolResult(
            tool_name="ipsw_diff",
            success=base.success,
            output=base.output,
            error=base.error,
            metadata=base.metadata,
        )


def get_tool_executor(
    domain: str,
    workspace_root: Optional[str] = None,
    ida_instance: Optional[Any] = None,
) -> BaseToolExecutor:
    if domain == "reverse_engineering":
        return IDAToolExecutor(workspace_root=workspace_root, ida_instance=ida_instance)
    return VSCodeToolExecutor(workspace_root=workspace_root)


def tool_executor_node(state: AgentState) -> AgentState:
    if state.tool_iteration >= state.max_tool_iterations:
        return state

    last_agent = state.agent_chain[-1] if state.agent_chain else None
    if not last_agent:
        return state

    last_output = state.intermediate_outputs.get(last_agent)
    if not last_output:
        return state

    parsed = parse_agent_output(last_output)

    if parsed.has_errors() and not parsed.tool_calls:
        lines = ["Tool call processing encountered errors. Please correct and retry:\n"]
        if parsed.parse_errors:
            lines.append("Parse Errors:")
            for err in parsed.parse_errors:
                lines.append(f"  - {err.error_type}: {err.message}")
                if err.context:
                    lines.append(f"    Context: {err.context}")
            lines.append("")
        lines.append("Format reminder:")
        lines.append(
            """
            Emit tool calls like this:
            <tool_call>
            {
            "tool_name": "read_file",
            "arguments": {
                "path": "main.py"
            },
            "target": "main.py",
            "reason": "Understand entry point"
            }
            </tool_call>

            Continue with your analysis after the tool call.
            """.strip()
        )
        error_feedback = "\n".join(lines)

        state.analysis_notes.append(f"Tool parsing error: {parsed.error_summary()}")
        agent_retry_prompt = (
            f"Your previous response had tool call formatting issues:\n"
            f"{error_feedback}\n\n"
            f"Please retry with corrected tool call format."
        )
        state.intermediate_outputs[f"{last_agent}__error_feedback"] = agent_retry_prompt
        return state

    for tool_call in parsed.tool_calls:
        tool_request = ToolRequest(
            type="tool_request",
            tool_name=tool_call.tool_name,
            arguments=tool_call.arguments,
            target=str(tool_call.target) if tool_call.target is not None else None,
            reason=tool_call.reason or "",
            needs_confirmation=tool_call.needs_confirmation,
            expected_outcome=tool_call.expected_outcome,
        )

        if not tool_request.domain:
            tool_request.domain = state.selected_domain or "software_dev"

        allowed_tools = state.tool_policy.allowed_tools or []
        if allowed_tools and tool_request.tool_name not in allowed_tools:
            result = ToolResult(
                tool_name=tool_request.tool_name,
                success=False,
                error=(
                    f"Tool '{tool_request.tool_name}' not allowed. "
                    f"Allowed tools: {', '.join(allowed_tools)}"
                ),
                output="",
                source="policy_check",
            )
        elif state.requires_tool_confirmation and tool_request.needs_confirmation:
            result = ToolResult(
                tool_name=tool_request.tool_name,
                success=False,
                error="Tool requires confirmation; no approval mechanism configured",
                output="",
                source="policy_check",
            )
        else:
            try:
                executor = get_tool_executor(
                    domain=tool_request.domain or "software_dev",
                    workspace_root=state.workspace_root,
                )
                result = executor.execute(tool_request)
            except Exception as exc:
                result = ToolResult(
                    tool_name=tool_request.tool_name,
                    success=False,
                    error=f"Execution failed: {str(exc)}",
                    output="",
                    source="executor",
                )

        tool_request.status = "executed" if result.success else "failed"
        state.register_tool_request(tool_request)
        state.register_tool_result(result)

        status = "OK" if result.success else "ERR"
        observation = (
            f"{status} {tool_request.tool_name}: {result.output[:500]}"
            if result.success
            else f"{status} {tool_request.tool_name} failed: {result.error}"
        )
        state.analysis_notes.append(observation)

    return state

def should_continue_tool_loop(state: AgentState) -> bool:
    if state.tool_iteration >= state.max_tool_iterations:
        return False

    last_agent = state.agent_chain[-1] if state.agent_chain else None
    if not last_agent:
        return False

    last_output = state.intermediate_outputs.get(last_agent)
    if not last_output:
        return False

    parsed = parse_agent_output(last_output)
    return parsed.has_tool_calls()
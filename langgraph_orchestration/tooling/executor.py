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


class IDAToolExecutor(BaseToolExecutor):
    """Tool executor for RE workflows"""

    def __init__(self, workspace_root: Optional[str] = None, ida_instance: Optional[Any] = None):
        super().__init__(workspace_root)
        self.ida_instance = ida_instance
        self._ida_modules = self._load_ida_modules(ida_instance)
        self._ida_available = bool(self._ida_modules.get("idc") and self._ida_modules.get("ida_funcs"))

    def execute(self, tool_request: ToolRequest) -> ToolResult:
        handlers = {
            "read_file": self._read_file,
            "read_many_files": self._read_many_files,
            "read_decompilation": self._read_decompilation,
            "read_disassembly": self._read_disassembly,
            "xrefs_to": self._xrefs_to,
            "xrefs_from": self._xrefs_from,
            "lookup_funcs": self._lookup_funcs,
            "basic_blocks": self._basic_blocks,
            "ipsw_cli": self._ipsw_cli,
            "ipsw_download": self._ipsw_download,
            "ipsw_extract": self._ipsw_extract,
            "ipsw_diff": self._ipsw_diff,
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

    def _load_ida_modules(self, ida_instance: Optional[Any]) -> dict[str, Any]:
        modules: dict[str, Any] = {
            "idaapi": ida_instance,
            "idc": None,
            "idautils": None,
            "ida_funcs": None,
            "ida_hexrays": None,
            "ida_gdl": None,
            "ida_lines": None,
        }
        for name in ["idaapi", "idc", "idautils", "ida_funcs", "ida_hexrays", "ida_gdl", "ida_lines"]:
            if modules.get(name) is not None:
                continue
            try:
                modules[name] = importlib.import_module(name)
            except Exception:
                modules[name] = None
        return modules

    def _read_file(self, req: ToolRequest) -> ToolResult:
        return VSCodeToolExecutor(self.workspace_root)._read_file(req)

    def _read_many_files(self, req: ToolRequest) -> ToolResult:
        return VSCodeToolExecutor(self.workspace_root)._read_many_files(req)

    def _offline_cache_path(self, prefix: str, target: str) -> str:
        safe_target = re.sub(r"[^A-Za-z0-9_.-]", "_", target)
        return os.path.join(self.workspace_root, ".ida_cache", f"{prefix}_{safe_target}.txt")

    def _read_offline_cache(self, prefix: str, target: str) -> Optional[str]:
        path = self._offline_cache_path(prefix, target)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()

    def _resolve_ea(self, target: Any) -> Optional[int]:
        if isinstance(target, int):
            return target
        if target is None:
            return None

        idc = self._ida_modules.get("idc")
        idaapi = self._ida_modules.get("idaapi")
        if idc is None:
            return None

        value = str(target).strip()
        if value.lower().startswith("0x"):
            try:
                return int(value, 16)
            except ValueError:
                return None

        try:
            numeric = int(value)
            return numeric
        except ValueError:
            pass

        ea = idc.get_name_ea_simple(value)
        badaddr = getattr(idaapi, "BADADDR", 0xFFFFFFFFFFFFFFFF) if idaapi is not None else 0xFFFFFFFFFFFFFFFF
        if ea == badaddr:
            return None
        return int(ea)

    def _require_live_ida(self, tool_name: str) -> Optional[ToolResult]:
        if self._ida_available:
            return None
        return ToolResult(
            tool_name=tool_name,
            success=False,
            output="",
            error=f"{tool_name} requires a live IDA Pro session",
        )

    def _read_decompilation(self, req: ToolRequest) -> ToolResult:
        func_name = req.arguments.get("function") or req.target
        if not func_name:
            return ToolResult(tool_name="read_decompilation", success=False, output="", error="No function provided")

        offline = self._read_offline_cache("decompile", str(func_name))
        if offline:
            return ToolResult(
                tool_name="read_decompilation",
                success=True,
                output=offline,
                metadata={"function": func_name, "source": "cache"},
            )

        not_live = self._require_live_ida("read_decompilation")
        if not_live:
            return not_live

        ida_hexrays = self._ida_modules.get("ida_hexrays")
        ida_lines = self._ida_modules.get("ida_lines")
        if ida_hexrays is None:
            return ToolResult(
                tool_name="read_decompilation",
                success=False,
                output="",
                error="Hex-Rays decompiler is unavailable in this IDA environment",
            )

        ea = self._resolve_ea(func_name)
        if ea is None:
            return ToolResult(
                tool_name="read_decompilation",
                success=False,
                output="",
                error=f"Unable to resolve function: {func_name}",
            )

        cfunc = ida_hexrays.decompile(ea)
        if cfunc is None:
            return ToolResult(
                tool_name="read_decompilation",
                success=False,
                output="",
                error=f"Unable to decompile function at {hex(ea)}",
            )

        lines = cfunc.get_pseudocode() or []
        cleaned: list[str] = []
        for line in lines:
            text = getattr(line, "line", str(line))
            if ida_lines is not None:
                text = ida_lines.tag_remove(text)
            cleaned.append(text)

        return ToolResult(
            tool_name="read_decompilation",
            success=True,
            output="\n".join(cleaned).strip() or str(cfunc),
            metadata={"function": str(func_name), "ea": hex(ea)},
        )

    def _read_disassembly(self, req: ToolRequest) -> ToolResult:
        target = req.arguments.get("address") or req.arguments.get("function") or req.target
        if not target:
            return ToolResult(tool_name="read_disassembly", success=False, output="", error="No target provided")

        offline = self._read_offline_cache("disasm", str(target))
        if offline:
            return ToolResult(
                tool_name="read_disassembly",
                success=True,
                output=offline,
                metadata={"target": target, "source": "cache"},
            )

        not_live = self._require_live_ida("read_disassembly")
        if not_live:
            return not_live

        idc = self._ida_modules["idc"]
        ida_funcs = self._ida_modules["ida_funcs"]
        idaapi = self._ida_modules.get("idaapi")

        ea = self._resolve_ea(target)
        if ea is None:
            return ToolResult(
                tool_name="read_disassembly",
                success=False,
                output="",
                error=f"Unable to resolve address/function: {target}",
            )

        max_instructions = int(req.arguments.get("max_instructions", 200))
        func = ida_funcs.get_func(ea)
        end_ea = func.end_ea if func else None
        badaddr = getattr(idaapi, "BADADDR", 0xFFFFFFFFFFFFFFFF) if idaapi is not None else 0xFFFFFFFFFFFFFFFF

        lines: list[str] = []
        current = ea
        for _ in range(max_instructions):
            if end_ea is not None and current >= end_ea:
                break
            asm = idc.generate_disasm_line(current, 0) or ""
            lines.append(f"{current:#x}: {asm}")
            nxt = idc.next_head(current, end_ea if end_ea is not None else badaddr)
            if nxt in (None, badaddr) or nxt <= current:
                break
            current = nxt

        return ToolResult(
            tool_name="read_disassembly",
            success=True,
            output="\n".join(lines),
            metadata={"target": str(target), "instruction_count": len(lines)},
        )

    def _xrefs_to(self, req: ToolRequest) -> ToolResult:
        target = req.arguments.get("address") or req.target
        if not target:
            return ToolResult(tool_name="xrefs_to", success=False, output="", error="No target provided")

        not_live = self._require_live_ida("xrefs_to")
        if not_live:
            return not_live

        idautils = self._ida_modules["idautils"]
        ea = self._resolve_ea(target)
        if ea is None:
            return ToolResult(tool_name="xrefs_to", success=False, output="", error=f"Unable to resolve: {target}")

        refs = list(idautils.XrefsTo(ea, 0))
        output = "\n".join(f"{xref.frm:#x} -> {xref.to:#x} (type={xref.type})" for xref in refs)
        return ToolResult(
            tool_name="xrefs_to",
            success=True,
            output=output,
            metadata={"target": str(target), "count": len(refs)},
        )

    def _xrefs_from(self, req: ToolRequest) -> ToolResult:
        target = req.arguments.get("address") or req.target
        if not target:
            return ToolResult(tool_name="xrefs_from", success=False, output="", error="No target provided")

        not_live = self._require_live_ida("xrefs_from")
        if not_live:
            return not_live

        idautils = self._ida_modules["idautils"]
        ea = self._resolve_ea(target)
        if ea is None:
            return ToolResult(tool_name="xrefs_from", success=False, output="", error=f"Unable to resolve: {target}")

        refs = list(idautils.XrefsFrom(ea, 0))
        output = "\n".join(f"{xref.frm:#x} -> {xref.to:#x} (type={xref.type})" for xref in refs)
        return ToolResult(
            tool_name="xrefs_from",
            success=True,
            output=output,
            metadata={"target": str(target), "count": len(refs)},
        )

    def _lookup_funcs(self, req: ToolRequest) -> ToolResult:
        pattern = req.arguments.get("pattern") or req.target
        if not pattern:
            return ToolResult(tool_name="lookup_funcs", success=False, output="", error="No pattern provided")

        not_live = self._require_live_ida("lookup_funcs")
        if not_live:
            return not_live

        idautils = self._ida_modules["idautils"]
        idc = self._ida_modules["idc"]
        max_results = int(req.arguments.get("max_results", 200))

        needle = str(pattern).lower()
        matches: list[str] = []
        for ea in idautils.Functions():
            name = idc.get_func_name(ea) or ""
            if needle in name.lower():
                matches.append(f"{ea:#x}: {name}")
                if len(matches) >= max_results:
                    break

        return ToolResult(
            tool_name="lookup_funcs",
            success=True,
            output="\n".join(matches),
            metadata={"pattern": str(pattern), "count": len(matches), "limited": len(matches) >= max_results},
        )

    def _basic_blocks(self, req: ToolRequest) -> ToolResult:
        function_target = req.arguments.get("function") or req.target
        if not function_target:
            return ToolResult(tool_name="basic_blocks", success=False, output="", error="No function provided")

        not_live = self._require_live_ida("basic_blocks")
        if not_live:
            return not_live

        ida_funcs = self._ida_modules["ida_funcs"]
        ida_gdl = self._ida_modules.get("ida_gdl")

        if ida_gdl is None:
            return ToolResult(
                tool_name="basic_blocks",
                success=False,
                output="",
                error="ida_gdl is unavailable in this IDA environment",
            )

        ea = self._resolve_ea(function_target)
        if ea is None:
            return ToolResult(
                tool_name="basic_blocks",
                success=False,
                output="",
                error=f"Unable to resolve function: {function_target}",
            )

        func = ida_funcs.get_func(ea)
        if func is None:
            return ToolResult(
                tool_name="basic_blocks",
                success=False,
                output="",
                error=f"No function found at {hex(ea)}",
            )

        flow = ida_gdl.FlowChart(func)
        lines: list[str] = []
        count = 0
        for block in flow:
            succs = [f"{succ.start_ea:#x}" for succ in block.succs()]
            lines.append(
                f"block {block.id}: {block.start_ea:#x}-{block.end_ea:#x}; succs=[{', '.join(succs)}]"
            )
            count += 1

        return ToolResult(
            tool_name="basic_blocks",
            success=True,
            output="\n".join(lines),
            metadata={"function": str(function_target), "ea": hex(ea), "block_count": count},
        )

    def _run_ipsw(self, args: list[str], timeout: int = 120) -> ToolResult:
        if not args:
            return ToolResult(tool_name="ipsw_cli", success=False, output="", error="No ipsw arguments provided")

        cmd = ["ipsw", *args]
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.workspace_root,
            )
        except FileNotFoundError:
            return ToolResult(
                tool_name="ipsw_cli",
                success=False,
                output="",
                error="ipsw CLI not found in PATH",
            )
        except subprocess.TimeoutExpired:
            return ToolResult(
                tool_name="ipsw_cli",
                success=False,
                output="",
                error=f"ipsw command timed out after {timeout}s",
            )

        stdout = (proc.stdout or "").strip()
        stderr = (proc.stderr or "").strip()
        output = stdout if stdout else stderr

        return ToolResult(
            tool_name="ipsw_cli",
            success=proc.returncode == 0,
            output=output,
            error=None if proc.returncode == 0 else (stderr or stdout or f"ipsw exited with code {proc.returncode}"),
            metadata={"command": " ".join(cmd), "exit_code": proc.returncode},
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
        output_dir = req.arguments.get("output_dir")
        timeout = int(req.arguments.get("timeout", 600))

        if not device or not version:
            return ToolResult(
                tool_name="ipsw_download",
                success=False,
                output="",
                error="ipsw_download requires device and version arguments",
            )

        args = ["download", "--device", str(device), "--version", str(version)]
        if output_dir:
            args.extend(["--output", str(output_dir)])

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
        timeout = int(req.arguments.get("timeout", 300))

        if not ipsw_path:
            return ToolResult(
                tool_name="ipsw_extract",
                success=False,
                output="",
                error="ipsw_extract requires ipsw or ipsw_path",
            )

        args = ["extract", "--ipsw", str(ipsw_path), str(artifact)]
        base = self._run_ipsw(args, timeout=timeout)
        return ToolResult(
            tool_name="ipsw_extract",
            success=base.success,
            output=base.output,
            error=base.error,
            metadata=base.metadata,
        )

    def _ipsw_diff(self, req: ToolRequest) -> ToolResult:
        old_dsc = req.arguments.get("old_dsc") or req.arguments.get("old")
        new_dsc = req.arguments.get("new_dsc") or req.arguments.get("new")
        json_output = bool(req.arguments.get("json", True))
        timeout = int(req.arguments.get("timeout", 180))

        if not old_dsc or not new_dsc:
            return ToolResult(
                tool_name="ipsw_diff",
                success=False,
                output="",
                error="ipsw_diff requires old_dsc and new_dsc arguments",
            )

        args = ["dyld", "--dsc-path", str(old_dsc), "--diff", str(new_dsc)]
        if json_output:
            args.append("--json")

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
            target=tool_call.target,
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

    if parsed.tool_calls:
        state.tool_iteration -= len(parsed.tool_calls)

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
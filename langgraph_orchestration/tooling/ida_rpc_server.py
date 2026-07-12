"""Runs inside a headless IDA Pro and answers decompiler requests from the rest
of the app.

decompiler_tools.py is the client: it calls the exposed_* methods here over rpyc
(decompilation, symbol/ObjC lookup, xrefs). IDA's API is not thread-safe, so every
call is queued onto IDA's main thread. This module also runs the annotation floor
(_auto_annotate_core + semantic variable renaming) — a deterministic pass that
renames opaque locals and adds comments before the RE graph re-decompiles a
function for the report."""

import os
import re
import rpyc
from rpyc.utils.server import ThreadedServer
import ida_hexrays
import ida_funcs
import ida_lines
import idc
import idaapi
import threading
import queue

if not ida_hexrays.init_hexrays_plugin():
    ida_hexrays.load_plugin()
    if not ida_hexrays.init_hexrays_plugin():
        print("Error: Hex-Rays decompiler is not available. The decompiler service cannot start.")

_work_queue: queue.Queue = queue.Queue()

def _run_on_main_thread(func, *args, timeout=120):
    result_event = threading.Event()
    cancel_event = threading.Event()
    result_container = {"value": None, "error": None}

    def task():
        if cancel_event.is_set():
            return  
        try:
            result_container["value"] = func(*args)
        except Exception as e:
            result_container["error"] = e
        finally:
            result_event.set()

    _work_queue.put(task)

    if not result_event.wait(timeout=timeout):
        cancel_event.set()  
        raise TimeoutError(f"Main thread execution timed out after {timeout}s")

    if result_container["error"] is not None:
        raise result_container["error"]
    return result_container["value"]


# ida default variable names that deterministic annotation floor rewrites
_DEFAULT_LVAR_RE = re.compile(r"^(?:v\d+|a\d+|x\d+|var_[0-9A-Fa-f]+|arg_[0-9A-Fa-f]+)$")
# also treat this floor's own past output (e.g. void_v5, n_a2, uiview_v6) as still
# re-nameable, so a semantic upgrade applies even on a .i64 the floor already touched
_RENAMEABLE_LVAR_RE = re.compile(
    r"^(?:[a-z][a-z0-9]{0,11}_)?(?:v\d+|a\d+|x\d+|var_[0-9A-Fa-f]+|arg_[0-9A-Fa-f]+)$"
)

def _type_prefix(type_str: str) -> str:
    """Derive a type-based prefix for deterministic variable renaming"""
    t = (type_str or "").lower()
    if "char *" in t or "char*" in t:
        return "str"
    if "cfstring" in t:
        return "cfstr"
    if "nsstring" in t:
        return "nsstr"
    if "bool" in t:
        return "flag"
    if "float" in t or "double" in t:
        return "flt"
    if "*" in t:
        token = re.sub(r"[^a-z0-9]", "", t.split("*")[0])
        return (token[:12] or "ptr")
    if any(k in t for k in ("int", "long", "short", "byte", "word", "dword", "qword", "unsigned", "signed")):
        return "n"
    token = re.sub(r"[^a-z0-9]", "", t)
    return token[:12] or "var"

def _pseudocode_lines(cfunc) -> list:
    """Return the tag-stripped pseudocode lines for a decompiled function"""
    return [ida_lines.tag_remove(i.line) for i in cfunc.get_pseudocode()]


def _semantic_name_from_assignment(rhs: str) -> str:
    """Derive a useful variable name from the right-hand side.

    Prefer the ObjC selector, method, or ivar it comes from. Returns '' when
    nothing useful can be derived"""
    if not rhs:
        return ""
    sel = ""
    m = re.search(r'objc_msgSend[A-Za-z0-9_]*\s*\([^,"]*,\s*"([^"]+)"', rhs)  # objc_msgSend(recv, "sel")
    if m:
        sel = m.group(1)
    if not sel:
        m = re.search(r'objc_msgSend\$([A-Za-z_][A-Za-z0-9_:]*)', rhs)          # objc_msgSend$sel
        if m:
            sel = m.group(1)
    if not sel:
        m = re.search(r'[-+]\[[^\]]*\s+([A-Za-z_][A-Za-z0-9_:]*)\]', rhs)       # +[Class sel] / -[obj sel]
        if m:
            sel = m.group(1)
    if not sel:
        m = re.search(r'->\s*_?([A-Za-z_][A-Za-z0-9_]*)', rhs)                  # x->_field
        if m:
            sel = m.group(1)
    if not sel:
        return ""
    first = re.sub(r'[^A-Za-z0-9]', '', sel.split(":")[0].lstrip("_"))          # first selector keyword
    if not first or not first[0].isalpha() or first.lower() in (
        "alloc", "init", "class", "self", "super", "id", "new", "type"
    ):
        return ""
    return first[0].lower() + first[1:]


def _lvar_semantic_renames(cfunc) -> dict:
    """Map each default-named local variable to a semantic name derived from its
    first assignment. Wrapped pseudocode lines are rejoined into statements first."""
    stmts, buf = [], ""
    for ln in _pseudocode_lines(cfunc):
        buf += ((" " if buf else "") + ln.strip())
        if ln.rstrip().endswith((";", "{", "}")):
            stmts.append(buf)
            buf = ""
    if buf:
        stmts.append(buf)
    out = {}
    for s in stmts:
        m = re.match(r'^\s*([A-Za-z_]\w*)\s*=\s*(.+?);\s*$', s)
        if not m:
            continue
        lhs, rhs = m.group(1), m.group(2)
        if not _RENAMEABLE_LVAR_RE.match(lhs) or lhs in out:
            continue
        name = _semantic_name_from_assignment(rhs)
        if name:
            out[lhs] = name
    return out

def _auto_annotate_core(func_ea: int, header_comment: str = "") -> dict:
    out = {"ok": False, "renamed": 0, "commented": 0, "func": int(func_ea)}
    f = ida_funcs.get_func(func_ea)
    if not f:
        return out
    out["ok"] = True
    start = f.start_ea

    # ensure an entry comment without overwriting LLM output
    try:
        existing = idc.get_cmt(start, 1) or idc.get_cmt(start, 0) or ""
        if header_comment:
            if not existing:
                idc.set_cmt(start, header_comment, 1)
                out["commented"] = 1
            elif header_comment not in existing:
                idc.set_cmt(start, existing + "\n" + header_comment, 1)
                out["commented"] = 1
            else:
                out["commented"] = 1
        elif existing:
            out["commented"] = 1
    except Exception:
        pass

    # rename opaque locals: prefer a semantic name derived from the assignment
    # (v5 -> ccTopViewLabel), fall back to a type prefix (v5 -> void_v5) when the
    # value has no name to borrow. Both via ida_hexrays.rename_lvar
    try:
        cfunc = ida_hexrays.decompile(f)
        if cfunc:
            semantic = _lvar_semantic_renames(cfunc)
            used = {str(v.name) for v in cfunc.get_lvars()}
            renames = []  # (old_name, new_name)
            for v in cfunc.get_lvars():
                name = str(v.name)
                if not _RENAMEABLE_LVAR_RE.match(name):
                    continue
                new_name = semantic.get(name, "")
                if not new_name:
                    if not _DEFAULT_LVAR_RE.match(name):
                        continue  # already type-prefixed and no semantic name -> leave it
                    try:
                        tstr = str(v.type())
                    except Exception:
                        tstr = ""
                    new_name = "{}_{}".format(_type_prefix(tstr), name)
                base, n = new_name, 2
                while new_name in used:          # dedup collisions deterministically
                    new_name = "{}_{}".format(base, n)
                    n += 1
                used.add(new_name)
                renames.append((name, new_name))
            for old_name, new_name in renames:
                try:
                    if ida_hexrays.rename_lvar(start, old_name, new_name):
                        out["renamed"] += 1
                except Exception:
                    pass
            if os.environ.get("RE_ANNOT_DEBUG") == "1":
                try:
                    with open("/tmp/annot_debug.log", "a") as _fh:
                        _fh.write("func=%s lvars=%d semantic=%s planned=%s renamed=%d\n" % (
                            hex(int(func_ea)), len(list(cfunc.get_lvars())),
                            dict(list(semantic.items())[:8]), renames[:8], out["renamed"]))
                except Exception:
                    pass
    except Exception as _e:
        if os.environ.get("RE_ANNOT_DEBUG") == "1":
            try:
                with open("/tmp/annot_debug.log", "a") as _fh:
                    _fh.write("func=%s EXC %s: %s\n" % (hex(int(func_ea)), type(_e).__name__, str(_e)[:200]))
            except Exception:
                pass

    return out


_TYPE_CMT_RE = re.compile(
    r"^(?:"
    r"(?:unsigned |signed |const |volatile )*"
    r"(?:__int\d+|int|char|void|bool|long|short|double|float|_DWORD|_QWORD|_BYTE|_WORD|id)"
    r"(?:\s*\*+)?"                                   # C primitive, optional pointer
    r"|(?:struct|enum)\b.*"                          # struct/enum X
    r"|_*[A-Za-z][A-Za-z0-9_]*\s*\*+"               # any identifier + pointer (NSString *)
    r"|_*[A-Za-z][A-Za-z0-9_]*(?:Ref|_t)\s*\**"     # FooRef / foo_t
    r")$"
)

def _is_auto_comment(text: str) -> bool:
    """Return True if a comment contains only IDA auto-generated text"""
    s = (text or "").strip()
    if not s:
        return True
    for line in s.splitlines():
        ls = line.strip()
        if not ls:
            continue
        if ls.startswith("jumptable") or ls.startswith("switch ") or _TYPE_CMT_RE.match(ls):
            continue
        return False
    return True

def _count_user_annotations_core(func_eas) -> dict:
    """Count persisted user annotations across functions"""
    res = {"named_lvars": 0, "comments": 0, "functions": 0}
    for fea in func_eas:
        try:
            fea = int(fea)
        except (ValueError, TypeError):
            continue
        f = ida_funcs.get_func(fea)
        if not f:
            continue
        res["functions"] += 1
        try:
            ea = f.start_ea
            while ea < f.end_ea and ea != idc.BADADDR:
                c = idc.get_cmt(ea, 1) or idc.get_cmt(ea, 0)
                if c and not _is_auto_comment(c):
                    res["comments"] += 1
                ea = idc.next_head(ea, f.end_ea)
        except Exception:
            pass
        try:
            uv = ida_hexrays.lvar_uservec_t()
            if ida_hexrays.restore_user_lvar_settings(uv, f.start_ea):
                for lv in uv.lvvec:
                    if lv.name:
                        res["named_lvars"] += 1
        except Exception:
            pass
    return res


class DecompilerService(rpyc.Service):
    """Expose IDA Pro's decompilation and analysis features to a remote client over RPC"""

    def on_connect(self, conn):
        print(f"[DecompilerService] Client connected: {conn}")

    def on_disconnect(self, conn):
        print(f"[DecompilerService] Client disconnected: {conn}")

    def exposed_decompile_function(self, address: int) -> str:
        """Decompiles the function at the given address and returns it as a string"""
        def _do():
            import idc
            seg = idc.get_segm_name(address)
            if seg == "__stubs":
                return f"# ERROR: Address 0x{address:x} is inside the '__stubs' segment (dynamic linker stub). Decompiling stubs is not supported. Please use get_xrefs_to on this stub address to locate callers."

            f = ida_funcs.get_func(address)
            if not f:
                return f"# ERROR: No function found at address 0x{address:x}"
            cfunc = ida_hexrays.decompile(f)
            if cfunc:
                return str(cfunc)
            return f"# ERROR: Failed to decompile function at 0x{address:x}"
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            return f"# ERROR: {e}"

    def exposed_get_xrefs_to(self, address: int) -> list:
        """Finds code cross-references to a given address, transitively following data references
        if they lead to data structures (like CFStrings or selector references) instead of functions"""
        def _do():
            import ida_funcs
            import idautils
            import ida_segment
            import idc
            
            xrefs = []
            visited = set()
            
            def collect_xrefs(current_addr, depth=0):
                if depth > 3:
                    return
                if current_addr in visited:
                    return
                visited.add(current_addr)
                
                local_xrefs = list(idautils.XrefsTo(current_addr))
                for xref in local_xrefs:
                    frm = int(xref.frm)
                    func = ida_funcs.get_func(frm)
                    
                    if func:
                        xrefs.append({
                            "from_address": frm,
                            "function_start": int(func.start_ea),
                            "type": str(idautils.XrefTypeName(xref.type)),
                            "via_address": int(current_addr) if current_addr != address else 0
                        })
                    else:
                        if depth == 0:
                            xrefs.append({
                                "from_address": frm,
                                "function_start": 0,
                                "type": str(idautils.XrefTypeName(xref.type)),
                                "via_address": 0
                            })
                        
                        seg = ida_segment.getseg(frm)
                        if seg:
                            collect_xrefs(frm, depth + 1)
            
            collect_xrefs(address)
            
            # if no actual code references were found, try manual pointer scanning
            if not any(x["function_start"] != 0 for x in xrefs):
                for s_ea in idautils.Segments():
                    s_name = idc.get_segm_name(s_ea).lower()
                    if any(k in s_name for k in ["selrefs", "cfstring", "objc", "const", "data", "got"]):
                        start = s_ea
                        end = idc.get_segm_end(start)
                        struct_offset = 16 if "cfstring" in s_name else 0
                        
                        for ptr_addr in range(start, end - 7, 8):
                            val = idc.get_qword(ptr_addr)
                            if (val & 0x00007fffffffffff) == address:
                                ref_target = ptr_addr - struct_offset
                                collect_xrefs(ref_target, depth=1)
            
            # deduplicate by (from_address, function_start)
            seen = set()
            dedup_xrefs = []
            for x in xrefs:
                key = (x["from_address"], x["function_start"])
                if key not in seen:
                    seen.add(key)
                    dedup_xrefs.append(x)
            return dedup_xrefs
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            return [{"error": f"Exception: {str(e)}"}]

    def exposed_rename_local_variable(self, func_address: int, old_name: str, new_name: str) -> bool:
        """Renames a local variable within a function's decompilation and commits it to the database"""
        def _do():
            f = ida_funcs.get_func(func_address)
            if not f:
                return False
            cfunc = ida_hexrays.decompile(f)
            if not cfunc:
                return False
            if not any(str(var.name) == old_name for var in cfunc.get_lvars()):
                return False
            return bool(ida_hexrays.rename_lvar(f.start_ea, old_name, new_name))
        try:
            return _run_on_main_thread(_do)
        except Exception:
            return False

    def exposed_get_local_variables(self, func_address: int) -> list:
        """Returns the names of all local variables in a function's decompilation"""
        def _do():
            f = ida_funcs.get_func(func_address)
            if not f:
                return []
            cfunc = ida_hexrays.decompile(f)
            if not cfunc:
                return []
            return [str(v.name) for v in cfunc.get_lvars()]
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in get_local_variables: {e}")
            return []

    def exposed_set_comment(self, address: int, comment: str) -> bool:
        """Sets a repeatable comment at a specific address in the disassembly"""
        def _do():
            import idc
            idc.set_cmt(address, comment, 1)
            return True
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in set_comment: {e}")
            return False

    def exposed_get_function_boundaries(self, ea: int):
        """Gets the start and end addresses of the function containing the given address"""
        def _do():
            func = idaapi.get_func(ea)
            if func:
                return (func.start_ea, func.end_ea)
            return (0, 0)
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in get_function_boundaries: {e}")
            return (0, 0)

    def exposed_get_segment_name(self, ea: int):
        """Gets the name of the segment containing the given address"""
        def _do():
            seg = idc.get_segm_name(ea)
            return seg if seg else ""
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in get_segment_name: {e}")
            return ""

    def exposed_lookup_symbol(self, symbol_name: str):
        """Looks up the memory address of a given symbol by exact name.
        Tries the raw name, with/without leading underscore."""
        print(f"[DecompilerService] Request to lookup symbol: {symbol_name}")
        def _do():
            import idc
            candidates = [
                symbol_name,
                "_" + symbol_name if not symbol_name.startswith("_") else symbol_name[1:],
            ]
            for c in candidates:
                ea = idc.get_name_ea_simple(c)
                if ea != idc.BADADDR:
                    return ea
            return 0
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in lookup_symbol: {e}")
            return 0

    def exposed_lookup_symbol_fuzzy(self, token: str):
        """
        Fuzzy symbol lookup: 
        -scans IDA's Names() table for entries that contain
        the token as a substring (case-insensitive, ignoring _ and - separators)
        -checks for ObjC sel_ prefix variants
        -returns a list of {name, address} dicts for the top-20 matches
        """
        print(f"[DecompilerService] Fuzzy lookup for: {token}")
        def _do():
            import idautils
            import idc
            needle = token.lower().replace("-", "").replace("_", "")

            sel_name = "sel_" + token
            ea = idc.get_name_ea_simple(sel_name)
            if ea != idc.BADADDR:
                return [{"name": sel_name, "address": int(ea)}]

            matches = []
            for ea, name in idautils.Names():
                norm = name.lower().replace("_", "").replace("-", "")
                if needle in norm:
                    matches.append({"name": name, "address": int(ea)})
                    if len(matches) >= 20:
                        break
            return matches
        try:
            return _run_on_main_thread(_do, timeout=120)
        except Exception as e:
            print(f"Error in lookup_symbol_fuzzy: {e}")
            return []

    def exposed_find_objc_method_impl(self, selector: str):
        """Find the real ObjC method for an exact selector.

        On stripped binaries, the selector may only exist as text, so scan Names()
        for an exact `-[Class selector]` / `+[Class selector]` match and skip
        objc_msgSend thunks"""
        print(f"[DecompilerService] ObjC method-impl lookup for: {selector}")
        want = selector.lstrip("_")  # ObjC private methods keep a leading _; match either way
        def _do():
            import idautils
            out = []
            for ea, name in idautils.Names():
                if not (name.startswith("-[") or name.startswith("+[")) or not name.endswith("]"):
                    continue
                inner = name[2:-1].split(" ", 1)  # ["Class", "selector..."]
                if len(inner) == 2 and inner[1].lstrip("_") == want:
                    out.append({"name": name, "address": int(ea)})
            return out
        try:
            return _run_on_main_thread(_do, timeout=120)
        except Exception as e:
            print(f"Error in find_objc_method_impl: {e}")
            return []

    def exposed_search_string(self, target_string: str):
        def _do():
            found = []
            try:
                import idautils
                for s in idautils.Strings():
                    s_str = str(s)
                    if s_str == target_string or target_string in s_str:
                        found.append(int(s.ea))
                        if len(found) >= 100:
                            break
            except Exception as e:
                print(f"[DecompilerService] Error in search_string: {e}")
            return found
        try:
            return _run_on_main_thread(_do, timeout=300)
        except Exception as e:
            print(f"Error in search_string outer: {e}")
            return []

    def exposed_save_ida_database(self, out_path: str = ""):
        """Saves the current IDA Pro database"""
        def _do():
            import ida_loader
            ida_loader.save_database(out_path if out_path else None, 0)
            return True
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in save_ida_database: {e}")
            return False

    def exposed_resolve_objc_dispatch(self, func_ea: int, call_ea: int):
        """Attempts to resolve the objc_msgSend class and selector at call_ea inside func_ea using Hex-Rays AST"""
        def _do():
            try:
                import ida_hexrays
                cfunc = ida_hexrays.decompile(func_ea)
                if not cfunc: return "error: could not decompile function"
                # extract the specific pseudocode line
                # and surrounding context (provide LLM with exact localized info)
                lines = []
                for item in cfunc.get_pseudocode():
                    clean_line = ida_lines.tag_remove(item.line)
                    lines.append(clean_line)
                    if f"{call_ea:X}" in item.line or f"{call_ea:x}" in item.line or hex(call_ea) in clean_line:
                        idx = len(lines) - 1
                        start = max(0, idx - 5)
                        return "\n".join(lines[start:idx+1])
                # if exact ea match fails, just return the whole function
                return "\n".join(_pseudocode_lines(cfunc))
            except Exception as e:
                return f"error: {e}"
        return _run_on_main_thread(_do)

    def exposed_trace_variable_source(self, func_ea: int, var_name: str):
        """Traces the source of a variable inside a function by dumping the def-use context"""
        def _do():
            try:
                import ida_hexrays
                cfunc = ida_hexrays.decompile(func_ea)
                if not cfunc: return "error: could not decompile function"
                lines = _pseudocode_lines(cfunc)
                # extract all lines containing the var_name
                trace_lines = [l for l in lines if var_name in l]
                if not trace_lines:
                    return f"error: Variable {var_name} not found in {hex(func_ea)}"
                return "Variable trace:\n" + "\n".join(trace_lines)
            except Exception as e:
                return f"error: {e}"
        return _run_on_main_thread(_do)

    def exposed_auto_annotate_function(self, func_ea: int, header_comment: str = "") -> dict:
        """Apply baseline annotations to a function"""
        try:
            return _run_on_main_thread(_auto_annotate_core, func_ea, header_comment)
        except Exception as e:
            print(f"Error in auto_annotate_function: {e}")
            return {"ok": False, "renamed": 0, "commented": 0, "func": int(func_ea)}

    def exposed_count_user_annotations(self, func_eas) -> dict:
        """Count persisted annotations for verification"""
        eas = list(func_eas) if func_eas else []
        try:
            return _run_on_main_thread(_count_user_annotations_core, eas)
        except Exception as e:
            print(f"Error in count_user_annotations: {e}")
            return {"named_lvars": 0, "comments": 0, "functions": 0}

    def exposed_shutdown(self):
        """Remotely shuts down the IDA Pro instance"""
        print("[DecompilerService] Received shutdown signal. Exiting IDA.")
        def _exit_task():
            import ida_pro
            ida_pro.qexit(0)
            import os
            os._exit(0)
        _work_queue.put(_exit_task)

def start_server(port):
    print(f"[DecompilerService] Starting RPC server on port {port}...")
    print("[DecompilerService] Waiting for connections from your agent...")
    try:
        t = ThreadedServer(
            DecompilerService,
            port=port,
            protocol_config={'allow_public_attrs': True}
        )
        t.start()
    except Exception as e:
        print(f"[DecompilerService] FATAL ERROR: Server failed to start: {e}")
        import ida_pro
        ida_pro.qexit(1)
        import os
        os._exit(1)


if __name__ == "__main__":
    port = 18861

    print("[DecompilerService] Waiting for auto-analysis to complete...")
    idaapi.auto_wait()
    print("[DecompilerService] Auto-analysis complete. Starting server thread.")

    th = threading.Thread(target=start_server, args=(port,), daemon=True)
    th.start()
    print("[DecompilerService] Server thread started. Main thread pumping work queue.")

    while True:
        try:
            task = _work_queue.get(timeout=0.1)
            task()
        except queue.Empty:
            pass
        except Exception as e:
            print(f"[DecompilerService] Error in main thread task: {e}")
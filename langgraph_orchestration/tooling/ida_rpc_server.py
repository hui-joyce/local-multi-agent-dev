"""Queue-based main-thread execution for headless mode"""
import rpyc
from rpyc.utils.server import ThreadedServer
import ida_hexrays
import ida_funcs
import idc
import idautils
import idaapi
import threading
import queue
import time

if not ida_hexrays.init_hexrays_plugin():
    ida_hexrays.load_plugin()
    if not ida_hexrays.init_hexrays_plugin():
        print("Error: Hex-Rays decompiler is not available. The decompiler service cannot start.")

_work_queue: queue.Queue = queue.Queue()

def _run_on_main_thread(func, *args, timeout=30):
    """Submit a callable to be executed on the main thread and wait for the result"""
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


class DecompilerService(rpyc.Service):
    """Expose IDA Pro's decompilation and analysis features to a remote client over RPC"""

    def on_connect(self, conn):
        print(f"[DecompilerService] Client connected: {conn}")

    def on_disconnect(self, conn):
        print(f"[DecompilerService] Client disconnected: {conn}")

    def exposed_decompile_function(self, address: int) -> str:
        """Decompiles the function at the given address and returns it as a string"""
        def _do():
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
        """Finds code cross-references to a given address"""
        def _do():
            xrefs = []
            for xref in idautils.XrefsTo(address):
                func = ida_funcs.get_func(xref.frm)
                xrefs.append({
                    "from_address": int(xref.frm),
                    "function_start": int(func.start_ea if func else 0),
                    "type": str(idautils.XrefTypeName(xref.type))
                })
            return xrefs
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            return [{"error": f"Exception: {str(e)}"}]

    def exposed_rename_local_variable(self, func_address: int, old_name: str, new_name: str) -> bool:
        """Renames a local variable within a function's decompilation"""
        def _do():
            f = ida_funcs.get_func(func_address)
            if not f:
                return False
            cfunc = ida_hexrays.decompile(f)
            if not cfunc:
                return False
            lvars = cfunc.get_lvars()
            for var in lvars:
                if var.name == old_name:
                    return cfunc.rename_lvar(var, new_name, True)
            return False
        try:
            return _run_on_main_thread(_do)
        except Exception:
            return False

    def exposed_set_comment(self, address: int, comment: str) -> bool:
        """Sets a repeatable comment at a specific address in the disassembly"""
        def _do():
            idc.set_comment(address, comment, 1)
            return True
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in set_comment: {e}")
            return False

    def exposed_get_function_name(self, ea: int):
        """Gets the name of the function containing the given address"""
        def _do():
            name = idc.get_func_name(ea)
            return name if name else ""
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in get_function_name: {e}")
            return ""

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

    def exposed_get_bytes(self, ea: int, size: int):
        """Reads raw bytes from the binary"""
        def _do():
            import ida_bytes
            return ida_bytes.get_bytes(ea, size)
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in get_bytes: {e}")
            return None

    def exposed_get_qword(self, ea: int):
        """Reads a 64-bit value from the binary"""
        def _do():
            val = idc.get_qword(ea)
            return val if val != idc.BADADDR else 0
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in get_qword: {e}")
            return 0

    def exposed_lookup_symbol(self, symbol_name: str):
        """Looks up the memory address of a given symbol"""
        print(f"[DecompilerService] Request to lookup symbol: {symbol_name}")
        def _do():
            import ida_name
            import idc
            ea = idc.get_name_ea_simple(symbol_name)
            if ea != idc.BADADDR:
                return ea
            if symbol_name.startswith("_"):
                ea = idc.get_name_ea_simple(symbol_name[1:])
                if ea != idc.BADADDR: return ea
            else:
                ea = idc.get_name_ea_simple("_" + symbol_name)
                if ea != idc.BADADDR: return ea
            return 0
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in lookup_symbol: {e}")
            return 0

    def exposed_search_string(self, target_string: str):
        """Searches for a string in known string sections only (fast, targeted bin_search)"""
        def _do():
            found = []
            try:
                import ida_bytes
                import ida_segment
                import idaapi
                import idautils

                encoded = target_string.encode("utf-8")
                hex_pattern = " ".join(f"{b:02x}" for b in encoded)
                pattern = ida_bytes.compiled_binpat_vec_t()
                ida_bytes.parse_binpat_str(pattern, 0, hex_pattern, 16)

                TARGET_SUFFIXES = (
                    "__TEXT.__cstring",
                    "__TEXT.__objc_methname",
                    "__TEXT.__oslogstring",
                    "__TEXT.__ustring",
                )

                for seg_ea in idautils.Segments():
                    seg = ida_segment.getseg(seg_ea)
                    if not seg:
                        continue
                    seg_name = idc.get_segm_name(seg_ea)
                    # Match both standalone ("__TEXT.__cstring") and DSC-prefixed
                    # ("iMessage.__TEXT.__cstring") section names.
                    if not any(seg_name.endswith(suffix) for suffix in TARGET_SUFFIXES):
                        continue
                    ea = seg.start_ea
                    while ea < seg.end_ea:
                        res = ida_bytes.bin_search(ea, seg.end_ea, pattern, ida_bytes.BIN_SEARCH_FORWARD)
                        ea_val = res[0] if isinstance(res, tuple) else res
                        if ea_val == idaapi.BADADDR:
                            break
                        found.append(int(ea_val))
                        ea = ea_val + len(encoded)
                        if len(found) >= 100:
                            break
                    if len(found) >= 100:
                        break
            except Exception as e:
                print(f"[DecompilerService] Error in search_string: {e}")
            return found
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in search_string: {e}")
            return []

    def exposed_save_ida_database(self, out_path: str = ""):
        """Saves the current IDA Pro database"""
        def _do():
            import ida_pro
            ida_pro.save_database(out_path if out_path else None, 0)
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
                    clean_line = ida_hexrays.tag_remove(item.line)
                    lines.append(clean_line)
                    if f"{call_ea:X}" in item.line or f"{call_ea:x}" in item.line or hex(call_ea) in clean_line:
                        idx = len(lines) - 1
                        start = max(0, idx - 5)
                        return "\n".join(lines[start:idx+1])
                # if exact ea match fails, just return the whole function
                return "\n".join([ida_hexrays.tag_remove(i.line) for i in cfunc.get_pseudocode()])
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
                lines = [ida_hexrays.tag_remove(i.line) for i in cfunc.get_pseudocode()]
                # Extract all lines containing the var_name
                trace_lines = [l for l in lines if var_name in l]
                if not trace_lines:
                    return f"error: Variable {var_name} not found in {hex(func_ea)}"
                return "Variable trace:\n" + "\n".join(trace_lines)
            except Exception as e:
                return f"error: {e}"
        return _run_on_main_thread(_do)

    def exposed_shutdown(self):
        """Remotely shuts down the IDA Pro instance"""
        import ida_pro
        print("[DecompilerService] Received shutdown signal. Exiting IDA.")
        ida_pro.qexit(0)


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

    # main thread loop
    while True:
        try:
            task = _work_queue.get(timeout=0.1)
            task()
        except queue.Empty:
            pass
        except Exception as e:
            print(f"[DecompilerService] Error in main thread task: {e}")
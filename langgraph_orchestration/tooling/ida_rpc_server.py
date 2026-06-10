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

def _run_on_main_thread(func, *args, timeout=120):
    """Submit a callable to be executed on the main thread and wait for the result."""
    result_event = threading.Event()
    result_container = {"value": None, "error": None}

    def task():
        try:
            result_container["value"] = func(*args)
        except Exception as e:
            result_container["error"] = e
        finally:
            result_event.set()

    _work_queue.put(task)

    if not result_event.wait(timeout=timeout):
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
            ea = idc.get_name_ea_simple(symbol_name)
            if ea != idc.BADADDR:
                return ea
            return 0
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in lookup_symbol: {e}")
            return 0

    def exposed_search_string(self, target_string: str):
        """Searches for a string in the binary. Uses IDA's string catalog (idautils.Strings) first, then falls back to raw byte search."""
        print(f"[DecompilerService] Request to search string: '{target_string}'")
        def _do():
            found = []
            import idautils
            for s in idautils.Strings():
                if target_string in str(s):
                    found.append(int(s.ea))
            if found:
                return found

            # Fallback: raw byte search with find_binary
            hex_str = " ".join(f"{ord(c):02X}" for c in target_string)
            ea = idc.get_inf_attr(idc.INF_MIN_EA)
            max_ea = idc.get_inf_attr(idc.INF_MAX_EA)
            while ea != idc.BADADDR and ea != -1 and ea < max_ea:
                ea = idc.find_binary(ea, idc.SEARCH_DOWN, hex_str)
                if ea != idc.BADADDR and ea != -1:
                    found.append(int(ea))
                    ea += len(target_string)
            return found
        try:
            return _run_on_main_thread(_do)
        except Exception as e:
            print(f"Error in search_string: {e}")
            return []

    def exposed_shutdown(self):
        """Remotely shuts down the IDA Pro instance"""
        import ida_pro
        print("[DecompilerService] Received shutdown signal. Exiting IDA.")
        ida_pro.qexit(0)


def start_server(port):
    print(f"[DecompilerService] Starting RPC server on port {port}...")
    print("[DecompilerService] Waiting for connections from your agent...")
    t = ThreadedServer(
        DecompilerService,
        port=port,
        protocol_config={'allow_public_attrs': True}
    )
    t.start()


if __name__ == "__main__":
    port = 18861

    print("[DecompilerService] Waiting for auto-analysis to complete...")
    idaapi.auto_wait()
    print("[DecompilerService] Auto-analysis complete. Starting server thread.")

    th = threading.Thread(target=start_server, args=(port,), daemon=True)
    th.start()
    print("[DecompilerService] Server thread started. Main thread pumping work queue.")

    # Main thread loop
    while True:
        try:
            task = _work_queue.get(timeout=0.1)
            task()
        except queue.Empty:
            pass
        except Exception as e:
            print(f"[DecompilerService] Error in main thread task: {e}")
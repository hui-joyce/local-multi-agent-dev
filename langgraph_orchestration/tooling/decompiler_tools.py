"""using remote IDA Pro service"""
from __future__ import annotations
import os
import subprocess
import time
import rpyc
from dotenv import load_dotenv

from langchain_core.tools import tool
load_dotenv()

DECOMPILER_HOST = "localhost"
DECOMPILER_PORT = 18861
IDA_EXECUTABLE_PATH = os.getenv("IDA_PATH")
IDA_RPC_SERVER_SCRIPT = os.getenv("IDA_RPC_SCRIPT_PATH")

@tool
def decompile_function(address: int) -> str:
    """Decompiles the function at the given address"""
    try:
        conn = rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT)
        decompiled_code = conn.root.exposed_decompile_function(address)
        conn.close()
        return decompiled_code
    except ConnectionRefusedError:
        return f"# ERROR: Connection to decompiler service was refused. Is the IDA Pro RPC server running on port {DECOMPILER_PORT}?"
    except Exception as e:
        return f"# ERROR: An unexpected error occurred during decompilation: {e}"

@tool
def get_xrefs_to(address: int) -> list[dict]:
    """Finds code cross-references to a given address"""
    try:
        conn = rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT)
        xrefs = conn.root.exposed_get_xrefs_to(address)
        conn.close()
        return xrefs
    except ConnectionRefusedError:
        return [{"error": f"Connection to decompiler service was refused on port {DECOMPILER_PORT}."}]
    except Exception as e:
        return [{"error": f"An unexpected error occurred: {e}"}]

@tool
def search_string(target_string: str) -> list:
    """Searches the binary for a specific string and returns a list of memory addresses where it is found.
    NOTE: These are DATA addresses, not function addresses. You MUST pass these addresses to `get_xrefs_to` to find which functions reference the string. Do NOT use `decompile_function` directly on these addresses."""
    try:
        conn = rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT, config={"sync_request_timeout": 120})
        addresses = conn.root.exposed_search_string(target_string)
        # Materialize the rpyc netref list into a plain Python list
        result = [int(a) for a in addresses] if addresses else []
        conn.close()
        return result
    except ConnectionRefusedError:
        return ["error: Connection to decompiler refused. Is IDA Pro running?"]
    except TimeoutError:
        return ["error: Decompiler request timed out"]
    except EOFError:
        return ["error: Decompiler connection closed unexpectedly"]
    except Exception as e:
        return [f"error: {str(e)}"]

@tool
def lookup_symbol(symbol_name: str) -> str:
    """Looks up the memory address of a symbol (like a function name or global variable) in the binary. Returns hex address string or error."""
    try:
        conn = rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT, config={"sync_request_timeout": 120})
        addr = conn.root.exposed_lookup_symbol(symbol_name)
        conn.close()
        if addr and addr != 0:
            return hex(int(addr))
        return f"error: Symbol '{symbol_name}' not found in binary"
    except ConnectionRefusedError:
        return "error: Connection to decompiler refused. Is IDA Pro running?"
    except TimeoutError:
        return "error: Decompiler request timed out"
    except EOFError:
        return "error: Decompiler connection closed unexpectedly"
    except Exception as e:
        return f"error: {str(e)}"

@tool
def rename_local_variable(func_address: int, old_name: str, new_name: str) -> bool:
    """Renames a local variable within a function's decompilation using the remote IDA Pro service"""
    try:
        conn = rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT)
        success = conn.root.exposed_rename_local_variable(func_address, old_name, new_name)
        conn.close()
        return success
    except ConnectionRefusedError:
        return False
    except Exception:
        return False

@tool
def start_ida_server_for_binary(binary_path: str) -> str:
    """
    Starts an IDA Pro instance in the background with the RPC server for a specific binary.
    Wait until the server is responsive before returning.
    """
    if not IDA_EXECUTABLE_PATH or not os.path.isfile(IDA_EXECUTABLE_PATH):
        return "# ERROR: IDA Pro executable path is not configured or invalid. Please set the IDA_PATH environment variable in your .env file."
    if not IDA_RPC_SERVER_SCRIPT or not os.path.isfile(IDA_RPC_SERVER_SCRIPT):
        return "# ERROR: IDA RPC server script path is not configured or invalid. Please set the IDA_RPC_SCRIPT_PATH environment variable in your .env file."
    if not os.path.isfile(binary_path):
        return f"# ERROR: Binary file not found at '{binary_path}'."
    stop_ida_server.invoke({})
    command = [
        IDA_EXECUTABLE_PATH,
        "-A",  # autonomous mode
        "-L/tmp/ida.log",
        f"-S{IDA_RPC_SERVER_SCRIPT}",
        binary_path,
    ]
    try:
        env = os.environ.copy()
        log_file = open("/tmp/ida_rpc_server.log", "w")
        subprocess.Popen(command, stdout=log_file, stderr=log_file, stdin=subprocess.DEVNULL, env=env)
    except Exception as e:
        return f"# ERROR: Failed to start IDA Pro process: {e}"
    for _ in range(300):  # Wait up to 10 mins
        try:
            with rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT, config={"sync_request_timeout": 2}) as conn:
                return f"Successfully started and connected to IDA Pro RPC server for binary: {os.path.basename(binary_path)}."
        except ConnectionRefusedError:
            time.sleep(2)
            
    return "# ERROR: Timed out waiting for IDA Pro RPC server to start."

@tool
def stop_ida_server() -> str:
    """Connects to the running IDA Pro RPC server and requests a shutdown"""
    try:
        with rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT, config={"sync_request_timeout": 5}) as conn:
            conn.root.exposed_shutdown()
        return "Shutdown signal sent to IDA Pro RPC server."
    except ConnectionRefusedError:
        return "No active IDA Pro RPC server found to stop."
    except EOFError:
        return "Shutdown signal sent to IDA Pro RPC server (connection closed by peer)."
    except Exception as e:
        return f"Shutdown signal sent, but connection terminated abnormally: {e}"

@tool
def set_comment(address: int, comment: str) -> bool:
    """Sets a comment at a specific address in the disassembly"""
    try:
        conn = rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT)
        success = conn.root.exposed_set_comment(address, comment)
        conn.close()
        return success
    except ConnectionRefusedError:
        return False
    except Exception:
        return False

@tool
def save_ida_database() -> str:
    """Saves the current IDA Pro database (.i64) with any annotations made"""
    try:
        conn = rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT)
        success = conn.root.exposed_save_ida_database("")
        conn.close()
        return "Successfully saved IDA database." if success else "Failed to save IDA database."
    except ConnectionRefusedError:
        return "Connection refused."
    except Exception as e:
        return f"Error saving database: {e}"

@tool
def get_entitlements(binary_path: str) -> str:
    """Extracts entitlements from a Mach-O binary using ipsw"""
    try:
        import subprocess
        result = subprocess.run(["ipsw", "ent", binary_path], capture_output=True, text=True, check=True)
        return result.stdout or result.stderr
    except subprocess.CalledProcessError as e:
        return f"Failed to get entitlements: {e.stderr}"
    except Exception as e:
        return f"Error: {e}"

@tool
def resolve_objc_dispatch(func_ea: int, call_ea: int) -> str:
    """Attempts to resolve the objc_msgSend class and selector at call_ea inside func_ea using Hex-Rays AST"""
    try:
        conn = rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT)
        result = conn.root.exposed_resolve_objc_dispatch(func_ea, call_ea)
        conn.close()
        return result
    except ConnectionRefusedError:
        return "Connection refused."
    except Exception as e:
        return f"Error: {e}"

@tool
def trace_variable_source(func_ea: int, var_name: str) -> str:
    """Traces the source of a variable inside a function by dumping the def-use context"""
    try:
        conn = rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT)
        result = conn.root.exposed_trace_variable_source(func_ea, var_name)
        conn.close()
        return result
    except ConnectionRefusedError:
        return "Connection refused."
    except Exception as e:
        return f"Error: {e}"
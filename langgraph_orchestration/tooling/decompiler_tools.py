"""using remote IDA Pro service"""
from __future__ import annotations
import os
import subprocess
import time
import rpyc
from typing import Union
from dotenv import load_dotenv

from langchain_core.tools import tool
load_dotenv()

DECOMPILER_HOST = "localhost"
DECOMPILER_PORT = 18861

RPC_TIMEOUT = 60
IDA_EXECUTABLE_PATH = os.getenv("IDA_PATH")
IDA_RPC_SERVER_SCRIPT = os.getenv("IDA_RPC_SCRIPT_PATH")

def _connect() -> rpyc.Connection:
    """Open a fresh rpyc connection with a consistent timeout"""
    return rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT, config={"sync_request_timeout": RPC_TIMEOUT})

@tool
def decompile_function(address: int) -> str:
    """Decompiles the function at the given address"""
    last_error = None
    for attempt in range(3):
        try:
            conn = _connect()
            result = conn.root.exposed_decompile_function(address)
            conn.close()
            return result
        except ConnectionRefusedError:
            return f"# ERROR: Connection refused. Is IDA Pro RPC server running on port {DECOMPILER_PORT}?"
        except TimeoutError:
            return "# ERROR: Decompiler request timed out."
        except EOFError as e:
            last_error = e
            time.sleep(2 * (attempt + 1))
        except Exception as e:
            return f"# ERROR: {e}"
    return f"# ERROR: Decompiler stream closed after 3 attempts: {last_error}"


@tool
def get_xrefs_to(address: int) -> list[dict]:
    """Finds code cross-references to a given address"""
    last_error = None
    for attempt in range(3):
        try:
            conn = _connect()
            xrefs = conn.root.exposed_get_xrefs_to(address)
            result = list(xrefs) if xrefs else []
            conn.close()
            return result
        except ConnectionRefusedError:
            return [{"error": f"Connection refused on port {DECOMPILER_PORT}."}]
        except TimeoutError:
            return [{"error": "Decompiler request timed out."}]
        except EOFError as e:
            last_error = e
            time.sleep(2 * (attempt + 1))
        except Exception as e:
            return [{"error": f"Unexpected error: {e}"}]
    return [{"error": f"Stream closed after 3 attempts: {last_error}"}]


@tool
def find_address(query: str) -> Union[dict, str]:
    """Finds an address in the binary by symbol name or string data"""
    import re

    original_query = query
    query = re.sub(r'^[-+]\s+', '', query).strip()  # strip diff markers (+/-)
    query = re.sub(r'^"|"$', '', query)              # strip surrounding quotes

    is_objc_selector = False

    # ObjC method: -[ClassName methodName:] or +[ClassName methodName:]
    if query.startswith("-[") or query.startswith("+["):
        match = re.search(r'\[.*? ([^\]]+)\]', query)
        if match:
            query = match.group(1)
            is_objc_selector = True

    # Block invoke: ___55-[Class method]_block_invoke
    elif "_block_invoke" in query and "-[" in query:
        match = re.search(r'\[.*? ([^\]]+)\]', query)
        if match:
            query = match.group(1)
            is_objc_selector = True

    # objc_msgSend stub: _objc_msgSend$selectorName
    elif query.startswith("_objc_msgSend$"):
        query = query.replace("_objc_msgSend$", "")
        is_objc_selector = True

    # Colon in query = ObjC selector stored in __objc_methname
    elif ":" in query:
        is_objc_selector = True

    try:
        conn = _connect()

        # symbol lookup (O(log N)) 
        if not is_objc_selector:
            addr = conn.root.exposed_lookup_symbol(query)
            if addr and addr != 0:
                conn.close()
                return {"type": "symbol", "query": query, "address": hex(int(addr))}

        # string search in known sections
        addresses = conn.root.exposed_search_string(query)
        conn.close()
        if addresses:
            return {"type": "string_data", "query": query, "addresses": [hex(int(a)) for a in addresses]}

        return f"error: Could not find '{query}' (from original '{original_query}') as a symbol or string."

    except ConnectionRefusedError:
        return "error: Connection to decompiler refused. Is IDA Pro running?"
    except TimeoutError:
        return "error: Decompiler request timed out"
    except EOFError:
        return "error: Decompiler connection closed unexpectedly"
    except Exception as e:
        return f"error: {e}"


@tool
def rename_local_variable(func_address: int, old_name: str, new_name: str) -> bool:
    """Renames a local variable within a function's decompilation"""
    try:
        conn = _connect()
        result = conn.root.exposed_rename_local_variable(func_address, old_name, new_name)
        conn.close()
        return result
    except Exception:
        return False


@tool
def start_ida_server_for_binary(binary_path: str) -> str:
    """Launches the IDA Pro application with the RPC server script for a specific binary"""
    if not IDA_EXECUTABLE_PATH or not os.path.isfile(IDA_EXECUTABLE_PATH):
        return "# ERROR: IDA_PATH not set or invalid."
    if not IDA_RPC_SERVER_SCRIPT or not os.path.isfile(IDA_RPC_SERVER_SCRIPT):
        return "# ERROR: IDA_RPC_SCRIPT_PATH not set or invalid."
    if not os.path.isfile(binary_path):
        return f"# ERROR: Binary not found: '{binary_path}'."

    stop_ida_server.invoke({})

    # Wait for the old server to fully shut down and release the port
    import socket
    for _ in range(30):  
        try:
            with socket.create_connection((DECOMPILER_HOST, DECOMPILER_PORT), timeout=1):
                time.sleep(1)
        except (ConnectionRefusedError, socket.timeout, OSError):
            break

    command = [
        IDA_EXECUTABLE_PATH,
        "-A",
        "-L/tmp/ida.log",
        f"-S{IDA_RPC_SERVER_SCRIPT}",
        binary_path,
    ]
    try:
        log_file = open("/tmp/ida_rpc_server.log", "w")
        subprocess.Popen(command, stdout=log_file, stderr=log_file, stdin=subprocess.DEVNULL, env=os.environ.copy())
    except Exception as e:
        return f"# ERROR: Failed to start IDA Pro: {e}"

    for _ in range(300):  # Wait up to 10 minutes
        try:
            with rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT, config={"sync_request_timeout": 2}):
                return f"Successfully started IDA Pro RPC server for: {os.path.basename(binary_path)}."
        except (ConnectionRefusedError, TimeoutError, OSError):
            time.sleep(2)

    return "# ERROR: Timed out waiting for IDA Pro RPC server to start."


@tool
def stop_ida_server() -> str:
    """Connects to the running IDA Pro RPC server and requests a shutdown"""
    import socket
    import subprocess
    msg = "Shutdown signal sent."
    try:
]        with socket.create_connection((DECOMPILER_HOST, DECOMPILER_PORT), timeout=2):
            pass
        with rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT, config={"sync_request_timeout": 5}) as conn:
            conn.root.exposed_shutdown()
    except Exception as e:
        msg = f"Shutdown failed or connection terminated: {e}"
        
    # kill lingering idat processes 
    try:
        subprocess.run(["pkill", "-9", "idat"], capture_output=True)
    except Exception:
        pass

    return msg


@tool
def set_comment(address: int, comment: str) -> bool:
    """Sets a comment at a specific address in the disassembly"""
    try:
        conn = _connect()
        result = conn.root.exposed_set_comment(address, comment)
        conn.close()
        return result
    except Exception:
        return False


@tool
def save_ida_database() -> str:
    """Saves the current IDA Pro database (.i64) with any annotations made"""
    try:
        conn = _connect()
        success = conn.root.exposed_save_ida_database("")
        conn.close()
        return "Successfully saved IDA database." if success else "Failed to save IDA database."
    except ConnectionRefusedError:
        return "Connection refused."
    except TimeoutError:
        return "Error: Request timed out."
    except Exception as e:
        return f"Error saving database: {e}"


@tool
def get_entitlements(binary_path: str) -> str:
    """Extracts entitlements from a Mach-O binary using ipsw"""
    try:
        result = subprocess.run(["ipsw", "ent", binary_path], capture_output=True, text=True, check=True)
        return result.stdout or result.stderr
    except subprocess.CalledProcessError as e:
        return f"Failed to get entitlements: {e.stderr}"
    except Exception as e:
        return f"Error: {e}"


@tool
def resolve_objc_dispatch(func_ea: int, call_ea: int) -> str:
    """Attempts to resolve the objc_msgSend class and selector at call_ea inside func_ea"""
    try:
        conn = _connect()
        result = conn.root.exposed_resolve_objc_dispatch(func_ea, call_ea)
        conn.close()
        return result
    except ConnectionRefusedError:
        return "Connection refused."
    except TimeoutError:
        return "Error: Request timed out."
    except Exception as e:
        return f"Error: {e}"


@tool
def trace_variable_source(func_ea: int, var_name: str) -> str:
    """Traces the source of a variable inside a function by dumping the def-use context"""
    try:
        conn = _connect()
        result = conn.root.exposed_trace_variable_source(func_ea, var_name)
        conn.close()
        return result
    except ConnectionRefusedError:
        return "Connection refused."
    except TimeoutError:
        return "Error: Request timed out."
    except Exception as e:
        return f"Error: {e}"
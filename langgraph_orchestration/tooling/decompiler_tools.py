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

# larger than the server-side _run_on_main_thread max timeout (300s)
# so the server always has time to complete and return cleanly before the client-side timeout fires
RPC_TIMEOUT = 360
IDA_EXECUTABLE_PATH = os.getenv("IDA_PATH")
IDA_RPC_SERVER_SCRIPT = os.getenv("IDA_RPC_SCRIPT_PATH")

def _connect() -> rpyc.Connection:
    """Open a fresh rpyc connection with a consistent timeout"""
    return rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT, config={"sync_request_timeout": RPC_TIMEOUT})

def _get_connection_error_msg() -> str:
    import subprocess
    try:
        result = subprocess.run(["pgrep", "-f", "ida64|idat"], capture_output=True, text=True)
        if result.stdout.strip():
            return f"error: Connection to decompiler refused. IDA Pro is running but not responding on port {DECOMPILER_PORT}."
    except Exception:
        pass
    return "error: Connection to decompiler refused. IDA Pro is NOT running."

@tool
def decompile_function(address: Union[int, str]) -> str:
    """Decompiles the function at the given address"""
    if isinstance(address, str):
        address = int(address, 16) if address.startswith("0x") else int(address)
    last_error = None
    for attempt in range(3):
        conn = None
        try:
            conn = _connect()
            result = conn.root.exposed_decompile_function(address)
            return result
        except ConnectionRefusedError:
            return _get_connection_error_msg()
        except TimeoutError:
            return "# ERROR: Decompiler request timed out."
        except EOFError as e:
            last_error = e
            wait = 2 * (attempt + 1)
            print(f"[decompile_function] EOFError on attempt {attempt+1}, retrying in {wait}s: {e}")
            time.sleep(wait)
        except Exception as e:
            return f"# ERROR: {e}"
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
    return f"# ERROR: Decompiler stream closed after 3 attempts: {last_error}"


@tool
def get_xrefs_to(address: Union[int, str]) -> list[dict]:
    """Finds code cross-references to a given address"""
    if isinstance(address, str):
        address = int(address, 16) if address.startswith("0x") else int(address)
    last_error = None
    for attempt in range(3):
        conn = None
        try:
            conn = _connect()
            xrefs = conn.root.exposed_get_xrefs_to(address)
            if xrefs:
                # convert the RPyC netrefs to local python dicts
                return [{str(k): (int(v) if isinstance(v, int) else str(v)) for k, v in dict(x).items()} for x in xrefs]
            return []
        except ConnectionRefusedError:
            return [{"error": _get_connection_error_msg()}]
        except TimeoutError:
            return [{"error": "Decompiler request timed out."}]
        except EOFError as e:
            last_error = e
            wait = 2 * (attempt + 1)
            print(f"[get_xrefs_to] EOFError on attempt {attempt+1}, retrying in {wait}s: {e}")
            time.sleep(wait)
        except Exception as e:
            return [{"error": f"Unexpected error: {e}"}]
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
    return [{"error": f"Stream closed after 3 attempts: {last_error}"}]


@tool
def find_address(query: str) -> Union[dict, str]:
    """Finds an address in the binary by symbol name, C-string, or ObjC selector.
    Accepts diff-report kebab-case names, raw symbol names, ObjC method syntax, and plain strings."""
    import re

    original_query = query
    query = re.sub(r'^[-+]\s+', '', query).strip()  # strip diff markers (+/-)
    query = re.sub(r'^"|"$', '', query)              # strip surrounding quotes

    # reject ObjC type encodings (method signature)     
    # eg metadata like B36@0:8@16B24@28, which is not searchable names              
    if re.match(r'^[a-zA-Z@\*\^v]{1,3}\d+[@:^]', query):
        return (
            f"error: '{original_query}' is an ObjC type encoding (method signature), "
            f"not a searchable symbol or string. Skip this query."
        )

    # classify query format and extract canonical token            
    is_objc_selector = False
    canonical = query

    if query.startswith("-[") or query.startswith("+["):
        m = re.search(r'\[.*? ([^\]]+)\]', query)
        if m:
            canonical = m.group(1)
            is_objc_selector = True

    elif "_block_invoke" in query and "-[" in query:
        m = re.search(r'\[.*? ([^\]]+)\]', query)
        if m:
            canonical = m.group(1)
            is_objc_selector = True

    elif query.startswith("_objc_msgSend$"):
        canonical = query.replace("_objc_msgSend$", "")
        is_objc_selector = True

    elif ":" in query:
        is_objc_selector = True

    def _kebab_to_camel(s: str) -> str:
        parts = s.replace("_", "-").split("-")
        return parts[0] + "".join(p.title() for p in parts[1:]) if len(parts) > 1 else s

    def _kebab_to_snake(s: str) -> str:
        return s.replace("-", "_")

    symbol_variants: list[str] = []
    string_variants: list[str] = []

    if is_objc_selector:
        # try with and without leading _ 
        base = canonical.lstrip("_")
        string_variants = list(dict.fromkeys([
            base,
            canonical,
            _kebab_to_camel(base),          
        ]))
        symbol_variants = list(dict.fromkeys([
            query,                          # e.g., _objc_msgSend$isFinished
            canonical,                      # e.g., isFinished
            "_objc_msgSend$" + base,
        ]))
    else:
        base = canonical
        snake = _kebab_to_snake(base)
        camel = _kebab_to_camel(base)

        symbol_variants = list(dict.fromkeys([
            base, "_" + base,
            snake, "_" + snake,
            camel, "_" + camel,
            "_OBJC_CLASS_$_" + base,
            "_OBJC_METACLASS_$_" + base,
        ]))
        string_variants = list(dict.fromkeys([base, snake, camel]))

        # handles diff-report slugs that never exist as a combined symbol
        if "-" in base:
            parts = base.split("-", 1)  # split on FIRST hyphen: [ClassName, method-name]
            class_part = parts[0]
            method_kebab = parts[1] if len(parts) > 1 else ""
            method_camel = _kebab_to_camel(method_kebab)
            method_snake = _kebab_to_snake(method_kebab)
            for extra in [class_part, method_camel, "_" + method_camel,
                          method_snake, "_" + method_snake]:
                if extra and extra not in symbol_variants:
                    symbol_variants.append(extra)

    # try every variant against both lookups, with retry on EOF   

    # for ObjC selectors, use the text before the first ':' as the IDA
    # selector stem, e.g. sel_shouldAcceptGroupMessagePayloadWithExistingChat
    objc_stem = None
    if is_objc_selector and ":" in canonical.lstrip("_"):
        objc_stem = canonical.lstrip("_").split(":")[0]

    last_error = None
    for attempt in range(3):
        conn = None
        try:
            conn = _connect()

            # part a - Exact symbol lookup for each variant (non-ObjC only)
            if symbol_variants:
                for variant in symbol_variants:
                    addr = conn.root.exposed_lookup_symbol(variant)
                    if addr and addr != 0:
                        # determine if this is a function or data
                        is_func = False
                        func_start = addr
                        try:
                            boundaries = conn.root.exposed_get_function_boundaries(addr)
                            if boundaries and boundaries[0] != 0:
                                is_func = True
                                func_start = boundaries[0]
                        except Exception:
                            pass
                        
                        seg_name = ""
                        try:
                            seg_name = conn.root.exposed_get_segment_name(addr)
                        except Exception:
                            pass

                        if is_func and seg_name != "__stubs":
                            return {
                                "type": "symbol",
                                "query": variant,
                                "original": original_query,
                                "address": hex(int(func_start)),
                                "segment": seg_name,
                            }
                        else:
                            return {
                                "type": "data_symbol",
                                "query": variant,
                                "original": original_query,
                                "address": hex(int(addr)),
                                "segment": seg_name,
                            }

            # part b - String search for each variant (covers __cstring + __objc_methname)
            for variant in string_variants:
                addresses = conn.root.exposed_search_string(variant)
                if addresses:
                    return {
                        "type": "string_data",
                        "query": variant,
                        "original": original_query,
                        "addresses": [hex(int(a)) for a in addresses],
                    }

            # part c - Fuzzy fallback via Names() (both symbols + ObjC selectors)
            fuzzy_token = objc_stem if objc_stem else _kebab_to_snake(canonical).replace("_", "")
            fuzzy_results = conn.root.exposed_lookup_symbol_fuzzy(fuzzy_token)
            if fuzzy_results:
                best = fuzzy_results[0]
                best_addr = best["address"]
                is_func = False
                func_start = best_addr
                try:
                    boundaries = conn.root.exposed_get_function_boundaries(best_addr)
                    if boundaries and boundaries[0] != 0:
                        is_func = True
                        func_start = boundaries[0]
                except Exception:
                    pass
                
                seg_name = ""
                try:
                    seg_name = conn.root.exposed_get_segment_name(best_addr)
                except Exception:
                    pass

                if is_func and seg_name != "__stubs":
                    return {
                        "type": "symbol_fuzzy",
                        "query": best["name"],
                        "original": original_query,
                        "address": hex(int(func_start)),
                        "segment": seg_name,
                        "all_matches": [
                            {"name": r["name"], "address": hex(int(r["address"]))}
                            for r in fuzzy_results
                        ],
                    }
                else:
                    return {
                        "type": "data_symbol_fuzzy",
                        "query": best["name"],
                        "original": original_query,
                        "address": hex(int(best_addr)),
                        "segment": seg_name,
                        "all_matches": [
                            {"name": r["name"], "address": hex(int(r["address"]))}
                            for r in fuzzy_results
                        ],
                    }



            return (
                f"error: Could not find '{canonical}' (from '{original_query}') "
                f"as symbol, string, or fuzzy name match."
            )


        except ConnectionRefusedError:
            return _get_connection_error_msg()
        except TimeoutError:
            return "error: Decompiler request timed out"
        except EOFError as e:
            last_error = e
            wait = 3 * (attempt + 1)
            print(f"[find_address] EOFError on attempt {attempt+1}, retrying in {wait}s: {e}")
            time.sleep(wait)
        except Exception as e:
            return f"error: {e}"
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    return f"error: Decompiler connection closed after 3 attempts: {last_error}"



@tool
def rename_local_variable(func_address: int, old_name: str, new_name: str) -> bool:
    """Renames a local variable within a function's decompilation"""
    for attempt in range(3):
        conn = None
        try:
            conn = _connect()
            result = conn.root.exposed_rename_local_variable(func_address, old_name, new_name)
            return result
        except ConnectionRefusedError:
            return False
        except EOFError as e:
            wait = 2 * (attempt + 1)
            print(f"[rename_local_variable] EOFError on attempt {attempt+1}, retrying in {wait}s: {e}")
            time.sleep(wait)
        except Exception:
            return False
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
    return False

@tool
def get_local_variables(func_address: int) -> str:
    """Returns the local variable names available in a function's decompilation"""
    last_error = None
    for attempt in range(3):
        conn = None
        try:
            conn = _connect()
            names = conn.root.exposed_get_local_variables(func_address)
            if names:
                return "Available variables: " + ", ".join(str(n) for n in names)
            return "No local variables found (function may not be decompilable)."
        except ConnectionRefusedError:
            return _get_connection_error_msg()
        except EOFError as e:
            last_error = e
            wait = 2 * (attempt + 1)
            print(f"[get_local_variables] EOFError on attempt {attempt+1}, retrying in {wait}s: {e}")
            time.sleep(wait)
        except Exception as e:
            return f"error: {e}"
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
    return f"error: stream closed after 3 attempts: {last_error}"


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

    import subprocess
    import socket

    # force kill any lingering ida64/idat processes just in case
    subprocess.run(["pkill", "-9", "-f", "idat"], capture_output=True)
    subprocess.run(["pkill", "-9", "-f", "ida64"], capture_output=True)
    
    # clean up only the unpacked working files (.id0/.id1/.id2/.nam/.til) left
    # by a previous aborted run
    # preserve any existing .i64 so annotations are
    # reloaded by IDA on the next open (drop -c to let IDA reuse it)
    has_saved_db = os.path.exists(binary_path + ".i64")
    for ext in [".id0", ".id1", ".id2", ".nam", ".til"]:
        try:
            db_file = binary_path + ext
            if os.path.exists(db_file):
                os.remove(db_file)
        except Exception:
            pass

    # wait for the port to be fully released
    for _ in range(60):  
        try:
            with socket.create_connection((DECOMPILER_HOST, DECOMPILER_PORT), timeout=1):
                time.sleep(1)
        except (ConnectionRefusedError, socket.timeout, OSError):
            break
    else:
        return "# ERROR: Port 18861 is still in use after attempting to kill old IDA instances."

    # launch IDA in the background
    # if a saved .i64 exists, omit -c so IDA reloads it (preserving annotations)
    # if no .i64 exists, keep -c so IDA creates a fresh database
    command = [
        IDA_EXECUTABLE_PATH,
        "-A",
        "-L/tmp/ida.log",
        f"-S{IDA_RPC_SERVER_SCRIPT}",
        binary_path,
    ]
    if not has_saved_db:
        command.insert(2, "-c")  # fresh DB only when no saved .i64 exists
    try:
        log_file = open("/tmp/ida_rpc_server.log", "w")
        subprocess.Popen(command, stdout=log_file, stderr=log_file, stdin=subprocess.DEVNULL, env=os.environ.copy())
    except Exception as e:
        return f"# ERROR: Failed to start IDA Pro: {e}"

    for _ in range(300):  # wait up to 10 minutes
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
        with socket.create_connection((DECOMPILER_HOST, DECOMPILER_PORT), timeout=2):
            pass
        with rpyc.connect(DECOMPILER_HOST, DECOMPILER_PORT, config={"sync_request_timeout": 5}) as conn:
            conn.root.exposed_shutdown()
    except Exception as e:
        msg = f"Shutdown failed or connection terminated: {e}"
        
    # kill lingering idat processes 
    try:
        subprocess.run(["pkill", "-9", "-f", "idat"], capture_output=True)
    except Exception:
        pass

    return msg


@tool
def set_comment(address: int, comment: str) -> bool:
    """Sets a comment at a specific address in the disassembly"""
    for attempt in range(3):
        conn = None
        try:
            conn = _connect()
            result = conn.root.exposed_set_comment(address, comment)
            return result
        except ConnectionRefusedError:
            return False
        except EOFError as e:
            wait = 2 * (attempt + 1)
            print(f"[set_comment] EOFError on attempt {attempt+1}, retrying in {wait}s: {e}")
            time.sleep(wait)
        except Exception:
            return False
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
    return False


@tool
def save_ida_database() -> str:
    """Saves the current IDA Pro database (.i64) with any annotations made"""
    last_error = None
    for attempt in range(3):
        conn = None
        try:
            conn = _connect()
            success = conn.root.exposed_save_ida_database("")
            return "Successfully saved IDA database." if success else "Failed to save IDA database."
        except ConnectionRefusedError:
            return _get_connection_error_msg()
        except TimeoutError:
            return "Error: Request timed out."
        except EOFError as e:
            last_error = e
            wait = 2 * (attempt + 1)
            print(f"[save_ida_database] EOFError on attempt {attempt+1}, retrying in {wait}s: {e}")
            time.sleep(wait)
        except Exception as e:
            return f"Error saving database: {e}"
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
    return f"Error saving database: stream closed after 3 attempts: {last_error}"


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
        return _get_connection_error_msg()
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
        return _get_connection_error_msg()
    except TimeoutError:
        return "Error: Request timed out."
    except Exception as e:
        return f"Error: {e}"
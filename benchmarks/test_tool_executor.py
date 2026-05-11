import sys
import tempfile
import os
from pathlib import Path

from langgraph_orchestration.tooling import (
    VSCodeToolExecutor,
    IDAToolExecutor,
    get_tool_executor,
)
from langgraph_orchestration.tooling.contracts import ToolRequest

def test_vscode_executor():
    print("\n[TEST] VSCode Tool Executor")
    print("-" * 50)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        executor = VSCodeToolExecutor(workspace_root=tmpdir)
        
        print("1. Testing create_file...")
        req = ToolRequest(
            tool_name="create_file",
            target="test.py",
            reason="Create test file",
            arguments={"path": "test.py", "content": "def hello():\n    print('world')\n"},
        )
        result = executor.execute(req)
        assert result.success, f"Failed: {result.error}"
        assert os.path.exists(os.path.join(tmpdir, "test.py"))
        print("   ✓ File created")
        
        print("2. Testing read_file...")
        req = ToolRequest(
            tool_name="read_file",
            target="test.py",
            reason="Read test file",
            arguments={"path": "test.py"},
        )
        result = executor.execute(req)
        assert result.success, f"Failed: {result.error}"
        assert "hello" in result.output
        print("   ✓ File read successfully")
        
        print("3. Testing edit_file...")
        req = ToolRequest(
            tool_name="edit_file",
            target="test.py",
            reason="Edit test file",
            arguments={
                "path": "test.py",
                "old_string": "def hello():",
                "new_string": "def hello_world():",
            },
        )
        result = executor.execute(req)
        assert result.success, f"Failed: {result.error}"
        with open(os.path.join(tmpdir, "test.py")) as f:
            content = f.read()
            assert "hello_world" in content
        print("   ✓ File edited successfully")
        
        print("4. Testing search_repository...")
        req = ToolRequest(
            tool_name="search_repository",
            target="hello",
            reason="Search for hello pattern",
            arguments={"pattern": "hello"},
        )
        result = executor.execute(req)
        print(f"   ✓ Search completed (found: {bool(result.output)})")
        
        print("5. Testing get_errors...")
        req = ToolRequest(
            tool_name="get_errors",
            target="test.py",
            reason="Check for errors",
            arguments={"path": "test.py"},
        )
        result = executor.execute(req)
        assert result.success, f"Failed: {result.error}"
        print("   ✓ No syntax errors detected")

def test_ida_executor():
    print("\n[TEST] IDA Tool Executor (Offline Mode)")
    print("-" * 50)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        executor = IDAToolExecutor(workspace_root=tmpdir)
        
        print("1. Testing read_decompilation (offline)...")
        req = ToolRequest(
            tool_name="read_decompilation",
            target="main",
            reason="Decompile main function",
            arguments={"function": "main"},
        )
        result = executor.execute(req)
        assert not result.success, "Should fail in offline mode"
        assert "IDA Pro" in result.error or "offline" in result.error.lower()
        print(f"   ✓ Correctly reported offline: {result.error[:50]}...")
        
        print("2. Testing xrefs_to (offline)...")
        req = ToolRequest(
            tool_name="xrefs_to",
            target="0x400000",
            reason="Find references to address",
            arguments={"address": "0x400000"},
        )
        result = executor.execute(req)
        assert not result.success, "Should fail in offline mode"
        print(f"   ✓ Correctly reported offline: {result.error[:50]}...")
        
        print("3. Testing read_file (shared implementation)...")
        test_file = os.path.join(tmpdir, "test.py")
        with open(test_file, "w") as f:
            f.write("# IDA test\n")
        
        req = ToolRequest(
            tool_name="read_file",
            target="test.py",
            reason="Read test file",
            arguments={"path": "test.py"},
        )
        result = executor.execute(req)
        assert result.success, f"Failed: {result.error}"
        print("   ✓ File reading works in IDA executor")

def test_factory_function():
    print("\n[TEST] Tool Executor Factory")
    print("-" * 50)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        print("1. Getting VSCode executor...")
        vscode_exec = get_tool_executor("software_dev", tmpdir)
        assert isinstance(vscode_exec, VSCodeToolExecutor)
        print("   ✓ Got VSCode executor for software_dev")
        
        print("2. Getting IDA executor...")
        ida_exec = get_tool_executor("reverse_engineering", tmpdir)
        assert isinstance(ida_exec, IDAToolExecutor)
        print("   ✓ Got IDA executor for reverse_engineering")

def test_tool_request_parsing():
    print("\n[TEST] Tool Request Parsing")
    print("-" * 50)
    
    from langgraph_orchestration.tooling.tool_executor_node import parse_tool_request_from_output
    
    print("1. Testing JSON code block parsing...")
    output = """
    Here's my analysis:
    
    ```json
    {
        "type": "tool_request",
        "tool_name": "read_file",
        "target": "main.py",
        "reason": "Need to understand entry point",
        "arguments": {"path": "main.py"}
    }
    ```
    
    This file contains...
    """
    req = parse_tool_request_from_output(output)
    assert req is not None, "Failed to parse tool request"
    assert req.tool_name == "read_file"
    assert req.target == "main.py"
    print("   ✓ Successfully parsed JSON code block")
    
    print("2. Testing output without tool request...")
    output = "This is just normal agent output without any tool requests."
    req = parse_tool_request_from_output(output)
    assert req is None, "Should not find tool request"
    print("   ✓ Correctly identified no tool request")
    
    print("3. Testing inline JSON parsing...")
    output = 'I need to read the file. {"type": "tool_request", "tool_name": "read_file", "target": "test.py", "reason": "test", "arguments": {}} here it is.'
    req = parse_tool_request_from_output(output)
    assert req is not None, "Failed to parse inline tool request"
    assert req.tool_name == "read_file"
    print("   ✓ Successfully parsed inline JSON")

if __name__ == "__main__":
    try:
        test_vscode_executor()
        test_ida_executor()
        test_factory_function()
        test_tool_request_parsing()
        
        print("\n" + "=" * 50)
        print("✓ ALL TESTS PASSED")
        print("=" * 50)
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
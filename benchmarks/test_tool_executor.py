import sys
import tempfile
import os
from pathlib import Path

from langgraph_orchestration.tooling import (
    VSCodeToolExecutor,
    IDAToolExecutor,
    get_tool_executor,
)
from langgraph_orchestration.tooling.tool import ToolRequest

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
    from langgraph_orchestration.tooling import parse_agent_output

    print("1. Testing structured tool_call parsing...")
    output = """
    Here's my analysis:

    <tool_call>
    {
        "tool_name": "read_file",
        "target": "main.py",
        "reason": "Need to understand entry point",
        "arguments": {"path": "main.py"}
    }
    </tool_call>

    This file contains...
    """
    parsed = parse_agent_output(output)
    assert parsed.tool_calls, "Failed to parse tool call"
    tool_call = parsed.tool_calls[0]
    assert tool_call.tool_name == "read_file"
    assert tool_call.target == "main.py"
    print("   ✓ Successfully parsed tool_call envelope")

    # Test 2: No tool request
    print("2. Testing output without tool request...")
    output = "This is just normal agent output without any tool requests."
    parsed = parse_agent_output(output)
    assert not parsed.tool_calls, "Should not find tool call"
    print("   ✓ Correctly identified no tool call")

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
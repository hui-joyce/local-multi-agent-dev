from langgraph_orchestration.graphs.reverse_engineering import (
    _collapse_repeats,
    _inject_real_decompilation,
    _sanitize_code_blocks,
    _sanitize_model_output,
)


class _ToolRes:
    def __init__(self, tool_name, success, output, decompile_address):
        self.tool_name = tool_name
        self.success = success
        self.output = output
        self.metadata = {"decompile_address": decompile_address}

class TestCollapseRepeats:
    def test_caps_runs_of_identical_lines(self):
        assert _collapse_repeats("a\na\na\na\na\nb") == "a\na\na\nb"

    def test_distinct_lines_untouched(self):
        text = "a\nb\nc\nd"
        assert _collapse_repeats(text) == text

    def test_blank_lines_do_not_count_as_repeats(self):
        assert _collapse_repeats("\n\n\n\n") == "\n\n\n\n"

class TestSanitizeCodeBlocks:
    def test_unbalanced_fence_is_closed(self):
        out = _sanitize_code_blocks("```c\nint x;\n")
        assert out.count("```") % 2 == 0

    def test_degenerate_block_is_removed(self):
        text = "```c\n" + ("void *v;\n" * 24) + "```"
        out = _sanitize_code_blocks(text)
        assert "removed" in out
        assert "void *" not in out

    def test_oversized_block_is_capped(self):
        body = "".join(f"L{i:04d}" + "x" * 90 + "\n" for i in range(100))  # ~9.5k chars
        out = _sanitize_code_blocks("```c\n" + body + "```")
        assert "truncated" in out
        assert len(out) < len("```c\n" + body + "```")

    def test_single_runaway_line_is_capped(self):
        out = _sanitize_code_blocks("```c\n" + "z" * 3000 + "\n```")
        assert "z" * 3000 not in out
        assert "z" * 2000 in out

    def test_prose_outside_fences_is_preserved(self):
        text = "before\n```c\nint x;\n```\nafter"
        out = _sanitize_code_blocks(text)
        assert "before" in out and "after" in out

class TestSanitizeModelOutput:
    def test_non_string_is_coerced(self):
        assert _sanitize_model_output(123) == "123"

    def test_whitespace_is_stripped(self):
        assert _sanitize_model_output("  ## Heading\n") == "## Heading"

class TestInjectRealDecompilation:
    SECTION = "## What this feature does\nsummary\n\n## How is it implemented\nprose\n"

    def test_injects_auto_decompilation_block(self):
        out = _inject_real_decompilation(
            self.SECTION, tool_results=[], auto_decomps=[{"address": "0x1", "code": "int f(){}"}]
        )
        assert "Decompilation at `0x1`" in out
        assert "int f(){}" in out

    def test_dedupes_by_address(self):
        decomps = [{"address": "0x1", "code": "A"}, {"address": "0x1", "code": "B"}]
        out = _inject_real_decompilation(self.SECTION, tool_results=[], auto_decomps=decomps)
        assert out.count("Decompilation at `0x1`") == 1

    def test_injects_decompilation_from_model_tool_results(self):
        tr = [_ToolRes("decompile_function", True, "int g(void){return 2;}", "0x2")]
        out = _inject_real_decompilation(self.SECTION, tool_results=tr, auto_decomps=[])
        assert "Decompilation at `0x2`" in out
        assert "int g(void){return 2;}" in out

    def test_notes_when_no_decompilation_available(self):
        out = _inject_real_decompilation(self.SECTION, tool_results=[], auto_decomps=[])
        assert "No decompilation was captured" in out

    def test_discards_model_authored_code_fences(self):
        section = "## How is it implemented\nprose ```c\nFAKE_HANDWRITTEN\n``` more\n"
        out = _inject_real_decompilation(section, tool_results=[], auto_decomps=[])
        assert "FAKE_HANDWRITTEN" not in out

    def test_returns_unchanged_when_section_absent(self):
        md = "## What this feature does\nonly a summary here\n"
        assert _inject_real_decompilation(md, tool_results=[], auto_decomps=[]) == md

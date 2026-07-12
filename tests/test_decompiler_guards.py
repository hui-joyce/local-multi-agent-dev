from langgraph_orchestration.graphs.reverse_engineering import _usable_decompilation
from langgraph_orchestration.tooling.decompiler_tools import _is_degenerate_decompilation


class TestIsDegenerateDecompilation:
    def test_empty_or_none_is_not_degenerate(self):
        assert _is_degenerate_decompilation("") is False
        assert _is_degenerate_decompilation(None) is False

    def test_error_sentinel_is_not_degenerate(self):
        assert _is_degenerate_decompilation("# ERROR: could not decompile") is False

    def test_normal_code_is_not_degenerate(self):
        assert _is_degenerate_decompilation("int main() { return 0; }") is False

    def test_runaway_void_star_flood_is_degenerate(self):
        flood = "void *x;\n" * 24
        assert _is_degenerate_decompilation(flood) is True

    def test_swift_dispatch_thunk_is_degenerate(self):
        assert _is_degenerate_decompilation("__swiftcall1(void *a, void *b)") is True

    def test_fastcall_thunk_is_degenerate(self):
        assert _is_degenerate_decompilation("__fastcall12(  void *self)") is True

class TestUsableDecompilation:
    def test_real_code_is_usable(self):
        assert _usable_decompilation("int f(void) { return 1; }") is True

    def test_none_and_empty_and_whitespace_are_unusable(self):
        assert _usable_decompilation(None) is False
        assert _usable_decompilation("") is False
        assert _usable_decompilation("   \n  ") is False

    def test_error_sentinel_is_unusable(self):
        assert _usable_decompilation("# ERROR: degenerate thunk") is False

    def test_non_string_is_unusable(self):
        assert _usable_decompilation(123) is False

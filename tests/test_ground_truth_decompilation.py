from langgraph_orchestration.prompts.reverse_engineering import (
    _format_ground_truth_decompilation,
)


class TestFormatGroundTruthDecompilation:
    def test_empty_input_returns_empty_string(self):
        assert _format_ground_truth_decompilation(None) == ""
        assert _format_ground_truth_decompilation([]) == ""

    def test_renders_verified_block_with_symbol_and_code(self):
        out = _format_ground_truth_decompilation(
            [{
                "symbol": "-[Auth verify:]",
                "address": "0x10",
                "code": "int verify(void){return 1;}",
            }]
        )
        assert "Verified Decompilation" in out
        assert "-[Auth verify:]" in out
        assert "0x10" in out
        assert "int verify(void){return 1;}" in out

    def test_skips_entries_without_code(self):
        entries = [{"symbol": "x", "address": "0x1", "code": ""}]
        assert _format_ground_truth_decompilation(entries) == ""

    def test_truncates_long_code_to_per_cap(self):
        out = _format_ground_truth_decompilation(
            [{"symbol": "big", "address": "0x1", "code": "q" * 5000}], per_cap=100
        )
        assert "q" * 5000 not in out
        assert "q" * 100 in out

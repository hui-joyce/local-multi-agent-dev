from langgraph_orchestration.graphs.reverse_engineering import _build_readme_diff_index

README = """\
# Firmware diff

#### AlphaKit
> summary line
```diff
+ added_symbol
- removed_symbol
```

#### BetaKit
> beta note

## Unrelated trailing section
should not be attributed to BetaKit
"""

class TestBuildReadmeDiffIndex:
    def test_indexes_each_component_section(self):
        idx = _build_readme_diff_index(README.splitlines())
        assert set(idx) == {"AlphaKit", "BetaKit"}

    def test_captures_diff_code_block(self):
        idx = _build_readme_diff_index(README.splitlines())
        assert "+ added_symbol" in idx["AlphaKit"]
        assert "- removed_symbol" in idx["AlphaKit"]

    def test_section_stops_at_next_heading(self):
        idx = _build_readme_diff_index(README.splitlines())
        assert "should not be attributed" not in idx["BetaKit"]

    def test_first_occurrence_wins(self):
        text = "#### Dup\n> first\n#### Dup\n> second\n"
        idx = _build_readme_diff_index(text.splitlines())
        assert "first" in idx["Dup"]
        assert "second" not in idx["Dup"]

    def test_respects_max_lines_cap(self):
        big = ["#### Huge"] + [f"> line {i}" for i in range(50)]
        idx = _build_readme_diff_index(big, max_lines=10)
        assert "... (truncated)" in idx["Huge"]
        # capped below 50 available lines
        assert idx["Huge"].count("\n") <= 11

    def test_missing_component_absent(self):
        idx = _build_readme_diff_index(README.splitlines())
        assert "GammaKit" not in idx

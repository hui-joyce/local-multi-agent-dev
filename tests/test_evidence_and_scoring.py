from langgraph_orchestration.graphs.reverse_engineering import (
    _component_change_volume,
    _evidence_sections,
    _extract_security_indicators,
    _security_score,
    _truncate_for_prompt,
)

EVIDENCE = """\
CStrings:
+ "hello world"
- "goodbye"
  unchanged context line
Symbols:
+ _authenticateUser
  context
- _oldHelper
"""

class TestEvidenceSections:
    def test_splits_cstrings_and_symbols_keeping_only_diff_lines(self):
        cstrings, symbols = _evidence_sections(EVIDENCE)
        assert cstrings == ['+ "hello world"', '- "goodbye"']
        assert symbols == ["+ _authenticateUser", "- _oldHelper"]

    def test_empty_evidence_is_empty(self):
        assert _evidence_sections("") == ([], [])
        assert _evidence_sections(None) == ([], [])

    def test_change_volume_counts_all_diff_lines(self):
        assert _component_change_volume(EVIDENCE) == 4

class TestSecurityIndicators:
    def test_detects_heap_and_entitlement_patterns(self):
        # patterns are word-bounded, so 'malloc' must appear as its own token
        ev = "Symbols:\n+ p = malloc(0x20)\n+ valueForEntitlement:\n"
        found = _extract_security_indicators(ev)
        assert "heap allocation" in found
        assert "entitlement check" in found

    def test_ignores_context_lines_without_diff_markers(self):
        # 'malloc' present but not on a +/- line = not an indicator
        assert _extract_security_indicators("  malloc(0x10)") == []

    def test_labels_are_deduplicated(self):
        ev = "Symbols:\n+ malloc(a)\n+ free(a)\n"  # both map to 'heap allocation'
        assert _extract_security_indicators(ev).count("heap allocation") == 1

class TestSecurityScore:
    def test_security_notes_match_is_top_score(self):
        assert _security_score({"security_notes_match": "CVE-2026-1"}) == 4

    def test_hard_indicator_scores_three(self):
        assert _security_score({"security_indicators": ["heap allocation"]}) == 3

    def test_security_vocabulary_scores_two(self):
        # 'crypt' inside 'decrypt' matches the security vocabulary
        assert _security_score({"evidence": "Symbols:\n+ _decryptPayload"}) == 2

    def test_symbol_churn_without_signal_scores_one(self):
        assert _security_score({"evidence": "Symbols:\n+ _drawRectInContext"}) == 1

    def test_no_code_change_scores_zero(self):
        assert _security_score({"evidence": 'CStrings:\n+ "Loading…"'}) == 0

class TestTruncateForPrompt:
    def test_short_text_is_unchanged(self):
        assert _truncate_for_prompt("abc", 10, "evidence") == "abc"

    def test_long_text_is_truncated_with_marker(self):
        out = _truncate_for_prompt("x" * 100, 10, "evidence")
        assert out.startswith("x" * 10)
        assert "truncated" in out
        assert "evidence" in out

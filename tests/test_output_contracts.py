import json

from ipsw_service.firmware_diff_service import FirmwareDiffService
from langgraph_orchestration.core import sanitize_agent_output
from langgraph_orchestration.graphs.reverse_engineering import (
    _COMPONENT_SECTIONS,
    _build_feature_targets,
)


def test_feature_target_reader_matches_the_report_writer():
    written = set(
        FirmwareDiffService._build_report_payload(
            FirmwareDiffService.__new__(FirmwareDiffService),
            diff_data={},
            cstring_count=0,
            gaps=[],
            notes=[],
            security_findings=[],
        )
    )
    expected = {key for key, _ in _COMPONENT_SECTIONS}
    assert expected <= written, (
        f"_build_feature_targets reads {sorted(expected - written)}, which "
        "FirmwareDiffService._build_report_payload does not write."
    )


def test_feature_targets_pick_up_paths_and_evidence():
    report = json.dumps(
        {
            "userland_changes": {"frameworks": ["/System/Library/Frameworks/Foo.framework/Foo"]},
            "cstring_context": ['Foo: + "new_string"'],
        }
    )
    (target,) = _build_feature_targets(report)
    assert target["name"] == "Foo"
    assert target["binary_path"] == "/System/Library/Frameworks/Foo.framework/Foo"
    assert "new_string" in target["evidence"]


def test_firmware_blobs_never_get_a_decompiler_target():
    """.im4p blobs and bundle IDs must reach triage but never the decompiler"""
    report = json.dumps({"base_firmware_changes": ["com.apple.driver.AppleFirmwareKit"]})
    (target,) = _build_feature_targets(report)
    assert "binary_path" not in target


def test_sanitizer_keeps_code_using_reserved_words():
    """Regression test for a sanitizer that removed lines containing 'tool', 'trace', or 'metrics'."""
    code = "def f():\n    metrics = compute()\n    trace = build()\n    return metrics, trace"
    assert sanitize_agent_output(code) == code


def test_sanitizer_keeps_the_tool_call_envelope():
    """Stripping these tags broke tool parsing for every software-dev agent"""
    text = '<tool_call>\n{"tool_name": "read_file"}\n</tool_call>'
    result = sanitize_agent_output(text)
    assert "<tool_call>" in result and "</tool_call>" in result


def test_sanitizer_still_removes_reasoning():
    assert sanitize_agent_output("<think>plan</think>answer") == "answer"

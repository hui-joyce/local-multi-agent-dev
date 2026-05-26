from __future__ import annotations

from dataclasses import asdict
from typing import Iterable
import json
import os

from ipsw_service.utils import read_text

from ipsw_service.models import FirmwareDiffResult, Finding

def _format_evidence_lines(finding: Finding) -> list[str]:
    lines: list[str] = []
    for item in finding.evidence:
        detail = f" ({item.details})" if item.details else ""
        lines.append(f"- {item.source}: {item.summary}{detail}")
    return lines or ["- Evidence pending from ipsw diff artifacts."]

def render_report(result: FirmwareDiffResult) -> str:
    summary = result.summary
    counts = summary.counts

    lines: list[str] = []
    lines.append("# Executive Summary")
    lines.append(f"- firmware versions compared: {summary.old_firmware} vs {summary.new_firmware}")
    lines.append(f"- extraction success status: {summary.extraction_status}")
    lines.append(
        "- total binaries added/removed/modified: "
        f"{counts.added_binaries}/{counts.removed_binaries}/{counts.modified_binaries}"
    )
    lines.append(f"- high-fmrisk changes detected: {summary.high_risk_changes}")
    lines.append("")

    lines.append("# Critical Findings")

    for index, finding in enumerate(result.findings, start=1):
        change_type = f"Potentially Security-Relevant Change ({finding.change_type or 'unspecified'})"
        lines.append(f"## Finding {index}: {finding.title}")
        binary_hint = "unknown"
        for item in finding.evidence:
            if "/" in item.summary:
                binary_hint = item.summary
                break
        lines.append(f"- Binary path and architecture: {binary_hint}")
        lines.append(f"- Change type: {change_type}")
        lines.append(f"- Potential impact: {finding.impact or 'Potentially security-relevant change.'}")
        lines.append(f"- Recommended mitigation steps: {finding.mitigation or 'Review and validate with additional analysis.'}")
        lines.append("- Evidence (symbols, paths, artifacts):")
        lines.extend(_format_evidence_lines(finding))
        lines.append("")

    lines.append("# Recommendations")
    lines.append("- Monitor newly added binaries and services in privileged paths for behavior changes.")
    lines.append("- Prioritize reverse engineering of entitlements and sandbox deltas flagged as high-risk.")
    lines.append("- Validate launchd/service diffs against expected platform changes and patch notes.")
    lines.append("")

    kernel_status = "available" if (result.artifacts.kernel_diff or result.artifacts.kext_diff) else "missing"
    dyld_status = "available" if result.artifacts.dyld_diff else "missing"
    lines.append("# Technical Details")
    lines.append(f"- kernelcache extraction summary: {kernel_status}")
    lines.append(f"- dyld_shared_cache extraction summary: {dyld_status}")
    lines.append("- filesystem extraction status: not executed (see diff artifacts)")
    lines.append(
        "- binary inventory counts: "
        f"added={counts.added_binaries}, removed={counts.removed_binaries}, modified={counts.modified_binaries}"
    )
    lines.append(f"- entitlement diff summary: {counts.entitlement_changes} changes")
    lines.append(f"- sandbox diff summary: {counts.sandbox_changes} changes")
    lines.append(f"- KEXT diff summary: {counts.kext_changes} changes")
    lines.append(f"- launchd/service diff summary: {counts.launchd_changes} changes")
    lines.append(f"- dyld diff summary: {counts.dyld_changes} changes")
    cstring_changes: list[str] = []
    metadata_path = result.artifacts.symbol_metadata or ""
    if metadata_path and os.path.isfile(metadata_path):
        try:
            data = json.loads(read_text(metadata_path))
            cstring_changes = data.get("cstring_changes", []) or []
        except Exception:
            cstring_changes = []

    lines.append(f"- cstring diff summary: {len(cstring_changes)} changes")
    if cstring_changes:
        lines.append("- cstring deltas:")
        for entry in cstring_changes[:20]:
            lines.append(f"  - {entry}")
        if len(cstring_changes) > 20:
            lines.append(f"  - ... {len(cstring_changes) - 20} more")
    lines.append(
        "- firmware component summary: "
        f"added={counts.firmware_added}, removed={counts.firmware_removed}, modified={counts.firmware_modified}"
    )
    lines.append(
        "- iBoot component summary: "
        f"added={counts.iboot_added}, removed={counts.iboot_removed}, modified={counts.iboot_modified}"
    )
    if result.notes:
        lines.append("- firmware highlights:")
        for note in result.notes:
            lines.append(f"  - {note}")
    lines.append("- evidence sources:")
    lines.append(f"  - report artifacts: {result.artifacts.report_markdown}")
    if result.gaps:
        lines.append("- unresolved gaps or blockers:")
        for gap in result.gaps:
            lines.append(f"  - {gap}")

    return "\n".join(lines).strip() + "\n"
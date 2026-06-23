from __future__ import annotations

from typing import Optional

def _section_heading(level: int, title: str) -> str:
    return f"{'#' * level} {title}"

def _emit_list(lines: list[str], items: list[str], indent: str = "") -> None:
    for item in items:
        lines.append(f"{indent}- {item}")

def render_report(
    report_payload: dict[str, object],
    notes: Optional[list[str]] = None,
    gaps: Optional[list[str]] = None,
) -> str:
    summary_metrics: dict = report_payload.get("summary_metrics", {}) or {}
    boundary_changes: dict = report_payload.get("boundary_changes", {}) or {}
    userland_changes: dict = report_payload.get("userland_changes", {}) or {}
    base_firmware_changes: list = report_payload.get("base_firmware_changes", []) or []
    cstring_context: list = report_payload.get("cstring_context", []) or []

    lines: list[str] = []

    # Summary Metrics
    if summary_metrics:
        lines.append(_section_heading(2, "Summary Metrics"))
        lines.append("")
        for k, v in summary_metrics.items():
            lines.append(f"- {k}: {v}")
        lines.append("")

    # Boundary Changes
    if boundary_changes:
        lines.append(_section_heading(2, "Boundary Changes"))
        lines.append("")
        
        entitlements = boundary_changes.get("entitlements", [])
        if entitlements:
            lines.append(_section_heading(3, f"Entitlements ({len(entitlements)})"))
            lines.append("")
            _emit_list(lines, entitlements)
            lines.append("")

        sandbox = boundary_changes.get("sandbox", [])
        if sandbox:
            lines.append(_section_heading(3, f"Sandbox ({len(sandbox)})"))
            lines.append("")
            _emit_list(lines, sandbox)
            lines.append("")

        launchd = boundary_changes.get("launchd", [])
        if launchd:
            lines.append(_section_heading(3, f"Launchd ({len(launchd)})"))
            lines.append("")
            _emit_list(lines, launchd)
            lines.append("")

        kexts = boundary_changes.get("kexts", [])
        if kexts:
            lines.append(_section_heading(3, f"Kexts ({len(kexts)})"))
            lines.append("")
            _emit_list(lines, kexts)
            lines.append("")

    # Userland Changes
    if userland_changes:
        lines.append(_section_heading(2, "Userland Changes"))
        lines.append("")
        
        frameworks = userland_changes.get("frameworks", [])
        if frameworks:
            lines.append(_section_heading(3, f"Frameworks ({len(frameworks)})"))
            lines.append("")
            _emit_list(lines, frameworks)
            lines.append("")

        standard_binaries = userland_changes.get("standard_binaries", [])
        if standard_binaries:
            lines.append(_section_heading(3, f"Standard Binaries ({len(standard_binaries)})"))
            lines.append("")
            _emit_list(lines, standard_binaries)
            lines.append("")

    # Base Firmware Changes
    if base_firmware_changes:
        lines.append(_section_heading(2, "Base Firmware Changes"))
        lines.append("")
        lines.append(_section_heading(3, f"Updated ({len(base_firmware_changes)})"))
        lines.append("")
        _emit_list(lines, base_firmware_changes)
        lines.append("")

    # CString Changes
    if cstring_context:
        lines.append(_section_heading(2, "CString Changes"))
        lines.append("")
        lines.append(f"- total: {len(cstring_context)}")
        _emit_list(lines, cstring_context)
        lines.append("")

    # Notes/Gaps 
    if notes:
        lines.append(_section_heading(2, "Notes"))
        lines.append("")
        _emit_list(lines, notes)
        lines.append("")

    if gaps:
        lines.append(_section_heading(2, "Gaps"))
        lines.append("")
        _emit_list(lines, gaps)
        lines.append("")

    return "\n".join(lines).strip() + "\n"
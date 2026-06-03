from __future__ import annotations

from typing import Optional

def _format_section(title: str, items: list[str]) -> list[str]:
    lines = [f"# {title}"]
    if not items:
        lines.append("- none")
        return lines
    lines.append(f"- total: {len(items)}")
    lines.extend(f"- {item}" for item in items)
    return lines

def render_report(
    report_payload: dict[str, object],
    notes: Optional[list[str]] = None,
    gaps: Optional[list[str]] = None,
) -> str:
    boundary = report_payload.get("boundary_changes", {}) or {}
    userland = report_payload.get("userland_changes", {}) or {}
    base_firmware = report_payload.get("base_firmware_changes", []) or []
    cstring_context = report_payload.get("cstring_context", []) or []

    lines: list[str] = []
    lines.append("# Boundary Changes")
    lines.append(f"- entitlements: {len(boundary.get('entitlements', []) or [])}")
    lines.append(f"- sandbox: {len(boundary.get('sandbox', []) or [])}")
    lines.append(f"- launchd: {len(boundary.get('launchd', []) or [])}")
    lines.append(f"- kexts: {len(boundary.get('kexts', []) or [])}")
    lines.append("")
    lines.extend(_format_section("Entitlements", boundary.get("entitlements", []) or []))
    lines.append("")
    lines.extend(_format_section("Sandbox", boundary.get("sandbox", []) or []))
    lines.append("")
    lines.extend(_format_section("Launchd", boundary.get("launchd", []) or []))
    lines.append("")
    lines.extend(_format_section("Kexts", boundary.get("kexts", []) or []))
    lines.append("")

    lines.append("# Userland Changes")
    lines.append(f"- frameworks: {len(userland.get('frameworks', []) or [])}")
    lines.append(f"- standard binaries: {len(userland.get('standard_binaries', []) or [])}")
    lines.append("")
    lines.extend(_format_section("Frameworks", userland.get("frameworks", []) or []))
    lines.append("")
    lines.extend(_format_section("Standard Binaries", userland.get("standard_binaries", []) or []))
    lines.append("")

    lines.extend(_format_section("Base Firmware Changes", base_firmware))
    lines.append("")
    lines.extend(_format_section("Cstring Context", cstring_context))

    if notes:
        lines.append("")
        lines.append("# Notes")
        lines.extend(f"- {note}" for note in notes)

    if gaps:
        lines.append("")
        lines.append("# Gaps")
        lines.extend(f"- {gap}" for gap in gaps)

    return "\n".join(lines).strip() + "\n"
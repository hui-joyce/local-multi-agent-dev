from __future__ import annotations

import re
from typing import Iterable

def extract_paths_by_keyword(output: str, keyword: str) -> list[str]:
    if not output:
        return []
    pattern = rf"(/[^\s]*{re.escape(keyword)}[^\s]*)"
    return list(dict.fromkeys(re.findall(pattern, output)))

def _parse_markdown_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            current = line[3:].strip()
            sections[current] = []
            continue
        if not current:
            continue
        if line.startswith("- "):
            sections[current].append(line[2:].strip())
    return sections

def _merge_sections(sections: dict[str, list[str]], keywords: Iterable[str]) -> list[str]:
    matched: list[str] = []
    for title, items in sections.items():
        lowered = title.lower()
        if any(keyword in lowered for keyword in keywords):
            matched.extend(items)
    return list(dict.fromkeys(matched))


def parse_diff_markdown(text: str) -> dict[str, list[str]]:
    sections = _parse_markdown_sections(text)

    added_binaries = _merge_sections(sections, ["added", "new"]) 
    removed_binaries = _merge_sections(sections, ["removed", "deleted"]) 
    modified_binaries = _merge_sections(sections, ["modified", "changed", "updated"]) 

    entitlements: list[str] = []
    sandbox: list[str] = []
    kexts: list[str] = []
    frameworks: list[str] = []
    launchd: list[str] = []

    for title, items in sections.items():
        lowered = title.lower()
        if "entitlement" in lowered:
            entitlements.extend(items)
        if "sandbox" in lowered:
            sandbox.extend(items)
        if "kext" in lowered:
            kexts.extend(items)
        if "framework" in lowered:
            frameworks.extend(items)
        if "launchd" in lowered or "service" in lowered:
            launchd.extend(items)

    # Fallback: scan lines for entitlements if sections not provided
    if not entitlements:
        for line in text.splitlines():
            if "com.apple." in line:
                entitlements.append(line.strip())

    return {
        "added_binaries": list(dict.fromkeys(added_binaries)),
        "removed_binaries": list(dict.fromkeys(removed_binaries)),
        "modified_binaries": list(dict.fromkeys(modified_binaries)),
        "entitlement_changes": list(dict.fromkeys(entitlements)),
        "sandbox_changes": list(dict.fromkeys(sandbox)),
        "kext_changes": list(dict.fromkeys(kexts)),
        "framework_changes": list(dict.fromkeys(frameworks)),
        "launchd_changes": list(dict.fromkeys(launchd)),
    }

def parse_simple_list_output(text: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return list(dict.fromkeys(lines))
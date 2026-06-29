from __future__ import annotations

import re
from typing import Iterable

_ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")

_CHANGE_KEYWORDS = {
    "added": ("new", "added", "add"),
    "modified": ("updated", "modified", "changed", "change"),
}
_ALL_CHANGE_KEYWORDS = sum(_CHANGE_KEYWORDS.values(), ())

_GROUP_HEADINGS = {
    "inputs",
    "kernel",
    "version",
    "kexts",
    "macho",
    "mach-o",
    "firmware",
    "iboot",
    "dsc",
    "dylibs",
    "webkit",
    "eof",
}

_ITEM_EXTENSIONS = (
    ".bin",
    ".im4p",
    ".img4",
    ".dylib",
    ".framework",
    ".bundle",
    ".kext",
    ".metallib",
    ".g18p",
)

# matches a bare com.apple.* entitlement token
_ENTITLEMENT_RE = re.compile(r"(?<![/\w])(com\.apple\.[a-z0-9.\-]+)", re.IGNORECASE)

def strip_ansi(text: str) -> str:
    if not text:
        return ""
    return _ANSI_ESCAPE_RE.sub("", text)

def extract_paths_by_keyword(output: str, keyword: str) -> list[str]:
    if not output:
        return []
    cleaned = strip_ansi(output)
    # strictly anchor to path-safe characters to prevent capturing punctuation
    pattern = rf"(/[a-zA-Z0-9_\-\./]*{re.escape(keyword)}[a-zA-Z0-9_\-\./]*)"
    return list(dict.fromkeys(re.findall(pattern, cleaned)))

def _heading_level(line: str) -> tuple[int, str]:
    stripped = line.lstrip()
    if not stripped.startswith("#"):
        return 0, ""
    count = 0
    for ch in stripped:
        if ch == "#":
            count += 1
        else:
            break
    if count == 0 or count > 6:
        return 0, ""
    title = stripped[count:].strip()
    return count, title

def _title_has_keyword(title: str, keywords: Iterable[str]) -> bool:
    lowered = title.lower()
    return any(keyword in lowered for keyword in keywords)

def _resolve_change_type(titles: list[str]) -> str | None:
    for title in reversed(titles):
        for change_type, keywords in _CHANGE_KEYWORDS.items():
            if _title_has_keyword(title, keywords):
                return change_type
    return None

def _resolve_component(titles: list[str]) -> str | None:
    for title in reversed(titles):
        lowered = title.lower()
        if "kext" in lowered:
            return "kext"
        if "dylib" in lowered:
            return "dylib"
        if "macho" in lowered or "mach-o" in lowered:
            return "macho"
        if "firmware" in lowered:
            return "firmware"
        if "iboot" in lowered:
            return "iboot"
        if "launchd" in lowered or "service" in lowered:
            return "launchd"
        if "kernel" in lowered:
            return "kernel"
    return None

def _looks_like_item(text: str) -> bool:
    if not text:
        return False
    lowered = text.lower()
    if text.startswith("/"):
        return True
    if "/" in text and len(text) > 2:  # prevent catching isolated slashes in conversational text
        return True
    if lowered.startswith("com.apple."):
        return True
    return any(lowered.endswith(ext) for ext in _ITEM_EXTENSIONS)

def _extract_item_token(text: str) -> str | None:
    """Tokenizes and extracts the core path, bundle ID, or markdown link from noisy text"""
    # matches explicit markdown links e.g. [name](/path)
    link_match = re.search(r"(\[.*?\]\(.*?\))", text)
    if link_match:
        return link_match.group(1)
    
    # split text to bypass surrounding conversational syntax and extract valid paths
    for word in text.split():
        clean_word = word.strip(":,()[]{}*`\"'")
        if _looks_like_item(clean_word):
            return clean_word
    return None

def _is_group_heading(title: str) -> bool:
    lowered = title.lower().strip()
    if lowered in _GROUP_HEADINGS:
        return True
    return any(keyword in lowered for keyword in ("view ", "updated", "removed", "new", "added"))

def _add_unique(items: list[str], item: str, seen: set[str]) -> None:
    if item and item not in seen:
        seen.add(item)
        items.append(item)

def parse_diff_markdown(text: str) -> dict[str, list[str]]:
    headings: list[str | None] = [None] * 6

    added_binaries: list[str] = []
    modified_binaries: list[str] = []
    macho_binaries: list[str] = []   # filesystem Mach-O origin (## MachO section)
    dsc_dylibs: list[str] = []       # dyld_shared_cache origin (## DSC section)
    entitlements: list[str] = []
    sandbox: list[str] = []
    kexts: list[str] = []
    launchd: list[str] = []
    firmware_added: list[str] = []
    firmware_modified: list[str] = []
    iboot_added: list[str] = []
    iboot_modified: list[str] = []

    seen: dict[str, set[str]] = {
        "added": set(),
        "modified": set(),
        "macho_binaries": set(),
        "dsc_dylibs": set(),
        "entitlements": set(),
        "sandbox": set(),
        "kexts": set(),
        "launchd": set(),
        "firmware_added": set(),
        "firmware_modified": set(),
        "iboot_added": set(),
        "iboot_modified": set(),
    }

    component_hint: str | None = None
    active_change_type: str | None = None
    active_section: str | None = None  # "macho" | "dsc" | None — set by ## headings
    in_diff_block: bool = False         # True while inside a ```diff...``` fence

    for raw in text.splitlines():
        line = strip_ansi(raw).rstrip()
        level, title = _heading_level(line)
        if level:
            # Top-level (##) headings determine the binary origin section
            if level == 2:
                lowered = title.lower()
                if "macho" in lowered or "mach-o" in lowered:
                    active_section = "macho"
                elif "dsc" in lowered:
                    active_section = "dsc"
                else:
                    active_section = None

            headings[level - 1] = title
            for idx in range(level, len(headings)):
                headings[idx] = None

            if title:
                ctype = _resolve_change_type([title])
                if ctype:
                    active_change_type = ctype
                elif level <= 3:
                    active_change_type = None

            if title and not _title_has_keyword(title, _ALL_CHANGE_KEYWORDS):
                hinted = _resolve_component([title])
                if hinted:
                    component_hint = hinted

            if level >= 4 and title and not _is_group_heading(title):
                item = _extract_item_token(title)
                if not item:
                    continue
                titles = [t for t in headings if t]
                change_type = _resolve_change_type(titles) or active_change_type
                if change_type:
                    _apply_item(
                        item, titles, change_type, component_hint, active_section,
                        added_binaries, modified_binaries, macho_binaries, dsc_dylibs,
                        kexts, launchd, firmware_added, firmware_modified,
                        iboot_added, iboot_modified, seen,
                    )
            continue

        stripped = line.strip()
        # Track diff fences — items inside a ```diff block are diff content, not binary paths.
        if stripped.startswith("```"):
            in_diff_block = stripped.startswith("```diff")
            continue

        if in_diff_block:
            continue

        if stripped.startswith("- "):
            raw_item = stripped[2:].strip()
            item = _extract_item_token(raw_item)
            if not item:
                continue
            titles = [t for t in headings if t]
            change_type = _resolve_change_type(titles) or active_change_type
            if not change_type:
                continue
            _apply_item(
                item, titles, change_type, component_hint, active_section,
                added_binaries, modified_binaries, macho_binaries, dsc_dylibs,
                kexts, launchd, firmware_added, firmware_modified,
                iboot_added, iboot_modified, seen,
            )
            continue

        if stripped.startswith(">"):
            raw_item = stripped[1:].strip()
            item = _extract_item_token(raw_item)
            if not item:
                continue
            titles = [t for t in headings if t]
            change_type = _resolve_change_type(titles) or active_change_type
            if not change_type:
                continue
            _apply_item(
                item, titles, change_type, component_hint, active_section,
                added_binaries, modified_binaries, macho_binaries, dsc_dylibs,
                kexts, launchd, firmware_added, firmware_modified,
                iboot_added, iboot_modified, seen,
            )
            continue

        if not stripped.startswith(("+", "-", "#")) and "com.apple." in stripped:
            match = _ENTITLEMENT_RE.search(stripped)
            if match:
                token = match.group(1)
                if token not in seen["entitlements"]:
                    seen["entitlements"].add(token)
                    entitlements.append(token)

        if "sandbox" in stripped.lower() and not stripped.startswith(("+", "-", "#")):
            cleaned = stripped.strip()
            if any(kw in cleaned.lower() for kw in ("allow", "deny", "filter", "operation", "profile", "policy")):
                if cleaned and cleaned not in seen["sandbox"]:
                    seen["sandbox"].add(cleaned)
                    sandbox.append(cleaned)

    return {
        "added_binaries": added_binaries,
        "modified_binaries": modified_binaries,
        "macho_binaries": macho_binaries,
        "dsc_dylibs": dsc_dylibs,
        "entitlement_changes": entitlements,
        "sandbox_changes": sandbox,
        "kext_changes": kexts,
        "launchd_changes": launchd,
        "firmware_added": firmware_added,
        "firmware_modified": firmware_modified,
        "iboot_added": iboot_added,
        "iboot_modified": iboot_modified,
    }

def _apply_item(
    item: str,
    titles: list[str],
    change_type: str,
    component_hint: str | None,
    active_section: str | None,
    added_binaries: list[str],
    modified_binaries: list[str],
    macho_binaries: list[str],
    dsc_dylibs: list[str],
    kexts: list[str],
    launchd: list[str],
    firmware_added: list[str],
    firmware_modified: list[str],
    iboot_added: list[str],
    iboot_modified: list[str],
    seen: dict[str, set[str]],
) -> None:
    component = _resolve_component(titles)
    if component_hint and (component is None or component in {"kernel", "dsc"}):
        component = component_hint

    # Route to flat change lists (used by classifier for counts)
    if change_type == "added":
        _add_unique(added_binaries, item, seen["added"])
    elif change_type == "modified":
        _add_unique(modified_binaries, item, seen["modified"])

    # Route to specialised component lists
    if component == "kext":
        _add_unique(kexts, item, seen["kexts"])

    lowered = item.lower()
    if component == "launchd" or "/launchdaemons" in lowered or "/launchagents" in lowered:
        _add_unique(launchd, item, seen["launchd"])

    if component == "firmware":
        target, key = (firmware_added, "firmware_added") if change_type == "added" else (firmware_modified, "firmware_modified")
        _add_unique(target, item, seen[key])

    if component == "iboot":
        target, key = (iboot_added, "iboot_added") if change_type == "added" else (iboot_modified, "iboot_modified")
        _add_unique(target, item, seen[key])

    if active_section == "macho":
        _add_unique(macho_binaries, item, seen["macho_binaries"])
    elif active_section == "dsc":
        _add_unique(dsc_dylibs, item, seen["dsc_dylibs"])

def parse_simple_list_output(text: str) -> list[str]:
    cleaned = strip_ansi(text)
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    return list(dict.fromkeys(lines))

def parse_dyld_diff_output(text: str) -> list[str]:
    cleaned = strip_ansi(text)
    items: list[str] = []
    seen: set[str] = set()

    for raw in cleaned.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line[0] not in "+-":
            continue
        entry = line[1:].strip()
        if not entry.startswith("/"):
            continue
        path = entry.split()[0]
        if "/BypassDyld" in path or "/Stub/" in path or "__dsc_expanded" in path:
            continue
        if path not in seen:
            seen.add(path)
            items.append(path)
    return items

def extract_cstring_diffs(text: str) -> list[str]:
    headings: list[str | None] = [None] * 6
    results: list[str] = []
    seen: set[str] = set()
    current_item: str | None = None
    in_diff_block = False
    in_cstring_section = False

    for raw in text.splitlines():
        line = strip_ansi(raw).rstrip()
        if line.strip().startswith("```"):
            if line.strip().startswith("```diff"):
                in_diff_block = True
                in_cstring_section = False
            else:
                in_diff_block = False
                in_cstring_section = False
            continue

        level, title = _heading_level(line)
        if level:
            headings[level - 1] = title
            for idx in range(level, len(headings)):
                headings[idx] = None
            if level >= 4 and title and not _is_group_heading(title):
                extracted = _extract_item_token(title)
                current_item = extracted if extracted else title.strip(" `*")
            continue

        if not in_diff_block:
            continue

        if line.strip() == "CStrings:":
            in_cstring_section = True
            continue
        elif line.strip().endswith(":") and not line.startswith("+") and not line.startswith("-"):
            # some other section like "Symbols:"
            in_cstring_section = False

        if not (line.startswith("+") or line.startswith("-")):
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue

        lowered = line.lower()
        if "__cstring" in lowered or "cstrings:" in lowered:
            continue

        if not in_cstring_section:
            continue

        label = current_item or ""
        entry = f"{label}: {line.strip()}" if label else line.strip()
        if entry not in seen:
            seen.add(entry)
            results.append(entry)

    return results

def extract_symbol_diffs(text: str) -> list[str]:
    headings: list[str | None] = [None] * 6
    results: list[str] = []
    seen: set[str] = set()
    current_item: str | None = None
    in_diff_block = False
    in_symbol_section = False

    for raw in text.splitlines():
        line = strip_ansi(raw).rstrip()
        if line.strip().startswith("```"):
            if line.strip().startswith("```diff"):
                in_diff_block = True
                in_symbol_section = False
            else:
                in_diff_block = False
                in_symbol_section = False
            continue

        level, title = _heading_level(line)
        if level:
            headings[level - 1] = title
            for idx in range(level, len(headings)):
                headings[idx] = None
            if level >= 4 and title and not _is_group_heading(title):
                extracted = _extract_item_token(title)
                current_item = extracted if extracted else title.strip(" `*")
            continue

        if not in_diff_block:
            continue

        if line.strip() == "Symbols:":
            in_symbol_section = True
            continue
        elif line.strip().endswith(":") and not line.startswith("+") and not line.startswith("-"):
            in_symbol_section = False

        if not (line.startswith("+") or line.startswith("-")):
            continue
        if line.startswith("+++") or line.startswith("---"):
            continue

        lowered = line.lower()
        if "symbols:" in lowered or "__symbol" in lowered:
            continue

        if not in_symbol_section:
            continue

        label = current_item or ""
        entry = f"{label}: {line.strip()}" if label else line.strip()
        if entry not in seen:
            seen.add(entry)
            results.append(entry)

    return results
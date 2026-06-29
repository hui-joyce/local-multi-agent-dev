from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

@dataclass
class DiffCounts:
    added_binaries: int = 0
    modified_binaries: int = 0
    cstring_count: int = 0
    entitlement_changes: int = 0
    sandbox_changes: int = 0
    kext_changes: int = 0
    launchd_changes: int = 0
    dyld_changes: int = 0
    kernel_changes: int = 0
    firmware_added: int = 0
    firmware_modified: int = 0
    iboot_added: int = 0
    iboot_modified: int = 0

@dataclass
class EvidenceItem:
    source: str
    summary: str
    details: Optional[str] = None

@dataclass
class Finding:
    title: str
    change_type: str
    impact: str = ""
    mitigation: str = ""
    confidence: float = 0.0
    evidence: list[EvidenceItem] = field(default_factory=list)

@dataclass
class FirmwareDiffArtifacts:
    output_dir: str
    report_json: str
    entitlement_diff: Optional[str] = None
    sandbox_diff: Optional[str] = None
    kext_diff: Optional[str] = None
    dyld_diff: Optional[str] = None
    kernel_diff: Optional[str] = None
    framework_diff: Optional[str] = None
    launchd_diff: Optional[str] = None
    raw_diff_dir: Optional[str] = None

@dataclass
class FirmwareDiffSummary:
    old_firmware: str
    new_firmware: str
    extraction_status: str
    counts: DiffCounts
    high_risk_changes: int

@dataclass
class FirmwareDiffResult:
    summary: FirmwareDiffSummary
    findings: list[Finding]
    artifacts: FirmwareDiffArtifacts
    gaps: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

@dataclass
class FirmwareDiffRequest:
    old_ipsw: str
    new_ipsw: str
    output_dir: Optional[str] = None
    old_kernelcache: Optional[str] = None
    new_kernelcache: Optional[str] = None
    old_dyld: Optional[str] = None
    new_dyld: Optional[str] = None
    device: Optional[str] = None
    old_version: Optional[str] = None
    new_version: Optional[str] = None
    include_entitlements: bool = True
    include_sandbox: bool = True
    include_kexts: bool = True
    include_launchd: bool = True
    include_fw_components: bool = True
    include_strs: bool = True
    clean_cache: bool = True


class DiffState(str, Enum):
    NEW = "new"
    REMOVED = "removed"
    UPDATED = "updated"

@dataclass
class MachODiff:
    path: str
    state: DiffState
    old_version: Optional[str] = None
    new_version: Optional[str] = None
    added_symbols: list[str] = field(default_factory=list)
    removed_symbols: list[str] = field(default_factory=list)
    added_cstrings: list[str] = field(default_factory=list)
    removed_cstrings: list[str] = field(default_factory=list)
    modified_objc_classes: list[str] = field(default_factory=list)

@dataclass
class KextDiff:
    path: str
    state: DiffState
    added_symbols: list[str] = field(default_factory=list)
    removed_symbols: list[str] = field(default_factory=list)

@dataclass
class EntitlementDiff:
    path: str
    state: DiffState
    added_keys: list[str] = field(default_factory=list)
    removed_keys: list[str] = field(default_factory=list)

@dataclass
class LaunchdDiff:
    path: str
    state: DiffState
    added_keys: list[str] = field(default_factory=list)
    removed_keys: list[str] = field(default_factory=list)

@dataclass
class SandboxDiff:
    profile_name: str
    state: DiffState
    added_rules: list[str] = field(default_factory=list)
    removed_rules: list[str] = field(default_factory=list)

@dataclass
class FirmwareComponentDiff:
    name: str
    state: DiffState
    hash: Optional[str] = None

@dataclass
class IDiffReport:
    """Represents the complete binary-level diff state produced by the Firmware Diff Service"""
    title: str
    machos: list[MachODiff] = field(default_factory=list)
    kexts: list[KextDiff] = field(default_factory=list)
    entitlements: list[EntitlementDiff] = field(default_factory=list)
    launchd_plists: list[LaunchdDiff] = field(default_factory=list)
    sandbox_profiles: list[SandboxDiff] = field(default_factory=list)
    firmwares: list[FirmwareComponentDiff] = field(default_factory=list)

    @classmethod
    def from_file(cls, filepath: str) -> "IDiffReport":
        import json
        import re
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        report = cls(title=data.get("title", ""))
        
        def parse_macho(path: str, state: DiffState, diff_str: str) -> MachODiff:
            macho = MachODiff(path=path, state=state)
            if not isinstance(diff_str, str):
                return macho
                
            for line in diff_str.splitlines():
                if line.startswith("+") and not line.startswith("+++"):
                    str_match = re.search(r'\"(.*?)\"', line)
                    if str_match:
                        macho.added_cstrings.append(str_match.group(1))
                    clean_line = line[1:].strip()
                    if clean_line.startswith("_") and not clean_line.startswith("__TEXT") and not clean_line.startswith("__DATA"):
                        macho.added_symbols.append(clean_line)
                        if "_OBJC_CLASS_$_" in clean_line:
                            macho.modified_objc_classes.append(clean_line.split("_OBJC_CLASS_$_")[-1])
                elif line.startswith("-") and not line.startswith("---"):
                    str_match = re.search(r'\"(.*?)\"', line)
                    if str_match:
                        macho.removed_cstrings.append(str_match.group(1))
                    clean_line = line[1:].strip()
                    if clean_line.startswith("_") and not clean_line.startswith("__TEXT") and not clean_line.startswith("__DATA"):
                        macho.removed_symbols.append(clean_line)
            return macho

        # parse DSC dylibs
        dylibs_data = data.get("dylibs", {})
        for state_str, items in dylibs_data.items():
            try:
                state = DiffState(state_str.lower())
            except ValueError:
                state = DiffState.UPDATED
            for path, diff_str in items.items():
                report.machos.append(parse_macho(path, state, diff_str))
                
        # parse filesystem machos
        machos_data = data.get("machos", {}).get("filesystem", {})
        for state_str, items in machos_data.items():
            try:
                state = DiffState(state_str.lower())
            except ValueError:
                state = DiffState.UPDATED
            for path, diff_str in items.items():
                report.machos.append(parse_macho(path, state, diff_str))
                
        return report
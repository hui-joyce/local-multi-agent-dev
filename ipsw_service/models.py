from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class DiffCounts:
    added_binaries: int = 0
    removed_binaries: int = 0
    modified_binaries: int = 0
    cstring_count: int = 0
    entitlement_changes: int = 0
    sandbox_changes: int = 0
    kext_changes: int = 0
    launchd_changes: int = 0
    dyld_changes: int = 0
    kernel_changes: int = 0
    firmware_added: int = 0
    firmware_removed: int = 0
    firmware_modified: int = 0
    iboot_added: int = 0
    iboot_removed: int = 0
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
    report_markdown: str
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
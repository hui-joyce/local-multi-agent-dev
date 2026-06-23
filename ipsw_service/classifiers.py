from __future__ import annotations

from dataclasses import asdict
from typing import Iterable

from ipsw_service.models import DiffCounts, EvidenceItem, Finding

HIGH_RISK_ENTITLEMENTS = [
    "com.apple.private.security.no-sandbox",
    "platform-application",
    "com.apple.private.tcc",
    "com.apple.private.security.container-required",
    "com.apple.private.skip-library-validation",
]

PRIVILEGED_PATH_HINTS = [
    "/usr/libexec",
    "/usr/sbin",
    "/sbin",
    "/System/Library/LaunchDaemons",
    "/System/Library/PrivateFrameworks",
]

# keywords that indicate an IPC/XPC surface within a sandbox policy line
_IPC_KEYWORDS = ("mach-lookup", "xpc")

class ChangeClassifier:
    def __init__(self) -> None:
        self.high_risk_entitlements = list(HIGH_RISK_ENTITLEMENTS)
        self.privileged_path_hints = list(PRIVILEGED_PATH_HINTS)

    def classify(self, diff_data: dict[str, list[str]]) -> tuple[DiffCounts, list[Finding]]:
        counts = DiffCounts(
            added_binaries=len(diff_data.get("added_binaries", [])),
            modified_binaries=len(diff_data.get("modified_binaries", [])),
            entitlement_changes=len(diff_data.get("entitlement_changes", [])),
            sandbox_changes=len(diff_data.get("sandbox_changes", [])),
            kext_changes=len(diff_data.get("kext_changes", [])),
            launchd_changes=len(diff_data.get("launchd_changes", [])),
            dyld_changes=len(diff_data.get("dyld_changes", [])),
            kernel_changes=len(diff_data.get("kernel_changes", [])),
            firmware_added=len(diff_data.get("firmware_added", [])),
            firmware_modified=len(diff_data.get("firmware_modified", [])),
            iboot_added=len(diff_data.get("iboot_added", [])),
            iboot_modified=len(diff_data.get("iboot_modified", [])),
        )

        findings: list[Finding] = []
        findings.extend(self._classify_entitlements(diff_data.get("entitlement_changes", [])))
        # sandbox classifier sub-tags IPC lines instead of emitting a separate
        # iPC finding for each, avoiding double-counting.
        findings.extend(self._classify_sandbox(diff_data.get("sandbox_changes", [])))
        findings.extend(self._classify_privileged_binaries(diff_data.get("added_binaries", [])))
        findings.extend(self._classify_launchd(diff_data.get("launchd_changes", [])))

        return counts, findings

    def _classify_entitlements(self, changes: Iterable[str]) -> list[Finding]:
        findings: list[Finding] = []
        for line in changes:
            for entitlement in self.high_risk_entitlements:
                if entitlement in line:
                    findings.append(
                        Finding(
                            title=f"Potential entitlement change: {entitlement}",
                            change_type="entitlement",
                            impact="Potential privilege boundary shift or sandbox relaxation.",
                            mitigation="Review entitlement provenance and ensure least privilege.",
                            confidence=0.7,
                            evidence=[EvidenceItem(source="entitlement_diff", summary=line)],
                        )
                    )
        return findings

    def _classify_sandbox(self, changes: Iterable[str]) -> list[Finding]:
        findings: list[Finding] = []
        for line in changes:
            lowered = line.lower()
            is_ipc = any(kw in lowered for kw in _IPC_KEYWORDS)
            if is_ipc:
                findings.append(
                    Finding(
                        title="Potential sandbox IPC/XPC exposure change",
                        change_type="ipc",
                        impact="Sandbox policy may allow new IPC/XPC endpoints.",
                        mitigation="Review mach service and XPC exposure for affected profiles.",
                        confidence=0.65,
                        evidence=[EvidenceItem(source="sandbox_diff", summary=line)],
                    )
                )
            else:
                findings.append(
                    Finding(
                        title="Potential sandbox policy change",
                        change_type="sandbox",
                        impact="Sandbox operations changed; may introduce new IPC or file access paths.",
                        mitigation="Review sandbox op diff and validate protections for affected services.",
                        confidence=0.6,
                        evidence=[EvidenceItem(source="sandbox_diff", summary=line)],
                    )
                )
        return findings

    def _classify_privileged_binaries(self, binaries: Iterable[str]) -> list[Finding]:
        findings: list[Finding] = []
        for binary in binaries:
            if any(hint in binary for hint in self.privileged_path_hints):
                findings.append(
                    Finding(
                        title="New privileged binary added",
                        change_type="binary_added",
                        impact="New executable in privileged path may expand attack surface.",
                        mitigation="Perform static analysis and entitlement review on the new binary.",
                        confidence=0.6,
                        evidence=[EvidenceItem(source="firmware_diff", summary=binary)],
                    )
                )
        return findings

    def _classify_launchd(self, changes: Iterable[str]) -> list[Finding]:
        findings: list[Finding] = []
        for line in changes:
            findings.append(
                Finding(
                    title="Launchd/service configuration change",
                    change_type="launchd",
                    impact="Service changes can expose new IPC surfaces or alter privilege boundaries.",
                    mitigation="Audit service plist changes and validate service entitlements.",
                    confidence=0.6,
                    evidence=[EvidenceItem(source="launchd_diff", summary=line)],
                )
            )
        return findings

def serialize_findings(findings: list[Finding]) -> list[dict]:
    return [asdict(finding) for finding in findings]
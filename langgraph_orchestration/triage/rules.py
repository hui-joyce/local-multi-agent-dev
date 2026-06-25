"""Deterministic triage for firmware diff evidence.

A component is HIGH_SIGNAL if its diff contains semantic added/removed changes.
Metadata-only changes (e.g. UUIDs, versions, timestamps, section sizes, or dylib
paths) are classified as LOW_SIGNAL and excluded from analysis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

HIGH_SIGNAL = "HIGH_SIGNAL"
LOW_SIGNAL = "LOW_SIGNAL"

# Build metadata that carries no behavioral meaning. Anchored at the +/- marker.
_METADATA_RE = re.compile(
    r"^[+\-]\s*("
    r"UUID:\s*[0-9A-Fa-f\-]+"             # UUID drift
    r'|"?\d+(?:\.\d+)+[A-Za-z0-9\-_]*"?'  # version string e.g. 1450.500.221.2.9
    r"|__TEXT\.__"                        # section sizes
    r"|__LINKEDIT"
    r"|__DATA\.__"                        # data section sizes (metadata churn)
    r"|__const"
    r"|__got"
    r"|/usr/lib/"                         # dylib deps
    r"|/System/Library/"
    r"|/usr/local/lib/"
    r")"
)

_TIMESTAMP_RE = re.compile(
    r'^[+\-]\s*"?\d{1,2}:\d{2}:\d{2}"?\s*$'
    r'|^[+\-]\s*"?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{4}"?\s*$',
    re.IGNORECASE,
)

@dataclass(frozen=True)
class TriageResult:
    signal: str
    reason: str
    evidence_line: str = ""

    @property
    def is_high_signal(self) -> bool:
        return self.signal == HIGH_SIGNAL


def _is_noise(stripped_line: str) -> bool:
    return bool(_METADATA_RE.match(stripped_line) or _TIMESTAMP_RE.match(stripped_line))


def triage_evidence_explained(evidence: str) -> TriageResult:
    """Classify diff evidence and return the deciding line for auditability"""
    if not evidence:
        return TriageResult(LOW_SIGNAL, "no evidence provided")

    for line in evidence.splitlines():
        stripped = line.strip()
        if not stripped or not stripped.startswith(("+", "-")):
            continue
        if _is_noise(stripped):
            continue
        return TriageResult(
            HIGH_SIGNAL,
            "semantic added/removed line present",
            evidence_line=stripped[:200],
        )

    return TriageResult(LOW_SIGNAL, "only metadata/timestamp churn detected")


def triage_evidence(evidence: str) -> str:
    return triage_evidence_explained(evidence).signal

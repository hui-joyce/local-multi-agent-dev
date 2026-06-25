"""Deterministic, rule-based triage for firmware-diff feature components.

This package is the single source of truth for the LOW_SIGNAL / HIGH_SIGNAL
decision. It must remain pure (no I/O, no model calls, no global state) so that
identical evidence always yields an identical signal.
"""

from langgraph_orchestration.triage.rules import (
    HIGH_SIGNAL,
    LOW_SIGNAL,
    TriageResult,
    triage_evidence,
)

__all__ = ["HIGH_SIGNAL", "LOW_SIGNAL", "TriageResult", "triage_evidence"]

#!/usr/bin/env python3
"""Independently re-derive and cross-check the release-impact figures for a firmware diff run.

The two headline figures are:

  cstring-level changes  -- how many "+"/"-" __cstring lines the release touched
  components touched     -- how many distinct binaries/components the release touched

Neither is produced by an LLM. Both are deterministic parses of the output of one
`ipsw diff` invocation. This script proves that by recomputing them from the raw
preserved tool output using the *production* parser (`ipsw_service.parsing`), then
cross-checking against the two derived artifacts the pipeline persisted:

    diff/*/README.md        raw consolidated `ipsw diff --markdown --strs` output
        |                   (also artifacts/dyld_diff.txt, which records the literal
        |                    ipsw command, its stdout, and the parsed item list)
        v  extract_cstring_diffs() / parse_diff_markdown()
    report.json             cstring_context, userland_changes, boundary_changes
        |
        v  _build_feature_targets() -> render_triage_summary()
    feature_analysis/00_SUMMARY.md   "Total components in diff: N"

A non-zero exit status means a figure could not be reproduced.

Usage:
    ./venv/bin/python benchmarks/verify_release_impact.py
    ./venv/bin/python benchmarks/verify_release_impact.py --run 20260704-145351 --breakdown
    ./venv/bin/python benchmarks/verify_release_impact.py --run 20260704-145351 \
        --component AppPredictionClient
"""

from __future__ import annotations

import argparse
import collections
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ipsw_service.parsing import extract_cstring_diffs  # noqa: E402

ARTIFACT_ROOT = "artifacts/firmware_diff"
_TOTAL_RE = re.compile(r"\*\*Total components in diff\*\*:\s*(\d+)")
_MARKDOWN_LINK_RE = re.compile(r"^\[(?P<label>[^\]]+)\]\([^)]*\)$")


def _read(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def split_sign(entry: str) -> str:
    """'+' or '-' for a '<component>: <+/- line>' entry from cstring_context."""
    body = entry.split(":", 1)[1].strip() if ":" in entry else entry.strip()
    return body[:1]


def component_of(entry: str) -> str | None:
    parts = entry.split(":", 1)
    return parts[0].strip() if len(parts) == 2 else None


def _label(entry: object) -> str | None:
    """Unwrap a '[label](path)' markdown link to its label (HEAD rule only)."""
    if not isinstance(entry, str):
        return None
    text = entry.strip()
    match = _MARKDOWN_LINK_RE.match(text)
    if match:
        text = match.group("label").strip()
    return text or None


def count_components(report: dict, rule: str) -> dict:
    """Count distinct components touched, as clause (a) changed binaries UNION
    clause (b) owners of at least one cstring/symbol line.

    Two rules exist for clause (a), because the pipeline changed:

      "legacy"  `_build_feature_targets` up to commit 10e8c82 -- only entries that
                literally start with "/", from boundary_changes.* + userland_changes.*
      "head"    commit dfc0a5f (2026-08-05) onward -- additionally unwraps markdown-link
                labels, accepts bare (non-path) labels, and includes base_firmware_changes

    Runs summarised before 2026-08-05 recorded the legacy figure, later runs the head
    figure. They differ materially: 3160 vs 3317 for run 20260703-025926. Point-release
    runs are usually rule-invariant (66 either way).
    """
    from_paths: set[str] = set()
    sections = ("boundary_changes", "userland_changes")
    if rule == "head":
        sections += ("base_firmware_changes",)

    for key in sections:
        section = report.get(key)
        groups = section.values() if isinstance(section, dict) else [section]
        for entries in groups:
            if not isinstance(entries, list):
                continue
            for item in entries:
                if rule == "legacy":
                    if isinstance(item, str) and item.startswith("/"):
                        from_paths.add(os.path.basename(item))
                else:
                    label = _label(item)
                    if label:
                        from_paths.add(os.path.basename(label))

    from_evidence: set[str] = set()
    for key in ("cstring_context", "symbol_context"):
        for line in report.get(key, []):
            name = component_of(line)
            if name:
                from_evidence.add(name)

    return {
        "total": len(from_paths | from_evidence),
        "paths": len(from_paths),
        "evidence": len(from_evidence),
        "evidence_only": len(from_evidence - from_paths),
        "evidence_only_names": sorted(from_evidence - from_paths),
    }


def verify(run_dir: str, breakdown: bool = False, component: str | None = None) -> bool:
    ok = True
    name = os.path.basename(run_dir.rstrip("/"))
    report_path = os.path.join(run_dir, "report.json")
    readmes = glob.glob(os.path.join(run_dir, "diff", "*", "README.md"))
    summary_path = os.path.join(run_dir, "feature_analysis", "00_SUMMARY.md")

    if not os.path.exists(report_path):
        print(f"[{name}] SKIP - no report.json persisted for this run")
        return True

    report = json.loads(_read(report_path))
    persisted = report["cstring_context"]

    print(f"[{name}]")

    # --- metric 1: recompute from the raw ipsw output, do not trust report.json ---
    if readmes:
        recomputed = extract_cstring_diffs(_read(readmes[0]))
        exact = recomputed == persisted
        ok &= exact
        print(f"  cstring-level changes  : {len(recomputed)}"
              f"   [recomputed from {os.path.relpath(readmes[0], run_dir)}]")
        print(f"    vs report.json       : {len(persisted)}"
              f"   list-identical={exact}{'' if exact else '   <-- MISMATCH'}")
    else:
        print(f"  cstring-level changes  : {len(persisted)}"
              f"   [report.json only - raw README.md not preserved]")

    signs = collections.Counter(split_sign(e) for e in persisted)
    print(f"    added / removed      : +{signs['+']} / -{signs['-']}"
          f"   (sums to {signs['+'] + signs['-']})")

    # --- metric 2: components, cross-checked against the run's own summary ---
    counts = {rule: count_components(report, rule) for rule in ("legacy", "head")}

    recorded = None
    if os.path.exists(summary_path):
        match = _TOTAL_RE.search(_read(summary_path))
        if match:
            recorded = int(match.group(1))

    matching = [r for r, c in counts.items() if c["total"] == recorded]
    rule = matching[0] if matching else "legacy"
    comp = counts[rule]

    print(f"  components touched     : {comp['total']}"
          f"   = {comp['paths']} changed binaries + {comp['evidence_only']} evidence-only")
    print(f"    of which had string/symbol evidence: {comp['evidence']}")
    if counts["legacy"]["total"] != counts["head"]["total"]:
        print(f"    rule sensitivity     : legacy={counts['legacy']['total']} "
              f"head={counts['head']['total']}  (quote the recorded one, name the rule)")

    if recorded is not None:
        agree = bool(matching)
        ok &= agree
        note = f"reproduced by '{rule}' rule" if agree else "<-- MISMATCH, no rule reproduces it"
        print(f"    vs 00_SUMMARY.md     : {recorded}   {note}")

    print(f"  NOT a delta, do not quote: summary_metrics.total_cstring_changes = "
          f"{report.get('summary_metrics', {}).get('total_cstring_changes')}")

    if breakdown:
        per = collections.Counter()
        per_sign: collections.Counter = collections.Counter()
        for entry in persisted:
            owner = component_of(entry)
            if owner:
                per[owner] += 1
                per_sign[(owner, split_sign(entry))] += 1
        print(f"  per-component tally ({len(per)} components with cstring changes):")
        for owner, total in per.most_common():
            print(f"    {owner:<45} {total:>6}  "
                  f"(+{per_sign[(owner, '+')]} -{per_sign[(owner, '-')]})")

    if component:
        hits = [e for e in persisted if component_of(e) == component]
        sub = collections.Counter(split_sign(e) for e in hits)
        print(f"  evidence for '{component}': {len(hits)} lines "
              f"(+{sub['+']} -{sub['-']})")
        for entry in hits:
            print(f"    {entry}")

    return bool(ok)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", help="run directory name or path (default: every run)")
    ap.add_argument("--breakdown", action="store_true",
                    help="print the per-component tally that sums to the total")
    ap.add_argument("--component", help="dump every cstring line for one component")
    args = ap.parse_args()

    if args.run:
        runs = [args.run if os.path.isdir(args.run) else os.path.join(ARTIFACT_ROOT, args.run)]
    else:
        runs = sorted(d for d in glob.glob(os.path.join(ARTIFACT_ROOT, "*")) if os.path.isdir(d))

    all_ok = True
    for run in runs:
        all_ok &= verify(run, breakdown=args.breakdown, component=args.component)
        print()

    print("ALL FIGURES REPRODUCED" if all_ok else "REPRODUCTION FAILED - see MISMATCH above")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

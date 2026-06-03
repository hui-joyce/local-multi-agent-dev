from __future__ import annotations

import os
from datetime import datetime, timezone
import re
from typing import Optional

from ipsw_service.agents.framework_diff_engine import FrameworkDiffEngine
from ipsw_service.agents.kernel_analysis_engine import KernelAnalysisEngine
from ipsw_service.classifiers import ChangeClassifier
from ipsw_service.cli import IpswCliRunner, build_dyld_diff_args
from ipsw_service.models import FirmwareDiffArtifacts, FirmwareDiffRequest, FirmwareDiffResult, FirmwareDiffSummary
from ipsw_service.parsing import (
    extract_cstring_diffs,
    parse_diff_markdown,
    parse_dyld_diff_output,
    parse_simple_list_output,
    strip_ansi,
)
from ipsw_service.agents.macho_analysis_engine import MachoAnalysisEngine
from ipsw_service.reporting import render_report
from ipsw_service.utils import ensure_dir, list_files, read_text, write_json, write_text

# Define noise filters for non-analyzable binaries
IGNORE_PATTERNS = [
    r"\.metallib$",                       # Metal compiled shaders
    r"\.g18p(?:_a0)?$",                   # Apple Silicon ISP microcode
    r"\.appex/",                          # UI Extensions (Widgets, watch faces)
    r"/VideoProcessors/",                 # Video processing bundles
    r"/NanoTimeKit/FaceBundles/",         # Watch faces
    r"/Applications/Kaleidoscope",        # Specific noisy apps
    r"CoreImage\.framework.*_bin"         # Precompiled CoreImage archives
]

_METADATA_ONLY_PATTERNS = (
    re.compile(r"^UUID:\s*", re.IGNORECASE),
    re.compile(r"^LC_BUILD_VERSION\b", re.IGNORECASE),
    re.compile(r"^LC_CODE_SIGNATURE\b", re.IGNORECASE),
    re.compile(r"^__LINKEDIT\b", re.IGNORECASE),
    re.compile(r"^__TEXT\.__info_plist\b", re.IGNORECASE),
)

_METAL_HINTS = (".metallib", ".g18p")
_MACHO_DIFF_DIRS = ("MACHOS/", "DYLIBS/")
_UUID_RE = re.compile(r"\bUUID:\s*([0-9A-Fa-f-]+)")

def _dedupe_stripped(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = strip_ansi(item).strip()
        if key and key not in seen:
            seen.add(key)
            result.append(item)
    return result


def _is_noisy_binary(path: str) -> bool:
    """Check if a binary path matches any noise filter patterns"""
    return any(re.search(pattern, path) for pattern in IGNORE_PATTERNS)


class FirmwareDiffService:
    def __init__(
        self,
        runner: Optional[IpswCliRunner] = None,
        workspace_root: Optional[str] = None,
    ):
        self.workspace_root = workspace_root or os.getcwd()
        self.runner = runner or IpswCliRunner(cwd=self.workspace_root)
        self.framework_diff_engine = FrameworkDiffEngine(self.runner)
        self.kernel_engine = KernelAnalysisEngine(self.runner)
        self.classifier = ChangeClassifier()

    def _format_tool_output(
        self,
        label: str,
        command: str,
        stdout: str,
        stderr: str,
        parsed_items: Optional[list[str]] = None,
    ) -> str:
        lines = [f"[{label}]", f"command: {command}"]
        if parsed_items is not None:
            lines.append(f"parsed_item_count: {len(parsed_items)}")
            if parsed_items:
                lines.append("parsed_items:")
                lines.extend(parsed_items)
        if stdout:
            lines.append("stdout:")
            lines.append(stdout.rstrip())
        if stderr:
            lines.append("stderr:")
            lines.append(stderr.rstrip())
        return "\n".join(lines).strip() + "\n"

    def _format_component_diff(self, label: str, items: list[str], note: Optional[str] = None) -> str:
        lines = [f"[{label}]", f"item_count: {len(items)}"]
        if note:
            lines.append(f"note: {note}")
        if items:
            lines.append("items:")
            lines.extend(items)
        else:
            lines.append("items: none detected")
        return "\n".join(lines).strip() + "\n"

    def run(self, request: FirmwareDiffRequest) -> FirmwareDiffResult:
        output_dir = request.output_dir or self._timestamped_output_dir()
        ensure_dir(output_dir)
        diff_dir = ensure_dir(os.path.join(output_dir, "diff"))
        ent_dir = ensure_dir(os.path.join(output_dir, "entitlements"))
        artifacts_dir = ensure_dir(os.path.join(output_dir, "artifacts"))

        gaps: list[str] = []
        low_memory = os.getenv("IPSW_DIFF_LOW_MEMORY") == "1"

        diff_result = self.framework_diff_engine.diff_firmware(
            request.old_ipsw,
            request.new_ipsw,
            diff_dir,
            include_fw=request.include_fw_components,
            include_launchd=request.include_launchd,
            include_strs=request.include_strs,
            markdown=True,
            low_memory=low_memory,
        )
        if not diff_result.get("success"):
            gaps.append(f"ipsw diff failed: {diff_result.get('stderr') or 'unknown error'}")

        diff_report_path = diff_result.get("markdown_report")
        diff_report_text = read_text(diff_report_path) if diff_report_path else ""
        diff_data = parse_diff_markdown(diff_report_text) if diff_report_text else {
            "added_binaries": [],
            "modified_binaries": [],
            "entitlement_changes": [],
            "sandbox_changes": [],
            "kext_changes": [],
            "framework_changes": [],
            "launchd_changes": [],
            "firmware_added": [],
            "firmware_modified": [],
            "iboot_added": [],
            "iboot_modified": [],
            "cstring_changes": [],
        }
        diff_report_root = os.path.dirname(diff_report_path) if diff_report_path else diff_dir
        
        if diff_report_text:
            diff_data["cstring_changes"] = extract_cstring_diffs(diff_report_text)
        macho_note = None
        if diff_report_path:
            macho_dir = os.path.join(diff_report_root, "MACHOS")
            if not os.path.isdir(macho_dir):
                macho_note = (
                    "MachO diff artifacts missing; filesystem diff likely failed or was skipped."
                )
                gaps.append(macho_note)

        added_raw = diff_data.get("added_binaries", [])
        modified_raw = diff_data.get("modified_binaries", [])

        diff_data["added_binaries"] = self._normalize_binary_list(added_raw, diff_report_root)
        filtered_modified = self._filter_modified_binaries(modified_raw, diff_report_root)
        diff_data["modified_binaries"] = filtered_modified

        # Compute explicit cstring count across candidate binaries.
        macho_engine = MachoAnalysisEngine(self.runner)
        cstring_count = 0
        try:
            seen: set[tuple[str, str]] = set()
            cstring_count += self._count_cstrings_for_items(
                diff_data.get("added_binaries", []), diff_report_root, request.new_dyld, macho_engine, seen
            )
            cstring_count += self._count_cstrings_for_items(
                diff_data.get("modified_binaries", []), diff_report_root, request.new_dyld, macho_engine, seen
            )
        except Exception as e:
            gaps.append(f"CString counting partially failed: {str(e)}")

        ent_diff_path: Optional[str] = None
        if request.include_entitlements:
            ent_result = self.framework_diff_engine.entitlements_diff(
                request.old_ipsw,
                request.new_ipsw,
                ent_dir,
                low_memory=low_memory,
            )
            if ent_result.get("success"):
                ent_files = ent_result.get("files", [])
                ent_diff_path = ent_files[0] if ent_files else None
            else:
                gaps.append(f"entitlements diff failed: {ent_result.get('stderr') or 'unknown error'}")

        kext_diff_path = None
        sandbox_diff_path = None
        kext_change_list: list[str] = []
        sandbox_change_list: list[str] = []
        kernel_change_list: list[str] = []
        if request.old_kernelcache and request.new_kernelcache:
            if request.include_kexts:
                kext_result = self.kernel_engine.diff_kexts(request.old_kernelcache, request.new_kernelcache)
                kext_diff_path = os.path.join(artifacts_dir, "kext_diff.txt")
                if not kext_result.get("success"):
                    gaps.append(f"kext diff failed: {kext_result.get('stderr') or 'unknown error'}")
                else:
                    kext_change_list = parse_simple_list_output(kext_result.get("diff", ""))
                write_text(
                    kext_diff_path,
                    self._format_tool_output(
                        "kext_diff",
                        kext_result.get("command", ""),
                        kext_result.get("diff", ""),
                        kext_result.get("stderr", ""),
                        parsed_items=kext_change_list if kext_result.get("success") else None,
                    ),
                )
            if request.include_sandbox:
                sandbox_result = self.kernel_engine.diff_sandbox_ops(request.old_kernelcache, request.new_kernelcache)
                sandbox_diff_path = os.path.join(artifacts_dir, "sandbox_diff.txt")
                if not sandbox_result.get("success"):
                    gaps.append(f"sandbox diff failed: {sandbox_result.get('stderr') or 'unknown error'}")
                else:
                    sandbox_change_list = parse_simple_list_output(sandbox_result.get("diff", ""))
                write_text(
                    sandbox_diff_path,
                    self._format_tool_output(
                        "sandbox_diff",
                        sandbox_result.get("command", ""),
                        sandbox_result.get("diff", ""),
                        sandbox_result.get("stderr", ""),
                        parsed_items=sandbox_change_list if sandbox_result.get("success") else None,
                    ),
                )
        else:
            gaps.append("kernelcache paths missing; kernel/KEXT/sandbox diffs skipped")

        dyld_diff_path = None
        dyld_change_list: list[str] = []
        if request.old_dyld and request.new_dyld:
            dyld_args = build_dyld_diff_args(request.old_dyld, request.new_dyld)
            dyld_result = self.runner.run(dyld_args)
            dyld_diff_path = os.path.join(artifacts_dir, "dyld_diff.txt")
            if dyld_result.success:
                dyld_change_list = parse_dyld_diff_output(dyld_result.stdout)
            write_text(
                dyld_diff_path,
                self._format_tool_output(
                    "dyld_diff",
                    dyld_result.command,
                    dyld_result.stdout,
                    dyld_result.stderr,
                    parsed_items=dyld_change_list if dyld_result.success else None,
                ),
            )
            if not dyld_result.success:
                gaps.append(f"dyld diff failed: {dyld_result.stderr or 'unknown error'}")
        else:
            gaps.append("dyld_shared_cache paths missing; dyld diff skipped")

        diff_data["kext_changes"] = _dedupe_stripped(
            diff_data.get("kext_changes", []) + kext_change_list
        )
        diff_data["sandbox_changes"] = _dedupe_stripped(
            diff_data.get("sandbox_changes", []) + sandbox_change_list
        )
        diff_data["dyld_changes"] = _dedupe_stripped(dyld_change_list)
        diff_data["kernel_changes"] = _dedupe_stripped(kernel_change_list)

        notes = self._build_firmware_notes(diff_data)
        if macho_note:
            notes.append(macho_note)

        counts, security_findings = self.classifier.classify(diff_data)
        counts.cstring_count = cstring_count

        summary = FirmwareDiffSummary(
            old_firmware=request.old_version or os.path.basename(request.old_ipsw),
            new_firmware=request.new_version or os.path.basename(request.new_ipsw),
            extraction_status=self._determine_extraction_status(request),
            counts=counts,
            high_risk_changes=len(security_findings),
        )

        report_markdown_path = os.path.join(output_dir, "report.md")
        report_json_path = os.path.join(output_dir, "report.json")

        kernel_diff_path = os.path.join(artifacts_dir, "kernel_diff.txt")
        launchd_diff_path = os.path.join(artifacts_dir, "launchd_diff.txt")
        write_text(
            kernel_diff_path,
            self._format_component_diff("kernel_diff", diff_data.get("kext_changes", [])),
        )
        write_text(
            launchd_diff_path,
            self._format_component_diff("launchd_diff", diff_data.get("launchd_changes", [])),
        )

        artifacts = FirmwareDiffArtifacts(
            output_dir=output_dir,
            report_markdown=report_markdown_path,
            report_json=report_json_path,
            entitlement_diff=ent_diff_path,
            sandbox_diff=sandbox_diff_path,
            kext_diff=kext_diff_path,
            dyld_diff=dyld_diff_path,
            kernel_diff=kernel_diff_path,
            framework_diff=diff_report_path,
            launchd_diff=launchd_diff_path,
            raw_diff_dir=diff_dir,
        )

        result = FirmwareDiffResult(
            summary=summary,
            findings=security_findings,
            artifacts=artifacts,
            gaps=gaps,
            notes=notes,
        )

        report_payload = self._build_report_payload(diff_data, cstring_count)
        report_text = render_report(report_payload, notes=notes, gaps=gaps)
        write_text(report_markdown_path, report_text)
        write_json(report_json_path, report_payload)

        return result

    def _build_firmware_notes(self, diff_data: dict[str, list[str]]) -> list[str]:
        def _filter_by_keywords(items: list[str], keywords: tuple[str, ...]) -> list[str]:
            return [item for item in items if any(kw in item.lower() for kw in keywords)]

        notes: list[str] = []
        
        for component, keywords in [
            ("filesystem", ("filesystem",)),
            ("enclaveOS", ("enclaveos", "enclave"))
        ]:
            for comp_type in ("added", "modified"):
                key = f"firmware_{comp_type}"
                items = diff_data.get(key, [])
                filtered = _filter_by_keywords(items, keywords)
                if filtered:
                    counts = {t: len(_filter_by_keywords(diff_data.get(f"firmware_{t}", []), keywords)) 
                             for t in ("added", "modified")}
                    notes.append(
                        f"{component} components: "
                        f"added={counts['added']}, modified={counts['modified']} "
                        f"(see framework diff report for paths)"                    
                    )
                    break
        return notes

    def _build_report_payload(self, diff_data: dict[str, list[str]], cstring_count: int) -> dict[str, object]:
        # Gather all specialized paths so we can subtract them
        specialized_paths = set(_dedupe_stripped([
            *diff_data.get("framework_changes", []),
            *diff_data.get("kext_changes", []),
            *diff_data.get("launchd_changes", []),
        ]))

        # Gather raw userland binaries
        raw_standard = _dedupe_stripped([
            *diff_data.get("added_binaries", []),
            *diff_data.get("modified_binaries", []),
        ])

        # Filter out the duplicates 
        standard_binaries = [bin for bin in raw_standard if bin not in specialized_paths]

        base_firmware_changes = _dedupe_stripped([
            *diff_data.get("firmware_added", []),
            *diff_data.get("firmware_modified", []),
            *diff_data.get("iboot_added", []),
            *diff_data.get("iboot_modified", []),
        ])

        return {
            "summary_metrics": {
                "total_cstring_changes": cstring_count 
            },
            "boundary_changes": {
                "entitlements": diff_data.get("entitlement_changes", []),
                "sandbox": diff_data.get("sandbox_changes", []),
                "launchd": diff_data.get("launchd_changes", []),
                "kexts": diff_data.get("kext_changes", []),
            },
            "userland_changes": {
                "frameworks": diff_data.get("framework_changes", []),
                "standard_binaries": standard_binaries,
            },
            "base_firmware_changes": base_firmware_changes,
            "cstring_context": diff_data.get("cstring_changes", []),
        }

    def _filter_modified_binaries(self, items: list[str], diff_dir: str) -> list[str]:
        if not items:
            return []

        filtered: list[str] = []
        records: dict[str, tuple[str, bool]] = {}

        for item in items:
            label, link = self._split_markdown_link(item)
            if self._should_ignore_binary(label) or _is_noisy_binary(label):
                continue

            is_metadata_only = False
            if link:
                normalized_link = link.replace("\\", "/")
                if normalized_link.startswith(_MACHO_DIFF_DIRS):
                    diff_path = os.path.join(diff_dir, link)
                    if os.path.exists(diff_path) and self._macho_diff_is_metadata_only(diff_path):
                        is_metadata_only = True

            identity = self._binary_identity(label, link, diff_dir)
            existing = records.get(identity)
            if existing and existing[1] and not is_metadata_only:
                records[identity] = (item, False)
            elif not existing:
                records[identity] = (item, is_metadata_only)

        return [item for item, is_metadata_only in records.values() if not is_metadata_only]

    def _normalize_binary_list(self, items: list[str], diff_dir: str) -> list[str]:
        if not items:
            return []
        filtered: list[str] = []
        seen: set[str] = set()
        for item in items:
            label, link = self._split_markdown_link(item)
            if self._should_ignore_binary(label) or _is_noisy_binary(label):
                continue
            identity = self._binary_identity(label, link, diff_dir)
            if identity not in seen:
                seen.add(identity)
                filtered.append(item)
        return filtered

    def _binary_identity(self, label: str, link: Optional[str], diff_dir: str) -> str:
        uuid = None
        if link:
            diff_path = os.path.join(diff_dir, link)
            if os.path.exists(diff_path):
                uuid = self._extract_uuid(diff_path)
        if uuid:
            return f"uuid:{uuid}"
        normalized = label.replace("\\", "/").strip().lower()
        return f"path:{normalized}"

    def _extract_uuid(self, diff_path: str) -> Optional[str]:
        diff_text = read_text(diff_path)
        match = _UUID_RE.search(diff_text)
        if match:
            return match.group(1).upper()
        return None

    def _split_markdown_link(self, item: str) -> tuple[str, Optional[str]]:
        match = re.search(r"\[(.*?)\]\((.*?)\)", item)
        if match:
            return match.group(1), match.group(2)
        return item, None

    def _resolve_binary_candidate(self, item: str, diff_dir: str) -> tuple[str, str]:
        label, _ = self._split_markdown_link(item)
        candidate = (label or item).strip()
        if not candidate:
            return "", ""

        candidate_path = ""
        if os.path.isabs(candidate) and os.path.exists(candidate):
            candidate_path = candidate
        elif diff_dir:
            name = os.path.basename(candidate)
            if name:
                for root, _, files in os.walk(diff_dir):
                    if name in files:
                        candidate_path = os.path.join(root, name)
                        break
        return candidate, candidate_path

    def _count_cstrings_for_items(
        self,
        items: list[str],
        diff_dir: str,
        dyld_cache_path: Optional[str],
        macho_engine: MachoAnalysisEngine,
        seen: set[tuple[str, str]],
    ) -> int:
        total = 0
        for item in items:
            if not item:
                continue
            candidate, candidate_path = self._resolve_binary_candidate(item, diff_dir)
            if not candidate and not candidate_path:
                continue
            key = (candidate_path or candidate, dyld_cache_path or "")
            if key in seen:
                continue
            seen.add(key)
            res = macho_engine.count_strings(
                candidate_path or candidate,
                diff_report_root=diff_dir,
                dyld_cache_path=dyld_cache_path,
            )
            total += int(res.get("count", 0) or 0)
        return total

    def _should_ignore_binary(self, label: str) -> bool:
        if os.getenv("IPSW_DIFF_INCLUDE_METAL") == "1":
            return False
        lowered = label.lower()
        return any(hint in lowered for hint in _METAL_HINTS)

    def _macho_diff_is_metadata_only(self, diff_path: str) -> bool:
        diff_text = read_text(diff_path)
        changed_lines: list[str] = []

        for line in diff_text.splitlines():
            if not line:
                continue
            if not (line.startswith("+") or line.startswith("-")):
                continue
            if line.startswith("+++") or line.startswith("---"):
                continue
            content = line[1:].strip()
            if content:
                changed_lines.append(content)

        if not changed_lines:
            return False

        return all(self._is_metadata_line(line) for line in changed_lines)

    def _is_metadata_line(self, content: str) -> bool:
        return any(pattern.search(content) for pattern in _METADATA_ONLY_PATTERNS)

    def _timestamped_output_dir(self) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        return os.path.join(self.workspace_root, "artifacts", "firmware_diff", timestamp)

    def _determine_extraction_status(self, request: FirmwareDiffRequest) -> str:
        dyld_ready = bool(
            request.old_dyld
            and request.new_dyld
            and os.path.exists(request.old_dyld)
            and os.path.exists(request.new_dyld)
        )
        kernel_ready = bool(
            request.old_kernelcache
            and request.new_kernelcache
            and os.path.exists(request.old_kernelcache)
            and os.path.exists(request.new_kernelcache)
        )
        if dyld_ready and kernel_ready:
            return "complete"
        if dyld_ready or kernel_ready:
            return "partial"
        return "missing"

    def _build_cstring_summary(self, diff_report_text: str) -> dict[str, dict[str, list[str]]]:
        cstring_entries = extract_cstring_diffs(diff_report_text)

        # build per-item buckets
        cstring_summary: dict[str, dict[str, list[str]]] = {}
        for entry in cstring_entries:
            if ":" in entry:
                label, diff_line = entry.split(":", 1)
                label = label.strip()
            else:
                label = "unknown"
                diff_line = entry
            diff_line = diff_line.strip()
            if not diff_line:
                continue
            sign = diff_line[0]
            text = diff_line[1:].strip()
            bucket = cstring_summary.setdefault(label or "unknown", {"added": [], "removed": [], "modified": []})
            if sign == "+":
                bucket["added"].append(text)
            elif sign == "-":
                bucket["removed"].append(text)

        # mark modified if same text appears in both added & removed
        for label, buckets in cstring_summary.items():
            added_set = set(buckets["added"])
            removed_set = set(buckets["removed"])
            modified = list(added_set & removed_set)
            if modified:
                buckets["modified"].extend(modified)
                buckets["added"] = [s for s in buckets["added"] if s not in modified]
                buckets["removed"] = [s for s in buckets["removed"] if s not in modified]

        # aggregate totals
        total_added = sum(len(b["added"]) for b in cstring_summary.values())
        total_removed = sum(len(b["removed"]) for b in cstring_summary.values())
        total_modified = sum(len(b["modified"]) for b in cstring_summary.values())

        return {
            "per_file": cstring_summary,
            "totals": {"added": total_added, "removed": total_removed, "modified": total_modified},
            "raw_entries": cstring_entries,
        }
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
    extract_symbol_diffs,
    parse_diff_markdown,
    parse_dyld_diff_output,
    parse_simple_list_output,
    strip_ansi,
)
from ipsw_service.agents.macho_analysis_engine import MachoAnalysisEngine
from ipsw_service.reporting import render_report
from ipsw_service.utils import ensure_dir, list_files, read_text, write_json, write_text

# define noise filters for non-analyzable binaries
IGNORE_PATTERNS = [
    r"\.metallib$",                       # metal compiled shaders
    r"\.g18p(?:_a0)?$",                   # apple Silicon ISP microcode
    r"\.appex/",                          # uI Extensions (Widgets, watch faces)
    r"/VideoProcessors/",                 # video processing bundles
    r"/NanoTimeKit/FaceBundles/",
    r"/Applications/Kaleidoscope",        # specific noisy apps
    r"CoreImage\.framework.*_bin"         # precompiled CoreImage archives
]

_METADATA_ONLY_PATTERNS = (
    re.compile(r"^UUID:\s*", re.IGNORECASE),
    re.compile(r"^LC_BUILD_VERSION\b", re.IGNORECASE),
    re.compile(r"^LC_CODE_SIGNATURE\b", re.IGNORECASE),
    re.compile(r"^__LINKEDIT\b", re.IGNORECASE),
    re.compile(r"^__TEXT\.__info_plist\b", re.IGNORECASE),
    re.compile(r"^sha256:\s*", re.IGNORECASE),
    re.compile(r"^sha1:\s*", re.IGNORECASE),
    # Mach-O version strings are purely compile-time metadata (e.g. "386.231.1.0.0")
    re.compile(r"^\d+(?:\.\d+){2,}$"),
    # Aggregate counts change on every recompile; only symbol/CString *names* matter
    re.compile(r"^(Functions|Symbols|CStrings):\s+\d+", re.IGNORECASE),
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
        def _extract_version(path: str) -> str:
            import os
            base = os.path.basename(path)
            parts = base.split('_')
            if len(parts) >= 3:
                return f"{parts[1]}_{parts[2]}".replace('.', '_')
            return base.replace('.ipsw', '')

        output_dir = request.output_dir or self._timestamped_output_dir()
        ensure_dir(output_dir)
        old_vs_new = f"{_extract_version(request.old_ipsw)}_vs_{_extract_version(request.new_ipsw)}"
        diff_dir = ensure_dir(os.path.join(output_dir, "diff", old_vs_new))
        ent_dir = ensure_dir(os.path.join(output_dir, "entitlements"))
        artifacts_dir = ensure_dir(os.path.join(output_dir, "artifacts"))

        gaps: list[str] = []
        low_memory = os.getenv("IPSW_DIFF_LOW_MEMORY") == "1"

        import tempfile
        temp_diff_dir_obj = tempfile.TemporaryDirectory()
        temp_diff_dir = temp_diff_dir_obj.name

        diff_result = self.framework_diff_engine.diff_firmware(
            request.old_ipsw,
            request.new_ipsw,
            temp_diff_dir,
            include_fw=request.include_fw_components,
            include_launchd=request.include_launchd,
            include_strs=request.include_strs,
            markdown=True,
            low_memory=low_memory,
            clean=request.clean_cache,
        )
        if not diff_result.get("success"):
            gaps.append(f"ipsw diff failed: {diff_result.get('stderr') or 'unknown error'}")

        diff_report_path = diff_result.get("markdown_report") or None
        diff_report_text = ""
        if diff_report_path and os.path.exists(diff_report_path):
            actual_diff_dir = os.path.dirname(diff_report_path)
            diff_report_text = self._consolidate_readme(actual_diff_dir, diff_report_path)

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
            "symbol_changes": [],
        }
        diff_report_root = temp_diff_dir
        
        if diff_report_text:
            diff_data["cstring_changes"] = extract_cstring_diffs(diff_report_text)
            diff_data["symbol_changes"] = extract_symbol_diffs(diff_report_text)
        macho_note = None
        if diff_report_path:
            # ipsw diff now inlines MachO diffs directly into the README.md, so the MACHOS dir is no longer generated
            if diff_report_text and "## MachO" not in diff_report_text and "## Mach-O" not in diff_report_text:
                macho_note = (
                    "MachO diff artifacts missing; filesystem diff likely failed or was skipped."
                )
                gaps.append(macho_note)

        added_raw = diff_data.get("added_binaries", [])
        modified_raw = diff_data.get("modified_binaries", [])

        diff_data["added_binaries"] = self._normalize_binary_list(added_raw, diff_report_root)
        filtered_modified = self._filter_modified_binaries(modified_raw, diff_report_root)
        diff_data["modified_binaries"] = filtered_modified

        dyld_diff_path = None
        dyld_change_list: list[str] = []
        if request.old_dyld and request.new_dyld:
            dyld_args = build_dyld_diff_args(request.old_dyld, request.new_dyld)
            dyld_result = self.runner.run(dyld_args)
            dyld_diff_path = os.path.join(artifacts_dir, "dyld_diff.txt")
            if dyld_result.success:
                dyld_change_list = parse_dyld_diff_output(dyld_result.stdout)
                
                filtered_dyld_change_list = self._filter_modified_binaries(dyld_change_list, diff_report_root)
                diff_data["framework_changes"] = list(dict.fromkeys(
                    diff_data.get("framework_changes", []) + filtered_dyld_change_list
                ))
                diff_data["modified_binaries"] = list(dict.fromkeys(
                    diff_data.get("modified_binaries", []) + filtered_dyld_change_list
                ))
                
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


        # compute explicit cstring count across candidate binaries
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

        # Save the inlined README report
        readme_output_path = os.path.join(diff_dir, "README.md")

        artifacts = FirmwareDiffArtifacts(
            output_dir=output_dir,
            report_json=report_json_path,
            entitlement_diff=ent_diff_path,
            sandbox_diff=sandbox_diff_path,
            kext_diff=kext_diff_path,
            dyld_diff=dyld_diff_path,
            kernel_diff=kernel_diff_path,
            framework_diff=readme_output_path,
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

        gaps = list(dict.fromkeys(gaps))
        notes = list(dict.fromkeys([n for n in notes if n not in gaps]))

        report_payload = self._build_report_payload(diff_data, cstring_count, gaps, notes, security_findings)
        
        md_content = []
        if gaps:
            md_content.append("## Gaps & Warnings\n")
            for g in gaps:
                md_content.append(f"- {g}")
            md_content.append("\n")
            
        if notes:
            md_content.append("## Analysis Notes\n")
            for n in notes:
                md_content.append(f"- {n}")
            md_content.append("\n")
            
        if security_findings:
            md_content.append("## Security Findings\n")
            for f in security_findings:
                md_content.append(f"- **{f.title}**: {f.impact}")
            md_content.append("\n")
            
        if md_content:
            diff_report_text += "\n\n" + "\n".join(md_content)
        
        # Save the inlined README report
        write_text(readme_output_path, diff_report_text)
        
        write_json(report_json_path, report_payload)

        # Cleanup the temp directory
        temp_diff_dir_obj.cleanup()

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

    def _build_report_payload(
        self, 
        diff_data: dict[str, list[str]], 
        cstring_count: int,
        gaps: list[str],
        notes: list[str],
        security_findings: list[Finding]
    ) -> dict[str, object]:
        # gather all specialized paths so we can subtract them
        specialized_paths = set(_dedupe_stripped([
            *diff_data.get("framework_changes", []),
            *diff_data.get("kext_changes", []),
            *diff_data.get("launchd_changes", []),
        ]))

        # gather raw userland binaries
        raw_standard = _dedupe_stripped([
            *diff_data.get("added_binaries", []),
            *diff_data.get("modified_binaries", []),
        ])

        # filter out the duplicates 
        standard_binaries = [bin for bin in raw_standard if bin not in specialized_paths]

        base_firmware_changes = _dedupe_stripped([
            *diff_data.get("firmware_added", []),
            *diff_data.get("firmware_modified", []),
            *diff_data.get("iboot_added", []),
            *diff_data.get("iboot_modified", []),
        ])

        analysis_notes = {"notes": notes}
        if gaps != notes:
            analysis_notes["gaps"] = gaps

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
            "symbol_context": diff_data.get("symbol_changes", []),
            "analysis_notes": analysis_notes
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
            return True

        return all(self._is_metadata_line(line) for line in changed_lines)

    def _is_metadata_line(self, content: str) -> bool:
        return any(pattern.search(content) for pattern in _METADATA_ONLY_PATTERNS)

    def _macho_diff_text_is_metadata_only(self, diff_text: str) -> bool:
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
            return True

        return all(self._is_metadata_line(line) for line in changed_lines)

    def _consolidate_readme(self, diff_dir: str, readme_path: str) -> str:
        if not os.path.exists(readme_path):
            return ""

        import re

        # ---------------------------------------------------------------------------
        # _emit_inline_entry: shared helper that filters and emits one already-parsed
        # inline diff entry (either from a sidecar file OR from an inline block in
        # the raw ipsw README).
        #
        # Returns a list of output lines to append, or [] if the entry should be
        # skipped (metadata-only, noisy binary, or no real code changes).
        #
        # strict=True  (default, used everywhere): require at least one non-metadata
        #   +/- line, i.e. an actual section-size change, symbol name, CString, etc.
        #   Pure recompile bumps (version string + UUID only) are excluded.
        # strict=False (fallback): keep entries that have any +/- line at all.
        #   Not currently used but retained for forward-compatibility.
        # ---------------------------------------------------------------------------
        def _emit_inline_entry(
            bin_name: str,
            original_path: str,
            inner_lines: list[str],
            strict: bool = True,
        ) -> list[str]:
            if self._should_ignore_binary(original_path) or _is_noisy_binary(original_path):
                return []

            # ---------------------------------------------------------------
            # Pre-process: strip sha256/sha1 hash suffixes from section lines
            # (e.g. "__TEXT.__text: 0xe0f8 sha256:abc…" → "__TEXT.__text: 0xe0f8")
            # ---------------------------------------------------------------
            cleaned_lines: list[str] = []
            for d_line in inner_lines:
                stripped = d_line.strip()
                if stripped.startswith("-sha") or stripped.startswith("+sha") or stripped in ("sha256:", "sha1:"):
                    continue
                if " sha256:" in d_line:
                    d_line = d_line.split(" sha256:")[0]
                elif " sha1:" in d_line:
                    d_line = d_line.split(" sha1:")[0]
                cleaned_lines.append(d_line)

            # ---------------------------------------------------------------
            # Collapse identical pairs using run-based grouping.
            #
            # ipsw formats changed blocks as ALL minus lines first, then ALL
            # plus lines (not interleaved adjacent pairs), so we collect
            # contiguous minus-runs and the immediately following plus-run,
            # then pair them by position.  When both sides have the same
            # content after sha-stripping (same section size, different hash)
            # the pair collapses to a context line — no real change.
            # ---------------------------------------------------------------
            consolidated_lines: list[str] = []
            ci = 0
            while ci < len(cleaned_lines):
                c_line = cleaned_lines[ci]
                if c_line.startswith("-") and not c_line.startswith("---"):
                    minus_run: list[str] = []
                    while ci < len(cleaned_lines) and cleaned_lines[ci].startswith("-") and not cleaned_lines[ci].startswith("---"):
                        minus_run.append(cleaned_lines[ci])
                        ci += 1
                    plus_run: list[str] = []
                    while ci < len(cleaned_lines) and cleaned_lines[ci].startswith("+") and not cleaned_lines[ci].startswith("+++"):
                        plus_run.append(cleaned_lines[ci])
                        ci += 1
                    max_len = max(len(minus_run), len(plus_run))
                    for j in range(max_len):
                        if j < len(minus_run) and j < len(plus_run):
                            m_content = minus_run[j][1:]
                            p_content = plus_run[j][1:]
                            if m_content == p_content:
                                consolidated_lines.append(" " + m_content)
                            else:
                                consolidated_lines.append(minus_run[j])
                                consolidated_lines.append(plus_run[j])
                        elif j < len(minus_run):
                            consolidated_lines.append(minus_run[j])
                        else:
                            consolidated_lines.append(plus_run[j])
                else:
                    consolidated_lines.append(c_line)
                    ci += 1

            has_real_diff = False
            has_any_diff = False
            for dl in consolidated_lines:
                if not (dl.startswith("+") or dl.startswith("-")):
                    continue
                if dl.startswith("+++") or dl.startswith("---"):
                    continue
                content = dl[1:].strip()
                if not content:
                    continue
                has_any_diff = True
                if not self._is_metadata_line(content):
                    has_real_diff = True
                    if strict:
                        break  # found a real code change — keep early

            if strict:
                if not has_real_diff:
                    return []
            else:
                if not has_any_diff:
                    return []

            out: list[str] = []
            out.append(f"#### {bin_name}")
            out.append("")
            out.append(f">  `{original_path}`")
            out.append("")
            out.append("```diff")
            for d_line in consolidated_lines:
                out.append(d_line)
            out.append("```")
            out.append("")
            return out

        # ---------------------------------------------------------------------------
        # parse_lines: recursively processes the raw ipsw README lines.
        #
        # Handles three cases:
        #  1. Index links  – e.g. "- [View N files](DYLIBS/foo.md)" → recurse
        #  2. Sidecar links – e.g. "- [/path/to/bin](DYLIBS/bin.md)" → inline
        #  3. Inline entries – ipsw has already inlined the diff blocks directly
        #     into the README (no sidecar files).  Detected by the pattern:
        #       #### BinaryName
        #       > `/full/path`
        #       ```diff
        #       …
        #       ```
        #     These are accumulated and filtered the same as sidecar entries.
        # ---------------------------------------------------------------------------
        def parse_lines(lines: list[str], current_prefix: str = "", in_dsc: bool = False) -> list[str]:
            out: list[str] = []

            # Strict filtering is applied in both MachO and DSC sections.
            # An entry must have at least one real (non-metadata) +/- line to be
            # included.  Start as True; updated by ## section headings.
            in_dsc_section: bool = in_dsc if in_dsc else True

            # State machine for inline entries
            inline_name: str = ""
            inline_path: str = ""
            inline_inner: list[str] = []
            inline_in_block = False
            inline_found_block = False
            # Whether we are currently accumulating an inline entry
            # (detected when we see "#### Name" followed by "> `/path`")
            pending_inline = False

            i = 0
            while i < len(lines):
                line = lines[i]

                # -----------------------------------------------------------------
                # Strict filtering applies everywhere (both ## MachO filesystem
                # and ## DSC dylibs): only include entries where at least one +/-
                # line is NOT pure metadata (version string, UUID, aggregate
                # count).  Entries whose only changes are a recompile bump are
                # not meaningful.
                # ---------------------------------------------------------------------------
                # (in_dsc_section is kept for forward-compatibility if we ever
                # need to distinguish the two sections again.)
                # -----------------------------------------------------------------
                if line.startswith("## "):
                    lowered_h2 = line[3:].strip().lower()
                    if "dsc" in lowered_h2:
                        in_dsc_section = True
                    elif "macho" in lowered_h2 or "mach-o" in lowered_h2:
                        in_dsc_section = True  # strict everywhere

                # -----------------------------------------------------------------
                # Skip raw HTML structural tags from ipsw output
                # -----------------------------------------------------------------
                if line.strip() in ("<details>", "</details>") or line.strip().startswith("<summary>"):
                    i += 1
                    continue

                # -----------------------------------------------------------------
                # If we're inside an inline diff block, collect content lines
                # -----------------------------------------------------------------
                if inline_in_block:
                    if line.strip().startswith("```"):
                        # End of the diff fence → flush the accumulated entry
                        inline_in_block = False
                        inline_found_block = True
                        result_lines = _emit_inline_entry(inline_name, inline_path, inline_inner, strict=in_dsc_section)
                        out.extend(result_lines)
                        # Reset state
                        inline_name = ""
                        inline_path = ""
                        inline_inner = []
                        inline_found_block = False
                        pending_inline = False
                    else:
                        inline_inner.append(line)
                    i += 1
                    continue

                # -----------------------------------------------------------------
                # Detect the start of an inline diff block after ">  `/path`"
                # -----------------------------------------------------------------
                if pending_inline and line.strip().startswith("```diff"):
                    inline_in_block = True
                    i += 1
                    continue

                # Detect ">  `/path/to/binary`" line — part of an inline entry
                path_match = re.match(r">\s+`([^`]+)`", line)
                if path_match and inline_name:
                    inline_path = path_match.group(1)
                    pending_inline = True
                    i += 1
                    continue

                if inline_name and not line.strip():
                    i += 1
                    continue

                if pending_inline and line.strip() and not line.strip().startswith("```"):
                    # buffered name/path didn't lead to a diff block — pass through
                    out.append(f"#### {inline_name}")
                    if inline_path:
                        out.append(f">  `{inline_path}`")
                    pending_inline = False
                    inline_name = ""
                    inline_path = ""

                # Silently swallow empty lines while waiting for a pending diff fence
                if pending_inline and not line.strip():
                    i += 1
                    continue

                # Detect "#### BinaryName" — potential start of an inline entry
                h4_match = re.match(r"####\s+(.+)", line)
                if h4_match:
                    h4_title = h4_match.group(1).strip()
                    is_section_header = (
                        "⬆️" in h4_title
                        or "🆕" in h4_title
                        or "Removed" in h4_title
                        or "Updated" in h4_title
                        or "Added" in h4_title
                    )
                    if not is_section_header:
                        # if the next non-empty line is "> `/path`"
                        # this is the start of an inline entry
                        j = i + 1
                        while j < len(lines) and not lines[j].strip():
                            j += 1
                        if j < len(lines) and re.match(r">\s+`[^`]+`", lines[j]):
                            # Flush any un-flushed pending
                            inline_name = h4_title
                            inline_path = ""
                            inline_inner = []
                            inline_in_block = False
                            inline_found_block = False
                            pending_inline = False
                            i += 1
                            continue

                # suppress stray raw ipsw section banners 
                raw_dylibs_banner = re.match(
                    r"##\s+Dylibs\s*[—–-]\s*(Updated|Added|Removed)\s*\(\d+\)", line
                )
                if raw_dylibs_banner:
                    i += 1
                    continue

                # index links  e.g. "- [View N files](DYLIBS/foo.md)"
                index_match = re.match(
                    r"-\s+\[View \d+ .*?files\]\((DYLIBS/.*\.md|MACHOS/.*\.md)\)", line
                )
                if index_match:
                    index_rel_path = index_match.group(1)
                    index_path = os.path.join(diff_dir, index_rel_path)
                    if os.path.exists(index_path):
                        index_lines = read_text(index_path).splitlines()
                        new_prefix = os.path.dirname(index_rel_path)
                        out.extend(parse_lines(index_lines, current_prefix=new_prefix, in_dsc=in_dsc_section))
                    i += 1
                    continue

                # sidecar links  e.g. "- [/path/to/bin](DYLIBS/bin.md)"
                link_match = re.match(r"-\s+\[(.*?)\]\((.*?\.md)\)", line)
                if link_match:
                    bin_name = os.path.basename(link_match.group(1))
                    sidecar_raw = link_match.group(2)

                    if not (sidecar_raw.startswith("MACHOS/") or sidecar_raw.startswith("DYLIBS/")):
                        sidecar_rel = os.path.join(current_prefix, sidecar_raw)
                    else:
                        sidecar_rel = sidecar_raw

                    sidecar_path = os.path.join(diff_dir, sidecar_rel)
                    original_path = link_match.group(1)

                    if os.path.exists(sidecar_path):
                        diff_text = read_text(sidecar_path)

                        inner: list[str] = []
                        in_b = False
                        found_b = False
                        for d_line in diff_text.splitlines():
                            if d_line.strip().startswith("```"):
                                if in_b:
                                    in_b = False
                                else:
                                    in_b = True
                                    found_b = True
                                continue
                            if in_b:
                                inner.append(d_line)

                        if not found_b:
                            for d_line in diff_text.splitlines():
                                if d_line.startswith("## ") or d_line.startswith("> "):
                                    continue
                                inner.append(d_line)

                        result_lines = _emit_inline_entry(bin_name, original_path, inner, strict=in_dsc_section)
                        out.extend(result_lines)
                    i += 1
                    continue

                out.append(line)
                i += 1

            return out

        lines = read_text(readme_path).splitlines()
        consolidated = parse_lines(lines)

        final_result: list[str] = []
        section_lines: list[str] = []
        current_header = ""

        def finalize_section(header: str, s_lines: list[str]) -> None:
            if "Removed" in header:
                return

            count = sum(1 for sl in s_lines if sl.startswith(">  `"))
            if count > 0:
                # preserve the original heading level from the raw ipsw README.
                # MachO filesystem uses ### and DSC dylibs use #### 
                new_header = re.sub(r"\(\d+\)", f"({count})", header)
                final_result.append(new_header)
                final_result.append("")
                final_result.append("<details>")
                if "Added" in header:
                    final_result.append("  <summary><i>View Added</i></summary>")
                else:
                    final_result.append("  <summary><i>View Updated</i></summary>")
                final_result.append("")
                final_result.extend(s_lines)
                final_result.append("</details>")
                final_result.append("")

        for line in consolidated:
            is_header = False
            if (
                (line.startswith("## ") or line.startswith("### ") or line.startswith("#### "))
                and "Removed" in line
            ):
                is_header = True
            elif (
                line.startswith("### ⬆️ Updated (")
                or line.startswith("### 🆕 Added (")
                or line.startswith("#### ⬆️ Updated (")
                or line.startswith("#### 🆕 Added (")
            ):
                is_header = True

            if is_header:
                if current_header:
                    finalize_section(current_header, section_lines)
                current_header = line
                section_lines = []
            else:
                if current_header:
                    if line.startswith("- `/"):
                        continue
                    # top-level headings that appear after the section
                    # entries (e.g. ### iBoot, ## DSC) are structural  
                    # close the current section and flow to final_result
                    if line.startswith("## ") or line.startswith("### "):
                        finalize_section(current_header, section_lines)
                        current_header = ""
                        section_lines = []
                        final_result.append(line)
                        continue
                    section_lines.append(line)
                else:
                    if line.startswith("- `/"):
                        continue
                    final_result.append(line)

        if current_header:
            finalize_section(current_header, section_lines)

        result = "\n".join(final_result)
        result = result.replace("## Inputs\n", "## IPSWs\n")
        return result

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

        total_added = sum(len(b["added"]) for b in cstring_summary.values())
        total_removed = sum(len(b["removed"]) for b in cstring_summary.values())
        total_modified = sum(len(b["modified"]) for b in cstring_summary.values())

        return {
            "per_file": cstring_summary,
            "totals": {"added": total_added, "removed": total_removed, "modified": total_modified},
            "raw_entries": cstring_entries,
        }
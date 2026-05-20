from __future__ import annotations

import os
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Optional

from ipsw_service.agents.framework_diff_engine import FrameworkDiffEngine
from ipsw_service.agents.kernel_analysis_engine import KernelAnalysisEngine
from ipsw_service.classifiers import ChangeClassifier, serialize_findings
from ipsw_service.cli import IpswCliRunner, build_dyld_diff_args
from ipsw_service.models import (
    DiffCounts,
    FirmwareDiffArtifacts,
    FirmwareDiffRequest,
    FirmwareDiffResult,
    FirmwareDiffSummary,
)
from ipsw_service.parsing import parse_diff_markdown, parse_simple_list_output
from ipsw_service.reporting import render_report
from ipsw_service.utils import ensure_dir, list_files, read_text, write_json, write_text

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

    def _format_tool_output(self, label: str, command: str, stdout: str, stderr: str) -> str:
        lines = [f"[{label}]", f"command: {command}"]
        if stdout:
            lines.append("stdout:")
            lines.append(stdout.rstrip())
        if stderr:
            lines.append("stderr:")
            lines.append(stderr.rstrip())
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
            markdown=True,
            low_memory=low_memory,
        )
        if not diff_result.get("success"):
            gaps.append(f"ipsw diff failed: {diff_result.get('stderr') or 'unknown error'}")

        diff_report_path = diff_result.get("markdown_report")
        diff_json_path = diff_result.get("json_report")
        diff_report_text = read_text(diff_report_path) if diff_report_path else ""
        diff_data = parse_diff_markdown(diff_report_text) if diff_report_text else {
            "added_binaries": [],
            "removed_binaries": [],
            "modified_binaries": [],
            "entitlement_changes": [],
            "sandbox_changes": [],
            "kext_changes": [],
            "framework_changes": [],
            "launchd_changes": [],
        }

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
                write_text(
                    kext_diff_path,
                    self._format_tool_output(
                        "kext_diff",
                        kext_result.get("command", ""),
                        kext_result.get("diff", ""),
                        kext_result.get("stderr", ""),
                    ),
                )
                if not kext_result.get("success"):
                    gaps.append(f"kext diff failed: {kext_result.get('stderr') or 'unknown error'}")
                else:
                    kext_change_list = parse_simple_list_output(kext_result.get("diff", ""))
            if request.include_sandbox:
                sandbox_result = self.kernel_engine.diff_sandbox_ops(request.old_kernelcache, request.new_kernelcache)
                sandbox_diff_path = os.path.join(artifacts_dir, "sandbox_diff.txt")
                write_text(
                    sandbox_diff_path,
                    self._format_tool_output(
                        "sandbox_diff",
                        sandbox_result.get("command", ""),
                        sandbox_result.get("diff", ""),
                        sandbox_result.get("stderr", ""),
                    ),
                )
                if not sandbox_result.get("success"):
                    gaps.append(f"sandbox diff failed: {sandbox_result.get('stderr') or 'unknown error'}")
                else:
                    sandbox_change_list = parse_simple_list_output(sandbox_result.get("diff", ""))
        else:
            gaps.append("kernelcache paths missing; kernel/KEXT/sandbox diffs skipped")

        dyld_diff_path = None
        dyld_change_list: list[str] = []
        if request.old_dyld and request.new_dyld:
            dyld_args = build_dyld_diff_args(request.old_dyld, request.new_dyld)
            dyld_result = self.runner.run(dyld_args)
            dyld_diff_path = os.path.join(artifacts_dir, "dyld_diff.txt")
            write_text(
                dyld_diff_path,
                self._format_tool_output(
                    "dyld_diff",
                    dyld_result.command,
                    dyld_result.stdout,
                    dyld_result.stderr,
                ),
            )
            if dyld_result.success:
                dyld_change_list = parse_simple_list_output(dyld_result.stdout)
            else:
                gaps.append(f"dyld diff failed: {dyld_result.stderr or 'unknown error'}")
        else:
            gaps.append("dyld_shared_cache paths missing; dyld diff skipped")

        diff_data["kext_changes"] = diff_data.get("kext_changes", []) + kext_change_list
        diff_data["sandbox_changes"] = diff_data.get("sandbox_changes", []) + sandbox_change_list
        diff_data["dyld_changes"] = dyld_change_list
        diff_data["kernel_changes"] = kernel_change_list

        counts, security_findings = self.classifier.classify(diff_data)

        findings = security_findings
        high_risk_changes = len(security_findings)

        extraction_status = self._determine_extraction_status(request)

        summary = FirmwareDiffSummary(
            old_firmware=request.old_version or os.path.basename(request.old_ipsw),
            new_firmware=request.new_version or os.path.basename(request.new_ipsw),
            extraction_status=extraction_status,
            counts=counts,
            high_risk_changes=high_risk_changes,
        )

        report_markdown_path = os.path.join(output_dir, "report.md")
        report_json_path = os.path.join(output_dir, "report.json")
        binary_inventory_path = os.path.join(output_dir, "binary_inventory.json")
        symbol_metadata_path = os.path.join(output_dir, "symbol_metadata.json")

        write_json(binary_inventory_path, {
            "added": diff_data.get("added_binaries", []),
            "removed": diff_data.get("removed_binaries", []),
            "modified": diff_data.get("modified_binaries", []),
        })

        write_json(symbol_metadata_path, {
            "dyld_changes": diff_data.get("dyld_changes", []),
            "kernel_changes": diff_data.get("kernel_changes", []),
        })

        artifacts = FirmwareDiffArtifacts(
            output_dir=output_dir,
            report_markdown=report_markdown_path,
            report_json=report_json_path,
            binary_inventory=binary_inventory_path,
            entitlement_diff=ent_diff_path,
            sandbox_diff=sandbox_diff_path,
            kext_diff=kext_diff_path,
            dyld_diff=dyld_diff_path,
            kernel_diff=None,
            framework_diff=diff_report_path,
            diff_json=diff_json_path,
            launchd_diff=None,
            raw_diff_dir=diff_dir,
            symbol_metadata=symbol_metadata_path,
        )

        result = FirmwareDiffResult(
            summary=summary,
            findings=findings,
            artifacts=artifacts,
            gaps=gaps,
            notes=[],
        )

        report_text = render_report(result)
        write_text(report_markdown_path, report_text)
        write_json(report_json_path, {
            "summary": asdict(summary),
            "findings": [asdict(f) for f in findings],
            "artifacts": asdict(artifacts),
            "gaps": gaps,
        })

        return result

    def _timestamped_output_dir(self) -> str:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        return os.path.join(self.workspace_root, "artifacts", "firmware_diff", timestamp)

    def _determine_extraction_status(self, request: FirmwareDiffRequest) -> str:
        dyld_ready = bool(request.old_dyld and request.new_dyld and os.path.exists(request.old_dyld) and os.path.exists(request.new_dyld))
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
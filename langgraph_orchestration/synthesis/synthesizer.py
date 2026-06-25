import re
import json
from typing import Optional
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.core.state_utils import StateManager

class Synthesizer:
    """Intelligently synthesizes multi-branch orchestration outputs."""

    def __init__(self, state: AgentState):
        self.state = state
        self.domain_outputs = {}
        self.execution_summary = []
        self.key_findings = []

    def _extract_key_findings(self, text: str, domain: str) -> list[str]:
        findings = []
        
        # extract numbered lists
        numbered = re.findall(r'^\d+\.\s+(.+?)$', text, re.MULTILINE)
        findings.extend(numbered[:5])
        
        # extract bold/emphasized items
        emphasized = re.findall(r'\*\*(.+?)\*\*', text)
        findings.extend(emphasized[:3])
        
        # extract headers with content
        headers = re.findall(r'#{1,3}\s+(.+?)(?:\n|$)', text)
        findings.extend(headers[:3])
        
        return list(dict.fromkeys(findings))[:5]

    def _extract_ipsw_targets(self) -> list[dict]:
        """Extract target devices/versions from firmware_locator output"""
        locator_output = self.state.intermediate_outputs.get("firmware_locator", "")
        if not locator_output:
            return []
        
        try:
            data = json.loads(locator_output)
            if isinstance(data, dict) and "targets" in data:
                return data.get("targets", [])
        except (json.JSONDecodeError, ValueError):
            pass
        
        # fallback: extract from text
        targets = []
        for match in re.finditer(r'version["\s:]+([0-9.]+)["\s,]*build["\s:]+([A-Z0-9]+)', locator_output):
            targets.append({
                "version": match.group(1),
                "build": match.group(2),
            })
        return targets

    def _count_extracted_artifacts(self) -> dict:
        """Count dyld and kernel artifacts extracted"""
        extractor_output = self.state.intermediate_outputs.get("ipsw_extractor", "")
        if not extractor_output:
            return {"dyld": 0, "kernel": 0}
        
        dyld_count = len(re.findall(r'dyld_shared_cache', extractor_output))
        kernel_count = len(re.findall(r'kernelcache', extractor_output))
        
        return {"dyld": dyld_count, "kernel": kernel_count}

    def _extract_reverse_engineering_summary(self) -> str:
        sections = []
        
        # workflow stage summary
        targets = self._extract_ipsw_targets()
        artifacts = self._count_extracted_artifacts()
        
        sections.append("## Reverse Engineering Workflow Summary\n")
        
        if targets:
            sections.append("### Targets Processed")
            for target in targets:
                version = target.get("version", "unknown")
                build = target.get("build", "unknown")
                device = target.get("device", "iPhone")
                sections.append(f"- {device} Version {version} (Build {build})")
        
        if artifacts["dyld"] > 0 or artifacts["kernel"] > 0:
            sections.append("\n### Artifacts Extracted")
            if artifacts["dyld"] > 0:
                sections.append(f"- dyld_shared_cache: {artifacts['dyld']} files")
            if artifacts["kernel"] > 0:
                sections.append(f"- kernelcache: {artifacts['kernel']} files")
        
        # tool execution status
        downloader_output = self.state.intermediate_outputs.get("firmware_downloader", "")
        if "Confirmed local artifacts" in downloader_output:
            count_match = re.search(r'Confirmed local artifacts:\s+(\d+)', downloader_output)
            if count_match:
                count = count_match.group(1)
                sections.append(f"\n### Download Status")
                sections.append(f"✓ Successfully downloaded {count} firmware artifacts")
        
        analysis_keys = [
            "firmware_diff_report",
            "firmware_analysis",
        ]
        
        analysis_findings = []
        for key in analysis_keys:
            output = self.state.intermediate_outputs.get(key, "").strip()
            if output:
                analysis_findings.extend(self._extract_key_findings(output, key))
        
        if analysis_findings:
            sections.append("\n### Key Findings")
            for finding in analysis_findings[:5]:
                if len(finding) > 10:
                    sections.append(f"- {finding}")
        
        return "\n".join(sections)

    def _deduplicate_findings(self, findings1: list[str], findings2: list[str]) -> list[str]:
        combined = findings1 + findings2
        unique = []
        seen = set()
        
        for finding in combined:
            normalized = finding.lower().strip()
            if normalized not in seen and len(normalized) > 5:
                seen.add(normalized)
                unique.append(finding)
        
        return unique

    def _build_domain_section(self, domain: str, content: str) -> str:
        if not content or not content.strip():
            return ""
        
        domain_names = {
            "software_dev": "Software Development Analysis",
            "reverse_engineering": "Reverse Engineering Analysis",
        }
        
        title = domain_names.get(domain, domain.replace("_", " ").title())
        return f"\n## {title}\n{content.strip()}"

    def _build_cross_domain_synthesis(self) -> str:
        sections = []
        
        dev_output = self.state.branch_outputs.get("software_dev", "")
        re_output = self.state.branch_outputs.get("reverse_engineering", "")
        
        if dev_output and re_output:
            sections.append("\n## Cross-Domain Analysis\n")
            sections.append(
                "Both software development and reverse engineering workflows were executed. "
                "This analysis combines architectural insights with platform-level changes."
            )
            
            dev_findings = self._extract_key_findings(dev_output, "software_dev")
            re_findings = self._extract_key_findings(re_output, "reverse_engineering")
            
            combined = self._deduplicate_findings(dev_findings, re_findings)
            if combined:
                sections.append("\n### Key Findings Across Domains")
                for i, finding in enumerate(combined[:5], 1):
                    sections.append(f"{i}. {finding}")
        
        return "\n".join(sections)

    def _build_execution_summary(self) -> str:
        if not self.state.agent_chain:
            return ""
        
        sections = ["\n## Execution Summary\n"]
        
        domains_executed = self.state.execution_domains
        if domains_executed:
            section_str = ", ".join(d.replace("_", " ").title() for d in domains_executed)
            sections.append(f"**Domains:** {section_str}")
        
        tool_count = len(set(r.tool_name for r in self.state.tool_results if r.success))
        if tool_count > 0:
            sections.append(f"**Tools Executed:** {tool_count}")
        
        # tool activity details
        if self.state.tool_results:
            success_count = sum(1 for r in self.state.tool_results if r.success)
            fail_count = len(self.state.tool_results) - success_count
            sections.append(f"**Tool Results:** {success_count} successful, {fail_count} failed")
        
        if self.state.dev_iteration > 0:
            sections.append(f"**Code Generation Iterations:** {self.state.dev_iteration}")
        if self.state.dev_test_passed:
            sections.append("**Latest Test Status:** PASS ✓")
        
        if self.state.analysis_notes:
            sections.append(f"\n### Analysis Notes")
            for note in self.state.analysis_notes[-3:]:
                sections.append(f"- {note}")
        
        return "\n".join(sections)

    def _build_tool_activity_summary(self) -> str:
        """Build a summary of tool activities."""
        if not self.state.tool_results:
            return ""
        
        sections = ["\n## Tool Activity Summary\n"]
        
        # group by tool name
        tool_groups = {}
        for result in self.state.tool_results:
            if result.tool_name not in tool_groups:
                tool_groups[result.tool_name] = {"success": 0, "failed": 0, "results": []}
            
            status = "success" if result.success else "failed"
            tool_groups[result.tool_name][status] += 1
            tool_groups[result.tool_name]["results"].append(result)
        
        for tool_name, data in sorted(tool_groups.items()):
            success_count = data["success"]
            fail_count = data["failed"]
            status_str = f"[{success_count} OK, {fail_count} ERR]" if fail_count > 0 else f"[{success_count} OK]"
            sections.append(f"### {tool_name} {status_str}")
            
            # include brief output from most recent result
            if data["results"]:
                recent = data["results"][-1]
                output = recent.output or recent.error or "No output"
                brief = output[:200] + "..." if len(output) > 200 else output
                sections.append(f"{brief}\n")
        
        return "\n".join(sections)

    def _build_recommendations(self) -> str:
        sections = []
        
        # check for failures
        failures = [r for r in self.state.tool_results if not r.success]
        if failures:
            sections.append("\n## Recommendations\n")
            sections.append("**Issues Encountered:**")
            for failure in failures[:3]:
                sections.append(f"- {failure.tool_name}: {failure.error}")
            sections.append("\nReview the tool activity section for details and retry as needed.")
        
        # check for incomplete workflows
        has_synthesis = any("synthesize" in step.lower() for step in self.state.agent_chain)
        if not has_synthesis:
            sections.append("\n**Note:** Workflow did not complete full synthesis. Check tool results above.")
        
        return "\n".join(sections)

    def synthesize(self) -> str:
        re_report = self.state.intermediate_outputs.get("firmware_diff_report", "")
        if re_report and self.state.execution_domains == ["reverse_engineering"]:
            return StateManager.sanitize_output(re_report)

        sections = []
        
        sections.append("# Orchestration Analysis Result\n")
        sections.append(f"**User Request:** {self.state.user_input}\n")
        
        dev_output = self.state.branch_outputs.get("software_dev")
        re_output = self.state.branch_outputs.get("reverse_engineering")
        
        if re_output:
            re_summary = self._extract_reverse_engineering_summary()
            if re_summary:
                sections.append(re_summary)
            else:
                sections.append(self._build_domain_section("reverse_engineering", re_output))
        
        if dev_output:
            sections.append(self._build_domain_section("software_dev", dev_output))
        
        # cross-domain synthesis if applicable
        cross_domain = self._build_cross_domain_synthesis()
        if cross_domain:
            sections.append(cross_domain)
        
        exec_summary = self._build_execution_summary()
        if exec_summary:
            sections.append(exec_summary)
        
        # tool activity
        if self.state.tool_results:
            tool_summary = self._build_tool_activity_summary()
            if tool_summary:
                sections.append(tool_summary)
        
        recommendations = self._build_recommendations()
        if recommendations:
            sections.append(recommendations)
        
        final = "\n".join(sections)
        return StateManager.sanitize_output(final)

def synthesize_orchestration_output(state: AgentState) -> str:
    synthesizer = Synthesizer(state)
    return synthesizer.synthesize()
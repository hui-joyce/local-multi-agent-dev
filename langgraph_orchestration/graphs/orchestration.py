import json
import re

from langgraph.graph import END, StateGraph

from langgraph_orchestration.agents import MLXAgentFactory
from langgraph_orchestration.core import sanitize_final_output
from langgraph_orchestration.graphs.reverse_engineering import build_reverse_engineering_graph
from langgraph_orchestration.graphs.software_dev import build_software_dev_graph
from langgraph_orchestration.state import AgentState


def build_orchestration_graph(factory: MLXAgentFactory = None):
    """
    Build the supervisor-driven orchestration graph.

    Routes user requests to one or both domain-specific subgraphs:
    - software_dev: Code generation, testing, architecture review
    - reverse_engineering: Firmware analysis, binary diff, symbol analysis
    """

    if factory is None or isinstance(factory, dict):
        factory = MLXAgentFactory()

    supervisor = factory.create_supervisor_agent()

    dev_graph = build_software_dev_graph(factory=factory)
    re_graph = build_reverse_engineering_graph(factory=factory)

    graph = StateGraph(AgentState)

    def supervisor_node(state: AgentState) -> AgentState:
        decision = supervisor.invoke(user_input=state.user_input)

        if not isinstance(decision, dict):
            raise ValueError(f"Supervisor must return a dict, got {type(decision)}: {decision}")

        execution_domains = decision.get("execution_domains")
        if not execution_domains:
            raise ValueError(f"Supervisor decision missing execution_domains: {decision}")

        primary_domain = decision.get("primary_domain")
        if not primary_domain:
            raise ValueError(f"Supervisor decision missing primary_domain: {decision}")

        split_tasks = decision.get("split_tasks", {})

        valid_domains = {"software_dev", "reverse_engineering"}
        execution_domains = [d for d in execution_domains if d in valid_domains]

        if not execution_domains:
            raise ValueError(
                f"Supervisor decision has no valid domains. Got: {decision.get('execution_domains')}"
            )
        if primary_domain not in valid_domains:
            raise ValueError(f"Supervisor decision has invalid primary_domain: {primary_domain}")

        state.execution_domains = execution_domains
        state.selected_domain = primary_domain
        state.split_tasks = split_tasks
        state.agent_chain.append("supervisor")

        return state

    def software_dev_router(state: AgentState) -> AgentState:
        dev_state = state.model_dump()
        dev_task = state.split_tasks.get("software_dev", "")
        if dev_task:
            dev_state["user_input"] = dev_task

        result = dev_graph.invoke(dev_state)
        updated = AgentState(**result)

        updated.execution_domains = state.execution_domains
        updated.selected_domain = state.selected_domain

        return updated

    def reverse_engineering_router(state: AgentState) -> AgentState:
        re_state = state.model_dump()
        re_task = state.split_tasks.get("reverse_engineering", "")
        if re_task:
            re_state["user_input"] = re_task

        result = re_graph.invoke(re_state)
        updated = AgentState(**result)

        updated.execution_domains = state.execution_domains
        updated.selected_domain = state.selected_domain

        return updated

    def final_synthesis(state: AgentState) -> AgentState:
        state.final_output = synthesize_orchestration_output(state)
        state.agent_chain.append("final_synthesis")
        return state

    def route_after_supervisor(state: AgentState) -> str:
        if (
            "software_dev" in state.execution_domains
            and "reverse_engineering" in state.execution_domains
        ):
            return "software_dev_and_re"
        elif "software_dev" in state.execution_domains:
            return "software_dev"
        else:
            return "reverse_engineering"

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("software_dev", software_dev_router)
    graph.add_node("reverse_engineering", reverse_engineering_router)
    graph.add_node("final_synthesis", final_synthesis)

    # add edges and routing
    graph.add_conditional_edges(
        "supervisor",
        route_after_supervisor,
        {
            "software_dev": "software_dev",
            "reverse_engineering": "reverse_engineering",
            "software_dev_and_re": "software_dev",  # start with software dev, then flow to RE
        },
    )

    # after software dev, route to RE if needed, otherwise to synthesis
    def route_after_software_dev(state: AgentState) -> str:
        if "reverse_engineering" in state.execution_domains:
            return "reverse_engineering"
        return "final_synthesis"

    graph.add_conditional_edges(
        "software_dev",
        route_after_software_dev,
        {
            "reverse_engineering": "reverse_engineering",
            "final_synthesis": "final_synthesis",
        },
    )

    # after reverse engineering, always route to synthesis
    graph.add_edge("reverse_engineering", "final_synthesis")

    # final synthesis to end
    graph.add_edge("final_synthesis", END)

    graph.set_entry_point("supervisor")

    compiled_graph = graph.compile()

    compiled_graph.name = "Multi-Domain Orchestration Engine"
    compiled_graph.description = "Supervisor-routed orchestration supporting software development and reverse engineering domains"

    return compiled_graph


_DOMAIN_TITLES = {
    "software_dev": "Software Development Analysis",
    "reverse_engineering": "Reverse Engineering Analysis",
}

_ARTIFACT_COUNT_RE = re.compile(r"Confirmed local artifacts:\s+(\d+)")
_MAX_NOTES = 5


def _firmware_targets(state: AgentState) -> list[dict]:
    """Devices and versions the locator resolved, or []"""
    payload = state.intermediate_outputs.get("firmware_locator", "")
    if not payload:
        return []
    try:
        data = json.loads(payload)
    except (json.JSONDecodeError, ValueError):
        return []
    targets = data.get("targets") if isinstance(data, dict) else None
    return targets if isinstance(targets, list) else []


def _reverse_engineering_summary(state: AgentState) -> str:
    """Structured account of the firmware pipeline run"""
    lines = ["## Reverse Engineering Workflow Summary", ""]

    targets = _firmware_targets(state)
    if targets:
        lines.append("### Targets Processed")
        for target in targets:
            device = target.get("device", "unknown device")
            version = target.get("version", "unknown")
            build = target.get("build", "unknown")
            lines.append(f"- {device} version {version} (build {build})")
        lines.append("")

    downloader = state.intermediate_outputs.get("firmware_downloader", "")
    match = _ARTIFACT_COUNT_RE.search(downloader)
    if match:
        lines.append(f"### Artifacts\n- {match.group(1)} firmware artifact(s) available locally\n")

    reports = state.feature_analysis_reports
    written = {name: path for name, path in reports.items() if name != "__summary__"}
    if written:
        lines.append(f"### Feature Analysis\n- {len(written)} component report(s) written")
        summary_path = reports.get("__summary__")
        if summary_path:
            lines.append(f"- Summary index: `{summary_path}`")
        lines.append("")

    if state.feature_triage_index:
        high = sum(1 for row in state.feature_triage_index if row.get("signal") == "HIGH_SIGNAL")
        total = len(state.feature_triage_index)
        lines.append(
            f"### Triage\n- {total} component(s) classified: "
            f"{high} HIGH_SIGNAL, {total - high} LOW_SIGNAL\n"
        )

    return "\n".join(lines).strip()


def _execution_summary(state: AgentState) -> str:
    if not state.agent_chain:
        return ""

    lines = ["## Execution Summary", ""]

    if state.execution_domains:
        pretty = ", ".join(domain.replace("_", " ").title() for domain in state.execution_domains)
        lines.append(f"- **Domains:** {pretty}")

    if state.tool_results:
        succeeded = sum(1 for result in state.tool_results if result.success)
        failed = len(state.tool_results) - succeeded
        lines.append(f"- **Tool calls:** {succeeded} succeeded, {failed} failed")

    if state.dev_iteration:
        lines.append(f"- **Code generation attempts:** {state.dev_iteration}")

    if state.analysis_notes:
        lines.append("")
        lines.append("### Analysis Notes")
        lines += [f"- {note}" for note in state.analysis_notes[-_MAX_NOTES:]]

    return "\n".join(lines)


def _failures(state: AgentState) -> str:
    failed = [result for result in state.tool_results if not result.success]
    if not failed:
        return ""
    lines = ["## Issues Encountered", ""]
    lines += [f"- {result.tool_name}: {result.error}" for result in failed[:3]]
    if len(failed) > 3:
        lines.append(f"- ... and {len(failed) - 3} more (see tool activity above)")
    return "\n".join(lines)


def synthesize_orchestration_output(state: AgentState) -> str:
    """Final user-facing answer for a completed run"""
    dev_output = state.branch_outputs.get("software_dev", "")
    re_output = state.branch_outputs.get("reverse_engineering", "")

    sections = ["# Orchestration Analysis Result", "", f"**Request:** {state.user_input}", ""]

    if re_output:
        # A firmware run has a structured story to tell; a generic RE run does not.
        summary = _reverse_engineering_summary(state) if _firmware_targets(state) else ""
        sections.append(
            summary or f"## {_DOMAIN_TITLES['reverse_engineering']}\n{re_output.strip()}"
        )

    if dev_output:
        sections.append(f"## {_DOMAIN_TITLES['software_dev']}\n{dev_output.strip()}")

    for block in (_execution_summary(state), _failures(state)):
        if block:
            sections.append(block)

    return sanitize_final_output("\n\n".join(section for section in sections if section))

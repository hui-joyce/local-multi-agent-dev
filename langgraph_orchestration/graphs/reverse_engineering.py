"""
Reverse-engineering graph for IPSW firmware-diff analysis.

Decompilation-injection pipeline: report code blocks are filled with actual IDA output, avoiding model-written pseudocode. 
The flow runs across four nodes:
  prepare_decompiler_node       - _auto_decompile_top_symbols decompiles the top
                                   security-relevant added functions into
                                   feature["_auto_decompilations"].
  unified_feature_analysis_node -  passes that code to the model as read-only ground
                                   truth; the model writes PROSE only.
  cleanup_decompiler_node       -  re-decompiles after the annotation floor runs, into
                                   feature["_final_decompilations"] (annotated version).
  feature_analysis_compile_node -  _inject_real_decompilation places the code into the
                                   "## How is it implemented" section (final over auto).

The actual pseudocode is produced by decompiler_tools.decompile_function.
"""

from __future__ import annotations

import json
import os
import re

from langgraph.graph import END, StateGraph

from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.core.state_utils import StateManager
from langgraph_orchestration.prompts.shared import get_allowed_tools, RE_IDA_ANALYSIS_TOOLS
from langgraph_orchestration.retrievers.config import RAGConfigManager
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.triage.rules import triage_evidence_explained
from langgraph_orchestration.tooling.executor import get_tool_executor, tool_executor_node, should_continue_tool_loop
from langgraph_orchestration.tooling.tool import ToolRequest, ToolResult
from langgraph_orchestration.inference.inference_engine import GenerationConfig
from ipsw_service.agents.ipsw_extractor import IpswExtractorAgent
from ipsw_service.cli import build_download_args
from ipsw_service.security_notes_service import SecurityNotesService
from ipsw_service.firmware_diff_service import FirmwareDiffService
from ipsw_service.models import FirmwareDiffRequest
from ipsw_service.utils import ensure_dir, read_text, write_text
from ipsw_service.firmware_catalog import FirmwareCatalogService


FEATURE_ANALYSIS_BUDGET = 100
FEATURE_ANALYSIS_RECURSION_LIMIT = FEATURE_ANALYSIS_BUDGET * 40

# Per-component tool-loop ceiling
# tool_iteration bumps 2 interations (request + result iterations) per tool call 
# about 15 tool calls for a complete stage (find_address → xrefs/decompile → rename/comment/save)
FEATURE_ANALYSIS_MAX_TOOL_ITERATIONS = 30

ANNOTATION_FAILURE_LIMIT = 5

FEATURE_EVIDENCE_CHAR_BUDGET = 120_000       # ~30k tokens
FEATURE_TOOL_CONTEXT_CHAR_BUDGET = 400_000   # ~100k tokens

# RE_DEBUG=1 opts into verbose per-iteration prompt dumps; off by default 
_RE_DEBUG = os.getenv("RE_DEBUG") == "1"

def _truncate_for_prompt(text: str, max_chars: int, label: str) -> str:
    if not text or len(text) <= max_chars:
        return text
    omitted = len(text) - max_chars
    return (
        text[:max_chars]
        + f"\n\n… [{label} truncated: {omitted:,} of {len(text):,} chars omitted to fit the model context window] …"
    )


def render_triage_summary(index: list[dict], version: str = "") -> str:
    """Render the consolidated feature-analysis classification index to markdown"""
    def eff_tier(row: dict) -> str:
        # authoritative LLM tier when analysed, else deterministic score estimate.
        return row.get("llm_tier") or row.get("pretier") or "—"

    def tier_rank(t: str) -> int:
        return {"TIER_1": 0, "TIER_2": 1, "TIER_3": 2}.get((t or "").upper(), 3)

    high = [r for r in index if r.get("signal") == "HIGH_SIGNAL"]
    low = [r for r in index if r.get("signal") != "HIGH_SIGNAL"]
    notes = [r for r in high if r.get("security_notes_match")]
    analysed = [r for r in high if r.get("saved")]
    suppressed = [r for r in high if r.get("selected") and not r.get("saved")]
    not_selected = [r for r in high if not r.get("selected")]
    # split un-analysed HIGH_SIGNAL
    overflow = [r for r in not_selected if (r.get("security_score") or 0) >= 2]
    low_relevance = [r for r in not_selected if (r.get("security_score") or 0) < 2]

    def row_md(r: dict) -> str:
        score = r.get("security_score")
        score_s = str(score) if score is not None else "—"
        notes_s = f"`{r['security_notes_match']}`" if r.get("security_notes_match") else "—"
        if r.get("saved") and r.get("report_path"):
            link = f"[report]({os.path.basename(r['report_path'])})"
        elif r.get("selected") and not r.get("saved"):
            link = "_suppressed (TIER_3)_"
        else:
            link = "_not analysed_"
        return f"| {r.get('name', '?')} | {eff_tier(r)} | {score_s} | {notes_s} | {link} |"

    def table(rows: list[dict]) -> list[str]:
        rows = sorted(rows, key=lambda r: (tier_rank(eff_tier(r)), -(r.get("security_score") or 0), r.get("name", "")))
        out = ["| Component | Tier | Sec score | Apple Security Notes | Report |",
               "|---|---|---|---|---|"]
        out += [row_md(r) for r in rows]
        return out

    def section(title: str, rows: list[dict], collapse_over: int = 60) -> list[str]:
        if not rows:
            return []
        out = [f"## {title}", ""]
        if len(rows) > collapse_over:
            out += [f"<details><summary>Show {len(rows)} components</summary>", ""]
            out += table(rows)
            out += ["", "</details>", ""]
        else:
            out += table(rows) + [""]
        return out

    def name_list(title: str, rows: list[dict]) -> list[str]:
        if not rows:
            return []
        out = [f"## {title}", "", f"<details><summary>Show {len(rows)} components</summary>", ""]
        out += [f"- {r.get('name', '?')}" for r in sorted(rows, key=lambda r: r.get("name", ""))]
        out += ["", "</details>", ""]
        return out

    lines: list[str] = [
        f"# Feature Analysis Summary{f' — iOS {version}' if version else ''}",
        "",
        f"- **Total components in diff**: {len(index)}  "
        f"(**HIGH_SIGNAL**: {len(high)}, **LOW_SIGNAL**: {len(low)})",
        f"- **Analysed** (report written): {len(analysed)}  |  "
        f"**Apple Security Notes matches**: {len(notes)}  |  "
        f"**Suppressed TIER_3**: {len(suppressed)}  |  "
        f"**HIGH_SIGNAL not analysed** (budget/security filter): {len(not_selected)}",
        "",
        "Tier shown is the LLM-assigned tier for analysed components, otherwise a "
        "deterministic estimate from the security score (4=Apple Security Notes, "
        "3=hard indicator, 2=security vocabulary, 1=code change, 0=asset/UI/log).",
        "",
    ]
    lines += section("🔴 Apple Security Notes matches — highest priority", notes)
    lines += section("Analysed components (reports written)", analysed)
    lines += section("HIGH_SIGNAL — analysed but suppressed (LLM rated TIER_3)", suppressed)
    lines += section(
        f"HIGH_SIGNAL — flagged security-relevant but not analysed ({len(overflow)}, over budget)",
        overflow,
    )
    lines += name_list(
        f"HIGH_SIGNAL — excluded, low/no security relevance ({len(low_relevance)})",
        low_relevance,
    )
    lines += name_list(f"LOW_SIGNAL — excluded ({len(low)}, metadata/timestamp churn only)", low)
    return "\n".join(lines)


_SECURITY_INDICATOR_RES = [
    (re.compile(r'\b(malloc|calloc|realloc|free)\b'), "heap allocation"),
    (re.compile(r'\bos_unfair_lock\b'), "lock primitive"),
    (re.compile(r'\bpanic\b|\babort\b|\b__stack_chk_fail\b'), "bounds/stack guard"),
    (re.compile(r'valueForEntitlement:', re.IGNORECASE), "entitlement check"),
    (re.compile(r'\b(UAF|use.after.free|out.of.bounds|OOB|buffer overflow|race condition)\b', re.IGNORECASE), "vulnerability class"),
    (re.compile(r'\bcom\.apple\.security\b|\bentitlements\b', re.IGNORECASE), "security entitlement"),
]

_SECURITY_VOCAB_RE = re.compile(
    r"\bauth|crypt|cipher|\bcert|entitl|sandbox|\bxpc\b|mach_|keychain|keystore"
    r"|\bsep\b|credential|password|passcode|privile|\btcc\b|codesign|provision"
    r"|decrypt|\bsign(?:ature|ed|ing)?\b|verify|token|secure|sanitiz|bounds"
    r"|overflow|use.after.free|\bUAF\b|\bOOB\b|\bnonce\b|attest|biometr|touchid"
    r"|faceid|kext|\bIOKit\b|mmap|vm_|kalloc",
    re.IGNORECASE,
)

# Scan both CStrings and Symbols: stripped ObjC method names surface in
# __objc_methname cstrings
_OBJC_METHOD_LITERAL_RE = re.compile(r"^[-+]\[[A-Za-z_]\w* [A-Za-z_][\w:]*\]$")
_OBJC_SELECTOR_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(?::(?:[A-Za-z_][A-Za-z0-9_]*)?)*$")


def _extract_security_indicators(evidence: str) -> list[str]:
    """Scan diff evidence for memory-safety and security-boundary patterns"""
    found: list[str] = []
    for pattern, label in _SECURITY_INDICATOR_RES:
        for line in evidence.splitlines():
            stripped = line.strip()
            if stripped.startswith(("+", "-")) and pattern.search(stripped):
                if label not in found:
                    found.append(label)
                break
    return found


def _evidence_sections(evidence: str) -> tuple[list[str], list[str]]:
    """Split feature evidence into (cstring_lines, symbol_lines), keeping only
    the actual +/- diff lines from each labelled section."""
    cstrings: list[str] = []
    symbols: list[str] = []
    bucket: list[str] | None = None
    for line in (evidence or "").splitlines():
        stripped = line.strip()
        if stripped.startswith("CStrings:"):
            bucket = cstrings
            continue
        if stripped.startswith("Symbols:"):
            bucket = symbols
            continue
        if bucket is not None and stripped.startswith(("+", "-")):
            bucket.append(stripped)
    return cstrings, symbols


def _usable_decompilation(code) -> bool:
    """True when decompile_function returned real pseudocode, not an empty string
    or a '# ERROR' sentinel (its contract for un-decompilable addresses)."""
    return isinstance(code, str) and bool(code.strip()) and not code.startswith("# ERROR")


def _component_change_volume(evidence: str) -> int:
    cstrings, symbols = _evidence_sections(evidence)
    return len(cstrings) + len(symbols)


def _security_score(target: dict) -> int:
    """Rank components by security relevance so a huge diff is narrowed to the
    components a security researcher actually cares about.

      4  Apple Security Notes name this component as changed this release
      3  hard security indicator (memory-safety, entitlement check, vuln class)
      2  security-relevant vocabulary (auth/crypto/sandbox/IPC/credential/...)
      1  code changed (symbol churn) but no security signal
      0  no code change and no security signal (asset/UI/log churn only)
    """
    if target.get("security_notes_match"):
        return 4
    if target.get("security_indicators"):
        return 3
    cstrings, symbols = _evidence_sections(target.get("evidence", ""))
    if any(_SECURITY_VOCAB_RE.search(line) for line in cstrings) or any(
        _SECURITY_VOCAB_RE.search(line) for line in symbols
    ):
        return 2
    if symbols:
        return 1
    return 0


def _pretier_from_score(score: int) -> str:
    """Deterministic tier estimate from the security score, used in the summary
    for HIGH_SIGNAL components that were not fully analysed by the LLM"""
    if score >= 3:
        return "TIER_1"
    if score == 2:
        return "TIER_2"
    return "TIER_3"


def _infer_feature_type(name: str, source: str) -> str:
    lowered = name.lower()
    if lowered.endswith(".framework"):
        return "framework"
    if lowered.endswith(".dylib"):
        return "dylib"
    if lowered.endswith(".kext"):
        return "kext"
    if lowered.endswith(".bundle"):
        return "bundle"
    if source == "launchd_changes":
        return "launchd"
    if source.startswith("firmware") or source.startswith("iboot"):
        return "firmware"
    return "component"


def _build_feature_targets(report_json_str: str, limit: int = 6) -> list[dict[str, str]]:
    try:
        data = json.loads(report_json_str)
    except json.JSONDecodeError:
        return []

    binary_map: dict[str, dict[str, str]] = {}

    def extract_paths(obj, source_name: str) -> None:
        if isinstance(obj, list):
            for item in obj:
                if isinstance(item, str) and item.startswith("/"):
                    name = os.path.basename(item)
                    binary_map[name] = {"path": item, "source": source_name}
        elif isinstance(obj, dict):
            for k, v in obj.items():
                extract_paths(v, k if k not in ["updated", "added", "modified", "dylibs", "frameworks", "standard_binaries"] else source_name)

    extract_paths(data.get("kernel", {}), "kernel")
    extract_paths(data.get("macho", {}), "macho")
    extract_paths(data.get("dsc", {}), "dsc")
    extract_paths(data.get("boundary_changes", {}), "boundary_changes")
    extract_paths(data.get("userland_changes", {}), "userland_changes")

    evidence_map: dict[str, dict[str, list[str]]] = {}

    for line in data.get("cstring_context", []):
        parts = line.split(":", 1)
        if len(parts) == 2:
            name = parts[0].strip()
            if name not in evidence_map:
                evidence_map[name] = {"cstrings": [], "symbols": []}
            evidence_map[name]["cstrings"].append(parts[1].strip())

    for line in data.get("symbol_context", []):
        parts = line.split(":", 1)
        if len(parts) == 2:
            name = parts[0].strip()
            if name not in evidence_map:
                evidence_map[name] = {"cstrings": [], "symbols": []}
            evidence_map[name]["symbols"].append(parts[1].strip())

    _ALLOWED_TOOL_NAMES = list(RE_IDA_ANALYSIS_TOOLS)

    def _make_target(name: str, evidence: str) -> dict:
        binary_info = binary_map.get(name, {})
        source = binary_info.get("source", "component")
        entry = {
            "name": name,
            "feature_type": _infer_feature_type(name, source),
            "source": source,
            "evidence": evidence,
            "allowed_tool_names": list(_ALLOWED_TOOL_NAMES),
        }
        if binary_info.get("path"):
            entry["binary_path"] = binary_info["path"]
        return entry

    targets: list[dict[str, str]] = []
    for name, ev_dict in evidence_map.items():
        ev_lines = []
        if ev_dict["cstrings"]:
            ev_lines.append("CStrings:")
            ev_lines.extend(ev_dict["cstrings"])
        if ev_dict["symbols"]:
            if ev_lines:
                ev_lines.append("")
            ev_lines.append("Symbols:")
            ev_lines.extend(ev_dict["symbols"])
        targets.append(_make_target(name, "\n".join(ev_lines)))

    # Changed binaries with NO cstring/symbol delta still get a target (empty
    # evidence). A content-light fix — e.g. a logging-redaction change that adds
    # no strings/symbols — otherwise lands in the changed list but never becomes a
    # target, so it can't be matched to an Apple advisory component. These are
    # LOW_SIGNAL by default and only surface if promoted by a Security Notes match.
    for name in binary_map:
        if name not in evidence_map:
            targets.append(_make_target(name, ""))

    # attach the deterministic triage signal to every target; filtering happens in
    # feature_analysis_select_node after Apple Security Notes matching, so an
    # advisory-named component can be promoted before the LOW_SIGNAL drop
    for t in targets:
        result = triage_evidence_explained(t.get("evidence", ""))
        t["_triage_signal"] = result.signal
        t["_triage_reason"] = result.reason
        if result.evidence_line:
            t["_triage_evidence_line"] = result.evidence_line
    return targets


# cap for a single fenced code block in a report
_MAX_CODE_BLOCK_CHARS = 6000
_MAX_LINE_REPEAT = 3

def _collapse_repeats(body: str) -> str:
    """Collapse any run of the same non-blank line to at most _MAX_LINE_REPEAT
    occurrences — a deterministic guard against model repetition-loop
    degeneration (e.g. the same `if (...) return;` block emitted hundreds of times)."""
    out: list[str] = []
    prev: str | None = None
    run = 0
    for line in body.split("\n"):
        stripped = line.strip()
        if stripped and stripped == prev:
            run += 1
            if run >= _MAX_LINE_REPEAT:
                continue
        else:
            prev, run = stripped, 0
        out.append(line)
    return "\n".join(out)

def _sanitize_code_blocks(text: str) -> str:
    """Neutralise degenerate or truncated pseudocode: collapse repeated lines,
    cap oversized blocks, and close any unbalanced code fence"""
    from langgraph_orchestration.tooling.decompiler_tools import _is_degenerate_decompilation

    parts = text.split("```")
    # odd indices are inside a fenced block
    for i in range(1, len(parts), 2):
        block = parts[i]
        nl = block.find("\n")
        lang = block[: nl + 1] if nl != -1 else ""
        body = block[nl + 1:] if nl != -1 else block
        if _is_degenerate_decompilation(body):
            # degenerate Hex-Rays void*-thunk dump (no usable logic)
            body = "// [removed: decompiler produced a degenerate void*-parameter thunk with no usable logic]\n"
        else:
            body = _collapse_repeats(body)
            # cap any single runaway line 
            body = "\n".join(
                (ln[:2000] + " /* …truncated… */") if len(ln) > 2000 else ln
                for ln in body.split("\n")
            )
            if len(body) > _MAX_CODE_BLOCK_CHARS:
                body = (
                    body[:_MAX_CODE_BLOCK_CHARS].rstrip()
                    + "\n// [truncated: decompiler/model output too long or degenerate]\n"
                )
        parts[i] = lang + body
    result = "```".join(parts)
    if result.count("```") % 2 == 1:  # an opened fence was never closed
        result += "\n```"
    return result

def _sanitize_model_output(text: str) -> str:
    if not isinstance(text, str):
        try:
            text = str(text)
        except Exception:
            return ""
    return _sanitize_code_blocks(text).strip()

def _inject_real_decompilation(markdown: str, tool_results, auto_decomps=None) -> str:
    """Insert sanitized tool output from two sources deduped by address: 
    (1) auto_decomps — deterministic top-symbol decompilations done in prepare_decompiler; 
    (2) decompile_function - model's calls captured during the tool loop.
    State if nothing is produced"""
    seen: set = set()
    blocks: list[str] = []

    def _add(addr, code: str) -> None:
        code = (code or "").strip()
        if not _usable_decompilation(code):
            return
        key = str(addr) if addr else code[:80]
        if key in seen:
            return
        seen.add(key)
        label = f"### Decompilation at `{addr}`\n\n" if addr else "### Decompilation\n\n"
        blocks.append(label + _sanitize_code_blocks("```c\n" + code + "\n```"))

    # (1) deterministic auto-decompilations first, then (2) model's own
    for d in auto_decomps or []:
        _add(d.get("address"), d.get("code", ""))
    for r in tool_results or []:
        if getattr(r, "tool_name", "") == "decompile_function" and getattr(r, "success", False):
            _add((getattr(r, "metadata", None) or {}).get("decompile_address"), getattr(r, "output", ""))

    m = re.search(r"(##\s*How is it implemented[^\n]*\n)(.*?)(?=\n##\s|\Z)", markdown, re.S | re.I)
    if not m:
        return markdown
    header, body = m.group(1), m.group(2)
    # discard model-authored code fences and fabricated "Decompile Output" headers
    prose = re.sub(r"```.*?```", "", body, flags=re.S)
    prose = re.sub(r"#{2,4}\s*Decompile Output:[^\n]*", "", prose).strip()

    if blocks:
        new_body = "\n\n" + "\n\n".join(blocks)
        if prose:
            new_body += "\n\n" + prose
    else:
        note = (
            "_No decompilation was captured for this component (the analyzer did not "
            "call `decompile_function`); the description below is derived from the "
            "symbol-level diff evidence, not from decompiled code._"
        )
        new_body = "\n\n" + note + (("\n\n" + prose) if prose else "")

    return markdown[: m.start()] + header + new_body.rstrip() + "\n\n" + markdown[m.end():].lstrip()

def _symbol_importance(sym: str) -> int:
    """Rank a candidate function by likely security relevance so the bounded
    auto-decompile budget targets interesting code. Reuses the
    same security vocabulary the component-level triage uses"""
    score = 0
    if _SECURITY_VOCAB_RE.search(sym):
        score += 5
    for _pat, _label in _SECURITY_INDICATOR_RES:
        if _pat.search(sym):
            score += 3
    m = re.search(r"\[[^\]]*\s+([^\]]+)\]", sym)  # ObjC selector, else bare name
    sel = m.group(1) if m else sym.lstrip("_")
    low = sel.lower()
    if ".cxx_destruct" in sym or "_block_invoke" in sym or low in ("dealloc", "init"):
        score -= 5
    if low.startswith("set") and sel.count(":") == 1:
        score -= 2                       # trivial setter
    score += min(sel.count(":"), 3)      # more args -> more logic
    score += min(len(sel) // 14, 2)      # more specific name
    return score


def _build_readme_diff_index(readme_lines: list[str], max_lines: int = 200) -> dict[str, str]:
    """One-pass map of component name -> its README diff block (capped at
    max_lines), reproducing the old per-component extractor for every
    '#### <name>' section in a single scan.

    A cross-major diff README can be hundreds of MB / millions of lines with
    thousands of component sections; re-splitting and rescanning it once per
    component was O(components x lines) and dominated startup (observed: ~40min
    of 100% CPU in PyUnicode_Splitlines before analysis even began). This is
    O(lines), scanned once, then O(1) lookup per component.
    """
    index: dict[str, str] = {}
    name = None            # current section: first token after '#### '
    in_code_block = False
    collecting = False     # still accumulating lines for the current section
    result: list[str] = []

    def _flush() -> None:
        # first occurrence wins, matching the old scanner's break-at-first
        if name is not None and name not in index:
            index[name] = "\n".join(result)

    for line in readme_lines:
        stripped = line.strip()
        if stripped.startswith("#### "):
            _flush()
            name = stripped[5:].split(" ", 1)[0]  # component name; ignore trailing text
            in_code_block = False
            collecting = True
            result = []
            continue
        if name is None or not collecting:
            continue
        if stripped.startswith("### ") or stripped.startswith("## "):
            _flush()
            name = None
            collecting = False
            continue
        if stripped == "```diff":
            in_code_block = True
            result.append(line)
            continue
        if in_code_block and stripped == "```":
            result.append(line)
            collecting = False           # matches the old 'break' at code-block end
            continue
        if in_code_block or stripped.startswith(">"):
            result.append(line)
            if len(result) >= max_lines:
                result.append("... (truncated)")
                collecting = False
    _flush()
    return index



def build_reverse_engineering_graph(factory: MLXAgentFactory = None):
    if factory is None or isinstance(factory, dict):
        factory = MLXAgentFactory()

    feature_engine = None
    def _get_feature_engine():
        nonlocal feature_engine
        if feature_engine is None:
            feature_engine = factory.ensure_loaded()
        return feature_engine

    _re_agents: dict = {}
    def _get_re_agent(kind: str):
        if kind not in _re_agents:
            creators = {
                "planning": factory.create_planning_agent,
                "code_analysis": factory.create_code_analysis_agent,
                "vulnerability_detection": factory.create_vulnerability_detection_agent,
            }
            _re_agents[kind] = creators[kind]()
        return _re_agents[kind]

    def _auto_decompile_top_symbols(feature: dict, max_funcs: int = 3) -> None:
        """Deterministically decompile the most security-relevant functions from
        the diff, using the same find_address -> decompile_function chain and
        guards as the model"""
        from langgraph_orchestration.tooling.decompiler_tools import find_address, decompile_function

        _dbg = os.environ.get("RE_AUTODECOMP_DEBUG") == "1"
        def _log(msg: str) -> None:
            if _dbg:
                try:
                    with open("/tmp/autodecomp_debug.log", "a") as fh:
                        fh.write(msg + "\n")
                except Exception:
                    pass

        cstrings, symbols = _evidence_sections(feature.get("evidence", ""))
        _skip = ("_OBJC_CLASS_$", "_OBJC_METACLASS_$", "_OBJC_IVAR_$", "__OBJC_",
                 "__swift_FORCE_LOAD", "_objc_msgSend$")

        def _accept(tok: str) -> bool:
            if tok.startswith(("-[", "+[")):
                return bool(_OBJC_METHOD_LITERAL_RE.match(tok))
            if tok.startswith(_skip) or tok.startswith(("T@", '@"')):
                return False
            if "_block_invoke" in tok or not _OBJC_SELECTOR_RE.match(tok):
                return False
            return (":" in tok) or tok.startswith("_")

        candidates: list[str] = []
        seen_tok: set[str] = set()
        for bucket in (symbols, cstrings):
            for line in bucket:
                if not line.startswith("+"):  # added code only
                    continue
                tok = line[1:].strip().strip('"')
                if not tok or tok in seen_tok:
                    continue
                if _accept(tok):
                    seen_tok.add(tok)
                    candidates.append(tok)
        # most security-relevant first, so the bounded budget isn't spent on boilerplate
        candidates.sort(key=_symbol_importance, reverse=True)
        _log(f"[{feature.get('name')}] symbols={len(symbols)} cstrings={len(cstrings)} "
             f"candidates={len(candidates)} top={candidates[:6]}")

        # Keep checking more names, not just the first few
        _probe_budget = 30
        decomps: list[dict] = []
        seen_addr: set[str] = set()
        for sym in candidates:
            if len(decomps) >= max_funcs or _probe_budget <= 0:
                break
            _probe_budget -= 1
            try:
                res = find_address.invoke({"query": sym})
                _log(f"  find_address({sym!r}) -> {res if not isinstance(res, dict) else {k: res.get(k) for k in ('type', 'address')}}")
                if not isinstance(res, dict) or res.get("type") != "symbol":
                    continue
                addr = res.get("address")
                if not addr or addr in seen_addr:
                    continue
                seen_addr.add(addr)
                code = decompile_function.invoke({"address": addr})
                _log(f"  decompile({addr}) -> {('ERROR:'+code[:50]) if isinstance(code, str) and code.startswith('# ERROR') else (str(len(code))+' chars')}")
            except Exception as e:
                _log(f"  EXC {sym!r}: {type(e).__name__}: {e}")
                continue
            if _usable_decompilation(code):
                decomps.append({"address": addr, "code": code, "symbol": sym})

        _log(f"[{feature.get('name')}] -> injected {len(decomps)}")
        if decomps:
            feature["_auto_decompilations"] = decomps

    full_download_timeout = 4 * 60 * 60

    graph = StateGraph(AgentState)

    def _parse_firmware_targets(state: AgentState) -> list[dict[str, str]]:
        if "parsed_firmware_targets" in state.intermediate_outputs:
            try:
                return json.loads(state.intermediate_outputs["parsed_firmware_targets"])
            except Exception:
                pass

        user_input = state.user_input
        targets: list[dict[str, str]] = []
        seen: set[tuple[str, str, str]] = set()

        ipsw_pattern = r"([\w,]+)_(\d+\.\d+(?:\.\d+)?)_([A-Za-z0-9]+)_Restore\.ipsw"
        for device, version, build in re.findall(ipsw_pattern, user_input):
            key = (device, version, build)
            if key in seen:
                continue
            seen.add(key)
            targets.append({"device": device, "version": version, "build": build})

        if targets:
            state.intermediate_outputs["parsed_firmware_targets"] = json.dumps(targets)
            return targets

        device_match = re.search(r"\b(iPhone\d+,\d+|iPad\d+,\d+|Watch\d+,\d+|AppleTV\d+,\d+)\b", user_input)
        versions_and_builds = re.findall(r"(?<![\w\.])(\d+\.\d+(?:\.\d+)?)(?:_([A-Za-z0-9]+))?(?![\w\.])", user_input)
        if device_match and versions_and_builds:
            for version, build in versions_and_builds[:2]:
                key = (device_match.group(1), version, build)
                if key in seen:
                    continue
                seen.add(key)
                targets.append({"device": device_match.group(1), "version": version, "build": build})

        state.intermediate_outputs["parsed_firmware_targets"] = json.dumps(targets)
        return targets

    _IPSW_REQUEST_KEYWORDS = (
        "ipsw", "firmware", "dyld", "kernelcache", "kernel cache", "dyld_shared_cache",
        "ota", "restore.ipsw", "sepos", "iboot",
    )

    def _is_ipsw_request(state: AgentState) -> bool:
        """Deterministic IPSW vs generic routing"""
        if _parse_firmware_targets(state):
            return True
        lowered = (state.user_input or "").lower()
        return any(keyword in lowered for keyword in _IPSW_REQUEST_KEYWORDS)

    def _run_tool_requests(state: AgentState, requests: list[ToolRequest]) -> tuple[list[ToolResult], list[str]]:
        executor = get_tool_executor("reverse_engineering", workspace_root=state.workspace_root)
        allowed = state.tool_policy.allowed_tools or []
        results: list[ToolResult] = []
        summary_lines: list[str] = []

        for req in requests:
            if allowed and req.tool_name not in allowed:
                result = ToolResult(
                    tool_name=req.tool_name,
                    success=False,
                    output="",
                    error=f"Tool not allowed: {req.tool_name}",
                )
            else:
                try:
                    result = executor.execute(req)
                except Exception as exc:
                    result = ToolResult(tool_name=req.tool_name, success=False, output="", error=str(exc))

            state.register_tool_request(req)
            state.register_tool_result(result)
            results.append(result)
            command = str(result.metadata.get("command", "")).strip()
            if result.success:
                command_info = f" | cmd={command}" if command else ""
                summary_lines.append(f"OK {req.tool_name}{command_info}: {(result.output or '')[:400]}")
            else:
                command_info = f" | cmd={command}" if command else ""
                summary_lines.append(f"ERR {req.tool_name}{command_info}: {result.error}")

        return results, summary_lines

    def _download_output_dir(state: AgentState) -> str:
        root = state.workspace_root or os.getcwd()
        return os.path.join(root, ".ipsw_downloads")

    def _extract_output_dir(state: AgentState) -> str:
        root = state.workspace_root or os.getcwd()
        return os.path.join(root, ".ipsw_extracted")

    def _is_download_extract_only_request(user_input: str) -> bool:
        lowered = (user_input or "").lower()
        if not ("download" in lowered and "extract" in lowered):
            return False
        blocked = ["compare", "diff", "vulnerable", "disassembly", "inference", "analysis"]
        has_blocked = any(token in lowered for token in blocked)
        if has_blocked:
            if "only" in lowered and "do not perform" in lowered:
                return True
            return False
        return True

    def _collect_confirmed_local_artifacts(state: AgentState) -> list[str]:
        if "confirmed_local_ipsws" in state.intermediate_outputs:
            try:
                return json.loads(state.intermediate_outputs["confirmed_local_ipsws"])
            except Exception:
                pass

        download_dir = _download_output_dir(state)
        if not os.path.isdir(download_dir):
            return []

        targets = _parse_firmware_targets(state)
        artifacts: list[str] = []

        for target in targets:
            device = target.get("device", "")
            version = target.get("version", "")
            build = target.get("build", "")

            if device and version and build:
                expected = f"{device}_{version}_{build}_Restore.ipsw"
                expected_path = os.path.join(download_dir, expected)
                if os.path.isfile(expected_path):
                    artifacts.append(expected_path)
                continue

            if device and version:
                prefix = f"{device}_{version}_"
                for name in os.listdir(download_dir):
                    if name.startswith(prefix) and name.endswith("_Restore.ipsw"):
                        full_path = os.path.join(download_dir, name)
                        if os.path.isfile(full_path):
                            artifacts.append(full_path)
                continue
                
            if version and build:
                suffix = f"_{version}_{build}_Restore.ipsw"
                for name in os.listdir(download_dir):
                    if name.endswith(suffix):
                        full_path = os.path.join(download_dir, name)
                        if os.path.isfile(full_path):
                            artifacts.append(full_path)

        if targets:
            artifacts = sorted(set(artifacts))
            state.intermediate_outputs["confirmed_local_ipsws"] = json.dumps(artifacts)
            return artifacts

        for name in os.listdir(download_dir):
            if not name.endswith(".ipsw"):
                continue
            full_path = os.path.join(download_dir, name)
            if os.path.isfile(full_path):
                artifacts.append(full_path)

        artifacts = sorted(set(artifacts))
        state.intermediate_outputs["confirmed_local_ipsws"] = json.dumps(artifacts)
        return artifacts

    def _parse_version_tuple(version: str) -> tuple[int, ...]:
        return tuple(int(part) for part in version.split(".") if part.isdigit())

    def _order_ipsw_paths(paths: list[str]) -> list[str]:
        def key(path: str) -> tuple[tuple[int, ...], str]:
            name = os.path.basename(path)
            match = re.search(r"_(\d+\.\d+(?:\.\d+)?)_([A-Za-z0-9]+)_Restore\.ipsw", name)
            if not match:
                return ((), name)
            return (_parse_version_tuple(match.group(1)), match.group(2))

        return sorted(paths, key=key)

    # diff report directory encodes the exact pair, e.g. 17_0_3_21A360_vs_17_1_21B80
    _DIFF_DIR_PAIR_RE = re.compile(
        r"(\d+(?:_\d+)+)_(\d+[A-Za-z][0-9A-Za-z]*)_vs_(\d+(?:_\d+)+)_(\d+[A-Za-z][0-9A-Za-z]*)"
    )

    def _diff_pair_from_report(state: AgentState, paths: list[str]) -> tuple[str | None, str | None]:
        """Derive the (old, new) IPSW pair from the diff report's own directory name
        (e.g. .../17_0_3_21A360_vs_17_1_21B80/README.md), matching local IPSWs by
        build"""
        report_path = state.intermediate_outputs.get("firmware_diff_report_path", "") or ""
        m = _DIFF_DIR_PAIR_RE.search(report_path)
        if not m:
            return None, None
        old_build, new_build = m.group(2), m.group(4)

        by_build: dict[str, str] = {}
        for p in paths:
            nm = _IPSW_NAME_RE.search(os.path.basename(p))
            if nm:
                by_build[nm.group(3)] = p  # build -> path
        return by_build.get(old_build), by_build.get(new_build)

    def _select_diff_pair(state: AgentState, paths: list[str]) -> tuple[str | None, str | None]:
        if "diff_pair_old" in state.intermediate_outputs and "diff_pair_new" in state.intermediate_outputs:
            old = state.intermediate_outputs["diff_pair_old"] or None
            new = state.intermediate_outputs["diff_pair_new"] or None
            return old, new

        # prefer the pair named by the diff report itself over disk oldest/newest
        old, new = _diff_pair_from_report(state, paths)
        if new:
            state.intermediate_outputs["diff_pair_old"] = old or ""
            state.intermediate_outputs["diff_pair_new"] = new or ""
            return old, new

        if len(paths) < 2:
            return None, None
        ordered = _order_ipsw_paths(paths)
        old, new = ordered[0], ordered[-1]
        state.intermediate_outputs["diff_pair_old"] = old or ""
        state.intermediate_outputs["diff_pair_new"] = new or ""
        return old, new

    def _is_cross_major_diff(state: AgentState) -> bool:
        """True when the diff spans different iOS major versions.

        A cross-major jump folds many releases of change into each single
        component, so the per-component evidence explodes and the model shouldn't
        spend its bounded output budget on a <think> trace.
        """
        path = state.intermediate_outputs.get("firmware_diff_report_path", "") or ""
        m = _DIFF_DIR_PAIR_RE.search(path)
        if not m:
            return False  # unknown pair -> preserve current behaviour (thinking on)
        try:
            old_major = int(m.group(1).split("_")[0])
            new_major = int(m.group(3).split("_")[0])
        except (ValueError, IndexError):
            return False
        return old_major != new_major

    def _format_version_from_ipsw(path: str) -> str | None:
        name = os.path.basename(path)
        match = re.search(r"_(\d+\.\d+(?:\.\d+)?)_([A-Za-z0-9]+)_Restore\.ipsw", name)
        if not match:
            return None
        version, build = match.group(1), match.group(2)
        return f"{version} ({build})"

    _IPSW_NAME_RE = re.compile(
        r"(iPhone\d+,\d+|iPad\d+,\d+|Watch\d+,\d+|AppleTV\d+,\d+)"
        r"_(\d+\.\d+(?:\.\d+)?)_([A-Za-z0-9]+)_Restore\.ipsw"
    )

    def _comparison_dirname(old_ipsw: str | None, new_ipsw: str | None) -> str | None:
        """Per-comparison .ipsw_features/ directory matching the firmware-diff naming
        scheme. Returns None if the new IPSW cannot be parsed"""
        def _parse(path: str | None) -> tuple[str, str, str] | None:
            if not path:
                return None
            m = _IPSW_NAME_RE.search(os.path.basename(path))
            return m.groups() if m else None 

        new_p = _parse(new_ipsw)
        if not new_p:
            return None
        device, new_ver, new_build = new_p
        new_tag = f"{new_ver.replace('.', '_')}_{new_build}"
        old_p = _parse(old_ipsw)
        if old_p:
            _, old_ver, old_build = old_p
            old_tag = f"{old_ver.replace('.', '_')}_{old_build}"
            return f"{device}__{old_tag}_vs_{new_tag}"
        return f"{device}__{new_tag}"

    def _slugify_feature(text: str) -> str:
        cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("._-")
        return cleaned or "feature"

    def _resolve_feature_output_dir(report_path: str, workspace_root: str | None) -> str:
        normalized = os.path.normpath(report_path)
        parts = normalized.split(os.sep)
        if "firmware_diff" in parts:
            idx = parts.index("firmware_diff")
            if idx + 1 < len(parts):
                base = os.sep.join(parts[: idx + 2])
                return ensure_dir(os.path.join(base, "feature_analysis"))

        root = workspace_root or os.getcwd()
        return ensure_dir(os.path.join(root, "artifacts", "firmware_diff", "feature_analysis"))

    def retrieve_re_context_node(state: AgentState) -> AgentState:

        report_path = state.intermediate_outputs.get("firmware_diff_report_path")
        report_text = state.intermediate_outputs.get("firmware_diff_report")
        if report_path and report_text:
            state.re_context = []
            state.selected_domain = "reverse_engineering"
            state.execution_domains = ["reverse_engineering"]
            state.re_task_plan = ["feature_analysis"]
            state.split_tasks = {}
            state.tool_policy.allowed_tools = get_allowed_tools("reverse_engineering")
            state.max_tool_iterations = FEATURE_ANALYSIS_MAX_TOOL_ITERATIONS
            return state

        RAGConfigManager.initialize()
        rag_manager = RAGConfigManager.get_rag_manager()
        config = RAGConfigManager.get_config()
        context = rag_manager.retrieve_reverse_engineering_context(
            query=state.user_input,
            top_k=config.default_top_k,
        )

        state.re_context = context
        state.selected_domain = "reverse_engineering"
        state.execution_domains = ["reverse_engineering"]
        state.re_task_plan = (
            ["firmware_analysis"]
            if _is_ipsw_request(state)
            else ["planning", "code_analysis", "vulnerability_detection"]
        )
        state.split_tasks = {}
        state.tool_policy.allowed_tools = get_allowed_tools("reverse_engineering")
        state.max_tool_iterations = state.tool_policy.max_iterations
        return StateManager.add_retrieved_context(state, context)

    def firmware_locator_node(state: AgentState) -> AgentState:
        targets = _parse_firmware_targets(state)
        if not targets and os.getenv("IPSW_DOWNLOADS_API_ENABLE") == "1":
            catalog = FirmwareCatalogService()
            identifier = catalog.resolve_by_model_hint(state.user_input)
            if identifier:
                resolved = catalog.resolve_latest_ipsw(identifier)
                if resolved:
                    targets = [{"device": resolved.get("device", ""), "version": resolved.get("version", ""), "build": resolved.get("build", "")}]
        if not targets:
            payload = {
                "status": "unresolved",
                "error": "Unable to resolve firmware targets from input.",
            }
        else:
            payload = {
                "status": "resolved",
                "targets": targets,
            }
        return StateManager.add_intermediate_output(
            state,
            "firmware_locator",
            json.dumps(payload, ensure_ascii=True, indent=2),
        )

    def firmware_downloader_node(state: AgentState) -> AgentState:
        targets = _parse_firmware_targets(state)
        requests: list[ToolRequest] = []
        output_dir = _download_output_dir(state)
        os.makedirs(output_dir, exist_ok=True)

        for target in targets:
            base = build_download_args(
                device=target["device"],
                version=target.get("version") or None,
                build=target.get("build") or None,
                output_dir=output_dir,
                resume_all=True,
            )

            requests.append(
                ToolRequest(
                    tool_name="ipsw_cli",
                    arguments={"args": base, "timeout": full_download_timeout},
                    target=f"{target['device']}:{target['version'] or target['build']}",
                    reason="Download firmware artifact.",
                )
            )

        _, summary = _run_tool_requests(state, requests)
        confirmed = _collect_confirmed_local_artifacts(state)
        summary.append(f"Confirmed local artifacts: {len(confirmed)}")
        for artifact in confirmed:
            summary.append(f"LOCAL_ARTIFACT {artifact}")

        if not requests:
            summary.append("No resolved targets; download stage skipped.")
        return StateManager.add_intermediate_output(state, "firmware_downloader", "\n".join(summary))

    def ipsw_extractor_node(state: AgentState) -> AgentState:
        local_ipsws = _collect_confirmed_local_artifacts(state)
        extractor = IpswExtractorAgent(workspace_root=state.workspace_root)
        output_dir = _extract_output_dir(state)
        payload = extractor.extract(local_ipsws, output_dir)
        if not local_ipsws:
            payload["note"] = "No confirmed local artifacts available; extraction skipped."
        return StateManager.add_intermediate_output(state, "ipsw_extractor", json.dumps(payload, ensure_ascii=True, indent=2))

    def _extracted_artifact_for_ipsw(
        ipsw_path: str, workspace_root: str | None, leaf_glob: str,
        select=lambda p: True,
    ) -> str | None:
        import glob as _glob
        stem = os.path.basename(ipsw_path).replace(".ipsw", "")
        extracted_root = os.path.join(workspace_root or os.getcwd(), ".ipsw_extracted")

        def _first(pattern: str) -> str | None:
            hits = sorted(p for p in _glob.glob(pattern, recursive=True) if select(p))
            return hits[0] if hits else None

        # 1. exact IPSW-stem directory
        found = _first(os.path.join(extracted_root, stem, "**", leaf_glob))
        if found:
            return found
        # 2. any directory for this build id (e.g. bare "23E254__iPhone18,1/")
        m = _IPSW_NAME_RE.search(os.path.basename(ipsw_path))
        build_id = m.group(3) if m else None
        if build_id:
            return _first(os.path.join(extracted_root, f"*{build_id}*", "**", leaf_glob))
        return None

    def _find_dsc_for_ipsw(ipsw_path: str, workspace_root: str | None) -> str | None:
        return _extracted_artifact_for_ipsw(ipsw_path, workspace_root, "dyld_shared_cache_arm64e")

    def _find_kernelcache_for_ipsw(ipsw_path: str, workspace_root: str | None) -> str | None:
        return _extracted_artifact_for_ipsw(
            ipsw_path, workspace_root, "kernelcache*",
            select=lambda p: "release" in os.path.basename(p),
        )

    def firmware_diff_service_node(state: AgentState) -> AgentState:
        local_ipsws = _collect_confirmed_local_artifacts(state)
        old_ipsw, new_ipsw = _select_diff_pair(state, local_ipsws)
        if not old_ipsw or not new_ipsw:
            payload = {"status": "skipped", "reason": "Need two IPSW artifacts for firmware diff."}
            return StateManager.add_intermediate_output(state, "firmware_diff_report", json.dumps(payload, ensure_ascii=True, indent=2))

        dyld_map: dict[str, str | None] = {}
        kernel_map: dict[str, str | None] = {}
        extractor_output = state.intermediate_outputs.get("ipsw_extractor", "")
        if extractor_output:
            try:
                data = json.loads(extractor_output)
                for entry in data.get("extractions", []):
                    ipsw = entry.get("ipsw")
                    if ipsw:
                        dyld_paths = entry.get("dyld_paths", [])
                        kernel_paths = entry.get("kernel_paths", [])
                        dyld_map[ipsw] = dyld_paths[0] if dyld_paths else None
                        kernel_map[ipsw] = kernel_paths[0] if kernel_paths else None
            except Exception:
                pass

        # scan .ipsw_extracted/ directly if extractor state missed DSC/kernel paths
        workspace_root = state.workspace_root
        for ipsw_path in (old_ipsw, new_ipsw):
            if not dyld_map.get(ipsw_path):
                found = _find_dsc_for_ipsw(ipsw_path, workspace_root)
                if found:
                    dyld_map[ipsw_path] = found
            if not kernel_map.get(ipsw_path):
                found = _find_kernelcache_for_ipsw(ipsw_path, workspace_root)
                if found:
                    kernel_map[ipsw_path] = found

        # surface any gap that would silently drop a whole cache's changes
        # a. if resolution collapsed old and new to the same file, 
        # b. if the old cache is simply absent, note that this diff is skipped
        def _check_diff_inputs(mapping: dict[str, str | None], label: str) -> None:
            old_p, new_p = mapping.get(old_ipsw), mapping.get(new_ipsw)
            if old_p and new_p and os.path.realpath(old_p) == os.path.realpath(new_p):
                mapping[old_ipsw] = None
                old_p = None
            if new_p and not old_p:
                state.record_analysis_note(
                    f"firmware_diff: old {label} missing from .ipsw_extracted — the "
                    f"{label} diff is SKIPPED (no coverage for changes in that cache, "
                    f"e.g. dyld_shared_cache dylibs). Re-extract the old IPSW's {label}."
                )
        _check_diff_inputs(dyld_map, "dyld_shared_cache")
        _check_diff_inputs(kernel_map, "kernelcache")

        request = FirmwareDiffRequest(
            old_ipsw=old_ipsw,
            new_ipsw=new_ipsw,
            old_dyld=dyld_map.get(old_ipsw),
            new_dyld=dyld_map.get(new_ipsw),
            old_kernelcache=kernel_map.get(old_ipsw),
            new_kernelcache=kernel_map.get(new_ipsw),
            old_version=_format_version_from_ipsw(old_ipsw),
            new_version=_format_version_from_ipsw(new_ipsw),
        )
        service = FirmwareDiffService(workspace_root=state.workspace_root)
        result = service.run(request)

        # use structured report.json as the diff report for the LLM
        report_json_path = result.artifacts.report_json
        diff_report_text = read_text(report_json_path) if report_json_path and os.path.isfile(report_json_path) else ""

        framework_diff_path = result.artifacts.framework_diff
        if framework_diff_path and os.path.isfile(framework_diff_path):
            diff_report_path = framework_diff_path
        else:
            diff_report_path = ""
            raw_dir = result.artifacts.raw_diff_dir
            if raw_dir and os.path.isdir(raw_dir):
                for root, _, files in os.walk(raw_dir):
                    if "README.md" in files:
                        diff_report_path = os.path.join(root, "README.md")
                        break
        state = StateManager.add_intermediate_output(state, "firmware_diff_report", diff_report_text)
        state.intermediate_outputs["firmware_diff_report_path"] = diff_report_path
        if result.artifacts.raw_diff_dir:
            state.intermediate_outputs["firmware_raw_diff_dir"] = result.artifacts.raw_diff_dir
        return state


    def _diff_report_has_evidence(report_json_str: str) -> bool:
        """True when the report JSON carries something feature targets can be built from"""
        if not report_json_str:
            return False
        try:
            data = json.loads(report_json_str)
        except (json.JSONDecodeError, ValueError):
            return False
        if not isinstance(data, dict):
            return False
        if data.get("cstring_context") or data.get("symbol_context"):
            return True
        uc = data.get("userland_changes", {})
        return bool(isinstance(uc, dict) and (uc.get("frameworks") or uc.get("standard_binaries")))

    def _find_report_json_on_disk(state: AgentState) -> str:
        """Recover the structured report.json from disk when the in-graph payload is
        missing/empty/a skip-stub"""
        search_dirs: list[str] = []
        report_path = state.intermediate_outputs.get("firmware_diff_report_path", "")
        if report_path:
            directory = os.path.dirname(report_path)
            for _ in range(4):  # README is a few levels below the diff output root
                search_dirs.append(directory)
                parent = os.path.dirname(directory)
                if parent == directory:
                    break
                directory = parent
        raw_dir = state.intermediate_outputs.get("firmware_raw_diff_dir", "")
        if raw_dir:
            search_dirs.extend([raw_dir, os.path.dirname(raw_dir)])

        seen: set[str] = set()
        for directory in search_dirs:
            if not directory or directory in seen:
                continue
            seen.add(directory)
            candidate = os.path.join(directory, "report.json")
            if os.path.isfile(candidate):
                try:
                    text = read_text(candidate)
                except Exception:
                    continue
                if _diff_report_has_evidence(text):
                    return text
        return ""

    def _resolve_diff_report_json(state: AgentState) -> str:
        """Single resilient source for the diff report JSON used by feature analysis"""
        inline = state.intermediate_outputs.get("firmware_diff_report", "")
        if _diff_report_has_evidence(inline):
            return inline
        recovered = _find_report_json_on_disk(state)
        if recovered:
            state.intermediate_outputs["firmware_diff_report"] = recovered
            state.record_analysis_note(
                "feature_analysis: in-graph diff report was empty/stub; recovered report.json from disk."
            )
            return recovered
        return inline

    def _find_readme_for_state(state: AgentState) -> str:
        """Return README text from the diff artifact directory, or '' if not found"""
        report_path = state.intermediate_outputs.get("firmware_diff_report_path", "")
        if report_path and report_path.endswith("README.md") and os.path.isfile(report_path):
            try:
                return read_text(report_path)
            except Exception:
                pass
        # else derive from raw_diff_dir
        raw_dir = state.intermediate_outputs.get("firmware_raw_diff_dir", "")
        if raw_dir and os.path.isdir(raw_dir):
            for root, _dirs, files in os.walk(raw_dir):
                if "README.md" in files:
                    try:
                        return read_text(os.path.join(root, "README.md"))
                    except Exception:
                        pass
        return ""

    def _resolve_target_version(state: AgentState) -> str | None:
        report_path = state.intermediate_outputs.get("firmware_diff_report_path", "") or ""

        # 1. 
        if report_path.endswith("README.md") and os.path.isfile(report_path):
            try:
                first_line = read_text(report_path).splitlines()[0]
                versions = re.findall(r"\d+\.\d+(?:\.\d+)?", first_line)
                if versions:
                    return versions[-1]
            except Exception:
                pass

        # 2. diff directory name
        m = re.search(r"_vs_(\d+(?:_\d+)*)_\d+[A-Za-z]\d+", report_path)
        if m:
            return m.group(1).replace("_", ".")

        # 3. the newer of the two local IPSW artifacts
        try:
            _, new_ipsw = _select_diff_pair(state, _collect_confirmed_local_artifacts(state))
            if new_ipsw:
                m = re.search(r"_(\d+\.\d+(?:\.\d+)?)_", os.path.basename(new_ipsw))
                if m:
                    return m.group(1)
        except Exception:
            pass
        return None

    def _write_triage_summary(state: AgentState) -> None:
        """Emit a single consolidated markdown index of every diff component and how
        it was classified — HIGH/LOW signal, security tier, Apple Security Notes
        match, and whether it was analysed — so researchers know where to focus."""
        index = state.feature_triage_index
        if not index:
            return

        report_path = state.intermediate_outputs.get("firmware_diff_report_path", "")
        output_dir = _resolve_feature_output_dir(report_path, state.workspace_root)
        version = state.intermediate_outputs.get("feature_triage_version", "")

        markdown = render_triage_summary(index, version)
        summary_path = os.path.join(output_dir, "00_SUMMARY.md")
        write_text(summary_path, markdown)

        high = sum(1 for r in index if r.get("signal") == "HIGH_SIGNAL")
        analysed = sum(1 for r in index if r.get("saved"))
        state.feature_analysis_reports["__summary__"] = summary_path
        state.record_analysis_note(
            f"feature_analysis summary written: {analysed} report(s), "
            f"{high} HIGH_SIGNAL / {len(index) - high} LOW_SIGNAL indexed -> {summary_path}"
        )

    def feature_analysis_select_node(state: AgentState) -> AgentState:
        if not state.feature_analysis_queue and not state.feature_analysis_targets:
            report_json_str = _resolve_diff_report_json(state)

            if not _diff_report_has_evidence(report_json_str):
                state.feature_analysis_targets = []
                state.feature_analysis_queue = []
                state.feature_analysis_current = None
                state.record_analysis_note(
                    "feature_analysis skipped: no diff report with component evidence "
                    "(checked in-graph payload and on-disk report.json)."
                )
                return state

            targets = _build_feature_targets(report_json_str)

            readme_text = _find_readme_for_state(state)
            if readme_text:
                # split + scan the README ONCE, then O(1) lookup per component
                readme_index = _build_readme_diff_index(readme_text.splitlines())
                for t in targets:
                    readme_diff = readme_index.get(t["name"], "")
                    if readme_diff:
                        t["evidence"] = t["evidence"] + "\n\nBinary diff (from README):\n" + readme_diff

            for t in targets:
                indicators = _extract_security_indicators(t.get("evidence", ""))
                if indicators:
                    t["security_indicators"] = indicators

            target_version = _resolve_target_version(state)
            notes_service = SecurityNotesService.for_version(target_version)
            matched = 0
            promoted = 0
            if notes_service.has_entries():
                for t in targets:
                    matched_component = notes_service.match_component(t["name"])
                    if not matched_component:
                        continue
                    t["security_notes_match"] = matched_component
                    matched += 1
                    if t.get("_triage_signal") != "HIGH_SIGNAL":
                        t["_triage_signal"] = "HIGH_SIGNAL"
                        t["_triage_reason"] = (
                            f"Apple Security Notes name this component ({matched_component}) "
                            "as changed this release"
                        )
                        promoted += 1
                note = (
                    f"Apple Security Notes (iOS {target_version}) matched {matched} of "
                    f"{len(targets)} component(s) by name"
                )
                if promoted:
                    note += f" ({promoted} promoted from LOW_SIGNAL)"
                state.record_analysis_note(note + ".")
            else:
                state.record_analysis_note(
                    "Apple Security Notes matching skipped: could not fetch advisory for "
                    f"version {target_version or 'unknown'}."
                )

            # keep only HIGH_SIGNAL components
            high_signal = [t for t in targets if t.get("_triage_signal") == "HIGH_SIGNAL"]
            # security score is computed for every HIGH_SIGNAL component so the
            # consolidated summary can rank/tier even the ones we don't fully analyse
            for t in high_signal:
                t["_security_score"] = _security_score(t)
            for t in targets:
                if t.get("_triage_signal") != "HIGH_SIGNAL":
                    print(f"[TRIAGE] Skipping {t.get('name', '?')} — LOW_SIGNAL ({t.get('_triage_reason', '')})")

            large_mode = len(high_signal) > FEATURE_ANALYSIS_BUDGET
            if large_mode:
                total_high = len(high_signal)
                # keep only security-relevant components (score >= 2): Apple-confirmed,
                # hard indicators, or security vocabulary. Pure code/asset churn drops
                candidates = [t for t in high_signal if t["_security_score"] >= 2]
                dropped = total_high - len(candidates)
                candidates.sort(
                    key=lambda t: (-t["_security_score"], -_component_change_volume(t.get("evidence", "")))
                )
                capped = candidates[:FEATURE_ANALYSIS_BUDGET]
                for t in capped:
                    t["_drop_tier3"] = True  # save-gate: suppress LLM-rated TIER_3 output
                notes_matches = sum(1 for t in capped if t.get("security_notes_match"))
                indicator_hits = sum(1 for t in capped if t.get("security_indicators"))
                selected = capped
                state.record_analysis_note(
                    f"feature_analysis large-workload mode: {total_high} HIGH_SIGNAL "
                    f"component(s) exceeded budget of {FEATURE_ANALYSIS_BUDGET}. "
                    f"Dropped {dropped} component(s) with no security relevance; "
                    f"analysing top {len(capped)} by security score "
                    f"({notes_matches} Apple Security Notes match(es), "
                    f"{indicator_hits} with hard security indicators). "
                    "Only TIER_1/TIER_2 reports will be emitted."
                )
            else:
                selected = high_signal

            # Resume (opt-in via FEATURE_ANALYSIS_RESUME=1): skip components that
            # already have a report on disk so a run that died partway (recursion /
            # token limit) finishes only the remaining components instead of
            # re-analysing everything. Skipped components are still recorded as
            # analysed in the index/summary.
            resume_done: dict[str, str] = {}
            if os.environ.get("FEATURE_ANALYSIS_RESUME") == "1":
                out_dir = _resolve_feature_output_dir(
                    state.intermediate_outputs.get("firmware_diff_report_path", ""),
                    state.workspace_root,
                )
                for t in selected:
                    existing = os.path.join(out_dir, f"{_slugify_feature(t.get('name', 'feature'))}_analysis.md")
                    if os.path.isfile(existing):
                        resume_done[t.get("name")] = existing
                if resume_done:
                    state.record_analysis_note(
                        f"feature_analysis resume: {len(resume_done)} of {len(selected)} selected "
                        f"component(s) already reported on disk; analysing the remaining "
                        f"{len(selected) - len(resume_done)}."
                    )

            # mark selected components and record a classification row for EVERY
            # component so the end-of-run summary can list HIGH/LOW signal + tier.
            selected_ids = {id(t) for t in selected}
            state.feature_triage_index = []
            for t in targets:
                is_high = t.get("_triage_signal") == "HIGH_SIGNAL"
                score = t.get("_security_score") if is_high else None
                done_path = resume_done.get(t.get("name")) if id(t) in selected_ids else None
                state.feature_triage_index.append({
                    "name": t.get("name", "?"),
                    "signal": t.get("_triage_signal", "LOW_SIGNAL"),
                    "security_score": score,
                    "pretier": _pretier_from_score(score) if is_high else None,
                    "security_notes_match": t.get("security_notes_match"),
                    "security_indicators": t.get("security_indicators", []),
                    "selected": id(t) in selected_ids,
                    "llm_tier": None,
                    "report_path": done_path,
                    "saved": True if done_path else None,
                })
            state.intermediate_outputs["feature_triage_version"] = str(target_version or "")

            # queue excludes components already completed on a prior (resumed) run
            remaining = [t for t in selected if t.get("name") not in resume_done]
            state.feature_analysis_targets = selected
            state.feature_analysis_queue = list(remaining)
            high_signal = selected
            if high_signal:
                state.record_analysis_note(f"feature_analysis targets: {len(high_signal)} HIGH_SIGNAL component(s).")
            else:
                state.record_analysis_note(
                    "feature_analysis: diff report parsed but all components were LOW_SIGNAL "
                    "(metadata/timestamp churn only)."
                )

        # pop next feature from queue, resetting tool state for each new component
        if state.feature_analysis_queue:
            state.feature_analysis_current = state.feature_analysis_queue.pop(0)
            # reset tool state so each component gets a fresh tool budget
            state.tool_iteration = 0
            state.tool_requests = []
            state.tool_results = []
            state.agent_chain = []
            # clear previous component's analysis output
            state.intermediate_outputs.pop("unified_feature_analysis", None)
        else:
            # queue drained — emit the consolidated classification summary once
            state.feature_analysis_current = None
            if not state.intermediate_outputs.get("feature_triage_summary_written"):
                _write_triage_summary(state)
                state.intermediate_outputs["feature_triage_summary_written"] = "1"
        return state

    def _is_macho_binary(filepath: str) -> bool:
        MACHO_MAGICS = {b'\xfe\xed\xfa\xce', b'\xfe\xed\xfa\xcf', b'\xce\xfa\xed\xfe', b'\xcf\xfa\xed\xfe', b'\xca\xfe\xba\xbe'}
        try:
            with open(filepath, 'rb') as f:
                magic = f.read(4)
            return magic in MACHO_MAGICS
        except (OSError, IOError):
            return False

    def prepare_decompiler_node(state: AgentState) -> AgentState:
        feature = state.feature_analysis_current
        if not feature:
            return state

        from langgraph_orchestration.tooling.decompiler_tools import start_ida_server_for_binary
        import subprocess

        def _find_macho_in_dir(directory: str, target_name: str) -> str | None:
            matches: list[str] = []
            for root, dirs, files in os.walk(directory):
                dirs.sort()
                for file in sorted(files):
                    if file == target_name:
                        candidate = os.path.join(root, file)
                        if _is_macho_binary(candidate):
                            matches.append(candidate)
            return sorted(matches)[0] if matches else None

        component_name = feature.get("name")
        if not component_name:
            return state

        feature_binary_path = feature.get("binary_path", "")

        # route extraction into a per-comparison subfolder so cached binaries and
        # annotated .i64 databases stay grouped by the firmware diff they came from
        import glob
        local_ipsws = _collect_confirmed_local_artifacts(state)
        old_ipsw, new_ipsw = _select_diff_pair(state, local_ipsws)
        features_root = os.path.join(state.workspace_root or os.getcwd(), ".ipsw_features")
        comparison_subdir = _comparison_dirname(old_ipsw, new_ipsw)
        output_dir = os.path.join(features_root, comparison_subdir) if comparison_subdir else features_root
        os.makedirs(output_dir, exist_ok=True)
        target_basename = os.path.basename(feature_binary_path) if feature_binary_path else component_name
        extracted_binary = None

        _dsc_path_prefixes = (
            "/System/Library/Frameworks/",
            "/System/Library/PrivateFrameworks/",
            "/usr/lib/",
        )

        # strategy 1: scan this comparison's folder to avoid re-extracting on every component
        if os.path.isdir(output_dir):
            extracted_binary = _find_macho_in_dir(output_dir, target_basename)
            if extracted_binary:
                state.record_analysis_note(
                    f"Re-using cached binary from .ipsw_features/{comparison_subdir or ''}: "
                    f"{os.path.basename(extracted_binary)}"
                )

        # strategy 2: extract from DSC / IPSW if not already cached
        if not extracted_binary:
            # strategy 2a: DSC dylib extraction (only if DSC already in .ipsw_extracted/)
            if feature_binary_path:
                dsc_path = None
                if new_ipsw:
                    dsc_path = _find_dsc_for_ipsw(new_ipsw, state.workspace_root)

                if dsc_path:
                    try:
                        subprocess.run(
                            ["ipsw", "dyld", "extract", dsc_path, feature_binary_path, "-o", output_dir],
                            check=True,
                            capture_output=True
                        )
                    except subprocess.CalledProcessError as e:
                        stderr = e.stderr.decode(errors='replace') if isinstance(e.stderr, bytes) else str(e.stderr)
                        if "not found in cache" in stderr:
                            state.record_analysis_note("Component not found in DSC (proceeding to filesystem extraction fallback).")
                        else:
                            error_line = [line for line in stderr.split('\n') if '⨯' in line or 'Error' in line]
                            short_err = error_line[0] if error_line else stderr[:100]
                            state.record_analysis_note(f"DSC extract failed ({os.path.basename(dsc_path)}): {short_err}")

                    extracted_binary = _find_macho_in_dir(output_dir, target_basename)

            # strategy 2b: Check existing DMG mounts (left by ipsw diff)
            if not extracted_binary and feature_binary_path:
                for mount_dir in sorted(glob.glob("/private/tmp/*.mount")):
                    if os.path.isdir(mount_dir):
                        mounted_file = os.path.join(mount_dir, feature_binary_path.lstrip("/"))
                        if os.path.isfile(mounted_file):
                            import shutil
                            dest_path = os.path.join(output_dir, target_basename)
                            shutil.copy2(mounted_file, dest_path)
                            extracted_binary = dest_path
                            state.record_analysis_note(f"Copied binary from existing mount: {mount_dir}")
                            break

            # strategy 2c: Direct file extraction from IPSW archive (fallback for daemons/apps only)
            _is_dsc_binary = feature_binary_path and any(
                feature_binary_path.startswith(p) for p in _dsc_path_prefixes
            )
            if not extracted_binary and new_ipsw and not _is_dsc_binary:
                pattern = f".*{re.escape(target_basename)}$"
                try:
                    subprocess.run(
                        ["ipsw", "extract", new_ipsw, "--files", "--pattern", pattern, "-o", output_dir],
                        check=True,
                        capture_output=True
                    )
                except subprocess.CalledProcessError as e:
                    stderr = e.stderr.decode(errors='replace') if isinstance(e.stderr, bytes) else str(e.stderr)
                    if "hdiutil: attach failed" in stderr or "Permission denied" in stderr:
                        state.record_analysis_note(
                            "Environment restricted from mounting DMGs. Skipping filesystem extraction for this non-DSC binary."
                        )
                    else:
                        error_line = [line for line in stderr.split('\n') if '⨯' in line or 'Error' in line]
                        short_err = error_line[0] if error_line else stderr[:100]
                        state.record_analysis_note(f"Failed to extract {component_name} from {new_ipsw}: {short_err}")

                if not extracted_binary:
                    extracted_binary = _find_macho_in_dir(output_dir, target_basename)
            elif _is_dsc_binary and not extracted_binary:
                state.record_analysis_note(
                    f"{component_name} is DSC-resident; Strategy 2c (--files) skipped. Extraction requires DSC to be present in .ipsw_extracted/."
                )

            if not extracted_binary and not feature_binary_path:
                state.record_analysis_note(
                    f"No binary_path in feature entry for {component_name}; "
                    "cannot attempt extraction. Decompiler unavailable."
                )

        if extracted_binary:
            feature["decompiler_available"] = True
            state.record_analysis_note(f"Decompiler target: {extracted_binary}")
            result = start_ida_server_for_binary.invoke({"binary_path": extracted_binary})
            state.record_analysis_note(f"Decompiler prepare: {result}")
            # deterministically decompile the top added CODE symbols so the report
            # carries real pseudocode even if the model later skips decompile_function
            if isinstance(result, str) and "Successfully started" in result:
                try:
                    _auto_decompile_top_symbols(feature)
                    n = len(feature.get("_auto_decompilations", []))
                    if n:
                        state.record_analysis_note(f"Auto-decompiled {n} top CODE symbol(s) for injection.")
                except Exception as e:
                    state.record_analysis_note(f"Auto-decompile skipped ({type(e).__name__}: {str(e)[:100]}).")
        else:
            feature["decompiler_available"] = False
            state.record_analysis_note(f"Could not locate Mach-O binary for {component_name}. Decompiler unavailable for this component.")
        return state

    def _parse_addr(value) -> int | None:
        try:
            if isinstance(value, str):
                value = value.strip()
                return int(value, 16) if value.lower().startswith("0x") else int(value)
            return int(value)
        except (ValueError, TypeError):
            return None

    def _collect_analyzed_func_addresses(state: AgentState) -> list[int]:
        """Functions covered by baseline annotations"""
        addrs: list[int] = []
        seen: set[int] = set()

        def _add(value) -> None:
            a = _parse_addr(value)
            if a and a not in seen:
                seen.add(a)
                addrs.append(a)

        # any tool that names a function carries an address we should annotate +
        # so collect function-address argument from all relevant tools 
        func_addr_args = {
            "decompile_function": "address",
            "rename_local_variable": "func_address",
            "trace_variable_source": "func_ea",
            "resolve_objc_dispatch": "func_ea",
        }
        for req in state.tool_requests:
            key = func_addr_args.get(req.tool_name)
            if key:
                _add(req.arguments.get(key))
        for res in state.tool_results:
            if res.tool_name == "find_address" and res.success and res.output:
                try:
                    data = json.loads(res.output.split("\n\nNOTE:")[0])
                except (json.JSONDecodeError, ValueError):
                    continue
                if data.get("type") in ("symbol", "symbol_fuzzy") and data.get("address"):
                    _add(data["address"])
        # deterministic auto-decompiled functions never pass through the model's tool
        # loop, so include them explicitly — otherwise the annotation floor (and its
        # semantic renames) never reaches the very functions the report injects
        feature = state.feature_analysis_current or {}
        for d in feature.get("_auto_decompilations") or []:
            _add(d.get("address"))
        return addrs

    def _build_review_header_comment(feature: dict) -> str:
        """Provenance line stamped at each analysed function so a researcher
        opening the .i64 sees why it was flagged"""
        parts = [f"[AI-RE] Component: {feature.get('name', 'component')}"]
        notes_match = feature.get("security_notes_match")
        if notes_match:
            parts.append(f"Apple Security Notes: {notes_match}")
        reason = feature.get("_triage_reason")
        if reason:
            parts.append(f"Triage: {reason}")
        parts.append("Auto-annotated for researcher review.")
        return " | ".join(parts)

    def cleanup_decompiler_node(state: AgentState) -> AgentState:
        import time as _time
        from langgraph_orchestration.tooling.decompiler_tools import (
            save_ida_database,
            stop_ida_server,
            auto_annotate_function,
            count_user_annotations,
        )

        feature = state.feature_analysis_current or {}
        ida_available = bool(feature.get("decompiler_available", False))
        func_addrs = _collect_analyzed_func_addresses(state) if ida_available else []

        audit = {
            "functions": len(func_addrs),
            "llm_renames": sum(1 for r in state.tool_results if r.tool_name == "rename_local_variable" and r.success),
            "llm_comments": sum(1 for r in state.tool_results if r.tool_name == "set_comment" and r.success),
            "auto_renames": 0,
            "auto_comments": 0,
            "verified_named_lvars": 0,
            "verified_comments": 0,
        }

        if ida_available and func_addrs:
            header = _build_review_header_comment(feature)
            for fea in func_addrs:
                try:
                    res = auto_annotate_function(fea, header)
                except Exception as exc:
                    state.record_analysis_note(f"Annotation floor error at {hex(fea)} (non-fatal): {exc}")
                    continue
                audit["auto_renames"] += int(res.get("renamed", 0) or 0)
                audit["auto_comments"] += int(res.get("commented", 0) or 0)
            state.record_analysis_note(
                f"Annotation floor: {audit['functions']} function(s) | AI-authored "
                f"renames={audit['llm_renames']} comments={audit['llm_comments']} | "
                f"auto-generated renames+={audit['auto_renames']} comments+={audit['auto_comments']}."
            )

        # Re-decompile the injected functions now that the annotation floor has run,
        # so the report shows the annotated code (semantic renames + comments) instead
        # of the raw pre-analysis snapshot. The IDA server is still up at this point.
        if ida_available:
            try:
                from langgraph_orchestration.tooling.decompiler_tools import decompile_function as _decompile
                injected = list(feature.get("_auto_decompilations") or [])
                seen_addr = {str(d.get("address")) for d in injected}
                for r in state.tool_results:  # include functions the model decompiled itself
                    if r.tool_name == "decompile_function" and r.success:
                        a = (getattr(r, "metadata", None) or {}).get("decompile_address")
                        if a and str(a) not in seen_addr:
                            injected.append({"address": a, "symbol": None})
                            seen_addr.add(str(a))
                final = []
                for d in injected:
                    addr = d.get("address")
                    if not addr:
                        continue
                    code = _decompile.invoke({"address": addr})
                    if _usable_decompilation(code):
                        final.append({"address": addr, "code": code, "symbol": d.get("symbol")})
                if final:
                    feature["_final_decompilations"] = final
            except Exception as exc:
                state.record_analysis_note(f"Post-annotation re-decompile skipped (non-fatal): {exc}")

        # retry save up to 3 times to guarantee .i64 is written before shutdown
        save_result = "Not attempted"
        for attempt in range(3):
            save_result = save_ida_database.invoke({})
            if "successfully" in save_result.lower():
                break
            state.record_analysis_note(f"Decompiler save attempt {attempt + 1} failed: {save_result}")
            _time.sleep(2)
        state.record_analysis_note(f"Decompiler save: {save_result}")

        if ida_available and func_addrs and "successfully" in save_result.lower():
            try:
                verify = count_user_annotations(func_addrs)
                audit["verified_named_lvars"] = int(verify.get("named_lvars", 0) or 0)
                audit["verified_comments"] = int(verify.get("comments", 0) or 0)
                state.record_analysis_note(
                    f"Annotation verification (post-save): named_lvars={audit['verified_named_lvars']}, "
                    f"comments={audit['verified_comments']} across {verify.get('functions', 0)} function(s)."
                )
                if audit["verified_named_lvars"] == 0 and audit["verified_comments"] == 0:
                    state.record_analysis_note(
                        "WARNING: annotation verification found zero persisted annotations for this component."
                    )
            except Exception as exc:
                state.record_analysis_note(f"Annotation verification error (non-fatal): {exc}")

        if isinstance(state.feature_analysis_current, dict):
            state.feature_analysis_current["_annotation_audit"] = audit

        stop_result = stop_ida_server.invoke({})
        state.record_analysis_note(f"Decompiler cleanup: {stop_result}")
        return state

    def unified_feature_analysis_node(state: AgentState) -> AgentState:
        feature = state.feature_analysis_current
        if not feature:
            return state
        from langgraph_orchestration.prompts.reverse_engineering import build_unified_feature_analysis_prompt

        ida_available = feature.get("decompiler_available", True)
        stage1_tools = {"find_address"}
        stage2_tools = {"get_xrefs_to", "decompile_function"}
        used_tool_names = {r.tool_name for r in state.tool_results}
        has_stage1_results = bool(used_tool_names & stage1_tools)
        has_stage2_results = bool(used_tool_names & stage2_tools)
        hard_at_limit = state.tool_iteration >= state.max_tool_iterations

        # Stop retrying failed annotation calls once they cross the limit; cleanup
        # still writes baseline renames and comments to the .i64
        comp_renames = sum(1 for r in state.tool_results if r.tool_name == "rename_local_variable" and r.success)
        comp_comments = sum(1 for r in state.tool_results if r.tool_name == "set_comment" and r.success)
        annotations_met = comp_renames >= 1 and comp_comments >= 1
        annot_failures = sum(
            1 for r in state.tool_results
            if r.tool_name in ("rename_local_variable", "set_comment") and not r.success
        )
        annotation_stalled = annot_failures >= ANNOTATION_FAILURE_LIMIT and not annotations_met
        if annotation_stalled and not feature.get("_annotation_stalled"):
            feature["_annotation_stalled"] = True
            state.record_analysis_note(
                f"{feature.get('name', 'component')}: {annot_failures} failed annotation "
                "attempt(s) with the rename+comment floor unmet — forcing the report and "
                "relying on the deterministic annotation floor in cleanup."
            )

        # force the report at the hard tool ceiling OR on an annotation stall
        force_finish = hard_at_limit or annotation_stalled
        # stage 1 (find_address) is always allowed, doesn't require IDA
        # stage 2 (decompile_function, get_xrefs_to) requires IDA to be loaded
        ida_at_limit = force_finish or not ida_available

        prompt = build_unified_feature_analysis_prompt(
            user_input=state.user_input,
            component_evidence=_truncate_for_prompt(
                feature.get("evidence", ""), FEATURE_EVIDENCE_CHAR_BUDGET, "component evidence"
            ),
            component_name=feature.get("name", "Unknown Component"),
            has_tool_results=bool(state.tool_results),
            at_limit=ida_at_limit,
            security_notes_match=feature.get("security_notes_match"),
            security_indicators=feature.get("security_indicators"),
            # ground the model's prose in the deterministically decompiled top functions
            decompilations=feature.get("_auto_decompilations"),
        )
        context_blocks = []
        if state.tool_results:
            context_blocks.append(StateManager.format_tool_activity(state))

        if context_blocks:
            tool_context = _truncate_for_prompt(
                "\n\n".join(context_blocks), FEATURE_TOOL_CONTEXT_CHAR_BUDGET, "tool output"
            )
            prompt += "\n\n=== RECENT TOOL EXECUTION CONTEXT ===\n" + tool_context + "\n=====================================\n"

            if force_finish:
                # tool budget exhausted, or annotation attempts stalled — stop tools
                prompt += (
                    "\n**CRITICAL FINAL INSTRUCTION**: Stop calling tools. "
                    "You MUST NOT output any more `<tool_call>` blocks. "
                    "Output the final report NOW starting EXACTLY with `## What this feature does`."
                )
            elif has_stage1_results and not has_stage2_results:
                # collect addresses from Stage 1 tool results to guide the model
                symbol_addrs = []
                string_addrs = []
                for r in state.tool_results:
                    if r.tool_name == "find_address" and r.success and r.output.strip():
                        # extract the JSON part before the NOTE: string
                        json_part = r.output.split("\n\nNOTE:")[0]
                        try:
                            data = json.loads(json_part)
                            if data.get("type") == "symbol":
                                symbol_addrs.append(data.get("address"))
                                prompt += "\n**HINT**: You have found a CODE symbol address. To investigate its logic, you MUST call `decompile_function` on that address now."
                            elif data.get("type") == "string_data":
                                addrs = data.get("addresses", [])
                                string_addrs.append(", ".join(addrs))
                            elif data.get("type") == "data_symbol":
                                # e.g. an ObjC class pointer _OBJC_CLASS_$_CDPDUnlockListener
                                string_addrs.append(data.get("address"))
                        except Exception:
                            pass
                addr_block = ""
                if symbol_addrs:
                    addr_block += f"- **Exported symbol addresses** (use `decompile_function`): {', '.join(symbol_addrs)}\n"
                if string_addrs:
                    addr_block += f"- **String data addresses** (use `get_xrefs_to` FIRST): {'; '.join(string_addrs)}\n"
                prompt += (
                    f"\n**CRITICAL STAGE 2 INSTRUCTION — MANDATORY DECOMPILATION**: "
                    f"You have completed Stage 1 and obtained these memory addresses:\n"
                    f"{addr_block}\n"
                    f"You MUST now proceed to Stage 2. You are NOT allowed to write the final report yet.\n"
                    f"**Execute in this exact order** (to avoid IDA stream timeouts):\n"
                    f"  STEP A — Call `get_xrefs_to` for EACH string data address above (all xrefs first, before any decompile).\n"
                    f"  STEP B — Call `decompile_function` on the exported symbol address.\n"
                    f"  STEP C — Call `decompile_function` on the most interesting CALLER functions found in Step A.\n"
                    f"  STEP D — Trace the full data flow: caller → function → what it does with the data.\n"
                    f"Output ONLY `<tool_call>` blocks in this order. Do NOT write the report yet."
                )
            elif has_stage2_results:
                # stage 2: allow annotations and iterative decompilation
                prompt += (
                    "\n**CRITICAL STAGE 2 INSTRUCTION**: You have obtained decompilation results. "
                    "Before writing the final report, you MUST use `rename_local_variable` and `set_comment` to annotate the code. "
                    "When you decipher variables or understand the data flow, document them. "
                    "Run `save_ida_database` to persist your annotations. "
                    "If you need to trace more code, use `get_xrefs_to` or `decompile_function`. "
                    "If you have fully analyzed and annotated the feature, transition to STAGE 3 and write the final report. "
                    "To write the report, start EXACTLY with `## What this feature does`. In `## How is it implemented`, write PROSE only and describe the caller chains — do NOT paste or invent code; the system inserts the real decompilation for you. "
                    "End with `---AI_PRIORITISATION_SCORE---` and the JSON score."
                )
            else:
                # intermediate state: continue gathering evidence
                prompt += (
                    "\n**INSTRUCTION**: Evaluate the tool results. If you need more data, output ONLY `<tool_call>` blocks. "
                    "Do NOT write the final report until Stage 2 decompilation is complete."
                )

        if _RE_DEBUG:
            print(f"\n\n[DEBUG STATE] tool_iteration={state.tool_iteration}/{state.max_tool_iterations} "
                  f"stage1={has_stage1_results} stage2={has_stage2_results} hard_at_limit={hard_at_limit}")
            print(f"\n\n[DEBUG PROMPT]\n{prompt}\n[END DEBUG PROMPT]\n\n")

        engine = _get_feature_engine()
        # disable thinking for cross-major diffs so the full output budget goes to the report
        # keep it for same-major point releases
        report_thinking = not _is_cross_major_diff(state)
        if _RE_DEBUG:
            print(f"[DEBUG THINKING] report generation enable_thinking={report_thinking}")
        chat_prompt = engine.build_prompt(user_input=prompt, system_prompt="", enable_thinking=report_thinking)
        try:
            output = engine.generate(
                chat_prompt,
                config=GenerationConfig(max_tokens=8192, temperature=0.0),
                stream=False,
            )
        except Exception as gen_err:
            # isolate per-component generation failures (e.g. model context-window
            # overflow, transient API errors) so one bad component can't abort the
            # whole run
            name = feature.get("name", "component")
            state.record_analysis_note(
                f"{name}: analysis generation failed ({type(gen_err).__name__}: "
                f"{str(gen_err)[:200]}); saved a stub and continued."
            )
            feature["_generation_failed"] = True
            state.tool_requests = []
            stub = (
                "## What this feature does\n"
                f"Automated analysis could not complete for `{name}` "
                f"({type(gen_err).__name__}). This typically happens when the component's "
                "changes are too large for the model's context window.\n\n"
                "## How is it implemented\n(Not available — analysis failed)\n\n"
                "## How to trigger this feature\n(Not available — analysis failed)\n\n"
                "## Vulnerability Assessment\n(Not available — analysis failed)\n\n"
                "## Evidence\n(Not available — analysis failed)"
            )
            return StateManager.add_intermediate_output(state, "unified_feature_analysis", stub)

        # parse and handle limit logic/broken output
        from langgraph_orchestration.tooling.parser import parse_agent_output
        parsed = parse_agent_output(output)
        
        is_forcing_report = force_finish or not ida_available
        output_has_report = "## What this feature does" in output
        output_has_tools = parsed.has_tool_calls() or "<tool_call>" in output
        needs_retry = False
        error_msg = ""

        # annotation gate: the model must annotate decompiled code (rename opaque
        # variables & comment data flow) before it is allowed to finish a
        # component. comp_renames/comp_comments/annotations_met were computed above;
        # have cap on attempts + tool budget so it never loops forever
        enforce_attempts = int(feature.get("_annot_enforce_attempts", 0))

        if is_forcing_report:
            # must write a final report — no tool calls allowed + report header is mandatory
            if output_has_tools or not output_has_report:
                needs_retry = True
                error_msg = (
                    "**SYSTEM ERROR**: You MUST write the final markdown report NOW using the evidence provided. "
                    "Tool calls are NOT accepted in this state. "
                    "Start your response EXACTLY with `## What this feature does`."
                )
        elif not output_has_tools and not output_has_report:
            # model produced neither tool calls nor a report — force it to call tools
            needs_retry = True
            error_msg = (
                "**SYSTEM ERROR**: Your response did not contain any `<tool_call>` blocks. "
                "You MUST call `find_address` on the key symbols and strings from the diff before writing the report. "
                "Output ONLY `<tool_call>` blocks now. Do NOT write a report in this turn."
            )
        elif (
            output_has_report
            and not output_has_tools
            and has_stage2_results
            and not annotations_met
            and enforce_attempts < 2
        ):
            # model tried to finish without annotating the decompiled code
            # push back to annotate first (meaningful renames + comments), then save.
            feature["_annot_enforce_attempts"] = enforce_attempts + 1
            needs_retry = True
            error_msg = (
                "**SYSTEM ERROR — ANNOTATIONS REQUIRED BEFORE REPORT**: You decompiled code but have not "
                f"annotated the database (so far: {comp_renames} variable rename(s), {comp_comments} comment(s)). "
                "Researchers review the saved .i64, so annotation is mandatory before the report. "
                "Output ONLY `<tool_call>` blocks now that: (1) call `rename_local_variable` to give meaningful "
                "names to opaque variables such as v1/v2/a1 in the functions you decompiled; (2) call `set_comment` "
                "to document the data flow and key call sites; then (3) call `save_ida_database`. "
                "Do NOT write the report in this turn."
            )
        elif not parsed.has_tool_calls() and "<tool_call>" in output:
            needs_retry = True
            error_msg = (
                "**SYSTEM ERROR**: Your `<tool_call>` block was incomplete or contained invalid JSON. "
                "Ensure you include the closing `</tool_call>` tag and valid JSON. "
                "If you were trying to output a final report, DO NOT include `<tool_call>` blocks at all."
            )
            
        if needs_retry:
            prompt += f"\n\n{output}\n\n{error_msg}"
            chat_prompt_retry = engine.build_prompt(user_input=prompt, system_prompt="", enable_thinking=report_thinking)
            try:
                output = engine.generate(
                    chat_prompt_retry,
                    config=GenerationConfig(max_tokens=8192, temperature=0.0),
                    stream=False,
                )
                parsed = parse_agent_output(output)
            except Exception as gen_err:
                # retry failed — keep the pre-retry output rather than aborting the run
                state.record_analysis_note(
                    f"{feature.get('name', 'component')}: retry generation failed "
                    f"({type(gen_err).__name__}); keeping prior output."
                )

        # ungrounded fallback: if the model's final report is invalid 
        report_ok = ("## What this feature does" in output) and ("<think>" not in output) and ("</think>" not in output)
        if is_forcing_report and not report_ok and feature.get("_auto_decompilations"):
            fb_prompt = build_unified_feature_analysis_prompt(
                user_input=state.user_input,
                component_evidence=_truncate_for_prompt(
                    feature.get("evidence", ""), FEATURE_EVIDENCE_CHAR_BUDGET, "component evidence"
                ),
                component_name=feature.get("name", "Unknown Component"),
                has_tool_results=bool(state.tool_results),
                at_limit=True,
                security_notes_match=feature.get("security_notes_match"),
                security_indicators=feature.get("security_indicators"),
                decompilations=None,  # drop grounding for the fallback
            )
            if context_blocks:
                fb_prompt += "\n\n=== RECENT TOOL EXECUTION CONTEXT ===\n" + tool_context + "\n=====================================\n"
            fb_prompt += (
                "\n**CRITICAL FINAL INSTRUCTION**: Output the final report NOW, starting EXACTLY with "
                "`## What this feature does`. Do NOT output any `<tool_call>` or `<think>` blocks."
            )
            try:
                alt = engine.generate(
                    engine.build_prompt(user_input=fb_prompt, system_prompt="", enable_thinking=False),
                    config=GenerationConfig(max_tokens=8192, temperature=0.0),
                    stream=False,
                )
                if ("## What this feature does" in alt) and ("<think>" not in alt) and ("</think>" not in alt):
                    output = alt
                    state.record_analysis_note(
                        f"{feature.get('name', 'component')}: grounded report invalid; ungrounded fallback succeeded."
                    )
                else:
                    state.record_analysis_note(
                        f"{feature.get('name', 'component')}: ungrounded fallback still invalid; keeping best output."
                    )
            except Exception as _fb_err:
                state.record_analysis_note(
                    f"{feature.get('name', 'component')}: ungrounded fallback error ({type(_fb_err).__name__})."
                )

        output = _sanitize_model_output(output)
        return StateManager.add_intermediate_output(state, "unified_feature_analysis", output)

    def route_after_unified_analysis(state: AgentState) -> str:
        # annotation loop stalled — go straight to cleanup (which runs the
        # deterministic annotation floor) instead of continuing on failing tools
        feature = state.feature_analysis_current
        if feature and feature.get("_annotation_stalled"):
            return "cleanup_decompiler"
        if should_continue_tool_loop(state):
            return "execute_tools"
        return "cleanup_decompiler"

    def feature_analysis_compile_node(state: AgentState) -> AgentState:
        feature = state.feature_analysis_current
        if not feature:
            return state

        raw_output = state.intermediate_outputs.get("unified_feature_analysis", "")
        if _RE_DEBUG:
            print(f"\n\n[DEBUG RAW OUTPUT]\n{raw_output}\n[END DEBUG RAW OUTPUT]\n\n")
        parts = raw_output.split("---AI_PRIORITISATION_SCORE---")
        
        markdown_report = StateManager.sanitize_output(parts[0].strip())
        # extract the core report starting from the primary header
        match = re.search(r'(## What this feature does[\s\S]*)', markdown_report, re.IGNORECASE)
        if match:
            markdown_report = match.group(1).strip()
            
        # strip any hallucinated tool logs that might be embedded anywhere
        _anchor = r'## What this feature does|## How is it implemented|## How to trigger this feature|## Vulnerability Assessment|## Evidence|---AI_PRIORITISATION_SCORE---|$'
        markdown_report = re.sub(r'## TOOL ACTIVITY[\s\S]*?(?=' + _anchor + ')', '', markdown_report, flags=re.IGNORECASE)
        markdown_report = re.sub(r'### Requested Tools[\s\S]*?(?=' + _anchor + ')', '', markdown_report, flags=re.IGNORECASE)
        markdown_report = re.sub(r'### Tool Results[\s\S]*?(?=' + _anchor + ')', '', markdown_report, flags=re.IGNORECASE)
        markdown_report = re.sub(r'<tool_call>[\s\S]*?(?:</tool_call>|(?=' + _anchor + '))', '', markdown_report, flags=re.IGNORECASE)
        
        markdown_report = markdown_report.strip()

        # deterministic decompilation injection
        markdown_report = _inject_real_decompilation(
            markdown_report,
            state.tool_results,
            feature.get("_final_decompilations") or feature.get("_auto_decompilations"),
        )

        report_failed = (
            not markdown_report
            or "## What this feature does" not in markdown_report
            or "<think>" in markdown_report
            or "</think>" in markdown_report
        )
        if report_failed:
            markdown_report = (
                "## What this feature does\n(Model failed to generate report content)\n\n"
                "## How is it implemented\n(No data)\n\n"
                "## How to trigger this feature\n(No data)\n\n"
                "## Vulnerability Assessment\n(No data)\n\n"
                "## Evidence\n(No data)"
            )
            
        score_json = parts[1].strip() if len(parts) > 1 else ""
        should_save = True

        # prepend auditable provenance header so every report explains why it exists
        triage_reason = feature.get("_triage_reason", "passed HIGH_SIGNAL triage")
        triage_line = feature.get("_triage_evidence_line", "")
        _auto_decomps = feature.get("_final_decompilations") or feature.get("_auto_decompilations") or []
        _decompilation_captured = any(
            _usable_decompilation((d or {}).get("code", "")) for d in _auto_decomps
        ) or any(
            getattr(r, "tool_name", "") == "decompile_function"
            and getattr(r, "success", False)
            and _usable_decompilation(getattr(r, "output", ""))
            for r in (state.tool_results or [])
        )
        analysis_mode = "decompiled" if _decompilation_captured else "evidence_only"
        provenance = (
            "## Triage Provenance\n"
            f"- **Inclusion**: HIGH_SIGNAL (deterministic rule engine)\n"
            f"- **Reason**: {triage_reason}\n"
        )
        if triage_line:
            provenance += f"- **Deciding evidence**: `{triage_line}`\n"
        provenance += f"- **Analysis mode**: {analysis_mode}\n"
        audit = feature.get("_annotation_audit")
        if audit:
            total_renames = audit.get("llm_renames", 0) + audit.get("auto_renames", 0)
            total_comments = audit.get("llm_comments", 0) + audit.get("auto_comments", 0)
            provenance += (
                f"- **Database annotations** — variable renames: {total_renames} "
                f"({audit.get('llm_renames', 0)} AI-authored, {audit.get('auto_renames', 0)} auto-generated); "
                f"comments: {total_comments} "
                f"({audit.get('llm_comments', 0)} AI-authored, {audit.get('auto_comments', 0)} auto-generated); "
                f"across {audit.get('functions', 0)} function(s); "
                f"verified persisted in .i64: {audit.get('verified_named_lvars', 0)} named variables, "
                f"{audit.get('verified_comments', 0)} comments.\n"
            )
        notes_match = feature.get("security_notes_match")
        if notes_match:
            provenance += (
                f"- **Apple Security Notes**: matches advisory component `{notes_match}` "
                "— Apple confirms a security-relevant change here; this analysis examines the "
                "likely vulnerability patch.\n"
            )
        provenance += "\n"
        markdown_report = provenance + markdown_report

        llm_tier = None
        if score_json:
            json_match = re.search(r'\{.*\}', score_json, re.DOTALL)
            if json_match:
                try:
                    parsed_score = json.loads(json_match.group(0))

                    tier = parsed_score.get("tier", "Unknown Tier")
                    # normalise any free-form tier value 
                    _tier_aliases = {
                        # numeric / shorthand
                        "1": "TIER_1", "tier1": "TIER_1", "tier 1": "TIER_1",
                        "2": "TIER_2", "tier2": "TIER_2", "tier 2": "TIER_2",
                        "3": "TIER_3", "tier3": "TIER_3", "tier 3": "TIER_3",
                        # descriptive words
                        "high": "TIER_1", "critical": "TIER_1", "high interest": "TIER_1",
                        "medium": "TIER_2", "medium interest": "TIER_2",
                        "low": "TIER_3", "low interest": "TIER_3", "noise": "TIER_3",
                    }
                    if isinstance(tier, str) and tier.lower() in _tier_aliases:
                        tier = _tier_aliases[tier.lower()]
                        parsed_score["tier"] = tier
                    if isinstance(tier, str):
                        llm_tier = tier

                    if isinstance(tier, str) and tier.upper() in ("TIER_3", "TIER3"):
                        # In large-workload mode we only emit TIER_1/TIER_2 reports.
                        # Apple Security Notes matches are always kept regardless of
                        # the LLM tier, since Apple confirms a security-relevant change.
                        if feature.get("_drop_tier3") and not feature.get("security_notes_match"):
                            should_save = False
                            state.record_analysis_note(
                                f"{feature.get('name', 'component')} scored {tier} after full analysis "
                                "— report suppressed (large-workload mode emits only TIER_1/TIER_2)."
                            )
                        else:
                            state.record_analysis_note(
                                f"{feature.get('name', 'component')} scored {tier} after full analysis — saved with advisory tier."
                            )

                    markdown_report += "\n\n## AI Prioritisation Scoring System\n\n"
                    method = parsed_score.get("method", "Unknown Method")
                    category = parsed_score.get("category", "Unknown Category")
                    reason = parsed_score.get("reason", "No reason provided")
                    markdown_report += f"- **{method}**\n  - **Tier**: {tier}\n  - **Category**: {category}\n  - **Reasoning**: {reason}\n\n"
                except json.JSONDecodeError:
                    state.record_analysis_note("Failed to parse JSON score from unified analysis output.")
                    markdown_report += "\n\n## AI Prioritisation Scoring System\n\n*(Failed to parse JSON score)*\n"
        else:
            markdown_report += "\n\n## AI Prioritisation Scoring System\n\nNo actionable methods or prioritisation targets identified for this component.\n\n"

        report_path = state.intermediate_outputs.get("firmware_diff_report_path", "")
        slug = _slugify_feature(feature.get("name", "feature"))

        saved_path = None
        if should_save:
            output_dir = _resolve_feature_output_dir(report_path, state.workspace_root)
            output_path = os.path.join(output_dir, f"{slug}_analysis.md")
            write_text(output_path, markdown_report)
            saved_path = output_path

            state.feature_analysis_reports[feature.get("name", slug)] = output_path
            state.intermediate_outputs["feature_analysis_reports"] = json.dumps(
                state.feature_analysis_reports,
                ensure_ascii=True,
                indent=2,
            )

        # fold the analysis result back into the consolidated triage index
        feature_name = feature.get("name")
        for row in state.feature_triage_index:
            if row.get("name") == feature_name:
                row["llm_tier"] = llm_tier
                row["saved"] = bool(should_save)
                row["report_path"] = saved_path
                break

        state.feature_analysis_current = None
        state.tool_requests.clear()
        state.tool_results.clear()
        state.tool_iteration = 0
        state.intermediate_outputs.pop("unified_feature_analysis", None)
        
        return state

    def route_after_feature_select(state: AgentState) -> str:
        """All items in the queue are already HIGH_SIGNAL (filtered at build time)"""
        if state.feature_analysis_current:
            return "prepare_decompiler"
        return "done"

    def re_planning_node(state: AgentState) -> AgentState:
        """MLXPlanningAgent: produce a structured RE plan / execution workflow."""
        from langgraph_orchestration.prompts.reverse_engineering import build_planning_prompt
        agent = _get_re_agent("planning")
        prompt = build_planning_prompt(state.user_input)
        plan = _sanitize_model_output(agent.invoke(user_input=prompt, context=state.re_context or None))
        return StateManager.add_intermediate_output(state, "re_plan", plan)

    def code_analysis_node(state: AgentState) -> AgentState:
        """MLXCodeAnalysisAgent: extract semantic insights, control/data flow, behaviour."""
        from langgraph_orchestration.prompts.reverse_engineering import build_code_analysis_prompt
        agent = _get_re_agent("code_analysis")
        plan = state.intermediate_outputs.get("re_plan", "")
        prompt = build_code_analysis_prompt(state.user_input, planning_output=plan)
        analysis = _sanitize_model_output(agent.invoke(user_input=prompt, context=state.re_context or None))
        return StateManager.add_intermediate_output(state, "code_analysis", analysis)

    def vulnerability_detection_node(state: AgentState) -> AgentState:
        """MLXVulnerabilityDetectionAgent: identify vulnerabilities and risky changes,
        using the code-analysis output as primary evidence."""
        from langgraph_orchestration.prompts.reverse_engineering import build_vulnerability_detection_prompt
        agent = _get_re_agent("vulnerability_detection")
        analysis = state.intermediate_outputs.get("code_analysis", "")
        prompt = build_vulnerability_detection_prompt(state.user_input, analysis_output=analysis)
        vulns = _sanitize_model_output(agent.invoke(user_input=prompt, context=state.re_context or None))
        return StateManager.add_intermediate_output(state, "vulnerability_detection", vulns)

    def firmware_analysis_node(state: AgentState) -> AgentState:
        stage_keys = [
            "firmware_locator",
            "firmware_downloader",
            "ipsw_extractor",
            "firmware_diff_report",
            "feature_analysis_reports",
        ]
        sections: list[str] = []
        for key in stage_keys:
            text = (state.intermediate_outputs.get(key) or "").strip()
            if text:
                sections.append(f"## {key}\n{text}")
        if state.tool_results:
            sections.append(StateManager.format_tool_activity(state))
        output = "\n\n".join(sections) if sections else "No IPSW execution output captured."
        return StateManager.add_intermediate_output(state, "firmware_analysis", output)

    def synthesize_output(state: AgentState) -> AgentState:
        is_generic_re = bool(state.re_task_plan) and any(
            t in state.re_task_plan for t in ("planning", "code_analysis", "vulnerability_detection")
        )
        if is_generic_re:
            sections: list[str] = []
            plan = (state.intermediate_outputs.get("re_plan") or "").strip()
            ca = (state.intermediate_outputs.get("code_analysis") or "").strip()
            vd = (state.intermediate_outputs.get("vulnerability_detection") or "").strip()
            if plan:
                sections.append(f"## Analysis Plan\n\n{plan}")
            if ca:
                sections.append(f"## Code Analysis\n\n{ca}")
            if vd:
                sections.append(f"## Vulnerability Assessment\n\n{vd}")
            final = "\n\n".join(sections) if sections else "Reverse engineering analysis produced no output."
            state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(final)
            state.agent_chain.append("reverse_engineering_synthesize")
            return state

        final = state.intermediate_outputs.get("firmware_analysis", "")
        if final:
            state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(final)
            state.agent_chain.append("reverse_engineering_synthesize")
            return state

        report = state.intermediate_outputs.get("firmware_diff_report", "")
        if report:
            state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(report)
            state.agent_chain.append("reverse_engineering_synthesize")
            return state

        final = "IPSW execution pipeline completed without synthesized content."

        state.branch_outputs["reverse_engineering"] = StateManager.sanitize_output(final)
        state.agent_chain.append("reverse_engineering_synthesize")
        return state

    def route_after_extractor(state: AgentState) -> str:
        if _is_download_extract_only_request(state.user_input):
            return "firmware_analysis"
        return "firmware_diff_service"

    def route_after_context(state: AgentState) -> str:
        if (
            state.intermediate_outputs.get("firmware_diff_report_path")
            and state.intermediate_outputs.get("firmware_diff_report")
        ):
            return "feature_analysis_select"
        if state.re_task_plan and any(
            t in state.re_task_plan for t in ("planning", "code_analysis", "vulnerability_detection")
        ):
            return "re_planning"
        return "firmware_locator"

    graph.add_node("retrieve_re_context", retrieve_re_context_node)
    graph.add_node("firmware_locator", firmware_locator_node)
    graph.add_node("firmware_downloader", firmware_downloader_node)
    graph.add_node("ipsw_extractor", ipsw_extractor_node)
    graph.add_node("firmware_diff_service", firmware_diff_service_node)
    graph.add_node("feature_analysis_select", feature_analysis_select_node)
    graph.add_node("prepare_decompiler", prepare_decompiler_node)
    graph.add_node("unified_feature_analysis", unified_feature_analysis_node)
    graph.add_node("feature_analysis_tool_executor", tool_executor_node)
    graph.add_node("cleanup_decompiler", cleanup_decompiler_node)
    graph.add_node("feature_analysis_compile", feature_analysis_compile_node)
    graph.add_node("firmware_analysis", firmware_analysis_node)
    graph.add_node("synthesize", synthesize_output)
    graph.add_node("re_planning", re_planning_node)
    graph.add_node("code_analysis", code_analysis_node)
    graph.add_node("vulnerability_detection", vulnerability_detection_node)

    graph.add_conditional_edges(
        "retrieve_re_context",
        route_after_context,
        {
            "feature_analysis_select": "feature_analysis_select",
            "firmware_locator": "firmware_locator",
            "re_planning": "re_planning",
        },
    )
    graph.add_edge("firmware_locator", "firmware_downloader")
    graph.add_edge("firmware_downloader", "ipsw_extractor")
    graph.add_conditional_edges(
        "ipsw_extractor",
        route_after_extractor,
        {
            "firmware_analysis": "firmware_analysis",
            "firmware_diff_service": "firmware_diff_service",
        },
    )
    graph.add_edge("firmware_diff_service", "feature_analysis_select")
    graph.add_conditional_edges(
        "feature_analysis_select",
        route_after_feature_select,
        {
            "prepare_decompiler": "prepare_decompiler",
            "done": "firmware_analysis",
        },
    )

    graph.add_edge("prepare_decompiler", "unified_feature_analysis")
    graph.add_conditional_edges(
        "unified_feature_analysis",
        route_after_unified_analysis,
        {
            "execute_tools": "feature_analysis_tool_executor",
            "cleanup_decompiler": "cleanup_decompiler",
        }
    )
    graph.add_edge("feature_analysis_tool_executor", "unified_feature_analysis")
    graph.add_edge("cleanup_decompiler", "feature_analysis_compile")
    graph.add_edge("feature_analysis_compile", "feature_analysis_select")
    graph.add_edge("firmware_analysis", "synthesize")
    graph.add_edge("re_planning", "code_analysis")
    graph.add_edge("code_analysis", "vulnerability_detection")
    graph.add_edge("vulnerability_detection", "synthesize")
    graph.add_edge("synthesize", END)

    graph.set_entry_point("retrieve_re_context")

    compiled = graph.compile()
    compiled.name = "Reverse Engineering IPSW Pipeline"
    compiled.description = "Deterministic IPSW execution pipeline for firmware reverse engineering"
    return compiled
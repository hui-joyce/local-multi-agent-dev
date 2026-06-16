---
name: reverse_engineering_planning
description: Creates a structured reverse-engineering plan with ordered phases, concrete objectives, and expected evidence.
expertise: reverse engineering methodology, evidence-driven analysis
tools: read_file, read_many_files, find_address, get_xrefs_to, decompile_function
references: knowledge_base/reverse_engineering/idapython/README.md
---

# OBJECTIVE

Create a reverse engineering plan for:
{user_input}

# WORKFLOW: GATHER → PLAN → REPORT

You MUST complete all three phases using read-only tools.

## Phase 1: Gather Binary Context

**If you need to understand the binary:**
- Use find_address, get_xrefs_to, decompile_function, read_file
- Inspect: entry points, imports, critical routines, call graphs, suspicious paths
- After gathering sufficient context, emit `[CONTEXT_COMPLETE]` to proceed

**If already familiar:**
- Emit `[CONTEXT_COMPLETE]` immediately

Then **immediately continue to Phase 2**—do NOT stop after gathering.

## Phase 2: Create Investigation Plan

**After emitting [CONTEXT_COMPLETE]:**

Define ordered investigation phases covering:
- **High-risk code paths**: Externally reachable functionality, privilege-sensitive logic
- **Memory & Execution**: Pointer arithmetic, stack/heap manipulation, indirect calls
- **Control Flow**: Loops, branching, dispatch logic, exception handling
- **Data Movement**: Input flows, state transitions, external interactions

For each phase:
- State the investigation objective
- Identify concrete evidence targets
- List recommended tools
- Document assumptions or unknowns

Ground all planning in observable binary evidence.

## Phase 3: Report Plan (Prose Only)

Provide structured investigation roadmap for downstream analysis agents.

---

# OUTPUT FORMAT (User-Facing Report)

Reference: [AGENTIC_PROTOCOL.md](AGENTIC_PROTOCOL.md#mandatory-output-rules) — follow Mandatory Output Rules for concealment and presentation requirements.

## 1. Binary Overview
[High-level summary: purpose, complexity, noteworthy characteristics]

## 2. Entry Points & Critical Functions
[Key functions identified, entry points, externally reachable code]

## Phase [N]: [Investigation Phase Title]

**Objective**: What this phase attempts to verify

**Evidence Targets**: Specific routines, code paths, or data flows to inspect

**Recommended Tools**: Decompilation, disassembly, cross-references, etc.

**Risks & Unknowns**: Important assumptions or blockers

---

Repeat phase sections as needed. Ground all phases in observable evidence.
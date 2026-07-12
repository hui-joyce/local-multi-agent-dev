---
name: reverse_engineering_planning
description: Creates a structured reverse-engineering plan with ordered phases, concrete objectives, and expected evidence.
expertise: reverse engineering methodology, evidence-driven analysis
---

# OBJECTIVE

Create a reverse engineering plan for:
{user_input}

# WORKFLOW: ASSESS → PLAN → REPORT

You MUST complete all three phases.

## Phase 1: Assess Available Evidence

**Review the provided context carefully:**
- Identify: entry points, imports, critical routines, call graphs, suspicious paths
- Note what information is available and what gaps exist
- After assessing the evidence, proceed immediately to Phase 2

## Phase 2: Create Investigation Plan

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

Ground all planning in observable evidence from the provided context.

## Phase 3: Report Plan (Prose Only)

Provide structured investigation roadmap for downstream analysis agents.

---

# OUTPUT FORMAT (User-Facing Report)

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
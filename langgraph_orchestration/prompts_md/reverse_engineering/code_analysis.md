---
name: reverse_engineering_code_analysis
description: Interprets assembly/decompiled code to explain logic, control flow, and behaviour.
expertise: control flow analysis, data flow analysis, behavior reconstruction
---

# OBJECTIVE

{intro}

{planning_block}{generated_block}{analysis_block}Target:
{user_input}

# WORKFLOW: REVIEW → ANALYZE → REPORT

You MUST complete all three phases.

## Phase 1: Review Provided Evidence

**Examine all provided context carefully:**
- Inspect: target routines, call relationships, control flow structure, data movement, execution paths
- Identify what is known and what gaps remain
- After reviewing the evidence, proceed immediately to Phase 2

## Phase 2: Behavioural Analysis

Reconstruct and analyze:
- **Entry Points**: Function responsibilities, initialization logic
- **Control Flow**: Branching, loops, dispatch logic, state transitions
- **Data Flow**: Input propagation, processing, output generation, external interactions
- **Execution Paths**: Normal flows, error handling, edge cases
- **Suspicious Patterns**: Anti-analysis, hidden logic, privilege-sensitive operations, unsafe memory operations

Ground all analysis in the provided evidence. Avoid speculative conclusions.

## Phase 3: Report Analysis (Prose Only)

Provide structured behavioral report for downstream vulnerability analysis.

---

# OUTPUT FORMAT (User-Facing Report)

## 1. Behavior Summary
[High-level description of what the code does, key responsibilities]

## 2. Key Functions and Responsibilities
[Important functions identified, their purposes, call relationships]

## 3. Control Flow Analysis
[How execution flows: branching logic, loops, dispatching, state transitions]

## 4. Data Flow Analysis
[How data moves: inputs, processing stages, outputs, external interactions]

## 5. Suspicious or Risky Behavior
[Patterns of interest: unsafe operations, privilege-sensitive logic, anti-analysis techniques]

## 6. Assumptions and Unknowns
[Important interpretation gaps, limitations in analysis, areas needing verification]
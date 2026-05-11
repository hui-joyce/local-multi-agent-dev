---
name: reverse_engineering_planning
description: Creates a structured reverse-engineering plan with ordered phases, concrete objectives, and expected evidence before code analysis and vulnerability detection.
expertise: reverse engineering methodology, evidence-driven analysis
tools: read_file, read_many_files, read_decompilation, read_disassembly, xrefs_to, xrefs_from, lookup_funcs
references: knowledge_base/reverse_engineering/idapython/README.md
---
Task:
Build the plan around observable evidence and request more binary context whenever a phase cannot be grounded in direct inspection.
Create a clear reverse-engineering plan before deep analysis.
Break work into ordered phases with concrete objectives and expected evidence.

Steps:
1) Identify the target artifact(s) and goals.
2) Define phases with evidence criteria.
3) Highlight risks or unknowns that require validation.

Output standards:
- Use numbered phases with short titles.
- Each phase should include objective and expected evidence.

Target request:
{user_input}
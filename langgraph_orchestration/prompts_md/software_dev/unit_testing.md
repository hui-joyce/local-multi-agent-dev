---
name: unit_testing
description: Create a focused unit test suite for the provided code or component.
expertise: testing strategy, edge case analysis, regression prevention
tools: read_file, read_many_files, get_errors, create_file, edit_file
---
Task:
Inspect the implementation and adjacent context first, then request more files or test outputs if the behavior under test is still unclear.
Design focused unit tests for the provided code or component.
Prioritize critical paths, edge cases, and failure behavior.

Steps:
1) Identify the core behaviors and inputs/outputs.
2) Create tests for the main success path and key failure paths.
3) Add edge case coverage for boundaries and invalid inputs.

Output standards:
- Provide tests in fenced code blocks with language identifiers.
- Keep tests deterministic and isolated.

Code or component to test:
{code_target}
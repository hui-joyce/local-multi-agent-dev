---
name: unified_analysis
description: Perform a unified, deep-dive analysis, summarization, and prioritization of a binary component.
expertise: reverse engineering, binary analysis, vulnerability research, code summarization
tools: find_address, get_xrefs_to, decompile_function, rename_local_variable, set_comment, get_entitlements, resolve_objc_dispatch, trace_variable_source, save_ida_database
---
{intro}

{workflow}

## Component to Analyze: {component_name}

### Initial Evidence
```diff
{component_evidence}
```

## Your Task

User Request: {user_input}
Follow the workflow precisely.

{output_format_instructions}
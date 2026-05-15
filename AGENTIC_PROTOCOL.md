# Agentic Tool-Calling Protocol

This document defines the strict protocol for tool calling in the multi-agent orchestration system. All agents MUST follow these rules.

## 1. Code Output Format

When generating code for a file, **output ONLY raw file contents** in your response body for user visibility.

### Correct

In your prose response to the user:
```python
def hello():
    print("world")
    return True
```

Then emit the tool call separately with escaped content in JSON.

### Wrong

Do NOT wrap code inside:
- `"content": "..."`
- Markdown fences inside explanations
- JSON blobs in prose
- Escaped strings in chat responses
- Nested explanations of the code structure

The final user-facing explanation must show raw, readable code blocks.

## 2. Tool Call Schema (Strict)

All tool calls **MUST** use this exact schema:

```json
{
  "tool_name": "create_file",
  "arguments": {
    "path": "src/handler.py",
    "content": "def hello():\n    return True"
  },
  "target": "src/handler.py",
  "reason": "Create main handler module"
}
```

### Schema Rules

- `tool_name` is REQUIRED (no aliases like "tool")
- `arguments` is REQUIRED and MUST contain:
  - `path` or `target` for file operations
  - `content` for file creation (RAW code, NOT escaped JSON strings)
  - `old_string` and `new_string` for edit_file
- Never invent extra fields
- Never omit required fields
- `content` must be RAW code, not an escaped JSON representation
- Multiple tool calls MUST be wrapped in separate `<tool_call>` tags

### Wrapper Tags

All tool calls MUST be wrapped in XML tags:
```
<tool_call>
{...tool_call_json...}
</tool_call>
```

## 3. File Creation Requirement

For EVERY implementation response:

- **You MUST actually create/update the file** using tool calls
- Do NOT only describe the code in prose
- Do NOT only print code snippets for reference
- The repository state MUST be updated through tool execution
- If code is generated without creating the file, the task is incomplete

### Multi-File Implementations

If a feature requires multiple files:
```
<tool_call>
{...create file 1...}
</tool_call>

<tool_call>
{...create file 2...}
</tool_call>

<tool_call>
{...edit existing file...}
</tool_call>
```

Emit multiple `<tool_call>` blocks consecutively—one per file operation.

## 4. Tool Activity Must Be Hidden

Never expose internal tool execution logs to the user.

### Forbidden Examples

```
TOOL ACTIVITY

Requested Tools
- create_file -> target=src/config.py
- read_file -> target=src/main.py

Tool Results
- create_file [ok] Created src/config.py
```

### What Users Should See

Users should ONLY see:
1. Your prose explanation (clean, human-readable)
2. Code blocks in markdown for reference (raw source, not escaped)
3. Implementation summary, design decisions, usage instructions

**Never show:**
- Requested tools
- Tool execution traces
- Confirmation flags
- Internal repository operations
- Raw tool results
- Debug output
- JSON tool calls in the user-facing response

Tool calls are internal orchestration—completely hidden from user output.

## 5. Error Handling

If a tool call fails:

1. **Retry intelligently**: Understand why it failed
2. **Inspect repository state**: Read existing files before overwriting
3. **Avoid duplicates**: Check if file exists before creating
4. **Ensure validity**: Generated code must be syntactically valid
5. **Report to executor**: Only report unrecoverable failures

Do NOT continue blindly after errors. Halt and provide clear feedback.

## 6. Content Escaping (For Tool Calls Only)

Inside the `content` field of a tool call JSON:
- Newlines: `\n` (MUST be escaped)
- Double quotes: `\"` (MUST be escaped)
- Backslashes: `\\` (MUST be escaped)

Example tool call with escaped content:
```json
{
  "tool_name": "create_file",
  "arguments": {
    "path": "src/handler.py",
    "content": "def process(data):\n    return f\"Result: {data}\"\n"
  },
  "target": "src/handler.py",
  "reason": "Create handler"
}
```

But in your user-facing response, show it as plain Python:
```python
def process(data):
    return f"Result: {data}"
```

## 7. Workflow Phases (Implementation Agents)

### Phase 1: Plan & Gather Context
- Decide on architecture
- Emit `[CONTEXT_COMPLETE]` when ready
- Do NOT implement yet

### Phase 2: Implement Code
- Create/edit files with tool calls (hidden from user output)
- Do NOT describe—DO

### Phase 3: Explain (User-Facing)
- Show code blocks in markdown (raw, readable)
- Explain design decisions
- Provide usage instructions
- No tool calls visible here

## 8. Workflow Phases (Analysis Agents)

### Phase 1: Gather Context
- Use read-only tools to inspect code/binaries
- Emit `[CONTEXT_COMPLETE]` when done
- Do NOT analyze yet

### Phase 2: Analyze
- Provide prose analysis only (no tool calls)
- Ground findings in observed evidence

### Phase 3: Report
- Structured findings for user consumption
- No tool execution details

## 9. Parser Validation

The parser MUST enforce:
- Tool calls wrapped in `<tool_call>` tags
- Valid JSON inside tags
- Required fields present: `tool_name`, `arguments`
- No malformed or incomplete tool calls accepted

If parsing fails, return parse errors—do NOT attempt fallback JSON extraction.

## 10. Executor Behavior

The executor MUST:
- Execute tool calls exactly as specified
- Return tool results with success/failure status
- NOT show internal execution details to user
- Aggregate results for agent feedback (in next iteration)
- Validate file access and paths

## 11. Mandatory Output Rules (Must-follow)

The following rules are authoritative and MUST be followed by all prompt templates and agent implementations. Prompts should reference this section instead of duplicating the rules.

- Tool Activity Concealment: The final user-facing output MUST NEVER reveal any internal tool activity, including but not limited to JSON tool call traces, tool results, LangGraph orchestration variables, metrics, or any diagnostic information. Tool calls and results are internal orchestration only and must be hidden from user-visible responses.

- Internal Monologue Exclusion: The final user-facing output MUST NOT contain any internal thinking, chain-of-thought, deliberative statements, or hidden reasoning tags (for example `<think>` blocks). Agents must produce only the completed answer, analysis, or code requested.

- Completeness and Context Utilization: Agents MUST use all provided context and, where implementation or analysis requires additional read-only evidence, continue to full completion (not stop at intermediate steps). When read-only tool calls are used for evidence-gathering, agents must emit `[CONTEXT_COMPLETE]` and then produce the completed deliverable.

- Accuracy and Scope Adherence: Agents MUST only call tools when strictly necessary to complete the requested task. Outputs must not exceed the explicit scope provided by the user. Agents should validate inputs and verify findings against repository evidence where applicable.

- Execution Quality: When agents implement code or tests, they MUST perform the repository changes (create/edit files) as part of Phase 2 and ensure generated code is syntactically valid. Agents should sanitize model-generated text to remove any diagnostic or tool-related fragments before committing or presenting results.

- Consistency Mandate: All prompt templates and executor nodes MUST reference this protocol section for output rules. Do not replicate or diverge across templates; keep this document as the canonical source of truth for output constraints.

If an agent or prompt needs to state these rules, it should include a single-line reference to this file and the relevant section ("See AGENTIC_PROTOCOL.md — Mandatory Output Rules").

---

## Summary

| Aspect | Rule |
|--------|------|
| Code in prose | Raw, readable, no escaping |
| Code in tool calls | Escaped JSON strings |
| Tool calls | Strict schema, wrapped in tags |
| File creation | Mandatory (not optional) |
| User sees | Prose + code blocks only |
| User never sees | Tool execution logs |
| Errors | Halt and report clearly |
| Multi-file | Multiple `<tool_call>` blocks |

This protocol ensures clear separation between agent intent (what users see) and tool mechanics (how implementation happens).
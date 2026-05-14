import re
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.tooling.tool import ToolRequest, ToolResult

class StateManager:
    @staticmethod
    def sanitize_output(text: str) -> str:
        if not text:
            return text
        
        # Unwrap internal reasoning (extract content, don't delete)
        text = re.sub(r'<think>(.*?)</think>', r'\1', text, flags=re.DOTALL)
        text = re.sub(r'<thinking>(.*?)</thinking>', r'\1', text, flags=re.DOTALL)
        
        # Remove tool call envelopes
        text = re.sub(r'<tool_call>.*?</tool_call>', '', text, flags=re.DOTALL)
        text = re.sub(r'\[CONTEXT_COMPLETE\]', '', text, flags=re.DOTALL)
        
        # Clean up excessive whitespace created by removal
        text = re.sub(r'\n\n\n+', '\n\n', text)
        
        return text.strip()
    
    @staticmethod
    def add_intermediate_output(
        state: AgentState,
        agent_name: str,
        output: str,
    ) -> AgentState:
        state.intermediate_outputs[agent_name] = output
        state.agent_chain.append(agent_name)
        return state
    
    @staticmethod
    def set_final_output(
        state: AgentState,
        output: str,
    ) -> AgentState:
        state.final_output = StateManager.sanitize_output(output)
        return state
    
    @staticmethod
    def add_retrieved_context(
        state: AgentState,
        context: list[str],
    ) -> AgentState:
        state.retrieved_context.extend(context)
        return state

    @staticmethod
    def add_tool_request(state: AgentState, request: ToolRequest) -> AgentState:
        state.register_tool_request(request)
        return state

    @staticmethod
    def add_tool_result(state: AgentState, result: ToolResult) -> AgentState:
        state.register_tool_result(result)
        return state

    @staticmethod
    def add_analysis_note(state: AgentState, note: str) -> AgentState:
        state.record_analysis_note(note)
        return state
    
    @staticmethod
    def format_agent_outputs(state: AgentState) -> str:
        from langgraph_orchestration.tooling.parser import parse_agent_output

        outputs = []
        for agent_name, raw_output in state.intermediate_outputs.items():
            parsed = parse_agent_output(raw_output)
            formatted_text = parsed.assistant_message.strip() if parsed.assistant_message else ""

            # format tool calls extracted by parser
            for tool_call in parsed.tool_calls:
                if tool_call.tool_name in ["create_file", "edit_file"]:
                    content = tool_call.arguments.get("content") or tool_call.arguments.get("file_text") or ""
                    path = tool_call.arguments.get("path") or tool_call.target or "Generated Code"
                    if content:
                        formatted_text += f"\n\n**File: `{path}`**\n```python\n{content}\n```\n"

            # fallback
            if parsed.parse_errors:
                formatted_text += "\n\n*(Parser encountered issues extracting tool calls. Please check your workspace for the files.)*"

            outputs.append(f"\n## {agent_name.upper()}\n{formatted_text.strip()}")

        if state.tool_results:
            outputs.append(StateManager.format_tool_activity(state))

        return "\n".join(outputs)
        
    @staticmethod
    def format_tool_activity(state: AgentState) -> str:
        if not state.tool_requests and not state.tool_results:
            return ""

        sections = ["\n## TOOL ACTIVITY"]

        if state.tool_requests:
            sections.append("\n### Requested Tools")
            for index, request in enumerate(state.tool_requests, start=1):
                sections.append(
                    f"{index}. {request.tool_name} -> target={request.target or 'n/a'} | confirmation={request.needs_confirmation}"
                )

        if state.tool_results:
            sections.append("\n### Tool Results")
            for index, result in enumerate(state.tool_results, start=1):
                status = "ok" if result.success else "error"
                sections.append(f"{index}. {result.tool_name} [{status}]\n{result.output}")

        return "\n".join(sections)
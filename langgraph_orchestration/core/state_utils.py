import re
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.tooling.tool import ToolRequest, ToolResult

class StateManager:
    @staticmethod
    def sanitize_output(text: str) -> str:
        """Remove internal reasoning blocks from user-facing output (e.g. <think>...</think>)"""
        if not text:
            return text
        
        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
        text = re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL)
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
        outputs = []
        for agent_name, output in state.intermediate_outputs.items():
            outputs.append(f"\n## {agent_name.upper()}\n{output}")
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
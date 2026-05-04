import re
from langgraph_orchestration.schemas.state import AgentState

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
    def format_agent_outputs(state: AgentState) -> str:
        outputs = []
        for agent_name, output in state.intermediate_outputs.items():
            outputs.append(f"\n## {agent_name.upper()}\n{output}")
        return "\n".join(outputs)
from langgraph_orchestration.schemas.state import AgentState

class StateManager:    
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
        state.final_output = output
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
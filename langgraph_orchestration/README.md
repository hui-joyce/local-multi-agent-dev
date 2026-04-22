## Architecture Overview

### High-Level Flow

### Key Components

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.graphs.orchestration import build_orchestration_graph

# Build the orchestration graph
graph = build_orchestration_graph()

# Create initial state
state = AgentState(user_input="Generate a Python function for fibonacci")

# Execute the graph
result = graph.invoke(state)

print(f"Domain: {result.selected_domain}")
print(f"Agents executed: {result.agent_chain}")
print(f"Output:\n{result.final_output}")
```

### Run Examples

```bash
python examples.py
```

This runs 4 different examples showcasing:
1. Software development code generation and testing
2. Reverse engineering vulnerability analysis
3. Code implementation with architecture review
4. Security threat detection

## Integration Points

### Adding a New Agent

1. Create agent class in `agents/` inheriting from `SyncBaseAgent`
2. Implement `invoke()` method
3. Add to domain subgraph in `graphs/`
4. Wire into appropriate node in graph builder

Example:
```python
class MyAgent(SyncBaseAgent):
    def __init__(self):
        super().__init__(
            name="my_agent",
            description="What this agent does"
        )
    
    def invoke(self, user_input: str, context=None) -> str:
        # Implementation
        return result
```

### Integrating Qdrant

```python
# In retrievers/qdrant_client.py
from qdrant_client import QdrantClient

class QdrantRetriever(BaseRetriever):
    def __init__(self, url: str = "http://localhost:6333"):
        self.client = QdrantClient(url=url)
        self.collection_name = "multi_agent_knowledge"
    
    def retrieve(self, query: str, top_k: int = 5, domain=None):
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=embed(query),
            limit=top_k,
        )
        return [hit.payload["text"] for hit in results]
```

### Connecting to LLM

```python
def invoke(self, user_input: str, context=None) -> str:
    # Call your local model
    response = model.generate(
        prompt=self._build_prompt(user_input, context),
        max_tokens=2048,
    )
    return response
```
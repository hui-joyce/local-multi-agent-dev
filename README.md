# Local Multi-Agent Development System

A production-ready **multi-agent AI orchestration system** featuring two specialized assistants: a **Software Development Assistant** and a **Reverse Engineering Assistant**. Built with LangGraph for intelligent agent coordination, Qdrant for RAG-enhanced context retrieval, and designed for local inference via MlX framework and Qwen 3.5 9B (4-bit quantized).

## System Overview

This system implements a **Supervisor-based multi-agent architecture** where:
- A central **Supervisor Agent** routes incoming requests to the appropriate domain
- Domain-specific **sub-agents** collaborate on specialized tasks
- **RAG (Retrieval-Augmented Generation)** enriches agent responses with domain knowledge
- All components are optimized for **local inference** 

### Two Specialized Domains

**Software Development Assistant**
- Code generation and implementation
- Automated unit test creation
- Architectural design review and best practices

**Reverse Engineering Assistant**
- Binary and assembly code analysis
- Vulnerability detection and security assessment
- Structured analysis planning for complex reverse engineering tasks

## System Architecture
<img width="800" alt="Query" src="https://github.com/user-attachments/assets/5206b3ca-e97b-4b3e-aa65-5c9d80d09c08" />

---

## Tech Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Orchestration** | LangGraph | ≥0.0.1 |
| **LLM Framework** | MLX-LM | 0.31.2|
| **State Management** | Pydantic | ≥1.7 |
| **Vector Database** | Qdrant | ≥1.0.0 |
| **Local Model** | Qwen 3.5 9B (4-bit) | - |
| **Language** | Python | 3.9+ |

---

## Quick Start

### Prerequisites
- Python 3.9 or higher
- ~8GB RAM (for Qwen 3.5 9B 4-bit)
- ~30GB disk space (model + vector database)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/local-multi-agent-dev.git
   cd local-multi-agent-dev
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**
   ```bash
   python3 examples.py
   ```
---

## How to Use the System

### Basic Usage

```python
from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.graphs.orchestration import build_orchestration_graph

# Build the orchestration graph
graph = build_orchestration_graph()

# Create a request
state = AgentState(user_input="Generate a Python sorting function")

# Execute the graph
result = graph.invoke(state.model_dump())

# Access results
print(f"Domain: {result['selected_domain']}")
print(f"Agents executed: {result['agent_chain']}")
print(f"Response:\n{result['final_output']}")
```
## Documentation

---

## Key Resources

- **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
- **Pydantic Docs**: https://docs.pydantic.dev/
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **Qwen Model**: https://github.com/QwenLM/Qwen

**Last Updated**: April 2026

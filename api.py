import os
import ipaddress
from typing import Optional
from functools import lru_cache
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from contextlib import asynccontextmanager

from langgraph_orchestration.schemas.state import AgentState
from langgraph_orchestration.graphs.orchestration import build_orchestration_graph
from langgraph_orchestration.retrievers.config import RAGConfigManager
from langgraph_orchestration.tooling.tool import ToolRequest, ToolResult

load_dotenv()
@lru_cache(maxsize=1)
def get_cached_graph():
    graph = build_orchestration_graph()
    graph.name = "Multi-Agent Orchestration"
    graph.description = "Supervisor-based multi-agent system routing to software development or reverse engineering domains"
    return graph

@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("LANGSMITH_TRACING", "false").lower() == "true":
        try:
            from langsmith import Client
            client = Client()
            print(f"✓ LangSmith connected to project: {os.getenv('LANGSMITH_PROJECT', 'default')}")
        except Exception as e:
            print(f"⚠ LangSmith warning: {e}")
    
    get_cached_graph()
    print("✓ Graph loaded and cached for LangSmith discovery")
    
    yield

app = FastAPI(
    title="Multi-Agent Orchestration API",
    description="Local inference with MLX-powered agents",
    version="1.0.0",
    lifespan=lifespan,
)


def _is_loopback_host(host: str) -> bool:
    if host in {"localhost", "127.0.0.1", "::1"}:
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://127.0.0.1",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:7860",
        "http://127.0.0.1:7860",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

class AgentRequest(BaseModel):
    user_input: str
    domain: Optional[str] = None


class AgentResponse(BaseModel):
    selected_domain: str
    agent_chain: list[str]
    final_output: str
    intermediate_outputs: dict[str, str]
    tool_requests: list[ToolRequest] = Field(default_factory=list)
    tool_results: list[ToolResult] = Field(default_factory=list)
    analysis_notes: list[str] = Field(default_factory=list)

class AddDocumentRequest(BaseModel):
    text: str
    domain: str
    metadata: Optional[dict] = None


class SearchRequest(BaseModel):
    query: str
    domain: Optional[str] = None
    top_k: Optional[int] = 5

# /root, /info, /invoke, /domains, /assistants, /assistants/search, /graph, /assistants/{assistant_id}/schemas, /threads, /threads/{thread_id}/messages endpoints
@app.get("/")
async def root():
    return {
        "status": "healthy",
        "service": "Multi-Agent Orchestration",
        "inference_backend": "MLX",
    }

@app.get("/info")
async def get_info():
    return {
        "name": "Multi-Agent Orchestration System",
        "version": "1.0.0",
        "inference_backend": "MLX (Apple Silicon)",
        "agents": {
            "software_dev": [
                "Code Generation",
                "Unit Testing",
                "Architectural Review",
            ],
            "reverse_engineering": [
                "Planning",
                "Code Analysis",
                "Vulnerability Detection",
            ],
        },
        "langsmith_enabled": os.getenv("LANGSMITH_TRACING", "false").lower() == "true",
    }


@app.post("/invoke", response_model=AgentResponse)
async def invoke_orchestration(request: AgentRequest):
    try:
        graph = get_cached_graph()
        initial_state = AgentState(user_input=request.user_input)
        result = graph.invoke(initial_state.model_dump())
        final_state = AgentState(**result)
        
        return AgentResponse(
            selected_domain=final_state.selected_domain,
            agent_chain=final_state.agent_chain,
            final_output=final_state.final_output,
            intermediate_outputs=final_state.intermediate_outputs,
            tool_requests=final_state.tool_requests,
            tool_results=final_state.tool_results,
            analysis_notes=final_state.analysis_notes,
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Orchestration failed: {str(e)}"
        )

@app.get("/domains")
async def list_domains():
    return {
        "domains": {
            "software_dev": {
                "name": "Software Development Assistant",
                "agents": [
                    "Code Generation",
                    "Unit Testing",
                    "Architectural Review",
                ],
                "description": "For code generation, testing, and architectural design",
            },
            "reverse_engineering": {
                "name": "Reverse Engineering Assistant",
                "agents": [
                    "Planning",
                    "Code Analysis",
                    "Vulnerability Detection",
                ],
                "description": "For binary analysis, vulnerability detection, and security assessment",
            },
        }
    }

@app.get("/assistants")
async def list_assistants():
    return {
        "assistants": [
            {
                "id": "multi-agent-orchestration",
                "name": "Multi-Agent Orchestration",
                "description": "Supervisor-based multi-agent system with domain routing",
                "config": {
                    "domains": ["software_dev", "reverse_engineering"],
                    "inference_backend": "MLX (Apple Silicon)",
                },
                "graph_url": "/graph"
            }
        ]
    }

@app.post("/assistants/search")
async def search_assistants(query: Optional[str] = None):
    return {
        "assistants": [
            {
                "id": "multi-agent-orchestration",
                "name": "Multi-Agent Orchestration",
                "description": "Supervisor-based multi-agent system with domain routing",
                "config": {
                    "domains": ["software_dev", "reverse_engineering"],
                    "inference_backend": "MLX (Apple Silicon)",
                },
                "graph_url": "/graph"
            }
        ]
    }

@app.get("/graph")
async def get_graph_structure():
    try:
        graph = get_cached_graph()
        graph_obj = graph.get_graph()
        return {
            "name": graph.name or "Multi-Agent Orchestration",
            "description": graph.description or "Supervisor-based multi-agent system",
            "nodes": [
                {"id": node[0], "name": node[0]}
                for node in graph_obj.nodes.items()
            ] if hasattr(graph_obj, 'nodes') else [],
            "edges": [
                {"source": edge[0], "target": edge[1]}
                for edge in graph_obj.edges
            ] if hasattr(graph_obj, 'edges') else [],
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get graph structure: {str(e)}"
        )

@app.get("/graph/schema")
async def get_graph_schema():
    """Returns OpenAI-compatible runnable schema for LangSmith discovery"""
    try:
        graph = get_cached_graph()
        return {
            "title": graph.name or "Multi-Agent Orchestration",
            "description": graph.description or "Supervisor-based multi-agent system",
            "type": "object",
            "properties": {
                "user_input": {
                    "type": "string",
                    "description": "User query or request"
                },
                "domain": {
                    "type": "string",
                    "enum": ["software_dev", "reverse_engineering"],
                    "description": "Optional domain specification"
                }
            },
            "required": ["user_input"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get graph schema: {str(e)}"
        )

@app.post("/langgraph")
async def invoke_langgraph(request: AgentRequest):
    """for LangSmith Studio integration"""
    try:
        graph = get_cached_graph()
        initial_state = AgentState(user_input=request.user_input)
        
        # Invoke with explicit tracing tags for LangSmith
        result = graph.invoke(
            initial_state.model_dump(),
            config={
                "run_name": "multi-agent-orchestration",
                "tags": ["orchestration", "multi-agent"]
            }
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Graph invocation failed: {str(e)}"
        )

@app.get("/test-graph")
async def test_graph():
    """Test endpoint to verify graph is properly registered with LangSmith"""
    try:
        graph = get_cached_graph()
        return {
            "status": "success",
            "graph_name": graph.name,
            "graph_description": graph.description,
            "graph_type": str(type(graph).__name__),
            "has_get_graph": hasattr(graph, 'get_graph'),
            "message": "Graph is properly registered and ready for LangSmith Studio"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Graph verification failed: {str(e)}"
        )

@app.get("/assistants/{assistant_id}")
async def get_assistant(assistant_id: str):
    if assistant_id == "multi-agent-orchestration" or assistant_id == "9ea4dd10-bca1-56b2-ba14-981def047f8b":
        return {
            "id": "multi-agent-orchestration",
            "name": "Multi-Agent Orchestration",
            "description": "Supervisor-based multi-agent system with domain routing",
            "config": {
                "domains": ["software_dev", "reverse_engineering"],
                "inference_backend": "MLX (Apple Silicon)",
            }
        }
    return {
        "error": "Assistant not found"
    }

@app.get("/assistants/{assistant_id}/schemas")
async def get_assistant_schemas(assistant_id: str):
    return {
        "input_schema": {
            "type": "object",
            "properties": {
                "user_input": {
                    "type": "string",
                    "description": "User query or request"
                }
            },
            "required": ["user_input"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "selected_domain": {
                    "type": "string",
                    "description": "Routing domain"
                },
                "agent_chain": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "final_output": {
                    "type": "string"
                },
                "intermediate_outputs": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            }
        }
    }

@app.get("/threads")
async def list_threads():
    return {"threads": []}


@app.post("/rag/add")
async def rag_add(doc: AddDocumentRequest):
    try:
        RAGConfigManager.initialize()
        admin = RAGConfigManager.get_admin_service()
        result = admin.add_document(doc.text, doc.domain, metadata=doc.metadata)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rag/search")
async def rag_search(req: SearchRequest):
    try:
        RAGConfigManager.initialize()
        rag = RAGConfigManager.get_rag_manager()
        results = rag.retrieve_for_agent(req.query, domain=req.domain, top_k=req.top_k)
        return {"results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/rag/stats")
async def rag_stats():
    try:
        RAGConfigManager.initialize()
        admin = RAGConfigManager.get_admin_service()
        return admin.get_statistics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/threads/{thread_id}/messages")
async def send_message(thread_id: str, request: AgentRequest):
    try:
        graph = get_cached_graph()
        initial_state = AgentState(user_input=request.user_input)
        result = graph.invoke(initial_state.model_dump())
        final_state = AgentState(**result)
        
        return {
            "thread_id": thread_id,
            "message": AgentResponse(
                selected_domain=final_state.selected_domain,
                agent_chain=final_state.agent_chain,
                final_output=final_state.final_output,
                intermediate_outputs=final_state.intermediate_outputs,
                tool_requests=final_state.tool_requests,
                tool_results=final_state.tool_results,
                analysis_notes=final_state.analysis_notes,
            )
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Message failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("API_PORT", "8000"))
    host = os.getenv("API_HOST", "127.0.0.1")
    
    print(f"\n{'='*60}")
    print(f"  Server: http://{host}:{port}")
    print(f"{'='*60}\n")
    
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
    )
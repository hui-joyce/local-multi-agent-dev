"""Local HTTP interface to the orchestration graph"""

from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.middleware.cors import CORSMiddleware  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from langgraph_orchestration.retrievers import (  # noqa: E402
    add_document,
    get_statistics,
    retrieve_context,
)
from langgraph_orchestration.runtime import get_runtime  # noqa: E402
from langgraph_orchestration.tooling.tool import ToolRequest, ToolResult  # noqa: E402

logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("mad.api")

AGENTS_BY_DOMAIN = {
    "software_dev": {
        "name": "Software Development Assistant",
        "description": "Code generation, testing, and architectural review",
        "agents": ["code_generation", "unit_testing", "architectural_review"],
    },
    "reverse_engineering": {
        "name": "Reverse Engineering Assistant",
        "description": "Firmware diffing, binary analysis, and vulnerability assessment",
        "agents": ["planning", "code_analysis", "vulnerability_detection"],
    },
}


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Loading model and building graph...")
    get_runtime().ensure_ready()
    logger.info("Ready")
    yield


app = FastAPI(
    title="Multi-Agent Orchestration API",
    description="Local inference with MLX-powered agents",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:7860",
        "http://127.0.0.1:7860",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class AgentRequest(BaseModel):
    user_input: str


class AgentResponse(BaseModel):
    selected_domain: str | None = None
    execution_domains: list[str] = Field(default_factory=list)
    agent_chain: list[str] = Field(default_factory=list)
    final_output: str = ""
    intermediate_outputs: dict[str, str] = Field(default_factory=dict)
    tool_requests: list[ToolRequest] = Field(default_factory=list)
    tool_results: list[ToolResult] = Field(default_factory=list)
    analysis_notes: list[str] = Field(default_factory=list)


class AddDocumentRequest(BaseModel):
    text: str
    domain: str
    metadata: dict | None = None


class SearchRequest(BaseModel):
    query: str
    domain: str | None = None
    top_k: int = 5


@app.get("/")
async def health():
    return {"status": "healthy", "service": "Multi-Agent Orchestration"}


@app.get("/info")
async def info():
    return {
        "name": "Multi-Agent Orchestration System",
        "version": "1.0.0",
        "inference_backend": "MLX (Apple Silicon)",
        "domains": AGENTS_BY_DOMAIN,
    }


@app.post("/invoke", response_model=AgentResponse)
async def invoke(request: AgentRequest):
    """Run the orchestration graph. Executes tools and writes to disk"""
    try:
        state = get_runtime().run(request.user_input)
    except Exception:
        logger.exception("Orchestration failed")
        raise HTTPException(status_code=500, detail="Orchestration failed") from None

    return AgentResponse(
        selected_domain=state.selected_domain,
        execution_domains=list(state.execution_domains),
        agent_chain=state.agent_chain,
        final_output=state.final_output or "",
        intermediate_outputs=state.intermediate_outputs,
        tool_requests=state.tool_requests,
        tool_results=state.tool_results,
        analysis_notes=state.analysis_notes,
    )


@app.post("/rag/add")
async def rag_add(request: AddDocumentRequest):
    result = add_document(request.text, request.domain, metadata=request.metadata)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message", "Request failed"))
    return result


@app.post("/rag/search")
async def rag_search(request: SearchRequest):
    results = retrieve_context(request.query, domain=request.domain, top_k=request.top_k)
    return {"results": results, "count": len(results)}


@app.get("/rag/stats")
async def rag_stats():
    return get_statistics()


def main() -> None:
    import uvicorn

    from langgraph_orchestration.core import enforce_bind_policy

    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", "8000"))
    enforce_bind_policy(host, surface="FastAPI service")

    print(f"\n{'=' * 60}")
    print(f"  Server: http://{host}:{port}")
    print("  Bind:   loopback-only, no request auth (local tool)")
    print(f"{'=' * 60}\n")

    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=os.getenv("API_RELOAD", "false").lower() == "true",
        log_level="info",
    )


if __name__ == "__main__":
    main()

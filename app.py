import gradio as gr
import sys
import threading
import queue
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from langgraph_orchestration.retrievers.config import RAGConfigManager
from langgraph_orchestration.agents.mlx_factory import MLXAgentFactory
from langgraph_orchestration.agents.mlx_agents import (
    MLXCodeGenerationAgent,
    MLXCodeAnalysisAgent,
    MLXArchitecturalReviewAgent,
    MLXVulnerabilityDetectionAgent,
)
RAGConfigManager.initialize()

# Global states
rag_enabled = False
current_agent_type = "Software Dev"
_agents_cache = {}
_request_queue = queue.Queue()
_response_queue = queue.Queue()

def _worker_thread():
    try:
        factory = MLXAgentFactory()
        inference_engine = factory.ensure_loaded()
        
        _agents_cache['code_gen'] = MLXCodeGenerationAgent(inference_engine)
        _agents_cache['code_analysis'] = MLXCodeAnalysisAgent(inference_engine)
        _agents_cache['arch_review'] = MLXArchitecturalReviewAgent(inference_engine)
        _agents_cache['vuln_detection'] = MLXVulnerabilityDetectionAgent(inference_engine)
        _agents_cache['ready'] = True
    except Exception as e:
        _response_queue.put(f"Init error: {e}")
        return
    
    # Process requests sequentially
    while True:
        try:
            request = _request_queue.get()
            if request is None:  
                break
            
            agent, message, context_text = request
            response = agent.invoke(message, context=context_text)
            _response_queue.put(response)
        except Exception as e:
            _response_queue.put(f"Error: {e}")

# Start worker thread
_worker = threading.Thread(target=_worker_thread, daemon=True)
_worker.start()

import time
for _ in range(30):
    if _agents_cache.get('ready'):
        break
    time.sleep(0.1)

def respond(message, history):
    try:
        domain = "software_dev" if current_agent_type == "Software Dev" else "reverse_engineering"
        
        # Get RAG context
        context_str = ""
        context_text = None
        if rag_enabled:
            try:
                retriever = RAGConfigManager.get_retriever()
                rag_context = retriever.retrieve_context(message, domain=domain, top_k=3)
                if rag_context:
                    context_text = [r.get('content', '') for r in rag_context]
                    context_str = "\n\n**Context:**\n" + "\n".join([r.get('content', '')[:100] for r in rag_context])
            except Exception as e:
                print(f"RAG error: {e}")
        
        # Select agent
        if current_agent_type == "Software Dev":
            if any(w in message.lower() for w in ['generate', 'write', 'create', 'code']):
                agent = _agents_cache['code_gen']
                agent_name = "CodeGen"
            elif any(w in message.lower() for w in ['review', 'architecture', 'design']):
                agent = _agents_cache['arch_review']
                agent_name = "ArchReview"
            else:
                agent = _agents_cache['code_analysis']
                agent_name = "Analysis"
        else:
            if any(w in message.lower() for w in ['vulnerability', 'security', 'exploit']):
                agent = _agents_cache['vuln_detection']
                agent_name = "VulnDetect"
            else:
                agent = _agents_cache['code_analysis']
                agent_name = "Analysis"
        
        # Queue request to worker thread
        _request_queue.put((agent, message, context_text))
        response = _response_queue.get(timeout=60)
        
        return f"[{agent_name}] {response}{context_str}"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio interface
with gr.Blocks(title="RAG Agent Chat - Testing") as demo:
    gr.Markdown("RAG Agent Chat Interface (Testing)")    
    with gr.Row():
        agent_type = gr.Radio(
            choices=["Software Dev", "Reverse Engineering"],
            value="Software Dev",
            label="Domain/Agent Type",
            interactive=True,
            info="Selects which specialized agents to use"
        )
        use_rag = gr.Checkbox(
            value=False,
            label="Enable RAG Context",
            interactive=True,
            info="Retrieve context from knowledge base"
        )
    
    # Update globals
    def update_agent(agent_val):
        global current_agent_type
        current_agent_type = agent_val
    
    def update_rag(rag_val):
        global rag_enabled
        rag_enabled = rag_val
    
    agent_type.change(fn=update_agent, inputs=agent_type)
    use_rag.change(fn=update_rag, inputs=use_rag)
    
    gr.ChatInterface(
        fn=respond,
        examples=[
            "Generate a Python function for API request handling",
            "Review this architecture pattern",
            "Analyze this code for security issues",
            "How would you design a scalable system?",
        ],
        title="Agent Chat",
        description="Chat with specialized RAG agents",
        analytics_enabled=False,
    )

if __name__ == "__main__":
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)
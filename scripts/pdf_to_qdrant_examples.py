# e.g. 1: Convert a single PDF with auto-detection
"""
Command line:
    python pdf_to_qdrant.py --pdf README.md --domain software_dev

This will:
- Auto-detect PDF complexity
- Convert to markdown
- Chunk intelligently
- Store in Qdrant
"""


# e.g. 2: Batch convert a directory
"""
Command line:
    python pdf_to_qdrant.py --dir ./research_papers --domain reverse_engineering

This will:
- Find all .pdf files in ./research_papers
- Convert each one
- Store all chunks in the reverse_engineering collection
"""


# e.g. 3: Force specific conversion method
"""
Use PyMuPDF4LLM (fast, simple PDFs):
    python pdf_to_qdrant.py --pdf report.pdf --domain software_dev --method pymupdf4llm

Use Docling (scanned documents, tables):
    python pdf_to_qdrant.py --pdf scanned.pdf --domain software_dev --method docling

Use VLM (complex, image-heavy):
    export GEMINI_API_KEY="your-key"
    python pdf_to_qdrant.py --pdf complex.pdf --domain software_dev --method vlm
"""


# e.g. 4: Customize chunking
"""
Smaller chunks (better for granular search):
    python pdf_to_qdrant.py --pdf api_docs.pdf --domain software_dev \
        --chunk-size 256 --overlap 50

Larger chunks (for broad topics):
    python pdf_to_qdrant.py --pdf book.pdf --domain software_dev \
        --chunk-size 1024 --overlap 200
"""


# e.g. 5: Query converted PDFs in Python
def example_query_pdfs():
    """Query PDFs stored in Qdrant."""
    from langgraph_orchestration.retrievers.config import RAGConfigManager
    
    # Initialize
    RAGConfigManager.initialize()
    rag_manager = RAGConfigManager.get_rag_manager()
    
    # Query software dev PDFs
    results = rag_manager.retrieve_software_dev_context(
        "How do I implement a REST API?",
        top_k=3
    )
    
    print("Retrieved documents:")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc[:200]}...")
    
    # Query reverse engineering PDFs
    results_re = rag_manager.retrieve_reverse_engineering_context(
        "Explain vulnerability assessment",
        top_k=2
    )
    
    print("\n\nReverse engineering results:")
    for i, doc in enumerate(results_re, 1):
        print(f"\n{i}. {doc[:200]}...")


# e.g. 6: Use in LangGraph orchestration
def example_in_langgraph():
    """Show how PDFs are used in orchestration graphs"""
    from langgraph_orchestration.retrievers.config import RAGConfigManager
    from langgraph_orchestration.schemas.state import AgentState
    
    RAGConfigManager.initialize()
    rag_manager = RAGConfigManager.get_rag_manager()
    
    # Simulate a state from the orchestration
    state = AgentState(
        user_input="Build a microservices architecture using Python",
        selected_domain="software_dev",
        execution_domains=["software_dev"],
    )
        context = rag_manager.retrieve_software_dev_context(
        query=state.user_input,
        top_k=3
    )
    
    # State now has enriched context
    state.dev_context = context
    
    print(f"Retrieved {len(context)} context documents for agent")
    print(f"First document:\n{context[0][:300]}...")


# e.g. 7: Inspect what's stored
def example_inspect_qdrant():
    """Check what PDFs are stored"""
    from langgraph_orchestration.retrievers.config import RAGConfigManager
    
    RAGConfigManager.initialize()
    admin_service = RAGConfigManager.get_admin_service()
    
    # Get statistics
    stats = admin_service.get_statistics()
    
    print("\n" + "="*60)
    print("Qdrant Collection Statistics")
    print("="*60)
    
    for domain, info in stats['collections'].items():
        print(f"\n{domain}:")
        print(f"  Documents: {info.get('document_count', 0)}")
        print(f"  Vector dim: {info.get('vector_size', 'N/A')}")
    
    print("\n" + "="*60)


# e.g. 8: Full end-to-end workflow
def example_full_workflow():
    """Complete workflow: convert -> store -> query"""
    import subprocess
    import sys
    from pathlib import Path
    
    # Step 1: Convert PDFs to Qdrant
    print("\n" + "="*60)
    print("Step 1: Converting PDFs...")
    print("="*60)
    
    # Example (replace with your PDF path)
    pdf_path = Path("./README.md")  # Use an actual PDF
    if pdf_path.exists():
        result = subprocess.run([
            sys.executable,
            "pdf_to_qdrant.py",
            "--pdf", str(pdf_path),
            "--domain", "software_dev"
        ], cwd=Path(__file__).parent)
    else:
        print(f"Note: {pdf_path} not found. Use actual PDF paths.")
    
    # Step 2: Inspect storage
    print("\n" + "="*60)
    print("Step 2: Inspecting Qdrant...")
    print("="*60)
    example_inspect_qdrant()
    
    # Step 3: Query
    print("\n" + "="*60)
    print("Step 3: Querying PDFs...")
    print("="*60)
    example_query_pdfs()

if __name__ == "__main__":
    import sys
    
    examples = {
        "1": ("Query PDFs", example_query_pdfs),
        "2": ("Use in LangGraph", example_in_langgraph),
        "3": ("Inspect Qdrant", example_inspect_qdrant),
        "4": ("Full workflow", example_full_workflow),
    }
    
    print("\nPDF to Qdrant Quick-Start Examples")
    print("="*60)
    print("\nChoose an example:")
    for key, (name, _) in examples.items():
        print(f"  {key}: {name}")
    print(f"  0: Run all (interactive)")
    
    choice = input("\nEnter choice (0-4): ").strip()
    
    if choice == "0":
        # Run all
        for key in sorted(examples.keys()):
            try:
                name, func = examples[key]
                print(f"\n\n{'='*60}")
                print(f"Running: {name}")
                print('='*60)
                func()
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()
    elif choice in examples:
        name, func = examples[choice]
        print(f"\nRunning: {name}\n")
        try:
            func()
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("Invalid choice")
        sys.exit(1)
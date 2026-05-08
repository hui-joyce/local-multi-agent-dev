import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langgraph_orchestration.retrievers.qdrant_client import QdrantRetriever

# Connect to embedded Qdrant
retriever = QdrantRetriever()

# Show collections
for domain in ["software_dev", "reverse_engineering", "shared"]:
    info = retriever.get_collection_info(domain)
    print(f"\n{'='*60}")
    print(f"Collection: {info['name']}")
    print(f"Domain: {info['domain']}")
    print(f"Document Count: {info['document_count']}")
    print(f"Vector Dimension: {info['vector_size']}")
    print('='*60)
    
    # Show sample documents
    if info['document_count'] > 0:
        try:
            scroll_result = retriever.client.scroll(
                collection_name=info['name'],
                limit=5,
            )
            print("\nFirst 5 documents:")
            for i, point in enumerate(scroll_result[0], 1):
                text = point.payload.get("text", "")[:100]
                print(f"  {i}. {text}...")
        except Exception as e:
            print(f"  Error: {e}")
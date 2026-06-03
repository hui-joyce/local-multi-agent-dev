# Scripts - CLI Tools for RAG & Knowledge Base Management

This directory contains command-line utilities for managing RAG system and knowledge base.

## Scripts Overview

### `load_documents_to_qdrant.py` - Load Markdown/Text/JSONL Chunks
**Load Markdown, text, or pre-chunked JSONL records into Qdrant.**

**Usage:**
```bash
# Load single file
python scripts/load_documents_to_qdrant.py --file README.md --domain software_dev
# Load directory
python scripts/load_documents_to_qdrant.py --dir ./docs --domain software_dev
# Load JSONL chunks
python scripts/load_documents_to_qdrant.py --file chunks.jsonl --domain shared
# Custom chunking
python scripts/load_documents_to_qdrant.py --dir ./docs --domain software_dev --chunk-size 256
```

**Supports:**
- `.md`, `.markdown` - Markdown files with structure-aware chunking
- `.txt` - Plain text files
- `.jsonl` - One chunk per line with `text` and optional `metadata`

---

### `inspect_qdrant.py` - View Stored Documents
**Inspect and debug what's currently in your Qdrant database.**

Shows:
- Collection names and sizes
- Document counts per collection
- Sample documents from each collection
- Vector dimensions

**Usage:**
```bash
python scripts/inspect_qdrant.py
```

**Output Example:**
```
Collection: agents_software_dev
  Documents: 42
  Vector Dimension: 384

  First 5 documents:
    1. Python is a high-level programming language...
    2. Object-oriented programming (OOP) is a paradigm...
    ...
```

---

## Quick Start

### 1. Ingest Your First Document
```bash
python scripts/load_documents_to_qdrant.py --file README.md --domain software_dev
```

### 2. Check What's Stored
```bash
python scripts/inspect_qdrant.py
```

---

## Common Workflows

### Add New Knowledge Base Documents
```bash
# Ingest all docs in a folder
python scripts/load_documents_to_qdrant.py --dir ./knowledge_base --domain software_dev

# Verify they're stored
python scripts/inspect_qdrant.py
```

### Troubleshoot Retrieval
```bash
# Check what's actually stored
python scripts/inspect_qdrant.py
```

---

## Troubleshooting

### "Qdrant database locked" error
The embedded Qdrant database only allows one process at a time.

**Solution:** Stop `langgraph dev` temporarily:
```bash
pkill -f "langgraph dev"
python scripts/load_documents_to_qdrant.py --file doc.md --domain software_dev
```

### "No files found"
Make sure you point `--dir` at a folder containing `.md`, `.markdown`, `.txt`, or `.jsonl` files.

---

## Integration with LangGraph

Once documents are in Qdrant, the orchestration graphs automatically use them:

```python
# In langgraph_orchestration/graphs/software_dev.py
from langgraph_orchestration.retrievers.config import RAGConfigManager

RAGConfigManager.initialize()
rag_manager = RAGConfigManager.get_rag_manager()

# Automatically retrieves from your converted PDFs
context = rag_manager.retrieve_software_dev_context(
    query=state.user_input,
    top_k=3
)
```
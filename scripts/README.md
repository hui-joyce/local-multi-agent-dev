# Scripts - CLI Tools for RAG & Knowledge Base Management

This directory contains command-line utilities for managing RAG system and knowledge base.

## Scripts Overview

### `pdf_to_qdrant.py` - PDF to Markdown to Qdrant Pipeline
**Main tool for converting PDFs into searchable embeddings.**

Implements intelligent PDF conversion with auto-detection of complexity tier:
- **Category 1 (Simple)**: PyMuPDF4LLM for digital PDFs
- **Category 2 (Medium)**: Docling for scanned documents with OCR
- **Category 3 (Complex)**: Vision-Language Models for visual content (not added yet)

**Usage:**
```bash
# Auto-detect and convert
python scripts/pdf_to_qdrant.py --pdf document.pdf --domain software_dev
# Batch convert directory
python scripts/pdf_to_qdrant.py --dir ./research_pdfs --domain reverse_engineering
# Force specific method
python scripts/pdf_to_qdrant.py --pdf doc.pdf --domain software_dev --method docling
# With VLM (complex PDFs)
python scripts/pdf_to_qdrant.py --pdf complex.pdf --domain software_dev --method vlm --vlm-api-key YOUR_KEY
```

**Options:**
- `--pdf`: Single PDF to convert
- `--dir`: Directory with PDFs
- `--domain`: Target domain (software_dev, reverse_engineering, shared)
- `--method`: Force conversion method (pymupdf4llm, docling, vlm)
- `--chunk-size`: Words per chunk (default: 512)
- `--overlap`: Word overlap between chunks (default: 100)

---

### `load_documents_to_qdrant.py` - Load Markdown/Text Files
**Load Markdown, PDF, or text files with intelligent chunking.**

Simpler alternative to `pdf_to_qdrant.py` if you already have Markdown files.

**Usage:**
```bash
# Load single file
python scripts/load_documents_to_qdrant.py --file README.md --domain software_dev
# Load directory
python scripts/load_documents_to_qdrant.py --dir ./docs --domain software_dev
# Load PDF (basic extraction)
python scripts/load_documents_to_qdrant.py --pdf research.pdf --domain reverse_engineering
# Custom chunking
python scripts/load_documents_to_qdrant.py --dir ./docs --domain software_dev --chunk-size 256
```

**Supports:**
- `.md`, `.markdown` - Markdown files with structure-aware chunking
- `.txt` - Plain text files
- `.pdf` - Basic PDF text extraction

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

### `pdf_to_qdrant_examples.py` - Interactive Examples
**Ready-to-use examples for common RAG operations.**

10 interactive examples including:
1. Query PDFs
2. Use in LangGraph
3. Inspect Qdrant
4. Full end-to-end workflow

**Usage:**
```bash
python scripts/pdf_to_qdrant_examples.py

# Choose example from interactive menu
```

---

## Quick Start

### 1. Convert Your First PDF
```bash
python scripts/pdf_to_qdrant.py --pdf my_document.pdf --domain software_dev
```

### 2. Check What's Stored
```bash
python scripts/inspect_qdrant.py
```

### 3. Try Examples
```bash
python scripts/pdf_to_qdrant_examples.py
```

---

## Installation

Install PDF conversion dependencies:

```bash
# Base (always needed)
pip install PyMuPDF pymupdf4llm

# Category 2: OCR support for scanned documents
pip install docling

# Category 3: VLM for complex PDFs
pip install google-genai
```

---

## Common Workflows

### Add New Knowledge Base Documents
```bash
# Convert all PDFs in a folder
python scripts/pdf_to_qdrant.py --dir ./knowledge_base --domain software_dev

# Verify they're stored
python scripts/inspect_qdrant.py

# Test retrieval
python scripts/pdf_to_qdrant_examples.py
```

### Troubleshoot Retrieval
```bash
# Check what's actually stored
python scripts/inspect_qdrant.py

# Run example queries
python scripts/pdf_to_qdrant_examples.py
```

---

## Troubleshooting

### "Qdrant database locked" error
The embedded Qdrant database only allows one process at a time.

**Solution:** Stop `langgraph dev` temporarily:
```bash
pkill -f "langgraph dev"
python scripts/pdf_to_qdrant.py --pdf doc.pdf --domain software_dev
```

### "PyMuPDF not found"
```bash
pip install PyMuPDF
```

### "Docling not installed" (for scanned PDFs)
```bash
pip install docling
```

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
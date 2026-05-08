#!/usr/bin/env python3
"""Load .md, .txt and PDF files into Qdrant with chunking"""

import sys, argparse, re
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from langgraph_orchestration.retrievers.config import RAGConfigManager

def load_file(file_path: Path) -> str:
    """Load any file type (PDF, markdown, text)"""
    if file_path.suffix.lower() == '.pdf':
        try:
            import PyPDF2
        except ImportError:
            raise ImportError("PyPDF2 not installed: pip install PyPDF2")
        with open(file_path, 'rb') as f:
            return '\n'.join(page.extract_text() for page in PyPDF2.PdfReader(f).pages)
    else:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 100) -> List[str]:
    """Split text into overlapping word-based chunks"""
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size - overlap) if words[i:i + chunk_size]]

def chunk_markdown(text: str, chunk_size: int = 512) -> List[str]:
    """Split markdown by headers, respecting chunk size"""
    sections = re.split(r'\n(?=#{1,6}\s)', text)
    chunks, current = [], ""
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        if len(current.split()) + len(section.split()) < chunk_size:
            current += ("\n\n" if current else "") + section
        else:
            if current:
                chunks.append(current.strip())
            current = section
    
    if current:
        chunks.append(current.strip())
    return chunks


def load_documents(file_paths: List[Path], domain: str, chunk_size: int = 512, overlap: int = 100, use_markdown_chunking: bool = True) -> None:
    """Load files into Qdrant with chunking"""
    all_chunks, all_metadata = [], []
    
    print(f"\n{'='*70}\nLoading {len(file_paths)} file(s) into {domain}\n{'='*70}\n")
    
    for file_path in file_paths:
        if not file_path.exists():
            print(f"  ✗ Not found: {file_path.name}")
            continue
        
        try:
            print(f"  Processing: {file_path.name}")
            content = load_file(file_path)
            
            is_md = file_path.suffix.lower() in ['.md', '.markdown']
            chunk_fn = chunk_markdown if (is_md and use_markdown_chunking) else chunk_text
            chunks = chunk_fn(content, chunk_size=chunk_size)
            
            print(f"    → {len(chunks)} chunks ({len(content)} chars)")
            
            all_chunks.extend(chunks)
            all_metadata.extend([{
                "source_file": file_path.name,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "file_type": file_path.suffix.lower(),
            } for i in range(len(chunks))])
        
        except Exception as e:
            print(f"    ✗ Error: {e}")
            continue
    
    if not all_chunks:
        print("No documents to load\n")
        return
    
    print(f"\nStoring {len(all_chunks)} chunks in Qdrant (domain={domain})...")
    RAGConfigManager.initialize()
    retriever = RAGConfigManager.get_retriever()
    
    try:
        retriever.add_documents(all_chunks, domain=domain, metadata=all_metadata, batch_size=32)
        info = retriever.get_collection_info(domain)
        print(f"  ✓ Stored {len(all_chunks)} chunks | Collection: {info['document_count']} docs\n")
    except Exception as e:
        print(f"  Error: {e}")
        raise



def main():
    parser = argparse.ArgumentParser(
        description="Load .md/.txt/PDF files into Qdrant",
        epilog="Examples:\n  python load_documents_to_qdrant.py --file README.md --domain software_dev\n  python load_documents_to_qdrant.py --dir ./docs --domain software_dev\n  python load_documents_to_qdrant.py --pdf research.pdf --domain reverse_engineering"
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', type=Path, help='Single file to load')
    group.add_argument('--dir', type=Path, help='Directory with files')
    group.add_argument('--pdf', type=Path, help='PDF file to load')
    
    parser.add_argument('--domain', required=True, choices=['software_dev', 'reverse_engineering', 'shared'])
    parser.add_argument('--chunk-size', type=int, default=512, help='Chunk size in words')
    parser.add_argument('--overlap', type=int, default=100, help='Word overlap')
    parser.add_argument('--extensions', default='.md,.markdown,.txt', help='Extensions for --dir')
    
    args = parser.parse_args()
    
    if args.file:
        files = [args.file]
    elif args.pdf:
        files = [args.pdf]
    else:
        exts = set(args.extensions.split(','))
        files = [f for f in args.dir.rglob('*') if f.is_file() and f.suffix.lower() in exts]
    
    if not files:
        print("No files found")
        sys.exit(1)
    
    load_documents(files, domain=args.domain, chunk_size=args.chunk_size, overlap=args.overlap)


if __name__ == '__main__':
    main()
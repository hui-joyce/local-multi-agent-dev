#!/usr/bin/env python3
"""Load markdown/text/JSONL chunk files into Qdrant"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from langgraph_orchestration.retrievers.config import RAGConfigManager

def load_file(file_path: Path) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def load_jsonl_chunks(file_path: Path) -> list[tuple[str, dict]]:
    chunks: list[tuple[str, dict]] = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            text = record.get('text', '')
            if not text:
                continue
            metadata = dict(record.get('metadata', {}))
            metadata.setdefault('source_file', file_path.name)
            metadata.setdefault('line_number', line_number)
            chunks.append((text, metadata))
    return chunks

def chunk_text(text: str, chunk_size: int = 512, overlap: int = 100) -> List[str]:
    words = text.split()
    if not words:
        return []
    step = max(1, chunk_size - overlap)
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), step)]

def chunk_markdown(text: str, chunk_size: int = 512) -> List[str]:
    sections = re.split(r'\n(?=#{1,6}\s)', text)
    chunks, current = [], ""
    for section in sections:
        section = section.strip()
        if not section:
            continue
        if len(current.split()) + len(section.split()) <= chunk_size:
            current += ("\n\n" if current else "") + section
        else:
            if current:
                chunks.append(current.strip())
            current = section
    if current:
        chunks.append(current.strip())
    return chunks


def load_documents(
    file_paths: List[Path],
    domain: str,
    chunk_size: int = 512,
    overlap: int = 100,
) -> None:
    all_chunks, all_metadata = [], []

    print(f"\n{'='*70}\nLoading {len(file_paths)} file(s) into {domain}\n{'='*70}\n")
    for file_path in file_paths:
        if not file_path.exists():
            print(f"  ✗ Not found: {file_path.name}")
            continue

        try:
            print(f"  Processing: {file_path.name}")
            suffix = file_path.suffix.lower()

            if suffix == '.jsonl':
                jsonl_chunks = load_jsonl_chunks(file_path)
                chunks = [text for text, _ in jsonl_chunks]
                metadata = [dict(item[1]) for item in jsonl_chunks]
            else:
                content = load_file(file_path)
                is_markdown = suffix in ['.md', '.markdown']
                chunk_fn = chunk_markdown if is_markdown else chunk_text
                chunks = chunk_fn(content, chunk_size=chunk_size)
                metadata = [{
                    "source_file": file_path.name,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "file_type": suffix,
                } for i in range(len(chunks))]

            print(f"    → {len(chunks)} chunks")
            all_chunks.extend(chunks)
            all_metadata.extend(metadata)

        except Exception as e:
            print(f"    ✗ Error: {e}")

    if not all_chunks:
        print("No documents to load\n")
        return

    print(f"\nStoring {len(all_chunks)} chunks in Qdrant (domain={domain})...")
    RAGConfigManager.initialize()
    retriever = RAGConfigManager.get_retriever()

    try:
        retriever.add_documents(all_chunks, domain=domain, metadata=all_metadata, batch_size=32)
        info = retriever.get_collection_info(domain)
        print(f"  ✓ Stored {len(all_chunks)} chunks | Collection: {info.get('document_count', 0)} docs\n")
    except Exception as e:
        print(f"  Error: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(
        description="Load markdown/text/JSONL chunk files into Qdrant",
        epilog="Examples:\n  python load_documents_to_qdrant.py --file README.md --domain software_dev\n  python load_documents_to_qdrant.py --dir ./docs --domain software_dev\n  python load_documents_to_qdrant.py --file chunks.jsonl --domain shared",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', type=Path, help='Single file to load')
    group.add_argument('--dir', type=Path, help='Directory with files')

    parser.add_argument('--domain', required=True, choices=['software_dev', 'reverse_engineering', 'shared'])
    parser.add_argument('--chunk-size', type=int, default=512, help='Chunk size in words')
    parser.add_argument('--overlap', type=int, default=100, help='Word overlap')
    parser.add_argument('--extensions', default='.md,.markdown,.txt,.jsonl', help='Extensions for --dir')

    args = parser.parse_args()

    if args.file:
        files = [args.file]
    else:
        exts = {ext.strip().lower() for ext in args.extensions.split(',') if ext.strip()}
        files = [f for f in args.dir.rglob('*') if f.is_file() and f.suffix.lower() in exts]

    if not files:
        print("No files found")
        sys.exit(1)

    load_documents(files, domain=args.domain, chunk_size=args.chunk_size, overlap=args.overlap)

if __name__ == '__main__':
    main()
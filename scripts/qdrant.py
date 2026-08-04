from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from langgraph_orchestration.retrievers import DOMAINS, get_retriever  # noqa: E402

_UNAVAILABLE = (
    "Vector database unavailable. Check the embedding model is downloaded "
    "(python -m langgraph_orchestration.inference --embeddings-only) and that no other "
    "process holds the embedded Qdrant."
)

# Section: chunking


def load_jsonl_chunks(file_path: Path) -> list[tuple[str, dict]]:
    """Each line is a pre-chunked record with ``text`` and optional ``metadata``"""
    chunks: list[tuple[str, dict]] = []
    with open(file_path, encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            text = record.get("text", "")
            if not text:
                continue
            metadata = dict(record.get("metadata", {}))
            metadata.setdefault("source_file", file_path.name)
            metadata.setdefault("line_number", line_number)
            chunks.append((text, metadata))
    return chunks


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 100) -> list[str]:
    words = text.split()
    if not words:
        return []
    step = max(1, chunk_size - overlap)
    return [" ".join(words[i : i + chunk_size]) for i in range(0, len(words), step)]


def chunk_markdown(text: str, chunk_size: int = 512) -> list[str]:
    """Split on headers, packing sections up to *chunk_size* words"""
    sections = re.split(r"\n(?=#{1,6}\s)", text)
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


def _chunk_file(file_path: Path, chunk_size: int, overlap: int) -> tuple[list[str], list[dict]]:
    suffix = file_path.suffix.lower()

    if suffix == ".jsonl":
        records = load_jsonl_chunks(file_path)
        return [text for text, _ in records], [dict(meta) for _, meta in records]

    content = file_path.read_text(encoding="utf-8")
    if suffix in (".md", ".markdown"):
        # Header splitting has no sliding window, so overlap does not apply.
        chunks = chunk_markdown(content, chunk_size=chunk_size)
    else:
        chunks = chunk_text(content, chunk_size=chunk_size, overlap=overlap)

    metadata = [
        {
            "source_file": file_path.name,
            "chunk_index": index,
            "total_chunks": len(chunks),
            "file_type": suffix,
        }
        for index in range(len(chunks))
    ]
    return chunks, metadata


# Section: commands


def load_documents(
    file_paths: list[Path], domain: str, chunk_size: int = 512, overlap: int = 100
) -> int:
    all_chunks: list[str] = []
    all_metadata: list[dict] = []

    print(f"\nLoading {len(file_paths)} file(s) into {domain}\n")
    for file_path in file_paths:
        if not file_path.exists():
            print(f"  [FAIL] Not found: {file_path.name}")
            continue
        try:
            chunks, metadata = _chunk_file(file_path, chunk_size, overlap)
            print(f"  {file_path.name} -> {len(chunks)} chunks")
            all_chunks.extend(chunks)
            all_metadata.extend(metadata)
        except (OSError, ValueError) as exc:
            print(f"  [FAIL] {file_path.name}: {type(exc).__name__}: {exc}")

    if not all_chunks:
        print("\nNo documents to load")
        return 1

    print(f"\nStoring {len(all_chunks)} chunks (domain={domain})...")
    retriever = get_retriever()
    if retriever is None:
        print(_UNAVAILABLE, file=sys.stderr)
        return 1
    retriever.add_documents(all_chunks, domain=domain, metadata=all_metadata, batch_size=32)
    info = retriever.get_collection_info(domain)
    print(f"  [OK] collection now holds {info.get('document_count', 0)} document(s)\n")
    return 0


def inspect_collections(sample: int = 5) -> int:
    retriever = get_retriever()
    if retriever is None:
        print(_UNAVAILABLE, file=sys.stderr)
        return 1
    for domain in DOMAINS:
        info = retriever.get_collection_info(domain)
        print(f"\n{'=' * 60}")
        print(f"Collection: {info['name']}  (domain={info['domain']})")
        print(f"Documents:  {info['document_count']}")
        print(f"Dimension:  {info['vector_size']}")
        print("=" * 60)

        if not info["document_count"]:
            continue
        try:
            points, _ = retriever.client.scroll(collection_name=info["name"], limit=sample)
        except Exception as exc:
            print(f"  Error reading points: {type(exc).__name__}: {exc}")
            continue
        for index, point in enumerate(points, 1):
            print(f"  {index}. {point.payload.get('text', '')[:100]}...")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Populate and inspect the embedded Qdrant vector database."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    loader = sub.add_parser("load", help="chunk files and store them")
    source = loader.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path, help="single file to load")
    source.add_argument("--dir", type=Path, help="directory to walk")
    loader.add_argument("--domain", required=True, choices=DOMAINS)
    loader.add_argument("--chunk-size", type=int, default=512, help="chunk size in words")
    loader.add_argument("--overlap", type=int, default=100, help="word overlap (plain text only)")
    loader.add_argument(
        "--extensions", default=".md,.markdown,.txt,.jsonl", help="extensions for --dir"
    )

    viewer = sub.add_parser("inspect", help="print collection stats and sample documents")
    viewer.add_argument("--sample", type=int, default=5, help="documents to preview per collection")

    args = parser.parse_args(argv)

    if args.command == "inspect":
        return inspect_collections(args.sample)

    if args.file:
        files = [args.file]
    else:
        wanted = {ext.strip().lower() for ext in args.extensions.split(",") if ext.strip()}
        files = sorted(
            path for path in args.dir.rglob("*") if path.is_file() and path.suffix.lower() in wanted
        )
    if not files:
        print("No files found", file=sys.stderr)
        return 1

    return load_documents(files, args.domain, args.chunk_size, args.overlap)


if __name__ == "__main__":
    sys.exit(main())

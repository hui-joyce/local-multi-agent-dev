"""3 tier PDF conversion: simple (PyMuPDF4LLM) → medium (Docling) → complex (VLM, not added yet)"""

import sys, argparse, os, re, time
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass

sys.path.insert(0, str(Path(__file__).parent))
from langgraph_orchestration.retrievers.config import RAGConfigManager

@dataclass
class ConversionResult:
    pdf_path: str
    method: str
    total_pages: int
    markdown_content: str
    processing_time: float
    success: bool
    error: Optional[str] = None


def _get_pdf_pages(pdf_path: Path) -> int:
    try:
        import fitz
        doc = fitz.open(pdf_path)
        count = len(doc)
        doc.close()
        return count
    except:
        return 0

def analyze_pdf(pdf_path: Path) -> Tuple[str, Dict]:
    """Classify PDF complexity (simple/medium/complex)"""
    try:
        import fitz
    except ImportError:
        raise ImportError("PyMuPDF not installed: pip install PyMuPDF")
    
    try:
        doc = fitz.open(pdf_path)
        total_pages = len(doc)
        total_text, total_images = 0, 0
        
        for page_idx in range(min(3, total_pages)):
            page = doc[page_idx]
            total_text += len(page.get_text().strip())
            total_images += len(page.get_images())
        
        doc.close()
        
        avg_text = total_text / max(3, total_pages)
        avg_imgs = total_images / max(3, total_pages)
        
        characteristics = {
            "total_pages": total_pages,
            "is_scanned": avg_text < 50,
            "has_images": avg_imgs > 0.5,
            "image_count": total_images,
            "text_density": avg_text,
            "avg_images_per_page": avg_imgs,
        }
        
        # Tier routing
        tier = "medium" if characteristics["is_scanned"] else ("complex" if avg_imgs > 2 else "simple")
        return tier, characteristics
    
    except Exception as e:
        print(f"  Could not analyze PDF: {e}, defaulting to 'simple'")
        return "simple", {"total_pages": 0, "text_density": 0, "avg_images_per_page": 0}


def _wrap_conversion(method_name: str, converter_fn, pdf_path: Path, *args) -> ConversionResult:
    """Wrapper to standardize conversion results"""
    start = time.time()
    try:
        md_text = converter_fn(pdf_path, *args)
        return ConversionResult(
            pdf_path=str(pdf_path),
            method=method_name,
            total_pages=_get_pdf_pages(pdf_path),
            markdown_content=md_text,
            processing_time=time.time() - start,
            success=True,
        )
    except Exception as e:
        return ConversionResult(
            pdf_path=str(pdf_path),
            method=method_name,
            total_pages=_get_pdf_pages(pdf_path),
            markdown_content="",
            processing_time=time.time() - start,
            success=False,
            error=str(e),
        )

def _convert_pymupdf4llm(pdf_path: Path) -> str:
    try:
        import pymupdf4llm
    except ImportError:
        raise ImportError("PyMuPDF4LLM not installed: pip install pymupdf4llm")
    return pymupdf4llm.to_markdown(str(pdf_path))

def _convert_docling(pdf_path: Path) -> str:
    try:
        from docling.document_converter import DocumentConverter, PdfFormatOption
        from docling.datamodel.base_models import InputFormat
        from docling.datamodel.pipeline_options import PdfPipelineOptions
    except ImportError:
        raise ImportError("Docling not installed: pip install docling")
    
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_table_structure = True
    pipeline_options.do_ocr = True
    pipeline_options.images_scale = 2.0
    pipeline_options.generate_picture_images = True
    
    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )
    result = converter.convert(str(pdf_path))
    return result.document.export_to_markdown()

def convert_simple_pdf_pymupdf4llm(pdf_path: Path) -> ConversionResult:
    return _wrap_conversion("pymupdf4llm", _convert_pymupdf4llm, pdf_path)

def convert_medium_pdf_docling(pdf_path: Path) -> ConversionResult:
    return _wrap_conversion("docling", _convert_docling, pdf_path)


def convert_pdf_smart(pdf_path: Path, method: Optional[str] = None) -> ConversionResult:
    """Route to optimal converter"""
    if method:
        converters = {
            "pymupdf4llm": convert_simple_pdf_pymupdf4llm,
            "docling": convert_medium_pdf_docling,
        }
        if method not in converters:
            raise ValueError(f"Unknown method: {method}")
        print(f"  Using specified method: {method}")
        return converters[method](pdf_path)
    
    # Auto-detect
    print(f"  Analyzing PDF complexity...")
    tier, chars = analyze_pdf(pdf_path)
    
    print(f"  Detected: {tier.upper()} | Pages: {chars['total_pages']} | "
          f"Images/page: {chars['avg_images_per_page']:.1f}")
    
    if tier == "simple":
        print(f"  → PyMuPDF4LLM (digital PDF)")
        return convert_simple_pdf_pymupdf4llm(pdf_path)
    else:
        print(f"  → Docling (scanned/complex)")
        return convert_medium_pdf_docling(pdf_path)

def chunk_markdown(text: str, chunk_size: int = 512, overlap: int = 100) -> List[str]:
    """Split markdown while preserving structure"""
    sections = re.split(r'\n(?=#{1,6}\s)', text)
    chunks, current_chunk, current_words = [], "", 0
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
        
        section_words = len(section.split())
        
        if current_words + section_words < chunk_size:
            current_chunk += ("\n\n" if current_chunk else "") + section
            current_words += section_words
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
                prev_words = current_chunk.split()[-overlap:]
                current_chunk = " ".join(prev_words) + "\n\n" + section if prev_words else section
            else:
                current_chunk = section
            current_words = len(current_chunk.split())
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def store_pdf_in_qdrant(result: ConversionResult, domain: str, chunk_size: int = 512, overlap: int = 100) -> None:
    if not result.success:
        print(f"  Cannot store failed conversion: {result.error}")
        return
    
    chunks = chunk_markdown(result.markdown_content, chunk_size, overlap)
    print(f"  Chunking markdown: {len(chunks)} chunks")
    
    pdf_filename = Path(result.pdf_path).name
    metadata = [{
        "source_pdf": pdf_filename,
        "source_path": result.pdf_path,
        "conversion_method": result.method,
        "chunk_index": i,
        "total_chunks": len(chunks),
        "total_pdf_pages": result.total_pages,
        "processing_time": result.processing_time,
    } for i in range(len(chunks))]
    
    print(f"  Adding to Qdrant (domain={domain})...")
    RAGConfigManager.initialize()
    retriever = RAGConfigManager.get_retriever()
    
    try:
        retriever.add_documents(chunks, domain=domain, metadata=metadata, batch_size=32)
        info = retriever.get_collection_info(domain)
        print(f"  ✓ Stored {len(chunks)} chunks | Collection: {info['document_count']} docs")
    except Exception as e:
        print(f"  Error storing in Qdrant: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="PDF → Markdown → Qdrant Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pdf_to_qdrant.py --pdf doc.pdf --domain software_dev
  python pdf_to_qdrant.py --dir ./pdfs --domain reverse_engineering
  python pdf_to_qdrant.py --pdf doc.pdf --domain software_dev --method docling
  python pdf_to_qdrant.py --pdf doc.pdf --domain software_dev --chunk-size 256
        """
    )
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--pdf', type=Path, help='Single PDF to convert')
    input_group.add_argument('--dir', type=Path, help='Directory with PDFs')
    
    parser.add_argument('--domain', required=True, choices=['software_dev', 'reverse_engineering', 'shared'], help='Target domain')
    parser.add_argument('--method', choices=['pymupdf4llm', 'docling'], help='Conversion method (auto-detect if unspecified)')
    parser.add_argument('--chunk-size', type=int, default=512, help='Words per chunk')
    parser.add_argument('--overlap', type=int, default=100, help='Word overlap')
    parser.add_argument('--extensions', default='.pdf', help='File extensions for --dir')
    
    args = parser.parse_args()
    
    files = [args.pdf] if args.pdf else [f for f in args.dir.rglob('*') if f.is_file() and f.suffix.lower() in set(args.extensions.split(','))]
    
    if not files:
        print("No files found")
        sys.exit(1)
    
    print(f"\n{'='*70}\nPDF → Qdrant Pipeline\n{'='*70}")
    print(f"Files: {len(files)} | Domain: {args.domain} | Method: {args.method or 'auto-detect'}\n")
    
    for pdf_path in files:
        print(f"Processing: {pdf_path.name}")
        try:
            result = convert_pdf_smart(pdf_path, method=args.method)
            if result.success:
                print(f"  ✓ Converted ({result.processing_time:.1f}s) | {len(result.markdown_content)} chars | Method: {result.method}")
                store_pdf_in_qdrant(result, domain=args.domain, chunk_size=args.chunk_size, overlap=args.overlap)
            else:
                print(f"  ✗ Failed: {result.error}")
        except Exception as e:
            print(f"  Error: {e}")
            import traceback
            traceback.print_exc()
    
    print(f"\n{'='*70}\nPipeline complete!\n{'='*70}\n")


if __name__ == '__main__':
    main()
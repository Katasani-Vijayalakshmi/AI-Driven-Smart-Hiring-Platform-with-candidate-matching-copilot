"""
backend/resume_loader.py
=========================
Resume File Loader — Part 1, Milestone 1
Extracts raw text from PDF and DOCX resume files.

Libraries:
    PyMuPDF (fitz) → PDF extraction
    python-docx    → DOCX extraction

Usage:
    text = load_resume("path/to/resume.pdf")
    text = load_resume("path/to/resume.docx")
"""

import os
import fitz          # PyMuPDF
import docx
from pathlib import Path


# ── PDF Extraction ─────────────────────────────────────────────
def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF resume using PyMuPDF (fitz).

    Iterates through every page and concatenates text blocks,
    preserving paragraph spacing with double newlines.

    Args:
        pdf_path: Absolute or relative path to the PDF file.

    Returns:
        Raw text string extracted from the PDF.

    Raises:
        FileNotFoundError: If the PDF does not exist.
        RuntimeError: If fitz cannot open the file.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(str(path))
    text = ""
    for page in doc:
        # Extract text with layout preservation
        page_text = page.get_text("text")   # plain text mode
        text += page_text + "\n\n"
    doc.close()
    return text.strip()


# ── DOCX Extraction ────────────────────────────────────────────
def extract_text_from_docx(docx_path: str) -> str:
    """
    Extract all text from a DOCX resume using python-docx.

    Parses paragraphs and also handles text inside tables,
    which is common in modern resume templates.

    Args:
        docx_path: Absolute or relative path to the DOCX file.

    Returns:
        Raw text string extracted from the DOCX.

    Raises:
        FileNotFoundError: If the DOCX does not exist.
    """
    path = Path(docx_path)
    if not path.exists():
        raise FileNotFoundError(f"DOCX not found: {docx_path}")

    document = docx.Document(str(path))

    # Collect paragraph text
    paragraphs = [para.text for para in document.paragraphs if para.text.strip()]

    # Also extract text from tables (many resumes use table-based layouts)
    table_text = []
    for table in document.tables:
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells if cell.text.strip()]
            if row_data:
                table_text.append("  |  ".join(row_data))

    all_text = "\n".join(paragraphs)
    if table_text:
        all_text += "\n\n" + "\n".join(table_text)

    return all_text.strip()


# ── Unified Loader ─────────────────────────────────────────────
def load_resume(file_path: str) -> str:
    """
    Unified resume loader — auto-detects format and dispatches
    to the appropriate extractor.

    Supported formats: .pdf, .docx, .doc

    Args:
        file_path: Path to the resume file.

    Returns:
        Extracted raw text.

    Raises:
        ValueError: If the file format is not supported.
        FileNotFoundError: If the file does not exist.
    """
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in (".docx", ".doc"):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError(
            f"Unsupported file format '{ext}'. "
            f"Supported: .pdf, .docx, .doc"
        )


# ── Quick CLI test ─────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python resume_loader.py <path/to/resume.pdf|.docx>")
        sys.exit(1)

    file = sys.argv[1]
    print(f"\n[resume_loader] Loading: {file}")
    text = load_resume(file)
    print(f"[resume_loader] Extracted {len(text)} characters\n")
    print("─" * 60)
    print(text[:2000])   # preview first 2000 chars
    print("─" * 60)

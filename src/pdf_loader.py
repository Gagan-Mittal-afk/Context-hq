"""A small, framework-free PDF text loader."""

from pathlib import Path

from pypdf import PdfReader


def load_pdf(pdf_path: str | Path) -> list[tuple[int, str]]:
    """Return the extracted text from each page in a PDF.

    Each item is a ``(page_number, text)`` tuple. Page numbers start at 1,
    which matches the page numbers people see in a PDF viewer.
    """
    path = Path(pdf_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {path}")

    if path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a .pdf file, got: {path.name}")

    reader = PdfReader(path)
    pages: list[tuple[int, str]] = []

    for page_number, page in enumerate(reader.pages, start=1):
        # Some PDF pages, such as image-only scans, have no extractable text.
        text = page.extract_text() or ""
        pages.append((page_number, text))

    return pages

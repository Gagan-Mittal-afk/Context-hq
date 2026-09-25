from pathlib import Path

from src.pdf_loader import load_pdf


PDF_PATH = Path("data/Context HQ Test Document.pdf")


def test_load_pdf():
    pages = load_pdf(PDF_PATH)

    assert len(pages) == 2

    assert pages[0][0] == 1
    assert pages[1][0] == 2

    assert isinstance(pages[0][1], str)
    assert isinstance(pages[1][1], str)

    assert "PDF loader" in pages[0][1]
    assert "pdf loader" in pages[1][1]
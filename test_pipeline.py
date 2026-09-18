from src.pdf_loader import load_pdf
from src.chunker import chunk_text

pages = load_pdf("data/Context HQ Test Document.pdf")

for page_number, text in pages:
    chunks = chunk_text(text, 10, 2)

    for chunk in chunks:
        print(f"Page {page_number}: {chunk}")
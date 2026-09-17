from src.pdf_loader import load_pdf
pages = load_pdf("data/Context HQ Test Document.pdf")

for page_number,text in pages:
    print(f"--- Page {page_number}---")
    print(text)
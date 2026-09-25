from pathlib import Path

from src.chunker import chunk_text
from src.embeddings import generate_embeddings
from src.pdf_loader import load_pdf
from src.vector_store import add_documents, create_collection


PDF_PATH = Path("data/Context HQ Test Document.pdf")


def test_pipeline():
    pages = load_pdf(PDF_PATH)

    documents = []
    metadatas = []

    for page_number, text in pages:
        chunks = chunk_text(
            text,
            chunk_size=500,
            overlap=100
        )

        for chunk_number, chunk in enumerate(chunks):
            documents.append(chunk)

            metadatas.append({
                "document_id": "test_pipeline_document",
                "source": "Context HQ Test Document.pdf",
                "page": page_number,
                "chunk": chunk_number
            })

    assert len(documents) > 0

    embeddings = generate_embeddings(documents)

    assert len(embeddings) == len(documents)
    assert len(embeddings[0]) == 384

    collection = create_collection()

    add_documents(
        collection,
        documents,
        metadatas,
        document_name="test_pipeline_document"
    )

    results = collection.query(
        query_embeddings=[embeddings[0].tolist()],
        n_results=1,
        where={
            "document_id": "test_pipeline_document"
        }
    )

    assert len(results["documents"][0]) == 1
    assert results["metadatas"][0][0]["document_id"] == (
        "test_pipeline_document"
    )
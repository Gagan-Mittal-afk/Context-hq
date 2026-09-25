from pathlib import Path
import tempfile

from src.pdf_loader import load_pdf
from src.chunker import chunk_text
from src.vector_store import add_documents, create_collection
from src.embeddings import get_embedding_dimension

def ingest_pdf(uploaded_file):
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    ) as temp_file:

        temp_file.write(uploaded_file.getbuffer())
        temp_path = Path(temp_file.name)

    try:
        pages = load_pdf(temp_path)

        documents = []
        metadatas = []

        document_name = Path(uploaded_file.name).stem

        for page_number, text in pages:

            chunks = chunk_text(
                text,
                chunk_size=500,
                overlap=100
            )

            for chunk_number, chunk in enumerate(chunks):

                documents.append(chunk)

                metadatas.append({
                    "document_id": document_name,
                    "source": uploaded_file.name,
                    "page": page_number,
                    "chunk": chunk_number
                })

        if not documents:
            raise ValueError(
                "No text could be extracted from the PDF."
            )

        collection = create_collection()

        existing = collection.get(
            where={"document_id": document_name}
        )

        if existing["ids"]:

            return {
                "filename": uploaded_file.name,
                "pages": 0,
                "chunks": 0,
                "embedding_dimensions": 0,
                "already_exists": True
            }

        add_documents(
            collection,
            documents,
            metadatas,
            document_name=document_name
        )

        return {
            "filename": uploaded_file.name,
            "pages": len(pages),
            "chunks": len(documents),
            "embedding_dimensions": get_embedding_dimension(),
            "already_exists": False
        }

    finally:
        temp_path.unlink(missing_ok=True)
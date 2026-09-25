from src.pdf_loader import load_pdf
from src.chunker import chunk_text
from src.embeddings import generate_embeddings
from src.vector_store import create_collection, add_documents


PDF_PATH = "data/Context HQ Test Document.pdf"


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
        "document_id": "Context HQ Test Document",
        "source": "Context HQ Test Document.pdf",
        "page": page_number,
        "chunk": chunk_number
})


print("Total chunks:", len(documents))

embeddings = generate_embeddings(documents)

print("Embedding dimensions:", len(embeddings[0]))

collection = create_collection()

add_documents(
    collection,
    documents,
    metadatas,
    document_name="context_hq_test_document"
)

print("Documents successfully added to Chroma!")
query = "What is this document about?"

results = collection.query(
    query_embeddings=generate_embeddings([query]).tolist(),
    n_results=3
)

print("\nQuery:")
print(query)

print("\nRetrieved documents:")

for i, document in enumerate(results["documents"][0]):
    print(f"\nResult {i + 1}:")
    print(document)

    print("Metadata:")
    print(results["metadatas"][0][i])

    print("Distance:")
    print(results["distances"][0][i])
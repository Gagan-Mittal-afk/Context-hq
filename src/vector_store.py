import chromadb

from src.embeddings import generate_embeddings


def create_collection():
    client = chromadb.PersistentClient(path="./chroma_db")

    collection = client.get_or_create_collection(
        name="context_hq"
    )

    return collection


def add_documents(
    collection,
    documents,
    metadatas=None,
    document_name="document"
):
    embeddings = generate_embeddings(documents)

    ids = [
        f"{document_name}_chunk_{i}"
        for i in range(len(documents))
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


def search(collection, query, n_results=3):
    query_embedding = generate_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results
    )

    return results


def list_documents():
    collection = create_collection()

    data = collection.get(
        include=["metadatas"]
    )

    documents = {}

    for metadata in data["metadatas"]:
        if not metadata:
            continue

        document_id = metadata.get("document_id")
        source = metadata.get("source")

        if document_id and source:
            documents[document_id] = source

    return [
        {
            "document_id": document_id,
            "source": source
        }
        for document_id, source in documents.items()
    ]


if __name__ == "__main__":
    collection = create_collection()

    documents = [
        "Machine learning is a branch of artificial intelligence.",
        "Supervised learning uses labelled training data.",
        "Unsupervised learning finds patterns in unlabelled data."
    ]

    metadatas = [
        {"source": "test_document", "chunk": 0},
        {"source": "test_document", "chunk": 1},
        {"source": "test_document", "chunk": 2}
    ]

    add_documents(
        collection,
        documents,
        metadatas
    )

    results = search(
        collection,
        "What is supervised learning?"
    )

    print("\nRetrieved documents:")
    print(results["documents"])

    print("\nDistances:")
    print(results["distances"])

    print("\nMetadata:")
    print(results["metadatas"])
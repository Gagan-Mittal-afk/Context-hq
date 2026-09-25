import chromadb

from src.embeddings import generate_embeddings


COLLECTION_NAME = "context_hq"
CHROMA_PATH = "./chroma_db"


def create_collection():
    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
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


def search(
    collection,
    query,
    n_results=3
):
    query_embedding = generate_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
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
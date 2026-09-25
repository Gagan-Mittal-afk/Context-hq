from src.embeddings import generate_embeddings
from src.vector_store import create_collection
from src.llm import generate_answer


def ask(
    question,
    document_id,
    chat_history=None,
    n_results=3
):
    collection = create_collection()

    query_embedding = generate_embeddings([question])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=n_results,
        where={"document_id": document_id}
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(documents)

    answer = generate_answer(
        context,
        question,
        chat_history=chat_history
    )

    return {
        "answer": answer,
        "sources": metadatas
    }
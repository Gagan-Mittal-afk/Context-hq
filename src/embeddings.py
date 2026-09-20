from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(texts):
    embeddings = model.encode(texts)

    return embeddings


if __name__ == "__main__":
    texts = [
        "Python is a programming language.",
        "Machine learning uses data to learn patterns.",
        "The Eiffel Tower is located in Paris."
    ]

    embeddings = generate_embeddings(texts)

    print("Number of texts:", len(texts))
    print("Embedding dimensions:", len(embeddings[0]))
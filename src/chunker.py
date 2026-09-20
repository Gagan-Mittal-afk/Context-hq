def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunk = text[start:end]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":
    text = """
    Machine learning is a branch of artificial intelligence.
    It allows computers to learn patterns from data.
    Supervised learning uses labelled data.
    Unsupervised learning finds patterns in unlabelled data.
    """

    chunks = chunk_text(text, chunk_size=100, overlap=20)

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1}:")
        print(chunk)
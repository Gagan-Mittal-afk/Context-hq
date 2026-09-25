from src.chunker import chunk_text


def test_chunk_text():
    text = (
        "Machine learning is a branch of artificial intelligence. "
        "It allows computers to learn patterns from data."
    )

    chunks = chunk_text(
        text,
        chunk_size=50,
        overlap=10
    )

    assert len(chunks) > 1
    assert all(isinstance(chunk, str) for chunk in chunks)
    assert all(len(chunk) <= 50 for chunk in chunks)
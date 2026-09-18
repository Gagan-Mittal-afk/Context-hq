def chunk_text(text, chunk_size, overlap):
    words = text.split()
    chunks = []

    step = chunk_size - overlap

    for start in range(0, len(words), step):
        if start >= len(words) - overlap:
            break
        chunk = words[start:start + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks
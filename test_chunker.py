from src.chunker import chunk_text

text = "A B C D E F G H I J"

chunks = chunk_text(text, 4, 1)

print(chunks)
import requests


def generate_answer(context, question):
    prompt = f"""
You are a helpful assistant for ContextHQ.

Answer the user's question using only the provided context.
If the answer cannot be found in the context, say that the
information is not available in the provided document.

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen3:8b",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    return response.json()["response"]
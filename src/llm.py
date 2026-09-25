import requests


def generate_answer(context, question, chat_history=None):
    if chat_history is None:
        chat_history = []

    history_text = ""

    for message in chat_history:
        role = message["role"].capitalize()
        content = message["content"]

        history_text += f"{role}: {content}\n"

    prompt = f"""
You are a helpful assistant for ContextHQ.

Answer the user's question using the provided document context
and conversation history.

Rules:
- Use the document context as the primary source of information.
- Use conversation history to understand references such as
  "it", "that", or "the previous answer".
- Do not invent information that is not supported by the context.
- If the answer cannot be found in the provided document context,
  say that the information is not available in the provided document.

Conversation history:
{history_text}

Document context:
{context}

Current question:
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
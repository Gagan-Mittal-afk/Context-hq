import requests

from src.llm import generate_answer


def test_generate_answer():
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )
        response.raise_for_status()

    except requests.RequestException:
        raise AssertionError(
            "Ollama is not running. Start Ollama before running this test."
        )

    answer = generate_answer(
        context="Python is a programming language.",
        question="What is Python?"
    )

    assert isinstance(answer, str)
    assert len(answer.strip()) > 0
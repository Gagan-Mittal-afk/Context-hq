from src.rag import ask


def test_rag():
    result = ask(
        question="What is this document about?",
        document_id="Context HQ Test Document"
    )

    assert isinstance(result, dict)

    assert "answer" in result
    assert "sources" in result

    assert isinstance(result["answer"], str)
    assert len(result["answer"].strip()) > 0

    assert isinstance(result["sources"], list)
    assert len(result["sources"]) > 0

    for source in result["sources"]:
        assert source["document_id"] == "Context HQ Test Document"
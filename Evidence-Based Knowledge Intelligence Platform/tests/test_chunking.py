from src.ingestion.chunking import chunk_documents


def test_chunk_documents_preserves_metadata():
    documents = [{
        "text": "This is a test document. " * 100,
        "source": "sample.txt",
        "page": 1,
    }]

    chunks = chunk_documents(
        documents,
        chunk_size=200,
        chunk_overlap=30,
    )

    assert chunks
    assert all(chunk["source"] == "sample.txt" for chunk in chunks)
    assert all(chunk["page"] == 1 for chunk in chunks)
    assert all(chunk["text"] for chunk in chunks)
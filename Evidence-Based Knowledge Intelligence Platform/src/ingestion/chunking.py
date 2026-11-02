from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: list[dict],
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[dict]:

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be non-negative and smaller than chunk_size"
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )

    chunks = []

    for document in documents:
        pieces = splitter.create_documents(
            texts=[document["text"]],
            metadatas=[{
                "source": document["source"],
                "page": document["page"],
            }],
        )

        for piece in pieces:
            chunks.append({
                "text": piece.page_content,
                "source": piece.metadata["source"],
                "page": int(piece.metadata["page"]),
                "start_index": int(
                    piece.metadata.get("start_index", 0)
                ),
            })

    return chunks
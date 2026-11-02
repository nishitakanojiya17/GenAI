from src.config import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    RAW_DATA_DIR,
)
from src.ingestion.chunking import chunk_documents
from src.ingestion.loader import load_documents
from src.retrieval.embedder import Embedder
from src.retrieval.vector_store import VectorStore


def main():
    print("Loading source documents...")
    documents = load_documents(RAW_DATA_DIR)

    if not documents:
        print(f"No PDF or TXT files found in {RAW_DATA_DIR}")
        return

    print(f"Loaded {len(documents)} pages/files.")

    print("Splitting documents into chunks...")
    chunks = chunk_documents(
        documents,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    if not chunks:
        print("No text chunks were created.")
        return

    print(f"Created {len(chunks)} chunks.")

    print("Loading embedding model...")
    embedder = Embedder()

    print("Generating embeddings...")
    embeddings = embedder.embed_documents(
        [chunk["text"] for chunk in chunks]
    )

    print("Writing chunks to ChromaDB...")
    vector_store = VectorStore()
    vector_store.add_chunks(chunks, embeddings)

    print(
        "Ingestion complete. "
        f"ChromaDB now contains {vector_store.collection.count()} chunks."
    )


if __name__ == "__main__":
    main()
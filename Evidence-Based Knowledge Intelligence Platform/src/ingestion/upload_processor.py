
from pathlib import Path

from src.config import CHUNK_OVERLAP, CHUNK_SIZE
from src.ingestion.loader import load_documents
from src.ingestion.chunking import chunk_documents
from src.retrieval.embedder import Embedder
from src.retrieval.vector_store import VectorStore


UPLOAD_DIR = Path("data/uploads")


def process_uploaded_file(filename: str, file_bytes: bytes):
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = Path(filename).name
    suffix = Path(safe_name).suffix.lower()

    if suffix not in {".pdf", ".txt"}:
        raise ValueError("Only PDF and TXT files are supported.")

    if not file_bytes:
        raise ValueError("The uploaded file is empty.")

    file_path = UPLOAD_DIR / safe_name

    if file_path.exists():
        raise FileExistsError(
            f"{safe_name} already exists. Rename the file before uploading it again."
        )

    file_path.write_bytes(file_bytes)

    try:
        documents = load_documents(UPLOAD_DIR)

        # Process only the newly uploaded file.
        documents = [
            doc for doc in documents
            if doc["source"] == safe_name
        ]

        if not documents:
            raise ValueError(
                "No readable text found. The PDF may be scanned or empty."
            )

        chunks = chunk_documents(
            documents,
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        if not chunks:
            raise ValueError("No text chunks were created.")

        embedder = Embedder()
        embeddings = embedder.embed_documents(
            [chunk["text"] for chunk in chunks]
        )

        vector_store = VectorStore()
        vector_store.add_chunks(chunks, embeddings)

        return len(documents), len(chunks), vector_store.collection.count()

    except Exception:
        file_path.unlink(missing_ok=True)
        raise

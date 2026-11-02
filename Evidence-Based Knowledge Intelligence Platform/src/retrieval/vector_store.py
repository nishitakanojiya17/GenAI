
import hashlib
import chromadb

from src.config import CHROMA_COLLECTION, CHROMA_PATH


class VectorStore:

    def __init__(self):
        CHROMA_PATH.mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(CHROMA_PATH)
        )

        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )

    @staticmethod
    def create_id(chunk: dict) -> str:
        content = (
            f"{chunk['source']}|"
            f"{chunk['page']}|"
            f"{chunk['start_index']}|"
            f"{chunk['text']}"
        )

        return hashlib.sha256(
            content.encode("utf-8")
        ).hexdigest()

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
        batch_size: int = 100,
    ) -> None:

        for start in range(0, len(chunks), batch_size):

            chunk_batch = chunks[start:start + batch_size]
            embedding_batch = embeddings[start:start + batch_size]

            self.collection.upsert(
                ids=[
                    self.create_id(chunk)
                    for chunk in chunk_batch
                ],
                documents=[
                    chunk["text"]
                    for chunk in chunk_batch
                ],
                embeddings=embedding_batch,
                metadatas=[
                    {
                        "source": chunk["source"],
                        "page": int(chunk["page"]),
                        "start_index": int(chunk["start_index"]),
                    }
                    for chunk in chunk_batch
                ],
            )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        source_filter: str | None = None,
    ) -> list[dict]:

        count = self.collection.count()

        if count == 0:
            return []

        query_arguments = {
            "query_embeddings": [query_embedding],
            "n_results": min(top_k, count),
            "include": [
                "documents",
                "metadatas",
                "distances",
            ],
        }

        if source_filter:
            query_arguments["where"] = {
                "source": source_filter
            }

        results = self.collection.query(
            **query_arguments
        )

        matches = []

        if not results["documents"] or not results["documents"][0]:
            return []

        for index, text in enumerate(results["documents"][0]):

            distance = results["distances"][0][index]

            # ChromaDB cosine distance is generally in [0, 2].
            # Convert it to a normalized similarity indicator.
            relevance_score = max(
                0.0,
                min(100.0, (1.0 - distance) * 100.0)
            )

            matches.append({
                "text": text,
                "metadata": results["metadatas"][0][index],
                "distance": distance,
                "relevance_score": relevance_score,
                "rank": index + 1,
            })

        return matches

    def delete_document(self, source: str) -> int:

        if not source or not source.strip():
            raise ValueError(
                "Document source cannot be empty."
            )

        existing = self.collection.get(
            where={"source": source},
            include=[],
        )

        ids = existing["ids"]

        if not ids:
            return 0

        self.collection.delete(ids=ids)

        return len(ids)

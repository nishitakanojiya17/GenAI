
from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.model = CrossEncoder(model_name)

    def rerank(self, question, retrieved_results, top_k=5):
        if not retrieved_results:
            return []

        pairs = [
            (question, result.get("text", ""))
            for result in retrieved_results
        ]

        scores = self.model.predict(pairs)

        reranked_results = []

        for result, score in zip(retrieved_results, scores):
            updated_result = result.copy()
            updated_result["rerank_score"] = float(score)

            # Preserve source information for traceability.
            updated_result["rerank_model"] = (
                "cross-encoder/ms-marco-MiniLM-L-6-v2"
            )

            reranked_results.append(updated_result)

        reranked_results.sort(
            key=lambda item: item["rerank_score"],
            reverse=True
        )

        return reranked_results[:top_k]

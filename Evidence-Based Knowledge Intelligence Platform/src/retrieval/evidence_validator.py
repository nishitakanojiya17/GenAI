
from typing import Any, Dict, List, Tuple


class EvidenceValidator:
    def __init__(self, min_rerank_score: float = -1.0):
        self.min_rerank_score = float(min_rerank_score)

    def validate(
        self,
        reranked_results: List[Dict[str, Any]],
        min_rerank_score: float = None,
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:

        threshold = (
            self.min_rerank_score
            if min_rerank_score is None
            else float(min_rerank_score)
        )

        accepted = []
        rejected = []

        for result in reranked_results or []:
            item = result.copy()

            try:
                score = float(item["rerank_score"])
            except (KeyError, TypeError, ValueError):
                item["validation_passed"] = False
                item["validation_reason"] = (
                    "Missing or invalid reranker score"
                )
                rejected.append(item)
                continue

            item["validation_threshold"] = threshold

            if score >= threshold:
                item["validation_passed"] = True
                item["validation_reason"] = (
                    "Accepted: reranker score meets the threshold"
                )
                accepted.append(item)
            else:
                item["validation_passed"] = False
                item["validation_reason"] = (
                    f"Reranker score {score:.4f} is below "
                    f"the threshold {threshold:.4f}"
                )
                rejected.append(item)

        return accepted, rejected

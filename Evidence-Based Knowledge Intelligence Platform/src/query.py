
from src.config import TOP_K
from src.retrieval.embedder import Embedder
from src.retrieval.vector_store import VectorStore
from src.generation.answerer import AnswerGenerator


def main():
    embedder = Embedder()
    vector_store = VectorStore()
    answer_generator = AnswerGenerator()

    print("Evidence-Based Knowledge Assistant ready.")
    print("Type 'exit' to quit.")

    while True:
        question = input("\nQuestion: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            query_embedding = embedder.embed_query(question)

            results = vector_store.search(
                query_embedding,
                top_k=TOP_K,
            )

            if not results:
                print("No indexed chunks found. Run ingestion first.")
                continue

            print("\nGenerating evidence-based answer...\n")

            answer = answer_generator.generate_answer(
                question,
                results,
            )

            print("ANSWER")
            print("=" * 80)
            print(answer)
            print("=" * 80)

            print("\nSOURCES USED")
            for rank, result in enumerate(results, start=1):
                metadata = result["metadata"]
                print(
                    f"[{rank}] {metadata.get('source', 'Unknown')} "
                    f"(page {metadata.get('page', 'Unknown')})"
                )

        except requests.exceptions.RequestException as error:
            print(f"Ollama connection error: {error}")
        except Exception as error:
            print(f"An error occurred: {error}")


if __name__ == "__main__":
    import requests
    main()

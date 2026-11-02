
import requests


class AnswerGenerator:

    def __init__(
        self,
        model="qwen2.5:3b",
        timeout=180,
    ):
        self.model = model
        self.timeout = timeout
        self.api_url = "http://localhost:11434/api/generate"

    def generate_answer(self, question, retrieved_results):

        if not retrieved_results:
            return (
                "I could not find relevant evidence in the selected "
                "documents. Please try another question."
            )

        # Prepare evidence and source references.
        evidence_parts = []

        for rank, result in enumerate(retrieved_results, start=1):

            metadata = result.get("metadata", {})

            source = metadata.get("source", "Unknown source")
            page = metadata.get("page", "Unknown page")
            content = result.get("text", "").strip()

            if not content:
                continue

            evidence_parts.append(
                f"""
[EVIDENCE {rank}]
Source: {source}
Page: {page}

Content:
{content}
"""
            )

        if not evidence_parts:
            return "The retrieved passages contain no readable text."

        evidence = "\n\n".join(evidence_parts)

        # Evidence-focused prompt.
        prompt = f"""
You are an academic knowledge assistant.

Answer the user's question using the supplied document evidence.

IMPORTANT INSTRUCTIONS:

1. Read ALL evidence passages before answering.
2. Identify the passages that directly relate to the question.
3. Combine relevant information from different passages when useful.
4. Give a direct answer. Do not refuse merely because the evidence
   does not contain every possible detail.
5. Explain all relevant information that IS supported by the evidence.
6. Do not introduce facts from your own general knowledge.
7. Do not invent definitions, examples, statistics, or claims.
8. If only part of the question is supported, answer that part and
   clearly identify what information is missing.
9. If none of the passages support an answer, say:
   "The retrieved evidence does not contain enough information
   to answer this question."
10. Cite factual claims using the exact evidence source and page.

CITATION FORMAT:

[EVIDENCE 1: filename, Page 1]

ANSWER FORMAT:

- Begin with a direct explanation.
- Use short paragraphs or bullet points where appropriate.
- Include relevant details from the evidence.
- Add citations next to the claims they support.
- Do not include unsupported information.

USER QUESTION:
{question}

DOCUMENT EVIDENCE:
{evidence}

Now provide the best answer supported by the evidence.
"""

        try:

            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "num_ctx": 8192,
                        "num_predict": 700,
                    },
                },
                timeout=self.timeout,
            )

            response.raise_for_status()

            response_data = response.json()

            answer = response_data.get("response", "").strip()

            if not answer:
                return (
                    "The AI model returned an empty response. "
                    "Please try again."
                )

            return answer

        except requests.exceptions.ConnectionError:

            return (
                "Could not connect to Ollama. "
                "Please ensure Ollama is running on your computer."
            )

        except requests.exceptions.Timeout:

            return (
                "The AI model took too long to respond. "
                "Please try again."
            )

        except requests.exceptions.RequestException as error:

            return (
                f"An error occurred while generating the answer: {error}"
            )

        except (ValueError, KeyError, TypeError):

            return (
                "Could not read the response from Ollama. "
                "Please try again."
            )

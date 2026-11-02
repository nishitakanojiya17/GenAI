# Evidence-Based Knowledge Intelligence Platform

## 1. Project Overview

The **Evidence-Based Knowledge Intelligence Platform** is an AI-powered application designed to extract, search, validate, and generate answers from uploaded documents.

The platform uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from documents and generate answers using a locally running Large Language Model (LLM).

It also uses semantic search, Cross-Encoder reranking, and evidence validation to improve the relevance of retrieved information and make answers easier to verify.

The application provides an interactive Streamlit dashboard where users can upload documents, ask questions, review supporting evidence, and download generated answers as PDF reports.

## 2. Project Objectives

- Develop an intelligent document question-answering system.
- Extract and process information from PDF and TXT documents.
- Convert document content into smaller text chunks.
- Generate vector embeddings for semantic search.
- Store and retrieve document embeddings using ChromaDB.
- Improve retrieval relevance using Cross-Encoder reranking.
- Validate retrieved evidence before answer generation.
- Generate answers using a locally hosted language model.
- Provide a user-friendly dashboard.
- Export generated answers and supporting evidence as PDF reports.

## 3. Technologies Used

| Technology            | Purpose                   |
| --------------------- | ------------------------- |
| Python                | Core programming language |
| Streamlit             | Web application interface |
| ChromaDB              | Vector database           |
| Hugging Face          | Text embedding models     |
| Sentence Transformers | Cross-Encoder reranking   |
| Ollama                | Local LLM execution       |
| Qwen 2.5:3B           | Answer generation model   |
| ReportLab             | PDF report generation     |
| PyPDF                 | PDF text extraction       |

## 4. System Architecture

The platform follows a Retrieval-Augmented Generation (RAG) architecture.

### Document Processing Pipeline

1. User uploads a PDF or TXT document.
2. The document loader extracts its text.
3. The extracted text is divided into smaller chunks.
4. The embedding model converts chunks into vector representations.
5. ChromaDB stores the chunks and their embeddings.

### Question Answering Pipeline

1. User enters a question through the Streamlit dashboard.
2. The question is converted into an embedding.
3. ChromaDB retrieves semantically relevant document chunks.
4. The Cross-Encoder reranker scores and sorts retrieved passages.
5. The Evidence Validator accepts or rejects passages according to the configured score threshold.
6. Accepted evidence is passed to the Ollama language model.
7. The language model generates an answer based on the supplied evidence.
8. The application displays the answer and its supporting sources.
9. The user can download the result as a PDF report.

## 5. Key Features

### Document Management

- Upload PDF and TXT files.
- Extract document text.
- Process and store document chunks.
- View uploaded documents.
- Delete documents from the knowledge base.

### Semantic Search

- Search documents based on meaning rather than exact keyword matching.
- Retrieve relevant passages using vector similarity.

### Cross-Encoder Reranking

- Re-evaluate retrieved passages against the user's question.
- Assign reranker scores.
- Sort passages by relevance.

### Evidence Validation

- Apply a configurable minimum reranker score.
- Separate accepted and rejected passages.
- Display supporting evidence for generated answers.

### AI Answer Generation

- Use the Qwen 2.5:3B model through Ollama.
- Generate answers using retrieved evidence.
- Include source references in generated answers.

### Interactive Dashboard

- Upload and manage documents.
- Ask questions.
- View generated answers.
- Inspect evidence and retrieval analytics.

### PDF Report Generation

- Export generated answers.
- Include the original question.
- Include accepted evidence.
- Display source filenames, page numbers, and reranker scores.

## 6. Installation and Setup

### Prerequisites

Install the following:

- Python
- Ollama
- Git (optional)

### Step 1: Clone or Open the Project

Open the project directory:

```powershell
cd "D:\GenAI\Evidence-Based Knowledge Intelligence Platform"
```

### Step 2: Activate the Virtual Environment

```powershell
.venv\Scripts\activate
```

If the virtual environment has not been created:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Install Dependencies

If the project contains a `requirements.txt` file:

```powershell
pip install -r requirements.txt
```

Otherwise, install the dependencies listed in the project setup.

### Step 4: Install and Run the Ollama Model

Pull the model:

```powershell
ollama pull qwen2.5:3b
```

Ensure Ollama is running and the model is available:

```powershell
ollama list
```

### Step 5: Run the Application

From the main project directory, execute:

```powershell
streamlit run app.py
```

The application will open in your web browser.

## 7. How to Use the Application

1. Open the application dashboard.
2. Upload a PDF or TXT document.
3. Wait for document processing to complete.
4. Select the document or search across the knowledge base.
5. Enter a question.
6. Click the Generate Answer button.
7. Review the generated answer.
8. Inspect accepted and rejected evidence.
9. Download the answer as a PDF report.

## 8. Project Structure

The main project components are organized as follows:

```text
Evidence-Based Knowledge Intelligence Platform/
│
├── app.py
├── README.md
│
├── src/
│   ├── config.py
│   ├── ingest.py
│   ├── query.py
│   │
│   ├── ingestion/
│   │   ├── loader.py
│   │   ├── chunking.py
│   │   └── upload_processor.py
│   │
│   ├── retrieval/
│   │   ├── embedder.py
│   │   ├── vector_store.py
│   │   ├── reranker.py
│   │   └── evidence_validator.py
│   │
│   └── generation/
│       ├── __init__.py
│       └── answerer.py
│
├── data/
│   └── uploads/
│
└── .venv/
```

_Note: This is the logical project structure based on the implemented modules. Your local directory may contain additional files and folders._

## 9. Advantages

- Supports document-based question answering.
- Uses semantic retrieval instead of relying only on keywords.
- Improves passage ranking using a Cross-Encoder.
- Provides a separate evidence validation stage.
- Runs the answer generation model locally through Ollama.
- Displays source information to support answer verification.
- Provides an interactive and easy-to-use interface.
- Supports PDF report export.

## 10. Limitations

- Answer quality depends on the content and quality of uploaded documents.
- Scanned PDFs without extractable text may not be processed successfully.
- Reranker scores are model-specific and are not probabilities of factual correctness.
- Evidence validation does not guarantee that every accepted passage is factually correct.
- The language model may occasionally produce unsupported interpretations, so generated answers should be checked against their cited evidence.
- Local answer generation depends on available system resources and Ollama model availability.

## 11. Future Enhancements

Possible future improvements include:

- Answer history and conversation management.
- Support for additional document formats.
- Advanced citation verification.
- Improved retrieval evaluation.
- User authentication and access control.
- Multilingual document support.
- More detailed performance analytics.

## 12. Conclusion

The Evidence-Based Knowledge Intelligence Platform demonstrates how Retrieval-Augmented Generation, semantic search, vector databases, reranking, evidence validation, and local language models can work together to build an intelligent document question-answering system.

The application provides a complete workflow from document upload and processing to evidence retrieval, answer generation, and PDF report export.

It aims to make document-based information retrieval more efficient, transparent, and verifiable.

---

**Project Name:** Evidence-Based Knowledge Intelligence Platform  
**Primary Language:** Python  
**Application Framework:** Streamlit  
**Vector Database:** ChromaDB  
**Language Model:** Qwen 2.5:3B via Ollama

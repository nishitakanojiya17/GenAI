
from pathlib import Path
from collections import Counter

import streamlit as st

from src.config import TOP_K
from src.retrieval.embedder import Embedder
from src.retrieval.vector_store import VectorStore
from src.retrieval.reranker import Reranker
from src.retrieval.evidence_validator import EvidenceValidator
from src.generation.answerer import AnswerGenerator
from src.ingestion.upload_processor import process_uploaded_file
from io import BytesIO
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)


def create_pdf_report(question, answer, accepted_results):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        textColor=colors.HexColor("#172554"),
        fontSize=19,
        leading=25,
        spaceAfter=15,
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#4338CA"),
        fontSize=13,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=14,
        spaceAfter=8,
    )

    story = []

    story.append(Paragraph(
        "Evidence-Based Knowledge Intelligence Platform",
        title_style,
    ))

    story.append(Paragraph(
        "Evidence-Based Answer Report",
        heading_style,
    ))

    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
        body_style,
    ))

    story.append(HRFlowable(
        width="100%",
        color=colors.HexColor("#CBD5E1"),
    ))

    story.append(Paragraph("Original Question", heading_style))
    story.append(Paragraph(escape(question), body_style))

    story.append(Paragraph("Generated Answer", heading_style))

    answer_html = escape(answer or "No answer was generated.")
    answer_html = answer_html.replace("\n", "<br/>")

    story.append(Paragraph(answer_html, body_style))

    story.append(Paragraph("Accepted Evidence", heading_style))

    for index, result in enumerate(accepted_results, start=1):
        metadata = result.get("metadata", {})

        source = escape(str(metadata.get("source", "Unknown")))
        page = escape(str(metadata.get("page", "Unknown")))
        evidence_text = escape(str(result.get("text", "")))
        evidence_text = evidence_text.replace("\n", "<br/>")

        story.append(Paragraph(
            f"<b>Evidence {index}</b>",
            body_style,
        ))

        story.append(Paragraph(
            f"<b>Source:</b> {source}<br/>"
            f"<b>Page:</b> {page}<br/>"
            f"<b>Reranker Score:</b> "
            f"{result.get('rerank_score', 0):.4f}",
            body_style,
        ))

        story.append(Paragraph(evidence_text, body_style))
        story.append(Spacer(1, 8))

    doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()


UPLOAD_DIR = Path("data/uploads")

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Evidence-Based Knowledge Intelligence Platform",
    page_icon="📚",
    layout="wide",
)

# --------------------------------------------------
# PROFESSIONAL DASHBOARD STYLING
# --------------------------------------------------


# --------------------------------------------------
# Professional dashboard styling
# --------------------------------------------------

st.markdown("""
<style>

/* Main page background */
.stApp {
    background-color: #F3F6FC;
    color: #24324B;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Main title */
h1 {
    color: #FFFFFF !important;
    font-weight: 800 !important;
}

/* Section headings */
h2, h3,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3 {
    color: #172554 !important;
    font-weight: 750 !important;
}

/* Hero banner */
.hero-banner {
    background: linear-gradient(120deg, #172554, #4338CA);
    padding: 35px;
    border-radius: 18px;
    margin-bottom: 30px;
}

.hero-banner h1 {
    color: #FFFFFF !important;
    font-size: 2.5rem;
}

.hero-banner p {
    color: #E0E7FF !important;
    font-size: 1.1rem;
}

/* Normal text and labels */
p, label, .stMarkdown,
[data-testid="stWidgetLabel"] {
    color: #334155;
}

/* Metric cards */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE4F2;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 3px 10px rgba(30, 41, 59, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #64748B !important;
}

[data-testid="stMetricValue"] {
    color: #1D4ED8 !important;
    font-weight: 800 !important;
}

/* Input fields */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #FFFFFF !important;
    color: #172554 !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 8px !important;
}

/* Dropdown */
.stSelectbox div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #172554 !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #FFFFFF;
    border: 1px dashed #94A3B8;
    padding: 18px;
    border-radius: 12px;
}

/* Buttons */
.stButton > button {
    background-color: #4338CA;
    color: #FFFFFF !important;
    border: none;
    border-radius: 9px;
    font-weight: 650;
    min-height: 42px;
}

.stButton > button:hover {
    background-color: #312E81;
    color: #FFFFFF !important;
    border: none;
}

/* Tables */
[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE4F2;
    border-radius: 10px;
}

/* Expanders */
[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid #DCE4F2;
    border-radius: 12px;
}

/* Slider labels and other captions */
.stCaption, small {
    color: #64748B !important;
}

/* Dividers */
hr {
    border-color: #DCE4F2;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">
    <h1>📚 Evidence-Based Knowledge Intelligence Platform</h1>
    <p>
        Intelligent document search, evidence validation,
        and AI-powered answer generation.
    </p>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# CACHED COMPONENTS
# --------------------------------------------------

@st.cache_resource
def get_embedder():
    return Embedder()


@st.cache_resource
def get_vector_store():
    return VectorStore()


@st.cache_resource
def get_answer_generator():
    return AnswerGenerator()


@st.cache_resource
def get_reranker():
    return Reranker()


@st.cache_resource
def get_evidence_validator():
    return EvidenceValidator(min_rerank_score=-1.0)


embedder = get_embedder()
vector_store = get_vector_store()
answer_generator = get_answer_generator()
reranker = get_reranker()
evidence_validator = get_evidence_validator()


# --------------------------------------------------
# DOCUMENT UTILITIES
# --------------------------------------------------

def get_uploaded_documents():
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    return sorted(
        [
            path for path in UPLOAD_DIR.iterdir()
            if path.is_file()
            and path.suffix.lower() in {".pdf", ".txt"}
        ],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def get_document_statistics():
    result = vector_store.collection.get(
        include=["metadatas"]
    )

    metadata_list = result.get("metadatas") or []
    chunk_counts = Counter()

    for metadata in metadata_list:
        if metadata:
            source = metadata.get("source", "Unknown")
            chunk_counts[source] += 1

    return chunk_counts, vector_store.collection.count()


# --------------------------------------------------
# DASHBOARD OVERVIEW
# --------------------------------------------------

st.header("📊 Knowledge Base Dashboard")

documents = get_uploaded_documents()
chunk_counts, total_chunks = get_document_statistics()

total_documents = len(documents)

total_storage = sum(
    document.stat().st_size
    for document in documents
)

storage_mb = total_storage / (1024 * 1024)

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Total Documents",
    total_documents,
    help="Number of uploaded PDF and TXT documents."
)

metric2.metric(
    "Total Chunks",
    total_chunks,
    help="Number of passages stored in ChromaDB."
)

metric3.metric(
    "Storage Used",
    f"{storage_mb:.2f} MB"
)

metric4.metric(
    "Average Chunks / Document",
    f"{total_chunks / total_documents:.1f}"
    if total_documents else "0"
)

st.divider()


# --------------------------------------------------
# DOCUMENT STATISTICS
# --------------------------------------------------

st.header("📄 Document Statistics")

if documents:
    dashboard_rows = []

    for document in documents:
        dashboard_rows.append({
            "Document": document.name,
            "Size (KB)": round(
                document.stat().st_size / 1024, 2
            ),
            "Chunks": chunk_counts.get(document.name, 0),
        })

    st.dataframe(
        dashboard_rows,
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("No uploaded documents are available yet.")

st.divider()


# --------------------------------------------------
# UPLOAD DOCUMENTS
# --------------------------------------------------

st.header("📤 Upload Documents")

st.caption(
    "Add PDF or TXT files to your searchable knowledge base."
)

uploaded_file = st.file_uploader(
    "Choose a PDF or TXT file",
    type=["pdf", "txt"],
)

if uploaded_file is not None:

    st.write(f"Selected file: **{uploaded_file.name}**")

    if st.button(
        "Upload and Process Document",
        type="primary",
    ):
        try:
            with st.spinner(
                "Processing document and creating embeddings..."
            ):
                page_count, chunk_count, collection_count = (
                    process_uploaded_file(
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                    )
                )

            st.success(
                f"Successfully processed {uploaded_file.name}!"
            )

            result1, result2, result3 = st.columns(3)

            result1.metric("Pages Processed", page_count)
            result2.metric("Chunks Created", chunk_count)
            result3.metric("Knowledge Base Chunks", collection_count)

            st.rerun()

        except Exception as error:
            st.error(f"Upload failed: {error}")

st.divider()


# --------------------------------------------------
# DOCUMENT MANAGEMENT
# --------------------------------------------------

st.header("🗂️ Document Management")

documents = get_uploaded_documents()

if documents:

    st.write(
        f"Total uploaded documents: **{len(documents)}**"
    )

    for document in documents:

        file_size = document.stat().st_size / 1024

        with st.expander(f"📄 {document.name}"):

            st.write(f"File size: {file_size:.2f} KB")

            st.write(
                f"Stored chunks: "
                f"{chunk_counts.get(document.name, 0)}"
            )

            if st.button(
                f"Delete {document.name}",
                key=f"delete_{document.name}",
            ):
                st.session_state["pending_delete"] = (
                    document.name
                )

    pending_delete = st.session_state.get(
        "pending_delete"
    )

    if pending_delete:

        st.warning(
            f"Are you sure you want to permanently delete "
            f"**{pending_delete}** and its stored chunks?"
        )

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:

            if st.button(
                "Yes, permanently delete",
                type="primary",
            ):
                try:
                    if Path(pending_delete).name != pending_delete:
                        raise ValueError("Invalid document path.")

                    file_path = UPLOAD_DIR / pending_delete

                    if not file_path.is_file():
                        raise FileNotFoundError(
                            "Document file not found."
                        )

                    with st.spinner(
                        "Deleting document and stored chunks..."
                    ):

                        deleted_chunks = (
                            vector_store.delete_document(
                                pending_delete
                            )
                        )

                        file_path.unlink()

                    del st.session_state["pending_delete"]

                    st.success(
                        f"Deleted {pending_delete} and "
                        f"{deleted_chunks} stored chunks."
                    )

                    st.rerun()

                except Exception as error:
                    st.error(f"Deletion failed: {error}")

        with cancel_col:

            if st.button("Cancel deletion"):
                del st.session_state["pending_delete"]
                st.rerun()

else:
    st.info("No uploaded documents to manage.")

st.divider()


# --------------------------------------------------
# ASK YOUR KNOWLEDGE BASE
# --------------------------------------------------

st.header("💬 Ask Your Knowledge Base")

st.caption(
    "Ask questions and receive answers grounded in your documents."
)

documents = get_uploaded_documents()

document_options = ["All Documents"] + [
    document.name for document in documents
]

selected_document = st.selectbox(
    "Choose a document to search",
    document_options,
)

question = st.text_area(
    "Enter your question:",
    placeholder=(
        "Example: Explain Feature Detection Methods."
    ),
    height=110,
)

minimum_relevance = st.slider(
    "Minimum relevance indicator",
    min_value=0,
    max_value=100,
    value=35,
    step=5,
)

minimum_reranker_score = st.number_input(
    "Minimum reranker score for evidence acceptance",
    min_value=-20.0,
    max_value=20.0,
    value=-1.0,
    step=0.5,
    help=(
        "Passages with reranker scores greater than "
        "or equal to this value are eligible for acceptance."
    ),
)

st.caption(
    "Relevance indicators are derived from ChromaDB cosine "
    "distance. Cross-Encoder scores are model-specific ranking "
    "outputs. Neither is a probability or direct measure of "
    "factual accuracy."
)


# --------------------------------------------------
# GENERATE ANSWER
# --------------------------------------------------

if st.button(
    "🚀 Generate Answer",
    type="primary",
    use_container_width=True,
):

    if not question.strip():

        st.warning("Please enter a question.")

    elif total_chunks == 0:

        st.warning(
            "Please upload and process a document first."
        )

    else:

        try:

            with st.spinner(
                "Retrieving and validating evidence..."
            ):

                query_embedding = embedder.embed_query(
                    question
                )

                source_filter = (
                    None
                    if selected_document == "All Documents"
                    else selected_document
                )

                # Stage 1: Retrieval
                candidate_results = vector_store.search(
                    query_embedding=query_embedding,
                    top_k=max(TOP_K * 2, TOP_K),
                    source_filter=source_filter,
                )

                # Stage 2: Relevance filtering
                filtered_results = [
                    result
                    for result in candidate_results
                    if result.get("relevance_score", 0)
                    >= minimum_relevance
                ]

                # Stage 3: Reranking
                reranked_results = reranker.rerank(
                    question=question,
                    retrieved_results=filtered_results,
                    top_k=TOP_K,
                )

                # Stage 4: Evidence validation
                accepted_results, rejected_results = (
                    evidence_validator.validate(
                        reranked_results,
                        min_rerank_score=minimum_reranker_score,
                    )
                )

                for position, result in enumerate(
                    accepted_results,
                    start=1,
                ):
                    result["rerank_rank"] = position

            # Save retrieval results
            st.session_state["last_question"] = question
            st.session_state["last_candidates"] = candidate_results
            st.session_state["last_filtered"] = filtered_results
            st.session_state["last_accepted"] = accepted_results
            st.session_state["last_rejected"] = rejected_results
            st.session_state["last_threshold"] = (
                minimum_reranker_score
            )

            # Stage 5: Answer generation
            if accepted_results:

                with st.spinner(
                    "Generating evidence-based answer..."
                ):

                    answer = answer_generator.generate_answer(
                        question,
                        accepted_results,
                    )

                st.session_state["last_answer"] = answer

            else:

                st.session_state["last_answer"] = None

        except Exception as error:

            st.error(
                f"Could not generate the answer: {error}"
            )


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

if "last_question" in st.session_state:

    candidate_results = st.session_state["last_candidates"]
    filtered_results = st.session_state["last_filtered"]
    accepted_results = st.session_state["last_accepted"]
    rejected_results = st.session_state["last_rejected"]

    actual_threshold = st.session_state["last_threshold"]
    answer = st.session_state["last_answer"]

    st.divider()

    st.header("📊 Evidence Validation Analytics")

    metric_a, metric_b, metric_c, metric_d = st.columns(4)

    metric_a.metric(
        "Retrieved Candidates",
        len(candidate_results),
    )

    metric_b.metric(
        "After Relevance Filtering",
        len(filtered_results),
    )

    metric_c.metric(
        "Accepted Evidence",
        len(accepted_results),
    )

    metric_d.metric(
        "Rejected Evidence",
        len(rejected_results),
    )

    st.caption(
        f"Evidence acceptance threshold: "
        f"{actual_threshold:.2f}"
    )

    if accepted_results:

        relevance_scores = [
            result.get("relevance_score", 0)
            for result in accepted_results
        ]

        rerank_scores = [
            result.get("rerank_score", 0)
            for result in accepted_results
        ]

        metric_e, metric_f = st.columns(2)

        metric_e.metric(
            "Average accepted relevance indicator",
            f"{sum(relevance_scores) / len(relevance_scores):.2f}%",
        )

        metric_f.metric(
            "Average accepted reranker score",
            f"{sum(rerank_scores) / len(rerank_scores):.4f}",
        )

    # --------------------------------------------------
    # GENERATED ANSWER
    # --------------------------------------------------

    st.header("🧠 Generated Answer")

    if answer:

        with st.container(border=True):
            st.markdown(answer)

    else:

        st.warning(
            "No passages passed evidence validation. "
            "An answer was not generated."
        )

    st.divider()

    # --------------------------------------------------
    # ACCEPTED EVIDENCE
    # --------------------------------------------------

    st.header("✅ Accepted Evidence")

    if accepted_results:

        with st.expander(
            "View validated source passages",
            expanded=True,
        ):

            for index, result in enumerate(
                accepted_results,
                start=1,
            ):

                metadata = result.get("metadata", {})

                st.subheader(
                    f"Accepted Evidence #{index}"
                )

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Relevance Indicator",
                    f"{result.get('relevance_score', 0):.2f}%",
                )

                col2.metric(
                    "Cosine Distance",
                    f"{result.get('distance', 0):.4f}",
                )

                col3.metric(
                    "Reranker Score",
                    f"{result.get('rerank_score', 0):.4f}",
                )

                st.caption(
                    f"Source: {metadata.get('source', 'Unknown')} "
                    f"| Page: {metadata.get('page', 'Unknown')}"
                )

                st.write(result.get("text", ""))

                st.divider()

    else:

        st.info("No evidence passages were accepted.")

    # --------------------------------------------------
    # REJECTED EVIDENCE
    # --------------------------------------------------

    st.header("❌ Rejected Evidence")

    with st.expander(
        "View rejected passages and validation reasons",
        expanded=False,
    ):

        if not rejected_results:

            st.info("No passages were rejected.")

        else:

            for index, result in enumerate(
                rejected_results,
                start=1,
            ):

                metadata = result.get("metadata", {})

                st.subheader(
                    f"Rejected Evidence #{index}"
                )

                st.write(
                    f"Source: {metadata.get('source', 'Unknown')} "
                    f"| Page: {metadata.get('page', 'Unknown')}"
                )

                st.write(
                    f"Reranker score: "
                    f"{result.get('rerank_score', 'Unavailable')}"
                )

                st.write(
                    result.get(
                        "validation_reason",
                        "Did not pass evidence validation.",
                    )
                )

                st.write(result.get("text", ""))

                st.divider()

# --------------------------------------------------
# PDF Report Download
# --------------------------------------------------

if "last_question" in st.session_state:

    st.divider()
    st.subheader("📥 Download Your Report")

    if st.session_state.get("last_answer"):

        pdf_file = create_pdf_report(
            question=st.session_state["last_question"],
            answer=st.session_state["last_answer"],
            accepted_results=st.session_state["last_accepted"],
        )

        st.download_button(
            label="📄 Download Answer as PDF",
            data=pdf_file,
            file_name="Evidence_Based_Answer_Report.pdf",
            mime="application/pdf",
            type="primary",
        )

    else:
        st.info(
            "Generate an answer with accepted evidence "
            "before downloading a report."
        )
        
# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Evidence-Based Knowledge Intelligence Platform | "
    "ChromaDB | Hugging Face Embeddings | "
    "Cross-Encoder Reranking | Evidence Validation | Ollama"
)

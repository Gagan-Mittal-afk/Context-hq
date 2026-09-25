import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.ingestion import ingest_pdf
from src.rag import ask
from src.vector_store import list_documents


st.set_page_config(
    page_title="ContextHQ",
    page_icon="C",
    layout="wide",
)


# -------------------------
# Custom styling
# -------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 1rem;
        color: #666666;
        margin-top: 0.2rem;
        margin-bottom: 2rem;
    }

    .document-status {
        padding: 0.6rem 0.8rem;
        border-left: 3px solid #666666;
        margin: 0.8rem 0 1.5rem 0;
        font-size: 0.9rem;
    }

    .source-item {
        padding: 0.35rem 0;
        margin-bottom: 0.2rem;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
        font-size: 0.9rem;
    }

    .empty-state {
        text-align: center;
        padding: 5rem 1rem;
        color: #666666;
    }

    .empty-state h2 {
        margin-bottom: 0.5rem;
    }

    .empty-state p {
        font-size: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# -------------------------
# Session state
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------
# Header
# -------------------------

st.markdown(
    '<div class="main-title">ContextHQ</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'A local document intelligence assistant powered by RAG.'
    '</div>',
    unsafe_allow_html=True
)


# -------------------------
# Sidebar
# -------------------------

st.sidebar.title("Documents")

st.sidebar.caption(
    "Upload a PDF and chat with its contents."
)

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


if uploaded_file:

    st.sidebar.caption(
        f"Selected: {uploaded_file.name}"
    )

    if st.sidebar.button(
        "Process Document",
        use_container_width=True
    ):

        with st.spinner("Processing document..."):

            try:

                result = ingest_pdf(uploaded_file)

                if result["already_exists"]:

                    st.sidebar.warning(
                        "This document has already been processed."
                    )

                else:

                    st.sidebar.success(
                        "Document processed successfully."
                    )

                    st.sidebar.write(
                        f"Pages: {result['pages']}"
                    )

                    st.sidebar.write(
                        f"Chunks: {result['chunks']}"
                    )

                    st.sidebar.write(
                        f"Embedding dimensions: "
                        f"{result['embedding_dimensions']}"
                    )

                st.rerun()

            except Exception as e:

                st.sidebar.error(
                    f"Error: {e}"
                )


# -------------------------
# Document selection
# -------------------------

documents = list_documents()


if documents:

    st.sidebar.divider()

    st.sidebar.subheader("Your Documents")

    document_options = {
        document["source"]: document["document_id"]
        for document in documents
    }

    selected_source = st.sidebar.selectbox(
        "Select document",
        list(document_options.keys())
    )

    selected_document_id = document_options[
        selected_source
    ]

else:

    selected_document_id = None
    selected_source = None

    st.sidebar.info(
        "No documents available."
    )


# -------------------------
# Sidebar controls
# -------------------------

st.sidebar.divider()

if st.sidebar.button(
    "Clear Chat",
    use_container_width=True
):

    st.session_state.messages = []

    st.rerun()


# -------------------------
# Current document status
# -------------------------

if selected_document_id:

    st.markdown(
        f"""
        <div class="document-status">
        Chatting with: <strong>{selected_source}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------
# Empty state
# -------------------------

if not selected_document_id:

    st.markdown(
        """
        <div class="empty-state">

        <h2>Start chatting with your documents</h2>

        <p>
        Upload and process a PDF from the sidebar to begin.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------
# Display chat history
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:

                st.markdown("#### Sources")

                for source in sources:

                    st.markdown(
                        f"""
                        <div class="source-item">
                        {source['source']} — Page {source['page']}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# -------------------------
# Chat input
# -------------------------

question = st.chat_input(
    "Ask a question about your document..."
)


if question:

    if not selected_document_id:

        st.warning(
            "Please upload and process a document first."
        )

    else:

        st.session_state.messages.append({
            "role": "user",
            "content": question,
        })

        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:

                    result = ask(
                        question,
                        document_id=selected_document_id,
                        chat_history=st.session_state.messages
                    )

                    answer = result["answer"]
                    sources = result["sources"]

                    st.write(answer)

                    if sources:

                        st.markdown("#### Sources")

                        for source in sources:

                            st.markdown(
                                f"""
                                <div class="source-item">
                                {source['source']} — Page {source['page']}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    })

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )
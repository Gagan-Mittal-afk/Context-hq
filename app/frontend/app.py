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
# Session state
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------------
# Header
# -------------------------

st.title("ContextHQ")
st.caption("Chat with your documents using local AI.")


# -------------------------
# Sidebar
# -------------------------

st.sidebar.header("Documents")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF",
    type=["pdf"],
)


if uploaded_file:

    st.sidebar.info(
        f"Selected: {uploaded_file.name}"
    )

    if st.sidebar.button(
        "Process PDF",
        use_container_width=True
    ):

        with st.spinner("Processing document..."):

            try:
                result = ingest_pdf(uploaded_file)

                if result["already_exists"]:

                    st.sidebar.warning(
                        "This document is already processed."
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

    document_options = {
        document["source"]: document["document_id"]
        for document in documents
    }

    selected_source = st.sidebar.selectbox(
        "Chat with",
        list(document_options.keys())
    )

    selected_document_id = document_options[
        selected_source
    ]

else:

    selected_document_id = None

    st.sidebar.info(
        "Upload a PDF to start chatting."
    )


# -------------------------
# Chat
# -------------------------

st.header("Ask your document")


if selected_document_id:

    st.caption(
        f"Currently chatting with: {selected_source}"
    )


# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:

                st.markdown("### Sources")

                for source in sources:

                    st.write(
                        f"{source['source']} — "
                        f"Page {source['page']}"
                    )


# New question

question = st.chat_input(
    "Ask something about your document..."
)


if question:

    if not selected_document_id:

        st.warning(
            "Please upload and process a PDF first."
        )

    else:

        # Store user message

        st.session_state.messages.append({
            "role": "user",
            "content": question,
        })

        with st.chat_message("user"):
            st.write(question)

        # Generate answer

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

                        st.markdown("### Sources")

                        for source in sources:

                            st.write(
                                f"{source['source']} — "
                                f"Page {source['page']}"
                            )

                    # Store assistant message

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    })

                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )
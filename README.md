# 📚 ContextHQ

> **A local Retrieval-Augmented Generation (RAG) application for intelligent document interaction.**

ContextHQ allows users to upload PDF documents and interact with them using natural-language questions.

It combines **PDF processing, semantic embeddings, vector search, document-aware retrieval, conversational context, and a local LLM** to generate answers grounded in the uploaded documents.

### 🔒 100% Local AI

ContextHQ uses **Ollama + Qwen3:8b** for local LLM inference and **Sentence Transformers** for local embeddings.

**No OpenAI API. No Gemini API. No cloud LLM required.**

---

# ✨ Features

| Feature | Description |
|---|---|
| 📄 **PDF Upload** | Upload and process PDF documents |
| ✂️ **Smart Chunking** | Split documents into smaller retrievable chunks |
| 🧠 **Local Embeddings** | Generate semantic embeddings using Sentence Transformers |
| 🗄️ **Vector Database** | Store and search embeddings using ChromaDB |
| 📚 **Multi-Document Support** | Upload and manage multiple PDFs |
| 🔐 **Document Isolation** | Retrieval is restricted to the selected document |
| 💬 **Conversational RAG** | Ask follow-up questions using conversation history |
| 📌 **Source Attribution** | Display the document and page used for an answer |
| ♻️ **Duplicate Protection** | Prevent the same document from being ingested repeatedly |
| 🤖 **Local LLM** | Run Qwen3:8b locally through Ollama |
| 🖥️ **Interactive UI** | Streamlit-based document chat interface |
| 🧪 **Automated Testing** | Unit and integration tests using pytest |

---

---

# 📸 Demo

## 🖥️ ContextHQ Interface

The ContextHQ interface allows users to upload PDFs, select documents, and interact with them through a conversational chat interface.

![ContextHQ Interface](screenshots/interface.png)

---

## 🧠 RAG in Action

ContextHQ retrieves relevant document chunks and provides the generated answer along with the source pages used for the response.

![ContextHQ RAG Demo](screenshots/rag-demo.png)

# 🧠 What is ContextHQ?

ContextHQ is a **Retrieval-Augmented Generation system** designed to answer questions using information from user-provided documents.

Instead of directly asking an LLM to answer a question, ContextHQ first retrieves the most relevant pieces of information from the uploaded document and then provides those pieces to the LLM as context.

This creates a pipeline where:

> **The document provides the knowledge → the vector database finds the relevant information → the LLM generates the response.**

---

# 🔄 How RAG Works

```text
                         PDF Document
                              |
                              v
                         PDF Loader
                              |
                              v
                           Chunking
                              |
                              v
                       Text Embeddings
                              |
                              v
                          ChromaDB
                              |
                              |
                     User asks a question
                              |
                              v
                       Query Embedding
                              |
                              v
                   Semantic Similarity Search
                              |
                              v
                  Relevant Document Chunks
                              |
                              v
                    Conversation History
                              |
                              v
                       Ollama + Qwen3
                              |
                              v
                       Generated Answer
                              |
                              v
                    Answer + Source Pages
```

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │    Streamlit UI     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    v                               v
             PDF Upload                       User Question
                    │                               │
                    v                               v
              PDF Loader                    Query Embedding
                    │                               │
                    v                               v
                Chunking                    Document Filtering
                    │                               │
                    v                               v
               Embeddings                    ChromaDB Search
                    │                               │
                    v                               v
                ChromaDB                    Relevant Chunks
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    v
                         Conversation History
                                    │
                                    v
                            Ollama / Qwen3
                                    │
                                    v
                              Final Answer
                                    │
                                    v
                           Source Attribution
```

---

# 🛠️ Tech Stack

### 💻 Language

- **Python 3.13**

### 🖥️ Frontend

- **Streamlit**

### 📄 Document Processing

- **pypdf**

### 🧠 Embeddings

- **Sentence Transformers**
- `all-MiniLM-L6-v2`
- **384-dimensional embeddings**

### 🗄️ Vector Database

- **ChromaDB**

### 🤖 Large Language Model

- **Qwen3:8b**

### ⚡ Local Model Runtime

- **Ollama**

### 🧪 Testing

- **pytest**

---

# 📁 Project Structure

```text
ContextHQ/
│
├── app/
│   └── frontend/
│       └── app.py
│
├── src/
│   ├── __init__.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── ingestion.py
│   ├── llm.py
│   ├── pdf_loader.py
│   ├── rag.py
│   └── vector_store.py
│
├── tests/
│   ├── test_chunker.py
│   ├── test_loader.py
│   ├── test_llm.py
│   ├── test_pipeline.py
│   └── test_rag.py
│
├── data/
│   └── Context HQ Test Document.pdf
│
├── .gitignore
├── pytest.ini
├── README.md
└── requirements.txt
```

---

# 🔧 Core Components

## 1. 📄 PDF Loader

**File:** `src/pdf_loader.py`

Responsible for extracting text from uploaded PDF documents.

The loader preserves **page numbers**, allowing retrieved chunks to be associated with their original source page.

---

## 2. ✂️ Chunker

**File:** `src/chunker.py`

Large documents are divided into smaller chunks before embeddings are generated.

Current configuration:

```text
Chunk Size: 500 characters
Overlap:     100 characters
```

### Why overlap?

The overlap helps preserve context between adjacent chunks.

For example:

```text
Chunk 1
[--------------------]

              Chunk 2
              [--------------------]
```

Some information appears in both chunks, reducing the chance of losing context at chunk boundaries.

---

## 3. 🧠 Embeddings

**File:** `src/embeddings.py`

ContextHQ uses:

```text
all-MiniLM-L6-v2
```

to convert text into **384-dimensional vectors**.

These vectors represent the semantic meaning of text.

This allows the system to retrieve conceptually similar content even when the wording isn't identical.

---

## 4. 🗄️ Vector Store

**File:** `src/vector_store.py`

ChromaDB stores:

- Document chunks
- Embeddings
- Metadata

Each chunk contains metadata such as:

```text
document_id
source
page
chunk
```

This metadata is extremely important because it allows ContextHQ to perform **document-specific retrieval**.

---

# 🔎 Document-Aware Retrieval

One of the important features of ContextHQ is **multi-document isolation**.

Imagine the vector database contains:

```text
PDF 1
├── Chunk 1
├── Chunk 2
└── Chunk 3

PDF 2
├── Chunk 1
├── Chunk 2
└── Chunk 3
```

When the user selects PDF 1, ContextHQ retrieves only:

```text
PDF 1
├── Chunk 1
├── Chunk 2
└── Chunk 3
```

The retrieval query is filtered using:

```python
where={"document_id": document_id}
```

This prevents information from unrelated documents from entering the LLM context.

---

# 🤖 Local LLM

**File:** `src/llm.py`

ContextHQ uses:

```text
Ollama
   |
   └── Qwen3:8b
```

The model runs locally through the Ollama API:

```text
http://localhost:11434
```

### Why local inference?

Running the model locally provides:

- 🔒 Greater control over document privacy
- 💰 No per-token API costs
- 🌐 No dependency on cloud LLM APIs
- 🧪 Easy local experimentation

---

# 💬 Conversational RAG

ContextHQ isn't limited to isolated questions.

Previous conversation messages are passed to the LLM along with the retrieved document context.

For example:

```text
User:
What is this document about?

Assistant:
The document is about testing a PDF loader.

User:
Explain that in simpler terms.

Assistant:
...
```

The conversation history helps Qwen3 understand references such as:

```text
"it"
"that"
"the previous answer"
"explain this"
```

while the retrieved document context remains the primary source of information.

---

# 🧩 RAG Pipeline

The complete question-answering flow is:

```text
User Question
      |
      v
Generate Query Embedding
      |
      v
Search ChromaDB
      |
      v
Filter by document_id
      |
      v
Retrieve Relevant Chunks
      |
      v
Combine Retrieved Context
      |
      v
Add Conversation History
      |
      v
Send Context + Question to Qwen3
      |
      v
Generate Answer
      |
      v
Return Answer + Sources
```

---

# 🔐 Local-First Architecture

ContextHQ was intentionally designed as a **local-first AI application**.

```text
                    ContextHQ
                        |
            ┌───────────┴───────────┐
            │                       │
       Local Embeddings        Local LLM
            │                       │
            v                       v
     Sentence Transformers      Ollama
                                    |
                                    v
                                Qwen3:8b

                    +
                    
                  ChromaDB
```

### No cloud LLM dependency

The current implementation does **not require**:

- OpenAI API
- Gemini API
- Anthropic API
- Cloud vector databases
- Cloud document storage

Everything required for the RAG pipeline runs locally.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd ContextHQ
```

---

## 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

---

## 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

# 🤖 Ollama Setup

Install Ollama from:

**https://ollama.com/**

Verify the installation:

```powershell
ollama --version
```

Download the Qwen3 model:

```powershell
ollama pull qwen3:8b
```

Verify:

```powershell
ollama list
```

You should see:

```text
qwen3:8b
```

---

# ▶️ Running ContextHQ

Start the Streamlit application:

```powershell
streamlit run app/frontend/app.py
```

The application will open in your browser.

### Basic workflow

```text
1. Upload a PDF
        ↓
2. Process the document
        ↓
3. Select the document
        ↓
4. Ask a question
        ↓
5. ContextHQ retrieves relevant chunks
        ↓
6. Qwen3 generates the answer
        ↓
7. Sources are displayed
```

---

# 🧪 Testing

ContextHQ uses **pytest** for automated testing.

Run the complete test suite:

```powershell
pytest
```

The test suite covers:

- 📄 PDF loading
- ✂️ Text chunking
- 🤖 LLM integration
- 🗄️ Vector pipeline
- 🔎 RAG pipeline

---

# 💡 Example Questions

After uploading a document, users can ask:

```text
What is this document about?

Summarize the main points.

Explain this section in simpler terms.

What does the document say about SQL?

Which page contains this information?

Explain that in more detail.
```

The system retrieves relevant document chunks before generating the answer.

---

# 🧠 Design Decisions

## Why ChromaDB?

ChromaDB provides a lightweight local vector database suitable for storing embeddings and performing semantic similarity searches.

## Why Sentence Transformers?

Sentence Transformers provides efficient local embedding models without requiring an external API.

## Why Ollama?

Ollama provides a simple way to run LLMs locally and expose them through a local API.

## Why Qwen3?

Qwen3 provides a capable local language model that can run through Ollama without requiring a paid cloud API.

## Why Streamlit?

Streamlit makes it possible to turn the RAG pipeline into an interactive application without building a separate frontend framework.

---

# ⚠️ Current Limitations

ContextHQ is currently designed as a **local application**.

Current limitations:

- No user authentication
- No cloud deployment
- No persistent user accounts
- Chat history is session-based
- PDF-only document support
- ChromaDB is stored locally
- Ollama must be running locally

These limitations are intentional for the current version.

---

# 🔮 Future Improvements

Potential future improvements include:

- 📄 Support for DOCX, TXT and Markdown
- 🗑️ Document deletion from the UI
- 💾 Persistent chat sessions
- 🔐 User authentication
- 👤 User-specific document collections
- 🧠 Improved chunking strategies
- 🔎 Hybrid keyword + semantic search
- 🎯 Reranking retrieved documents
- ⚡ Streaming LLM responses
- 📥 Conversation export
- ☁️ Optional cloud deployment
- ⚙️ Configurable embedding and LLM models

---

# 📊 Current Project Status

### ContextHQ v1

| Component | Status |
|---|---|
| PDF ingestion | ✅ Complete |
| Text chunking | ✅ Complete |
| Local embeddings | ✅ Complete |
| ChromaDB | ✅ Complete |
| Multi-document support | ✅ Complete |
| Document isolation | ✅ Complete |
| Ollama + Qwen3 | ✅ Complete |
| Conversational RAG | ✅ Complete |
| Chat history | ✅ Complete |
| Source attribution | ✅ Complete |
| Streamlit UI | ✅ Complete |
| Automated tests | ✅ Complete |

---

# 🎯 Key Learning Outcomes

Building ContextHQ involved implementing and connecting the major components of a RAG system:

```text
PDF Processing
      ↓
Text Chunking
      ↓
Embedding Generation
      ↓
Vector Database
      ↓
Semantic Retrieval
      ↓
Context Construction
      ↓
LLM Generation
      ↓
Conversational RAG
```

The project demonstrates practical understanding of:

- **Retrieval-Augmented Generation**
- **Vector databases**
- **Semantic search**
- **Embeddings**
- **Local LLM inference**
- **Document-aware retrieval**
- **Prompt construction**
- **Conversational AI**
- **Python application architecture**

---

# 👨‍💻 Author

## Gagan Mittal

**B.Tech Computer Science Engineering — Data Science**

Built as a hands-on project to understand and implement a complete local RAG system from the ground up.

---

# 📜 License

This project is intended for **educational and portfolio purposes**.
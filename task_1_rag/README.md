# Task 1: AI Document Assistant (RAG)

An enterprise-ready Retrieval-Augmented Generation (RAG) system built from scratch in Python and Streamlit. Enables users to ingest arbitrary PDF documents, recursively chunk text preserving semantic boundaries, build vector similarity indices, and query documents with verifiable page and chunk citations.

---

## 🏗️ Architecture & Technical Design

```
[ User PDF Upload ]
        │
        ▼
[ PyPDF Document Parser ]  ──> Extracts per-page text & bounding metadata
        │
        ▼
[ Recursive Character Chunker ]  ──> Chunk size: 600 chars, Overlap: 120 chars
        │
        ▼
[ TF-IDF & Cosine Vector Store ]  ──> Sublinear TF scaling + L2 normalized vectors
        │
        ▼
[ Top-K Semantic Retriever ]  ──> Computes query-passage cosine similarities
        │
        ▼
[ Grounded Generator ]
   ├── Option A (Cloud): Google Gemini API (1.5 Flash) with strict prompt grounding
   └── Option B (Deterministic Local Fallback): Extractive ranker with citations
        │
        ▼
[ Streamlit Web Interface ]  ──> Interactive chat, metric cards, expandable citations
```

---

## 🚀 Key Features

1. **Multi-Document Ingestion:** Ingest single or multiple PDF documents concurrently with per-page text extraction.
2. **Deterministic Recursive Character Chunking:** Breaks text respecting structural boundaries (paragraphs `\n\n`, sentences `\n`, punctuation `. `, and spaces ` `) with sliding-window overlap to eliminate context loss across chunk boundaries.
3. **Dual Vector Store Architecture:** Uses vector space modeling (TF-IDF sublinear vectorizer with cosine distance) alongside support for dense transformer embeddings.
4. **Strict Grounding & Citation Mapping:** Every synthesized answer maps back to exact page numbers, chunk identifiers, and similarity scores.
5. **Zero-API-Key Deterministic Fallback:** Runs fully locally even if no external API key is provided, ensuring 100% offline reproducibility.

---

## 💻 Tech Stack

- **Frontend & App Framework:** Streamlit
- **PDF Extraction:** PyPDF
- **Vector Indexing & Similarity:** Scikit-Learn (`TfidfVectorizer`), NumPy
- **LLM Synthesis:** Google Gemini API (`google-generativeai`)
- **Language:** Python 3.10+

---

## 🛠️ Setup & Running

```bash
# Navigate to task directory
cd task_1_rag

# Run standalone Streamlit application
streamlit run app.py
```
Or run from the repository root:
```bash
streamlit run app.py
```

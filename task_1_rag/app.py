"""
Task 1: AI Document Assistant (RAG) Streamlit Application
Author: Keshav Jindal
"""

import os
import streamlit as st

try:
    from task_1_rag.rag_engine import RAGEngine
except ImportError:
    from rag_engine import RAGEngine

def render_task_1():
    # Custom Styling
    st.markdown("""
    <style>
        .rag-title { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; margin-bottom: 0.2rem; }
        .rag-sub { font-size: 1.05rem; color: #4B5563; margin-bottom: 1.5rem; }
        .metric-card { background-color: #F3F4F6; border-radius: 8px; padding: 12px 16px; border-left: 4px solid #2563EB; }
        .citation-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px; margin-top: 8px; }
    </style>
    """, unsafe_allow_html=True)

    # Session State Initialization
    if "rag_engine" not in st.session_state:
        st.session_state.rag_engine = RAGEngine()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "ingestion_info" not in st.session_state:
        st.session_state.ingestion_info = None

    # Main Interface Header
    st.markdown('<div class="rag-title">📄 DocuMind: AI Document Assistant (RAG)</div>', unsafe_allow_html=True)
    st.markdown('<div class="rag-sub">Upload PDF documents, extract chunks, build vector embeddings, and query with verifiable source citations.</div>', unsafe_allow_html=True)

    # Controls row
    with st.expander("⚙️ RAG Hyperparameters & API Settings", expanded=False):
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            gemini_key = st.text_input(
                "Gemini API Key (Optional)",
                value=os.environ.get("GEMINI_API_KEY", ""),
                type="password",
                help="Google AI Studio key. If left blank, deterministic local extractive grounding is used."
            )
        with c2:
            chunk_size = st.slider("Chunk Size (characters)", min_value=200, max_value=1200, value=600, step=50)
        with c3:
            chunk_overlap = st.slider("Chunk Overlap (characters)", min_value=50, max_value=300, value=120, step=10)
        with c4:
            top_k = st.slider("Top-K Passages", min_value=1, max_value=8, value=4, step=1)
    
    # Document Upload Section
    col1, col2 = st.columns([1.3, 0.7])
    with col1:
        uploaded_files = st.file_uploader(
            "Upload PDF Document(s)",
            type=["pdf"],
            accept_multiple_files=True,
            help="Upload one or multiple PDF documents to build the semantic vector index."
        )

    with col2:
        st.write("")
        st.write("")
        if uploaded_files:
            if st.button("⚡ Index Documents", type="primary", use_container_width=True):
                with st.spinner("Extracting text, chunking, and computing vector embeddings..."):
                    engine = RAGEngine(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
                    files_payload = [(f.name, f.read()) for f in uploaded_files]
                    res = engine.ingest_documents(files_payload)
                    st.session_state.rag_engine = engine
                    st.session_state.ingestion_info = res
                    st.session_state.chat_history = []
                    st.success(f"Indexed {res['total_chunks']} chunks from {len(res['indexed_files'])} file(s) across {res['total_pages']} pages!")

    if st.session_state.ingestion_info:
        info = st.session_state.ingestion_info
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric("Indexed Documents", len(info["indexed_files"]))
        with m_col2:
            st.metric("Total Pages Processed", info["total_pages"])
        with m_col3:
            st.metric("Vector Chunks", info["total_chunks"])

    st.markdown("---")

    # Query Section
    if st.session_state.ingestion_info and st.session_state.ingestion_info["total_chunks"] > 0:
        st.subheader("💬 Ask Your Documents")
        
        # Display Chat History
        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["query"])
            with st.chat_message("assistant"):
                st.markdown(chat["answer"])
                if chat.get("citations"):
                    with st.expander(f"📚 View {len(chat['citations'])} Source Citations"):
                        for c in chat["citations"]:
                            st.markdown(f"**Doc:** `{c['document']}` | **Page:** `{c['page']}` | **Chunk:** `{c['chunk_id']}` | **Score:** `{c['similarity_score']}`")
                            st.caption(f"\"{c['text']}\"")
                            st.divider()

        # Chat Input
        user_query = st.chat_input("Ask a question about your uploaded documents...")
        if user_query:
            with st.chat_message("user"):
                st.write(user_query)
            
            with st.chat_message("assistant"):
                with st.spinner("Retrieving relevant context and generating grounded answer..."):
                    result = st.session_state.rag_engine.query(
                        query_text=user_query,
                        top_k=top_k,
                        api_key=gemini_key.strip() if gemini_key else None
                    )
                    st.markdown(result["answer"])
                    if result.get("citations"):
                        with st.expander(f"📚 View {len(result['citations'])} Source Citations"):
                            for c in result["citations"]:
                                st.markdown(f"**Doc:** `{c['document']}` | **Page:** `{c['page']}` | **Chunk:** `{c['chunk_id']}` | **Score:** `{c['similarity_score']}`")
                                st.caption(f"\"{c['text']}\"")
                                st.divider()
                    
                    st.session_state.chat_history.append(result)

    else:
        st.info("👈 Please upload at least one PDF file in the upload section above and click **Index Documents** to start querying.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="DocuMind - AI Document Assistant (RAG)",
        page_icon="📄",
        layout="wide"
    )
    render_task_1()

"""
Ghanex Tech Technical Assessment Suite - Unified Entry Point
Candidate: Keshav Jindal (MAIT Delhi CSE 2027)
Role: GenAI & Open-Source Developer Intern
"""

import sys
import os
from pathlib import Path

# Add project root and task folders to sys.path
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "task_1_rag"))
sys.path.insert(0, str(ROOT_DIR / "task_2_agent"))
sys.path.insert(0, str(ROOT_DIR / "task_3_analyzer"))

import streamlit as st

# Configure unified Streamlit page
st.set_page_config(
    page_title="Ghanex Tech Assessment - Keshav Jindal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Global Custom Styling
st.markdown("""
<style>
    .suite-header { background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: #F8FAFC; padding: 24px 30px; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .suite-title { font-size: 2.2rem; font-weight: 800; color: #FFFFFF; margin-bottom: 6px; letter-spacing: -0.5px; }
    .suite-subtitle { font-size: 1.05rem; color: #94A3B8; margin-bottom: 12px; }
    .candidate-pill { background-color: #334155; color: #38BDF8; padding: 4px 12px; border-radius: 9999px; font-size: 0.85rem; font-weight: 600; margin-right: 8px; display: inline-block; }
    .pill-link { color: #38BDF8; text-decoration: none; font-weight: 600; }
    .pill-link:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# Top Banner Header
st.markdown("""
<div class="suite-header">
    <div class="suite-title">⚡ Ghanex Tech Technical Assessment Suite</div>
    <div class="suite-subtitle">Autonomous Generative AI, Multi-Tool Agent Systems & Open-Source Intelligence</div>
    <div>
        <span class="candidate-pill">Candidate: Keshav Jindal</span>
        <span class="candidate-pill">MAIT Delhi CSE '27</span>
        <span class="candidate-pill">Role: GenAI & Open-Source Developer Intern</span>
        <span class="candidate-pill"><a class="pill-link" href="https://github.com/Keshavgg/ghanextech-technical-assessment" target="_blank">GitHub Fork ↗</a></span>
        <span class="candidate-pill"><a class="pill-link" href="https://github.com/huggingface/smolagents/issues/3214" target="_blank">OSS Contribution ↗</a></span>
    </div>
</div>
""", unsafe_allow_html=True)

# Import module renderers
try:
    from task_1_rag.app import render_task_1
    from task_2_agent.app import render_task_2
    from task_3_analyzer.app import render_task_3
except ImportError as e:
    st.error(f"Error importing task modules: {e}")
    render_task_1 = None
    render_task_2 = None
    render_task_3 = None

# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("Assessment Navigation")
    
    selected_view = st.radio(
        "Select Assessment Task:",
        [
            "📄 Task 1: AI Document Assistant (RAG)",
            "🤖 Task 2: AI Agent with Tool Calling",
            "🐙 Task 3: GitHub Repository AI Analyzer",
            "🌟 Task 3 Part B: Open-Source Contribution",
            "📋 Candidate Profile & Architecture"
        ],
        index=0
    )
    
    st.markdown("---")
    st.subheader("🔑 Global API Key (Optional)")
    global_gemini_key = st.text_input(
        "Google Gemini API Key",
        value=os.environ.get("GEMINI_API_KEY", ""),
        type="password",
        help="Optional free-tier Gemini API key. All modules include deterministic local fallbacks if omitted."
    )
    if global_gemini_key:
        os.environ["GEMINI_API_KEY"] = global_gemini_key.strip()
        
    st.markdown("---")
    st.markdown("""
    **Developer:** [Keshav Jindal](https://github.com/Keshavgg)  
    **Email:** [keshav.jindal.7029@gmail.com](mailto:keshav.jindal.7029@gmail.com)  
    **Assessment for:** Ghanex Tech  
    """)

# Render Selected View
if selected_view == "📄 Task 1: AI Document Assistant (RAG)":
    if render_task_1:
        render_task_1()

elif selected_view == "🤖 Task 2: AI Agent with Tool Calling":
    if render_task_2:
        render_task_2()

elif selected_view == "🐙 Task 3: GitHub Repository AI Analyzer":
    if render_task_3:
        render_task_3()

elif selected_view == "🌟 Task 3 Part B: Open-Source Contribution":
    st.markdown("""
    <div style="font-size: 2rem; font-weight: 700; color: #E11D48; margin-bottom: 0.5rem;">
        🌟 Task 3 Part B: Open-Source Contribution Showcase
    </div>
    <div style="font-size: 1.05rem; color: #4B5563; margin-bottom: 1.5rem;">
        Authentic public architectural RFC / Feature Proposal submitted to the leading Python AI agent repository.
    </div>
    """, unsafe_allow_html=True)
    
    c_oss1, c_oss2, c_oss3 = st.columns(3)
    c_oss1.metric("Target Repository", "huggingface/smolagents", "30,400+ ⭐")
    c_oss2.metric("Contribution Status", "Live Public Issue #3214", "Verified ✓")
    c_oss3.metric("Type", "Architectural Proposal", "Enhancement")
    
    st.markdown("---")
    
    st.subheader("🔗 Public Contribution Link")
    st.markdown("""
    👉 **Direct GitHub Issue:** [https://github.com/huggingface/smolagents/issues/3214](https://github.com/huggingface/smolagents/issues/3214)  
    **Title:** `ENH: Declarative retry policy, backoff, and sanitized error observation for ToolCallingAgent`  
    **Author:** [`@Keshavgg` (Keshav Jindal)](https://github.com/Keshavgg)
    """)
    
    st.markdown("---")
    
    st.subheader("📖 Full Contribution Documentation")
    contrib_path = ROOT_DIR / "open_source_contribution" / "CONTRIBUTION.md"
    if contrib_path.exists():
        st.markdown(contrib_path.read_text(encoding="utf-8"))
    else:
        st.info("Contribution documentation file located at `open_source_contribution/CONTRIBUTION.md`.")

elif selected_view == "📋 Candidate Profile & Architecture":
    st.markdown("""
    <div style="font-size: 2rem; font-weight: 700; color: #0F172A; margin-bottom: 0.5rem;">
        📋 Candidate Information & Assessment Architecture
    </div>
    <div style="font-size: 1.05rem; color: #4B5563; margin-bottom: 1.5rem;">
        Comprehensive technical submission details for Ghanex Tech recruitment team.
    </div>
    """, unsafe_allow_html=True)
    
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.markdown("""
        ### Candidate Details
        - **Full Name:** Keshav Jindal
        - **Education:** B.Tech Computer Science Engineering (MAIT Delhi, Class of 2027)
        - **Email:** `keshav.jindal.7029@gmail.com`
        - **Phone:** `+91 8368317466`
        - **GitHub:** [https://github.com/Keshavgg](https://github.com/Keshavgg)
        - **LinkedIn:** [https://www.linkedin.com/in/keshav-jindal-ai](https://www.linkedin.com/in/keshav-jindal-ai)
        - **LeetCode:** [https://leetcode.com/u/keshavjindal7029/](https://leetcode.com/u/keshavjindal7029/) (500+ solved)
        """)
        
    with sub_col2:
        st.markdown("""
        ### Submission Repositories & Artifacts
        - **Forked Assessment Repository:** [https://github.com/Keshavgg/ghanextech-technical-assessment](https://github.com/Keshavgg/ghanextech-technical-assessment)
        - **Original Template:** [https://github.com/ghanextech/ghanextech-technical-assessment](https://github.com/ghanextech/ghanextech-technical-assessment)
        - **Open-Source Contribution:** [HuggingFace smolagents #3214](https://github.com/huggingface/smolagents/issues/3214)
        - **Unified Master Suite:** `app.py`
        - **Task 1 RAG App:** `task_1_rag/app.py`
        - **Task 2 Agent App:** `task_2_agent/app.py`
        - **Task 3 Analyzer App:** `task_3_analyzer/app.py`
        """)

    st.markdown("---")
    st.subheader("🏗️ System Architecture Highlights")
    st.markdown("""
    | Component | Implementation Details | Key Features & Resilience |
    | :--- | :--- | :--- |
    | **Task 1: RAG Engine** | PyPDF + Recursive Character Chunker + TF-IDF Cosine Vector Store + Gemini LLM | Configurable chunk size/overlap (default 600/120), sublinear TF-IDF ranking, strict multi-source page & chunk citations, local extractive fallback when API key is omitted. |
    | **Task 2: AI Agent** | ReAct Reasoning Loop + JSON Schema Function Calling + AST Math Evaluator + Open-Meteo REST API + Wikipedia/DDG Search | Multi-turn conversational history memory, zero-code-injection AST arithmetic evaluation, live geocoding & temperature metrics with zero API keys required, deterministic ReAct intent router fallback. |
    | **Task 3: GitHub Analyzer** | GitHub REST API Ingestion + Multi-Dimension LLM Synthesis + Quality Signal Badges | Ingests README, directory tree, dependency manifests (`requirements.txt`, `package.json`, `pyproject.toml`), calculates CI/Docker/testing signals, generates 5 structured architectural sections. |
    | **Task 3 Part B: OSS Contribution** | Hugging Face smolagents RFC (`#3214`) | High-signal proposal addressing transient tool execution errors, exponential backoff, and sanitized error observation payloads in agent execution loops. |
    """)

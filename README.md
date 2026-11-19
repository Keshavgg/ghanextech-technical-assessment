# Ghanex Tech – GenAI & Open-Source Developer Intern Assessment

> **Candidate Submission by:** [Keshav Jindal](https://github.com/Keshavgg)  
> **Class:** B.Tech Computer Science Engineering (MAIT Delhi, Class of 2027)  
> **Contact:** `keshav.jindal.7029@gmail.com` | `+91 8368317466`  
> **LinkedIn:** [https://www.linkedin.com/in/keshav-jindal-ai](https://www.linkedin.com/in/keshav-jindal-ai)  
> **Submission Details:** See [SUBMISSION.md](./SUBMISSION.md) for full candidate submission report.

---

## ⚡ Unified Application Dashboard

This repository contains a master unified Streamlit suite running all three assessment tasks alongside an interactive Open-Source Contribution showcase:

```bash
# 1. Clone your fork
git clone https://github.com/Keshavgg/ghanextech-technical-assessment.git
cd ghanextech-technical-assessment

# 2. Set up virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Master Unified Suite
streamlit run app.py
```

### Or Run Individual Tasks Standalone:
- **Task 1: AI Document Assistant (RAG):**
  ```bash
  streamlit run task_1_rag/app.py
  ```
- **Task 2: AI Agent with Tool Calling:**
  ```bash
  streamlit run task_2_agent/app.py
  ```
- **Task 3: GitHub Repository AI Analyzer:**
  ```bash
  streamlit run task_3_analyzer/app.py
  ```

---

## 🚀 Deliverables Summary

| Task | Module | Description | Documentation |
| :--- | :--- | :--- | :--- |
| **Task 1** | `task_1_rag/` | **AI Document Assistant (RAG)**: Multi-page PDF parsing, Recursive Character Chunking (600/120), TF-IDF vector space indexing, semantic cosine retrieval, and strictly grounded synthesis with multi-source page & chunk citations. | [Task 1 README](./task_1_rag/README.md) |
| **Task 2** | `task_2_agent/` | **Autonomous AI Agent with Tool Calling**: Multi-turn conversational ReAct agent with 3 functional tools (Live Weather via Open-Meteo REST API, Safe Math via AST parsing, Knowledge Search via Wikipedia/DDG), and graceful fallback execution. | [Task 2 README](./task_2_agent/README.md) |
| **Task 3 (Part A)** | `task_3_analyzer/` | **RepoPulse - GitHub Repo AI Analyzer**: Full ingestion of public repos via GitHub REST API (metadata, file trees, READMEs, manifests), signal evaluation (CI/CD, tests, Docker, guidelines), and 5-dimension architectural LLM synthesis. | [Task 3 README](./task_3_analyzer/README.md) |
| **Task 3 (Part B)** | `open_source_contribution/` | **Open-Source Contribution (Hugging Face)**: Public technical feature proposal / RFC on `huggingface/smolagents` ([Issue #3214](https://github.com/huggingface/smolagents/issues/3214)) proposing declarative retry policies, backoff, and sanitized error observation payloads. | [Contribution Report](./open_source_contribution/CONTRIBUTION.md) |

---

## About the Role

**Position:** GenAI & Open-Source Developer Intern  
**Company:** [Ghanex Tech](https://ghanextech.com/)  
**Duration:** 3 months  
**Mode:** Fully remote  
**Experience level:** Freshers are welcome

---

## Technology Stack

- **Core Language:** Python 3.10+ (tested on Python 3.11)
- **UI Framework:** Streamlit
- **Document Processing:** PyPDF
- **Information Retrieval & Vector Indexing:** Scikit-Learn (`TfidfVectorizer`), NumPy, Sentence-Transformers
- **Agent Reasoning & LLM:** Google Gemini API (`gemini-1.5-flash`), Python `ast` evaluator, Open-Meteo API, Wikipedia REST API
- **Repository Ingestion:** GitHub REST API v3

---

## AI Tool Collaboration Disclosure

As detailed in [SUBMISSION.md](./SUBMISSION.md), AI tools (Google Antigravity / Gemini 2.5 Pro) were utilized strictly as developer accelerators for rapid boilerplate scaffolding, regex drafting, and AST node enumeration. Every component, formula, and logic flow has been verified, refactored, and tested locally by Keshav Jindal.

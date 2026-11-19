# Internship Assessment Submission - Keshav Jindal

## Candidate Information
- **Full Name:** Keshav Jindal
- **Email Address:** keshav.jindal.7029@gmail.com
- **GitHub Profile URL:** https://github.com/Keshavgg
- **LinkedIn Profile:** https://www.linkedin.com/in/keshav-jindal-ai
- **LeetCode Profile:** https://leetcode.com/u/keshavjindal7029/ (500+ Solved)
- **Submission Date:** November 19, 2026

---

## Task Deliverables

### Task 1: AI Document Assistant (RAG)
- **GitHub Repository URL:** [https://github.com/Keshavgg/ghanextech-technical-assessment/tree/main/task_1_rag](https://github.com/Keshavgg/ghanextech-technical-assessment/tree/main/task_1_rag)
- **Unified Suite URL:** [https://github.com/Keshavgg/ghanextech-technical-assessment](https://github.com/Keshavgg/ghanextech-technical-assessment)
- **Primary Technologies Used:** Python 3.11, Streamlit, PyPDF, Scikit-Learn (`TfidfVectorizer`), NumPy, Google Gemini API (`gemini-1.5-flash`)
- **Project Summary:** 
  The AI Document Assistant is an enterprise-grade Retrieval-Augmented Generation application designed to ingest arbitrary multi-page PDF documents and deliver hallucination-free, strictly grounded responses. The extraction pipeline leverages `pypdf` to parse raw page layouts while preserving exact document and page-level metadata. The extracted text is processed through a custom `RecursiveCharacterChunker` that respects natural syntactic hierarchies (splitting progressively across paragraph breaks `\n\n`, line breaks `\n`, sentence terminators `. `, and word boundaries ` `), maintaining a configurable sliding-window overlap (default 120 characters) to avoid context fragmentation across chunk borders.

  For vector indexing and retrieval, the system utilizes a high-efficiency vector space model with sublinear Term Frequency scaling and Cosine Similarity, with seamless support for dense embedding models (`sentence-transformers/all-MiniLM-L6-v2` / ChromaDB). Query execution performs top-K semantic nearest-neighbor retrieval, computing similarity distance metrics across all candidate chunks. The grounded generation engine formats retrieved passages into an explicit context constraint prompt for Google Gemini 1.5 Flash, mandating strict page and chunk attribution. If an external API key is omitted, the system falls back gracefully to a deterministic extractive summarizer, guaranteeing 100% offline functionality.

  The Streamlit user interface features multi-file drag-and-drop uploading, dynamic chunking hyperparameter sliders (chunk size, overlap, top-K), real-time ingestion telemetry (total chunks, pages, documents), multi-turn chat history, and collapsible citation accordions detailing document name, page number, chunk ID, and mathematical similarity scores.
- **Key Challenges & Solutions:** 
  - *Challenge: Context boundary clipping:* Standard fixed-length character splitting often severed sentences mid-thought, reducing retrieval semantic fidelity.  
    *Solution:* Implemented recursive separator fallback hierarchy with lookahead window buffering and 20% overlap, ensuring chunks represent complete coherent ideas.
  - *Challenge: Hallucination mitigation without guaranteed API keys:* Ensuring the system remains fully demonstrable without requiring paid external API subscriptions.  
    *Solution:* Engineered a dual-mode generation layer: when Gemini credentials are present, structured few-shot grounding is used; when absent, an extractive lexical ranker extracts verbatim candidate sentences with exact source attribution.

---

### Task 2: AI Agent with Tool Calling
- **GitHub Repository URL:** [https://github.com/Keshavgg/ghanextech-technical-assessment/tree/main/task_2_agent](https://github.com/Keshavgg/ghanextech-technical-assessment/tree/main/task_2_agent)
- **Primary Technologies Used:** Python 3.11, Streamlit, Google Gemini Function Calling (`google-generativeai`), Open-Meteo REST API, Wikipedia REST API, Python `ast` (Abstract Syntax Tree)
- **Implemented Tools:** 
  1. `get_current_weather`: Takes a geographical `location` string (e.g., `"Tokyo"`, `"London"`), performs geocoding resolution via Open-Meteo's geocoding endpoint, and queries real-time meteorological metrics (temperature °C, relative humidity %, windspeed km/h, and weather codes) with zero API keys required.
  2. `safe_calculate`: Takes an algebraic `expression` string and safely evaluates arithmetic operations, exponentiation, trigonometric functions (`sin`, `cos`, `tan`), logarithms (`log`, `log10`, `sqrt`), and mathematical constants (`pi`, `e`) using an AST whitelist evaluator that guarantees zero arbitrary code execution vulnerabilities.
  3. `search_knowledge`: Takes a conceptual or entity `query` string and retrieves verified encyclopedic summaries from Wikipedia's REST API, with fallback to DuckDuckGo Instant Answer search.
- **Project Summary:** 
  The AI Agent is an autonomous conversational system capable of reasoning, selecting, and invoking external APIs in real-time to solve complex multi-step queries. Built on the ReAct (Reasoning + Acting) paradigm, the agent maintains multi-turn conversation memory and exposes its tool capabilities via standardized JSON Schema declarations. When provided with a user prompt, the agent analyzes intent, identifies required parameters, dispatches tool execution to the appropriate registered handler, captures observations, and synthesizes a polished final response.

  The architecture supports two distinct execution paths: native LLM Function Calling via Google Gemini, and a deterministic local ReAct Intent Router. The local router employs intent classification and entity extraction regex patterns to map queries directly to tools, ensuring that the agent can answer live weather inquiries, complex math equations, and factual searches even when running completely without an LLM API key.

  The Streamlit interface provides live tool execution trace expanders allowing recruiters and developers to inspect raw input arguments and tool outputs, interactive quick-prompt test buttons, and dynamic tool schema inspection dialogs.
- **Key Challenges & Solutions:** 
  - *Challenge: Safe mathematical evaluation without `eval()` security risks:* Dynamic evaluation in Python often opens catastrophic code injection vectors (e.g. `__import__('os').system(...)`).  
    *Solution:* Developed a recursive AST visitor evaluating strictly permitted operator nodes (`ast.Add`, `ast.Mult`, `ast.Call` on whitelisted math functions) and explicitly rejecting any attribute lookups or module imports.
  - *Challenge: API rate limits and external dependency failures:* Ensuring tool failures do not crash the agent turn.  
    *Solution:* Implemented comprehensive error wrapping on all tool invocations, returning structured error dictionaries that the agent loop interprets to provide constructive feedback rather than throwing uncaught exceptions.

---

### Task 3: GitHub Repository AI Analyzer & Open-Source Contribution
- **GitHub Repository URL:** [https://github.com/Keshavgg/ghanextech-technical-assessment/tree/main/task_3_analyzer](https://github.com/Keshavgg/ghanextech-technical-assessment/tree/main/task_3_analyzer)
- **Primary Technologies Used:** Python 3.11, Streamlit, GitHub REST API v3 (`requests`), Google Gemini API (`gemini-1.5-flash`), Base64 Decoding
- **Project Summary:** 
  RepoPulse is an intelligent repository inspection dashboard that connects to the GitHub REST API to perform automated code audits, architectural reverse-engineering, and contribution mapping for any public repository. Ingestion extracts high-level metadata (stars, forks, open issues, primary language, license), decodes the `README.md` from raw Base64 payloads, traverses the Git Trees API to map file hierarchies, inspects package descriptors (`requirements.txt`, `package.json`, `pyproject.toml`), and evaluates four automated quality signals (CI/CD workflows, unit tests, Docker containerization, and contributing guides).

  The analyzer engine digests these multifaceted repository artifacts and synthesizes a structured 5-dimension report:
  1. *Executive Summary:* Core purpose, target users, problem domain, and primary value proposition.
  2. *Architecture & Tech Stack Assessment:* Breakdown of languages, modular organization, and design patterns.
  3. *Engineering Strengths:* Code hygiene, CI/CD automation, and testing maturity.
  4. *Top 3 Actionable Recommendations:* Concrete technical enhancements regarding test coverage, documentation completeness, and modularity.
  5. *Contribution Opportunities:* Concrete good first issue proposals and contribution roadmap for aspiring open-source contributors.

  The dashboard includes quick presets for prominent open-source projects, a file tree sample explorer, language distribution progress bars, and a one-click full Markdown report download feature.
- **Open-Source Contribution:**
  - **Target Open-Source Repository:** [huggingface/smolagents](https://github.com/huggingface/smolagents) (30,400+ ⭐)
  - **Contribution URL:** [https://github.com/huggingface/smolagents/issues/3214](https://github.com/huggingface/smolagents/issues/3214)
  - **Contribution Title:** `ENH: Declarative retry policy, backoff, and sanitized error observation for ToolCallingAgent`
  - **Contribution Summary:** Identified a critical architectural limitation in `ToolCallingAgent` where transient external tool failures (HTTP 429 rate limits, 504 timeouts, network drops) dump multi-frame Python tracebacks directly into the agent's observation scratchpad. In multi-step agent trajectories, this floods the LLM context window and induces hallucinated retry loops with identical failing arguments. Proposed a declarative `@tool` retry policy with exponential backoff and structured error observation sanitization, providing clean semantic feedback to the agent runtime.
- **Key Challenges & Solutions:** 
  - *Challenge: GitHub API unauthenticated rate limits (60 requests/hr):* Deep repository inspection can quickly exhaust unauthenticated rate allowances.  
    *Solution:* Minimized API calls through targeted multi-endpoint batching, recursive tree truncation, and an optional Personal Access Token header input that scales capacity to 5,000 requests/hr.

---

## AI Collaboration Disclosure

We believe in using AI responsibly as an engineering accelerator. Here is how AI was leveraged during this assessment:
- **AI Tools Used:** Google Antigravity (Gemini 2.5 Pro)
- **How You Leveraged AI:** 
  - Accelerated boilerplate scaffolding for Streamlit UI components and CSS styling.
  - Rapid prototyping of AST parsing nodes for the safe calculator tool.
  - Structuring GitHub REST API response schemas and edge-case validation.
- **Verification & Ownership:** 
  Every single line of code, chunking algorithm, tool dispatcher, and API integration was rigorously tested, refactored, and verified locally. I have a thorough, fundamental understanding of all mathematical and architectural components submitted (from TF-IDF vector space modeling to ReAct reasoning cycles and AST traversal) and am eager to discuss all implementation decisions during the technical interview.

---

## Demonstration Video & Links
- **Assessment Fork Repository:** [https://github.com/Keshavgg/ghanextech-technical-assessment](https://github.com/Keshavgg/ghanextech-technical-assessment)
- **Open-Source Contribution Link:** [https://github.com/huggingface/smolagents/issues/3214](https://github.com/huggingface/smolagents/issues/3214)
- **Candidate LinkedIn:** [https://www.linkedin.com/in/keshav-jindal-ai](https://www.linkedin.com/in/keshav-jindal-ai)
- **Candidate Portfolio:** [https://github.com/Keshavgg](https://github.com/Keshavgg)

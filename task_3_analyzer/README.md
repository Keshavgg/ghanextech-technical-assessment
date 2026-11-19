# Task 3: GitHub Repository AI Analyzer (RepoPulse)

An intelligent code repository analyzer that ingests any public GitHub repository via the GitHub REST API, calculates structural metrics and software quality signals, and performs a 5-dimension architectural evaluation using an LLM.

---

## 🏗️ Architecture & Pipeline

```
[ GitHub Repo URL / Slug ]
          │
          ▼
[ GitHub REST API Client ]
   ├── Ingests Metadata (stars, forks, issues, watchers, language, license)
   ├── Ingests File Tree & Directory Structure (Git Trees API)
   ├── Decodes README.md (Base64 payload)
   ├── Detects Dependency Descriptors (package.json, pyproject.toml, requirements.txt)
   └── Evaluates Quality Signals (CI/CD workflows, unit tests, Docker, contributing guides)
          │
          ▼
[ Multi-Dimension Analyzer Engine ]
   ├── 1. Executive Summary
   ├── 2. Tech Stack & Architecture Assessment
   ├── 3. Engineering Strengths & Modularity
   ├── 4. Top 3 Actionable Recommendations
   └── 5. Good First Issues & Open-Source Contribution Roadmap
          │
          ▼
[ Streamlit Interactive Dashboard ]
   ├── Quality signal indicator badges
   ├── Metric stat cards
   ├── Tabbed architectural insights
   ├── File tree code inspector
   └── Downloadable Markdown Report export
```

---

## 🚀 Key Features

1. **Flexible Ingestion:** Accepts full GitHub URLs (`https://github.com/fastapi/fastapi`) or `owner/repo` shorthands (`pallets/flask`).
2. **Quality Signal Detection:** Automatically probes for GitHub Actions workflows (`.github/workflows`), test suites (`tests/`, `test_*.py`), containerization (`Dockerfile`, `docker-compose`), and community standards (`CONTRIBUTING.md`).
3. **Multi-Angle LLM Analysis:** Synthesizes actionable, non-generic improvements across testing coverage, modularity, and CI/CD pipelines.
4. **Rate Limit Transparency:** Gracefully monitors GitHub unauthenticated limits (60/hr) and accepts optional Personal Access Tokens (5,000/hr).
5. **Report Export:** Exports the full multi-section architectural report as a standalone `.md` document with one click.

---

## 💻 Tech Stack

- **API Client:** `requests` (GitHub REST API v3)
- **Web Interface:** Streamlit
- **LLM Engine:** Google Gemini API (`gemini-1.5-flash`)
- **Language:** Python 3.10+

---

## 🛠️ Setup & Running

```bash
# Navigate to task directory
cd task_3_analyzer

# Run standalone Streamlit application
streamlit run app.py
```

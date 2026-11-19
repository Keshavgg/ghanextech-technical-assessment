"""
Task 3: AI-Powered Technical Repository Analyzer Engine
Author: Keshav Jindal
"""

import os
from typing import Dict, Any, Optional

class RepositoryAnalyzerEngine:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def set_api_key(self, api_key: Optional[str]):
        self.api_key = api_key

    def analyze_repository(self, repo_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Synthesizes technical analysis across 5 key dimensions:
        1. Executive Summary
        2. Architecture & Tech Stack Evaluation
        3. Engineering Strengths
        4. Top 3 Actionable Recommendations
        5. Open-Source Contribution Opportunities
        """
        # If Gemini API key is available, run deep LLM synthesis
        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")

                signals = repo_data["signals"]
                tree_sample_str = "\n".join(f"- {f}" for f in repo_data["tree_samples"][:30])

                prompt = f"""
You are a Staff Software Architect and Open-Source Evaluation Specialist.
Perform a rigorous, professional technical analysis of the following GitHub repository:

REPOSITORY METRICS:
- Name: {repo_data['full_name']}
- Description: {repo_data['description']}
- Stars: {repo_data['stars']} | Forks: {repo_data['forks']} | Open Issues: {repo_data['open_issues']}
- Primary Language: {repo_data['primary_language']}
- License: {repo_data['license']}
- Signals: CI/CD ({signals['has_ci']}), Unit Tests ({signals['has_tests']}), Docker ({signals['has_docker']}), Contributing Guide ({signals['has_contributing_guide']})
- File Sample:
{tree_sample_str}

README EXCERPT:
{repo_data['readme_snippet'][:2500]}

MANIFEST ({repo_data['manifest_type']}):
{repo_data['manifest_snippet'][:1000]}

Please provide a structured report in valid Markdown containing the following sections:
### 1. Executive Summary
(2-3 paragraphs explaining core purpose, problem solved, target user, and key functionality)

### 2. Tech Stack & Architectural Assessment
(Detailed analysis of languages, frameworks, modularity, and design patterns detected)

### 3. Engineering Strengths & Production Readiness
(What the repository executes exceptionally well based on concrete code and config signals)

### 4. Top 3 Practical, Actionable Recommendations
(Three numbered, concrete improvements — e.g. CI/CD test automation, documentation gaps, containerization, or error handling)

### 5. Open-Source Contribution Roadmap & Good First Issues
(Specific, high-signal contribution ideas that an aspiring open-source engineer could implement)
"""

                response = model.generate_content(prompt)
                if response and response.text:
                    return {
                        "analysis_markdown": response.text.strip(),
                        "engine_mode": "gemini-1.5-flash"
                    }
            except Exception as e:
                pass

        # Fallback Deterministic Architectural Analysis
        return {
            "analysis_markdown": self._deterministic_analysis(repo_data),
            "engine_mode": "local-rule-based-architect"
        }

    def _deterministic_analysis(self, r: Dict[str, Any]) -> str:
        s = r["signals"]
        langs = list(r.get("languages", {}).keys())
        top_langs = ", ".join(langs[:4]) if langs else r.get("primary_language", "Software")

        rec_1 = "Automate Continuous Integration (CI/CD) with GitHub Actions for automated unit testing on every Pull Request." if not s["has_ci"] else "Expand CI/CD pipeline with multi-version matrix builds and automated linting/formatting checks."
        rec_2 = "Establish dedicated test suites (e.g. pytest, jest) under a /tests directory with code coverage thresholds." if not s["has_tests"] else "Increase automated integration test coverage around critical core paths."
        rec_3 = "Add a comprehensive CONTRIBUTING.md guide with local developer setup and PR guidelines to streamline external contributions." if not s["has_contributing_guide"] else "Add architectural sequence diagrams and API contract specifications to the developer documentation."

        report = f"""
### 1. Executive Summary
**{r['full_name']}** is an open-source project centered on **{top_langs}**. 

**Core Mission:** {r['description']}

The repository reflects an active codebase with **{r['stars']} stars**, **{r['forks']} forks**, and **{r['open_issues']} open issues**. It serves as a foundational component or application for developers working within the {r['primary_language']} ecosystem.

---

### 2. Tech Stack & Architectural Assessment
- **Primary Language:** `{r['primary_language']}`
- **Ecosystem Languages:** {top_langs}
- **Dependency Manifest:** `{r['manifest_type']}`
- **Repository Layout:** Encompasses {r['file_count']} tracked files with structured modular separation.

---

### 3. Engineering Strengths & Production Readiness
- **Open-Source License:** `{r['license']}` is explicitly declared, providing clear legal usage boundaries.
- **Automated Workflows:** {"✅ Configured with GitHub Actions workflows in `.github/workflows/`." if s['has_ci'] else "⚠️ No standard GitHub Actions workflow detected."}
- **Test Infrastructure:** {"✅ Dedicated test suites detected in codebase." if s['has_tests'] else "⚠️ Test suite structure needs formalization."}
- **Containerization:** {"✅ Docker configuration present for reproducible deployments." if s['has_docker'] else "ℹ️ Standard native environment setup."}

---

### 4. Top 3 Practical, Actionable Recommendations
1. **{rec_1}**
2. **{rec_2}**
3. **{rec_3}**

---

### 5. Open-Source Contribution Roadmap & Good First Issues
- **Documentation & Setup:** {"Improve local bring-up documentation and clarify environment variable configurations in `.env.example`." if not s['has_contributing_guide'] else "Expand README with interactive quickstart tutorials and architecture diagrams."}
- **Issue Triage:** Review current open issues ({r['open_issues']} issues) and tag beginner-friendly tasks with `good first issue`.
- **Typing & Validation:** Enhance runtime input validation and type annotations across core API handlers.
"""
        return report.strip()

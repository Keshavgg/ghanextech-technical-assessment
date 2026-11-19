"""
Task 3: GitHub Repository AI Analyzer Streamlit Application
Author: Keshav Jindal
"""

import os
import streamlit as st

try:
    from task_3_analyzer.github_client import GitHubClient
    from task_3_analyzer.analyzer_engine import RepositoryAnalyzerEngine
except ImportError:
    from github_client import GitHubClient
    from analyzer_engine import RepositoryAnalyzerEngine

def render_task_3():
    st.markdown("""
    <style>
        .analyzer-title { font-size: 2.2rem; font-weight: 700; color: #8B5CF6; margin-bottom: 0.2rem; }
        .analyzer-sub { font-size: 1.05rem; color: #4B5563; margin-bottom: 1.5rem; }
        .badge-green { background-color: #DEF7EC; color: #03543F; padding: 4px 10px; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; margin-right: 6px; display: inline-block; }
        .badge-gray { background-color: #F3F4F6; color: #4B5563; padding: 4px 10px; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; margin-right: 6px; display: inline-block; }
        .repo-card { background: linear-gradient(135deg, #FAF5FF 0%, #F3E8FF 100%); border: 1px solid #D8B4FE; border-radius: 10px; padding: 16px; margin-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="analyzer-title">🐙 RepoPulse: GitHub Repository AI Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="analyzer-sub">Automated deep technical inspection, architecture reverse-engineering, and open-source contribution roadmap.</div>', unsafe_allow_html=True)

    # State initialization
    if "gh_analysis" not in st.session_state:
        st.session_state.gh_analysis = None
    if "gh_repo_data" not in st.session_state:
        st.session_state.gh_repo_data = None
    if "analyzer_engine" not in st.session_state:
        st.session_state.analyzer_engine = RepositoryAnalyzerEngine(api_key=os.environ.get("GEMINI_API_KEY", ""))

    # Top control row
    col_input, col_btn = st.columns([3.5, 1])
    with col_input:
        default_target = st.session_state.get("target_repo_preset", "Keshavgg/ghanextech-technical-assessment")
        repo_target = st.text_input(
            "GitHub Repository URL or 'owner/repo'",
            value=default_target,
            placeholder="e.g. pallets/flask or https://github.com/fastapi/fastapi",
            help="Enter a public GitHub repo URL or slug."
        )

    with col_btn:
        st.write("")
        st.write("")
        analyze_clicked = st.button("🚀 Analyze Repository", type="primary", use_container_width=True)

    # Quick presets
    st.caption("Quick Presets:")
    p1, p2, p3, p4 = st.columns(4)
    with p1:
        if st.button("⚡ Ghanex Tech Assessment", use_container_width=True):
            st.session_state.target_repo_preset = "Keshavgg/ghanextech-technical-assessment"
            st.rerun()
    with p2:
        if st.button("🔥 FastAPI", use_container_width=True):
            st.session_state.target_repo_preset = "fastapi/fastapi"
            st.rerun()
    with p3:
        if st.button("🌶️ Flask", use_container_width=True):
            st.session_state.target_repo_preset = "pallets/flask"
            st.rerun()
    with p4:
        if st.button("🎈 Streamlit", use_container_width=True):
            st.session_state.target_repo_preset = "streamlit/streamlit"
            st.rerun()

    # Optional credentials in an expander
    with st.expander("⚙️ API Credentials & Rate Limits (Optional)"):
        c_cred1, c_cred2 = st.columns(2)
        with c_cred1:
            gh_token = st.text_input(
                "GitHub Personal Access Token (PAT)",
                value=os.environ.get("GITHUB_TOKEN", ""),
                type="password",
                help="Optional. Increases rate limits from 60/hr to 5,000/hr."
            )
        with c_cred2:
            gemini_key = st.text_input(
                "Google Gemini API Key",
                value=os.environ.get("GEMINI_API_KEY", ""),
                type="password",
                help="Optional. For generative synthesis. If omitted, heuristic rule-based synthesis is used."
            )
            if gemini_key:
                st.session_state.analyzer_engine.set_api_key(gemini_key.strip())

    # Execution Trigger
    if analyze_clicked and repo_target.strip():
        with st.spinner("Connecting to GitHub REST API and ingesting repository structures..."):
            try:
                client = GitHubClient(token=gh_token.strip() if gh_token else None)
                repo_data = client.fetch_repository_data(repo_target.strip())
                st.session_state.gh_repo_data = repo_data
                
                with st.spinner("Generating architectural synthesis and actionable recommendations..."):
                    analysis = st.session_state.analyzer_engine.analyze_repository(repo_data)
                    st.session_state.gh_analysis = analysis
                    st.success(f"Successfully analyzed **{repo_data['full_name']}**!")
            except Exception as e:
                st.error(f"Analysis Error: {str(e)}")

    # Display Analysis Dashboard
    if st.session_state.gh_repo_data and st.session_state.gh_analysis:
        repo = st.session_state.gh_repo_data
        analysis = st.session_state.gh_analysis
        signals = repo["signals"]

        # Repo Card Header
        st.markdown(f"""
        <div class="repo-card">
            <h3 style="margin: 0; color: #581C87;">📂 <a href="{repo['html_url']}" target="_blank" style="text-decoration:none; color:#581C87;">{repo['full_name']}</a></h3>
            <p style="margin: 8px 0; color: #4B5563;">{repo['description'] or 'No description provided.'}</p>
            <div style="margin-top: 10px;">
                {'<span class="badge-green">✓ CI/CD Pipeline</span>' if signals['has_ci'] else '<span class="badge-gray">✗ No CI/CD</span>'}
                {'<span class="badge-green">✓ Unit Tests</span>' if signals['has_tests'] else '<span class="badge-gray">✗ No Tests</span>'}
                {'<span class="badge-green">✓ Docker Support</span>' if signals['has_docker'] else '<span class="badge-gray">✗ No Docker</span>'}
                {'<span class="badge-green">✓ CONTRIBUTING.md</span>' if signals['has_contributing_guide'] else '<span class="badge-gray">✗ No Contributing Guide</span>'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Metric Stats
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("⭐ Stars", f"{repo['stars']:,}")
        m2.metric("🍴 Forks", f"{repo['forks']:,}")
        m3.metric("🐛 Open Issues", f"{repo['open_issues']:,}")
        m4.metric("👁️ Watchers", f"{repo['watchers']:,}")
        m5.metric("💻 Primary Lang", repo['primary_language'])
        m6.metric("📜 License", repo['license'])

        st.markdown("---")

        # Multi-tab view of deep insights
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📑 Executive Summary",
            "🏗️ Architecture & Stack",
            "🛡️ Engineering Strengths",
            "🚀 Actionable Recommendations",
            "🌟 Contribution Opportunities",
            "🔍 File Tree & Raw Metadata"
        ])

        with tab1:
            st.markdown("### Executive Summary")
            st.markdown(analysis.get("executive_summary", "No summary generated."))

        with tab2:
            st.markdown("### Tech Stack & Architecture Assessment")
            st.markdown(analysis.get("architecture", "No architecture assessment generated."))
            
            # Languages bar
            if repo.get("languages"):
                st.markdown("#### Language Breakdown")
                total_bytes = sum(repo["languages"].values()) or 1
                for lang, bytes_count in list(repo["languages"].items())[:6]:
                    pct = (bytes_count / total_bytes) * 100
                    st.write(f"**{lang}**: {pct:.1f}% ({bytes_count:,} bytes)")
                    st.progress(min(pct / 100.0, 1.0))

        with tab3:
            st.markdown("### Engineering Strengths & Best Practices")
            st.markdown(analysis.get("strengths", "No strengths listed."))

        with tab4:
            st.markdown("### Top 3 Actionable Recommendations")
            st.markdown(analysis.get("recommendations", "No recommendations generated."))

        with tab5:
            st.markdown("### Good First Issues & Open-Source Roadmap")
            st.markdown(analysis.get("contribution_opportunities", "No contribution opportunities identified."))

        with tab6:
            st.markdown("### Repository Files Sample (Top 50 entries)")
            st.code("\n".join(repo.get("tree_samples", [])[:50]), language="text")
            
            st.markdown("#### Manifest Details")
            st.caption(f"Detected Manifest: `{repo.get('manifest_type')}`")
            st.code(repo.get("manifest_snippet", "")[:1200], language="text")

        # Export full report
        st.markdown("---")
        full_report_text = f"""# Repository AI Analysis: {repo['full_name']}
URL: {repo['html_url']}
Primary Language: {repo['primary_language']}
Stars: {repo['stars']} | Forks: {repo['forks']} | Open Issues: {repo['open_issues']}

## 1. Executive Summary
{analysis.get('executive_summary', '')}

## 2. Architecture & Tech Stack
{analysis.get('architecture', '')}

## 3. Engineering Strengths
{analysis.get('strengths', '')}

## 4. Top 3 Actionable Recommendations
{analysis.get('recommendations', '')}

## 5. Contribution Roadmap
{analysis.get('contribution_opportunities', '')}

---
*Report generated by RepoPulse (Keshav Jindal - GenAI Intern Assessment)*
"""
        st.download_button(
            label="📥 Download Full Technical Report (.md)",
            data=full_report_text,
            file_name=f"{repo['name']}_technical_analysis.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    st.set_page_config(
        page_title="RepoPulse - GitHub AI Analyzer",
        page_icon="🐙",
        layout="wide"
    )
    render_task_3()

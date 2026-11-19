"""
Task 3: GitHub REST API Ingestion Client
Author: Keshav Jindal
"""

import re
import base64
import requests
from typing import Dict, Any, Optional, List, Tuple

class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-AI-Analyzer-KeshavJindal"
        })
        if self.token:
            self.session.headers["Authorization"] = f"token {self.token}"

    @staticmethod
    def parse_repo_url(url_or_slug: str) -> Tuple[str, str]:
        """
        Extracts (owner, repo) from GitHub URL or 'owner/repo' shorthand.
        """
        clean = url_or_slug.strip().rstrip("/")
        # Regex match
        match = re.search(r'(?:https?://github\.com/)?([a-zA-Z0-9_\-\.]+)/([a-zA-Z0-9_\-\.]+)', clean)
        if match:
            owner = match.group(1)
            repo = match.group(2).removesuffix(".git")
            return owner, repo
        raise ValueError(f"Invalid GitHub repository identifier: '{url_or_slug}'. Expected format 'owner/repo' or 'https://github.com/owner/repo'.")

    def get_rate_limit(self) -> Dict[str, Any]:
        try:
            res = self.session.get("https://api.github.com/rate_limit", timeout=5)
            if res.status_code == 200:
                core = res.json().get("resources", {}).get("core", {})
                return {
                    "limit": core.get("limit", 60),
                    "remaining": core.get("remaining", 60),
                    "reset": core.get("reset")
                }
        except Exception:
            pass
        return {"limit": 60, "remaining": "Unknown", "reset": None}

    def fetch_repository_data(self, repo_url: str) -> Dict[str, Any]:
        """
        Fetches repository metadata, README, file tree, and dependency descriptors.
        """
        owner, repo = self.parse_repo_url(repo_url)
        base_api = f"https://api.github.com/repos/{owner}/{repo}"

        # 1. Fetch Repository Metadata
        meta_res = self.session.get(base_api, timeout=8)
        if meta_res.status_code == 404:
            raise FileNotFoundError(f"Repository '{owner}/{repo}' not found. Verify it is public and spelled correctly.")
        elif meta_res.status_code == 403:
            raise PermissionError("GitHub API rate limit exceeded. Please provide a GitHub Personal Access Token in settings.")
        elif meta_res.status_code != 200:
            raise RuntimeError(f"GitHub API error: HTTP {meta_res.status_code} - {meta_res.text}")

        meta = meta_res.json()
        default_branch = meta.get("default_branch", "main")

        # 2. Fetch Languages Breakdown
        lang_res = self.session.get(f"{base_api}/languages", timeout=6)
        languages = lang_res.json() if lang_res.status_code == 200 else {}

        # 3. Fetch README Content
        readme_content = ""
        readme_res = self.session.get(f"{base_api}/readme", timeout=6)
        if readme_res.status_code == 200:
            raw_b64 = readme_res.json().get("content", "")
            try:
                readme_content = base64.b64decode(raw_b64).decode("utf-8", errors="replace")
            except Exception:
                readme_content = ""

        # 4. Fetch File Tree (Recursive)
        tree_res = self.session.get(f"{base_api}/git/trees/{default_branch}?recursive=1", timeout=8)
        tree_files = []
        if tree_res.status_code == 200:
            tree_data = tree_res.json()
            tree_files = [item.get("path") for item in tree_data.get("tree", []) if item.get("type") == "blob"]

        # 5. Inspect Architecture & Signals
        has_tests = any(re.search(r'(?:test|tests|spec|__tests__)/', f, re.I) for f in tree_files)
        has_ci = any(f.startswith(".github/workflows/") for f in tree_files)
        has_docker = any("dockerfile" in f.lower() or "docker-compose" in f.lower() for f in tree_files)
        has_contributing = any("contributing" in f.lower() for f in tree_files)
        has_license = bool(meta.get("license"))

        # 6. Fetch Package Manifest if present
        manifest_content = ""
        manifest_type = "None"
        for candidate in ["requirements.txt", "pyproject.toml", "package.json", "Cargo.toml", "go.mod"]:
            if candidate in tree_files:
                man_res = self.session.get(f"{base_api}/contents/{candidate}", timeout=5)
                if man_res.status_code == 200:
                    raw_man = man_res.json().get("content", "")
                    try:
                        manifest_content = base64.b64decode(raw_man).decode("utf-8", errors="replace")
                        manifest_type = candidate
                        break
                    except Exception:
                        pass

        return {
            "owner": owner,
            "repo": repo,
            "full_name": meta.get("full_name"),
            "description": meta.get("description") or "No description provided.",
            "stars": meta.get("stargazers_count", 0),
            "forks": meta.get("forks_count", 0),
            "watchers": meta.get("watchers_count", 0),
            "open_issues": meta.get("open_issues_count", 0),
            "primary_language": meta.get("language") or "Undetermined",
            "license": meta.get("license", {}).get("name") if meta.get("license") else "No License",
            "topics": meta.get("topics", []),
            "default_branch": default_branch,
            "created_at": meta.get("created_at"),
            "updated_at": meta.get("updated_at"),
            "html_url": meta.get("html_url"),
            "languages": languages,
            "file_count": len(tree_files),
            "tree_samples": tree_files[:40],
            "signals": {
                "has_tests": has_tests,
                "has_ci": has_ci,
                "has_docker": has_docker,
                "has_contributing_guide": has_contributing,
                "has_license": has_license
            },
            "readme_snippet": readme_content[:4000],
            "manifest_type": manifest_type,
            "manifest_snippet": manifest_content[:1500]
        }

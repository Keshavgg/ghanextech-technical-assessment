"""
Tool: Live Web & Knowledge Search Tool
Author: Keshav Jindal
"""

import requests
from typing import Dict, Any

def search_knowledge(query: str, max_results: int = 3) -> Dict[str, Any]:
    """
    Searches online knowledge sources for real-time facts, documentation, or historical details.
    
    Parameters:
        query (str): The search query (e.g. "Who created Python programming language?", "What is RAG in AI?").
        max_results (int): Maximum number of search snippets to retrieve (default 3).
        
    Returns:
        dict: Top relevant knowledge summaries or error notice.
    """
    if not query or not query.strip():
        return {"error": "Query parameter cannot be empty."}

    q_clean = query.strip()
    
    # Strategy 1: Wikipedia REST API Summary
    try:
        wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{requests.utils.quote(q_clean)}"
        wiki_res = requests.get(wiki_url, timeout=5, headers={"User-Agent": "GhanexTechAssessmentBot/1.0"})
        if wiki_res.status_code == 200:
            data = wiki_res.json()
            title = data.get("title")
            extract = data.get("extract")
            page_url = data.get("content_urls", {}).get("desktop", {}).get("page")
            if extract:
                return {
                    "success": True,
                    "source": "Wikipedia",
                    "title": title,
                    "summary": extract,
                    "url": page_url
                }
    except Exception:
        pass

    # Strategy 2: DuckDuckGo Instant Answer API
    try:
        ddg_url = f"https://api.duckduckgo.com/?q={requests.utils.quote(q_clean)}&format=json&no_redirect=1&no_html=1"
        ddg_res = requests.get(ddg_url, timeout=5)
        if ddg_res.status_code == 200:
            data = ddg_res.json()
            abstract = data.get("AbstractText")
            heading = data.get("Heading")
            if abstract:
                return {
                    "success": True,
                    "source": "DuckDuckGo Instant Answer",
                    "title": heading,
                    "summary": abstract,
                    "url": data.get("AbstractURL")
                }
            
            # Related topics fallback
            related = data.get("RelatedTopics", [])
            snippets = []
            for item in related[:max_results]:
                if isinstance(item, dict) and item.get("Text"):
                    snippets.append(item["Text"])
            if snippets:
                return {
                    "success": True,
                    "source": "DuckDuckGo Topics",
                    "title": q_clean,
                    "summary": "\n\n".join(snippets)
                }
    except Exception as e:
        return {"error": f"Search lookup failed: {str(e)}"}

    return {
        "success": False,
        "message": f"No direct summary found for '{q_clean}'. Try rephrasing with specific entity keywords."
    }

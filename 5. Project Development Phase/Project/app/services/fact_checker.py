import requests
from app.config import FACT_CHECK_API


def fact_check(query: str) -> str:
    """
    Return a short Wikipedia summary for the given query.

    Uses the Wikipedia REST API (no API key required). The endpoint returns
    a JSON object with an `extract` field containing the opening paragraph
    of the most relevant article.

    Args:
        query: Search term / topic to look up.

    Returns:
        Summary string, or a user-friendly error message.
    """
    try:
        # Wikipedia REST API: spaces must be replaced with underscores
        formatted_query = query.strip().replace(" ", "_")
        url = f"{FACT_CHECK_API}/{formatted_query}"
        
        # Wikipedia requires a custom User-Agent header to avoid 403 Forbidden responses
        headers = {
            "User-Agent": "PersonalizedNetworkingAssistant/1.0 (contact@example.com)"
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        extract = data.get("extract", "").strip()
        if not extract:
            return "No summary found for this topic."
        return extract
    except requests.exceptions.ConnectionError:
        return "Fact-checking failed: Could not connect to Wikipedia."
    except requests.exceptions.Timeout:
        return "Fact-checking failed: Request timed out."
    except Exception:
        return "Fact-checking failed. Please try a different search term."
import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

MAX_SOURCES = 3


def search(query: str) -> list[dict]:
    """
    Run a Tavily search and return top results.
    Returns list of {"title": str, "url": str}
    """
    response = tavily_client.search(
        query,
        max_results=MAX_SOURCES,
        search_depth="basic",
    )
    results = response.get("results", [])[:MAX_SOURCES]
    return [{"title": r.get("title", r["url"]), "url": r["url"]} for r in results]
import httpx
from bs4 import BeautifulSoup

MAX_CHARS = 2000
SKIP_DOMAINS = {"instagram.com", "twitter.com", "x.com", "youtube.com", "tiktok.com"}


def scrape(url: str) -> str:
    """
    Scrape plain text from a URL. Returns empty string on failure.
    Skips known non-scrapable domains.
    """
    if any(domain in url for domain in SKIP_DOMAINS):
        return ""

    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"}
        resp = httpx.get(url, headers=headers, timeout=8, follow_redirects=True)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        content = soup.find("article") or soup.find("main") or soup.body
        text = content.get_text(separator=" ", strip=True) if content else ""
        return text[:MAX_CHARS]
    except Exception:
        return ""
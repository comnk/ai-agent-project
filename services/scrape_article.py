import httpx

from bs4 import BeautifulSoup

MAX_CHARS_PER_ARTICLE = 3000

def scrape_article(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"}
        resp = httpx.get(url, headers=headers, timeout=8, follow_redirects=True)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
 
        content = soup.find("article") or soup.find("main") or soup.body
        text = content.get_text(separator=" ", strip=True) if content else ""
 
        return text[:MAX_CHARS_PER_ARTICLE]
    except Exception as e:
        return f"[Could not scrape {url}: {e}]"
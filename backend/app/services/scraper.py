import asyncio
import httpx
from bs4 import BeautifulSoup

MAX_CHARS = 2000
SKIP_DOMAINS = {"instagram.com", "twitter.com", "x.com", "youtube.com", "tiktok.com"}

async_client = None
 
def get_client() -> httpx.AsyncClient:
    global async_client
    if async_client is None:
        async_client = httpx.AsyncClient(
            headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"},
            timeout=8,
            follow_redirects=True,
        )
    return async_client

def extract_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    content = soup.find("article") or soup.find("main") or soup.body
    text = content.get_text(separator=" ", strip=True) if content else ""
    return text[:MAX_CHARS]
 
 
def scrape(url: str) -> str:
    if any(domain in url for domain in SKIP_DOMAINS):
        return ""
    try:
        with httpx.Client(
            headers={"User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"},
            timeout=8,
            follow_redirects=True,
        ) as client:
            resp = client.get(url)
            resp.raise_for_status()
            return extract_text(resp.text)
    except Exception:
        return ""
 
 
async def scrape_async(url: str) -> str:
    if any(domain in url for domain in SKIP_DOMAINS):
        return ""
    try:
        client = get_client()
        resp = await client.get(url)
        resp.raise_for_status()
        return extract_text(resp.text)
    except Exception:
        return ""
 
 
async def scrape_many(urls: list[str]) -> dict[str, str]:
    tasks = [scrape_async(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return {
        url: (text if isinstance(text, str) else "")
        for url, text in zip(urls, results)
    }
 
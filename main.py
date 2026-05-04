import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from tavily import TavilyClient
from google import genai

from models.research import ResearchRequest, ResearchResponse
from models.source import Source
from services.scrape_article import scrape_article
from services.build_prompt import build_prompt

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TAVILY_API_KEY:
    raise RuntimeError("TAVILY_API_KEY not set in environment")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in environment")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
gemini_client = genai.Client()

app = FastAPI(title="Research API - Week 1 MVP")

MAX_SOURCES = 3
MAX_CHARS_PER_ARTICLE = 3000


@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    query = request.query.strip()
    
    if not query:
        raise HTTPException(status_code=400, detail="Query must not be empty")

    try:
        search_response = tavily_client.search(query,
        max_results=MAX_SOURCES,
            search_depth="basic",
            include_answer=False,
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Tavily search failed: {str(e)}")
    
    results = search_response.get("results", [])[:MAX_SOURCES]
    
    if (not results):
        raise HTTPException(status_code=404, detail="No search results found")
    
    scraped_articles = []
    
    for result in results:
        url = result.get("url", "")
        title = result.get("title", url)
        text = scrape_article(url)
        scraped_articles.append({"title": title, "url": url, "text": text})
    
    prompt = build_prompt(query, scraped_articles)
    
    try:
        gemini_response = gemini_client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
        )
        answer = gemini_response.text.strip()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Gemini generation failed: {str(e)}")
    
    sources = [
        Source(title=a["title"], url=a["url"])
        for a in scraped_articles
    ]
 
    return ResearchResponse(answer=answer, sources=sources)
    

@app.get("/health")
def health_check():
    return {"status": "ok"}
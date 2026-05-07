from google.adk.agents import LlmAgent

from services.search import search
from services.scraper import scrape

def search_and_scrape(question: str) -> dict:
    results = search(question)
    sources = []
    
    for result in results:
        text = scrape(result["url"])
        if text:
            sources.append({"url": result["url"], "title": result["title"], "text": text})
    return {
        "question": question,
        "sources": sources,
        "source_count": len(sources),
    }
    
research_agent = LlmAgent(
    name="research_agent",
    model="gemini-3-flash-preview",
    description="Researches sub-questions from the plan using web search.",
    instruction="""You are a research agent. You will receive a research plan in session state under 'plan'.
 
For each task in the plan, call the search_and_scrape tool with the task's question.
After calling the tool for ALL tasks, compile the results into a JSON object:
 
{
  "research_results": [
    {
      "question": "...",
      "summary": "2-3 sentence answer based on sources",
      "sources": ["url1", "url2"],
      "confidence": 0.0-1.0
    }
  ]
}
 
Confidence score: 1.0 if 3 sources, 0.67 if 2, 0.33 if 1, 0.0 if none.
Return ONLY the JSON, no markdown, no explanation.""",
    tools=[search_and_scrape],
    output_key="research",
)
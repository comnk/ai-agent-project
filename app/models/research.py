from pydantic import BaseModel

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    answer: str
    research_results: list[dict]
    all_sources: list[str]
    session_id: str

    model_config = {"extra": "ignore"}
from pydantic import BaseModel
from .source import Source

class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    answer: str
    sources: list[Source]
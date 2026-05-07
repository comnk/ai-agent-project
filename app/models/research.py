from pydantic import BaseModel

class ResearchRequest(BaseModel):
    query: str
    

class VerificationSummary(BaseModel):
    SUPPORTED: int
    DISPUTED: int
    UNCERTAIN: int
    avg_confidence: float
    total_claims: int   

class ResearchResponse(BaseModel):
    answer: str
    research_results: list[dict]
    extracted_claims: list[dict]
    verifications: list[dict]
    contradictions: list[dict]
    topic_clusters: dict
    verification_summary: VerificationSummary
    claims_stored: int
    similar_past_claims: list[dict]
    all_sources: list[str]
    session_id: str
 
    model_config = {"extra": "ignore"}
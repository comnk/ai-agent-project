from fastapi import APIRouter
from pydantic import BaseModel

from ml.similarity import score_similarity
from ml.stance_classifier import predict_stance

ml_router = APIRouter(prefix="/ml", tags=["ml"])

class StanceRequest(BaseModel):
    claim: str
    evidence: str
 
 
@ml_router.post("/stance")
def test_stance(request: StanceRequest):
    result = predict_stance(request.claim, request.evidence)
    return {"claim": request.claim, "evidence": request.evidence, **result}
 
class SimilarityRequest(BaseModel):
    text_a: str
    text_b: str
 
 
@ml_router.post("/similarity")
def test_similarity(request: SimilarityRequest):
    """Test semantic similarity between two texts."""
    score = score_similarity(request.text_a, request.text_b)
    return {"text_a": request.text_a, "text_b": request.text_b, "similarity": score}
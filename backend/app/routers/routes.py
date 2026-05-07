from fastapi import APIRouter, HTTPException

from models.research import ResearchRequest, ResearchResponse
from orchestrator.pipeline import run_pipeline
from storage.store_claims import get_all_claims, query_similar_claims

router = APIRouter()

@router.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    query = request.query.strip()
    
    if not query:
        raise HTTPException(status_code=400, detail="Query must not be empty")
    try:
        return await run_pipeline(query)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Pipeline error: {e}")

@router.get("/claims/search")
def search_claims(q: str, n: int = 5):
    results = query_similar_claims(q, n_results=n)
    return {"query": q, "results": results, "count": len(results)}
 
 
@router.get("/claims")
def list_claims(limit: int = 50):
    claims = get_all_claims(limit=limit)
    return {"claims": claims, "count": len(claims)}
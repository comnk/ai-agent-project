from fastapi import APIRouter, HTTPException

from models.research import ResearchRequest, ResearchResponse
from orchestrator.pipeline import run_pipeline

router = APIRouter()

@router.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query must not be empty")
 
    try:
        result = await run_pipeline(query)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Pipeline error: {e}")
import json, uuid

from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from agents.planner import planner_agent
from agents.research import research_agent
from agents.writer import writer_agent
from agents.claim_extractor import claim_extractor_agent

from storage.store_claims import add_claims, query_similar_claims

research_pipeline = SequentialAgent(
    name="ResearchPipeline",
    description="Full research pipeline: plan sub-questions, research each, extract claims, write final answer",
    sub_agents=[planner_agent, research_agent, claim_extractor_agent, writer_agent]
)

session_service = InMemorySessionService()

async def run_pipeline(query: str) -> dict:
    """Runs the research pipeline on the given query and returns the final answer."""
    session_id = str(uuid.uuid4())
    
    similar_claims = query_similar_claims(query, n_results=5)
    
    session = await session_service.create_session(
        user_id="api_user",
        app_name="ResearchPipeline",
        session_id=session_id,
        state={"similar_past_claims": similar_claims},
    )
    
    runner = Runner(
        agent=research_pipeline,
        app_name="ResearchPipeline",
        session_service=session_service,
    )
    
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )
    
    async for event in runner.run_async(
        user_id="api_user",
        session_id=session_id,
        new_message=user_message,
    ):
        pass
 
    final_session = await session_service.get_session(
        app_name="ResearchPipeline",
        user_id="api_user",
        session_id=session_id,
    )
    state = final_session.state
 
    research_raw = state.get("research", "{}")
    try:
        research_data = json.loads(research_raw) if isinstance(research_raw, str) else research_raw
        research_results = research_data.get("research_results", [])
    except (json.JSONDecodeError, AttributeError):
        research_results = []
        
    claims_raw = state.get("extracted_claims", "{}")
    try:
        claims_data = json.loads(claims_raw) if isinstance(claims_raw, str) else claims_raw
        extracted_claims = claims_data.get("claims", [])
    except (json.JSONDecodeError, AttributeError):
        extracted_claims = []
 
    stored_ids = []
    if extracted_claims:
        stored_ids = add_claims(extracted_claims, task_id=session_id)
 
    seen = set()
    all_sources = []
    for r in research_results:
        for url in r.get("sources", []):
            if url not in seen:
                seen.add(url)
                all_sources.append(url)
 
    return {
        "answer": state.get("final_answer", "No answer generated."),
        "research_results": research_results,
        "extracted_claims": extracted_claims,
        "claims_stored": len(stored_ids),
        "similar_past_claims": similar_claims,
        "all_sources": all_sources,
        "session_id": session_id,
    }
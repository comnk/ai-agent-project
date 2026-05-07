import json, uuid

from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from agents.planner import planner_agent
from agents.research import research_agent
from agents.writer import writer_agent
from agents.claim_extractor import claim_extractor_agent
from agents.verification import verification_agent
from agents.contradiction import contradiction_agent

from storage.store_claims import add_claims, query_similar_claims

research_pipeline = SequentialAgent(
    name="ResearchPipeline",
    description="Full research pipeline: plan sub-questions, research each, extract claims, verify them, detect contradictions, and write final answer",
    sub_agents=[
        planner_agent,
        research_agent,
        claim_extractor_agent,
        verification_agent,
        contradiction_agent,
        writer_agent,
    ],
)

session_service = InMemorySessionService()

def parse_json_state(raw) -> dict:
    """Safely parse a state value that may be a string or already a dict."""
    if isinstance(raw, dict):
        return raw
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {}

async def run_pipeline(query: str) -> dict:
    """Runs the research pipeline on the given query and returns the final answer."""
    session_id = str(uuid.uuid4())
 
    similar_claims = query_similar_claims(query, n_results=5)
 
    await session_service.create_session(
        app_name="research_app",
        user_id="api_user",
        session_id=session_id,
        state={"similar_past_claims": similar_claims},
    )
 
    runner = Runner(
        agent=research_pipeline,
        app_name="research_app",
        session_service=session_service,
    )
 
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=query)],
    )
 
    async for event in runner.run_async(
        user_id="api_user",
        session_id=session_id,
        new_message=user_message,
    ):
        pass

    final_session = await session_service.get_session(
        app_name="research_app",
        user_id="api_user",
        session_id=session_id,
    )
    state = final_session.state
 
    research_data = parse_json_state(state.get("research", {}))
    research_results = research_data.get("research_results", [])
 
    claims_data = parse_json_state(state.get("extracted_claims", {}))
    extracted_claims = claims_data.get("claims", [])
 
    verifications_data = parse_json_state(state.get("verifications", {}))
    verifications = verifications_data.get("verifications", [])
 
    contradictions_data = parse_json_state(state.get("contradictions", {}))
    contradictions = contradictions_data.get("contradictions", [])
    topic_clusters = contradictions_data.get("topic_clusters", {})
    
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
 
    status_counts = {"SUPPORTED": 0, "DISPUTED": 0, "UNCERTAIN": 0}
    for v in verifications:
        status = v.get("status", "UNCERTAIN")
        status_counts[status] = status_counts.get(status, 0) + 1
 
    avg_confidence = (
        round(sum(v.get("confidence", 0) for v in verifications) / len(verifications), 2)
        if verifications else 0.0
    )
 
    return {
        "answer": state.get("final_answer", "No answer generated."),
        "research_results": research_results,
        "extracted_claims": extracted_claims,
        "verifications": verifications,
        "contradictions": contradictions,
        "topic_clusters": topic_clusters,
        "verification_summary": {
            **status_counts,
            "avg_confidence": avg_confidence,
            "total_claims": len(verifications),
        },
        "claims_stored": len(stored_ids),
        "similar_past_claims": similar_claims,
        "all_sources": all_sources,
        "session_id": session_id,
    }
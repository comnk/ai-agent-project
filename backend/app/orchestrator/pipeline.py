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

from ml.ml_service import enhance_verifications, ml_filter_contradictions

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
 
    async for event in runner.run_async(
        user_id="api_user",
        session_id=session_id,
        new_message=types.Content(
            role="user", parts=[types.Part(text=query)]
        ),
    ):
        pass
 
    final_session = await session_service.get_session(
        app_name="research_app",
        user_id="api_user",
        session_id=session_id,
    )
    state = final_session.state
 
    research_results = parse_json_state(state.get("research", {})).get("research_results", [])
    extracted_claims = parse_json_state(state.get("extracted_claims", {})).get("claims", [])
    verifications = parse_json_state(state.get("verifications", {})).get("verifications", [])
    contradictions_data = parse_json_state(state.get("contradictions", {}))
    contradictions = contradictions_data.get("contradictions", [])
    topic_clusters = contradictions_data.get("topic_clusters", {})
 
    if verifications and extracted_claims:
        verifications = enhance_verifications(verifications, extracted_claims)

    ml_candidate_pairs = []
    if extracted_claims:
        pairs = ml_filter_contradictions(extracted_claims)
        ml_candidate_pairs = [
            {
                "claim_a": p[0].get("claim"),
                "claim_b": p[1].get("claim"),
                "similarity": p[2],
            }
            for p in pairs
        ]
 
    stored_ids = add_claims(extracted_claims, task_id=session_id) if extracted_claims else []
 
    seen = set()
    all_sources = []
    for r in research_results:
        for url in r.get("sources", []):
            if url not in seen:
                seen.add(url)
                all_sources.append(url)
 
    status_counts = {"SUPPORTED": 0, "DISPUTED": 0, "UNCERTAIN": 0}
    for v in verifications:
        status_counts[v.get("status", "UNCERTAIN")] = (
            status_counts.get(v.get("status", "UNCERTAIN"), 0) + 1
        )
 
    avg_confidence = (
        round(sum(v.get("confidence", 0) for v in verifications) / len(verifications), 3)
        if verifications else 0.0
    )
    
    stance_counts = {"SUPPORTS": 0, "OPPOSES": 0, "NEUTRAL": 0}
    for v in verifications:
        stance = v.get("ml_stance", "NEUTRAL")
        stance_counts[stance] = stance_counts.get(stance, 0) + 1
 
    return {
        "answer": state.get("final_answer", "No answer generated."),
        "research_results": research_results,
        "extracted_claims": extracted_claims,
        "verifications": verifications,
        "contradictions": contradictions,
        "topic_clusters": topic_clusters,
        "ml_candidate_pairs": ml_candidate_pairs,
        "verification_summary": {
            **status_counts,
            "avg_confidence": avg_confidence,
            "total_claims": len(verifications),
            "ml_stance_counts": stance_counts,
        },
        "claims_stored": len(stored_ids),
        "similar_past_claims": similar_claims,
        "all_sources": all_sources,
        "session_id": session_id,
    }
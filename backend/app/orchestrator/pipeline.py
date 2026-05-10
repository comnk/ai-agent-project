import asyncio
import json
import uuid

from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from app.agents.planner import planner_agent
from app.agents.research import research_agent
from app.agents.claim_extractor import claim_extractor_agent
from app.agents.verification import verification_agent
from app.agents.contradiction import contradiction_agent
from agents.writer import writer_agent
from app.storage.store_claims import add_claims, query_similar_claims
from app.ml.ml_service import enhance_verifications, ml_filter_contradictions
from app.services.deduplication import deduplicate_claims

research_pipeline = SequentialAgent(
    name="research_pipeline",
    description="Full research pipeline with verification and contradiction detection.",
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
APP_NAME = "research_app"


def parse_json_state(raw) -> dict:
    if isinstance(raw, dict):
        return raw
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {}


async def run_pipeline(query: str) -> dict:
    session_id = str(uuid.uuid4())

    similar_claims_raw = await asyncio.to_thread(query_similar_claims, query, 3)

    similar_claims = [
        {
            "claim": c.get("claim", ""),
            "topic": c.get("topic", ""),
            "source_url": c.get("source_url", ""),
            "similarity": c.get("similarity", 0),
            "claim_type": c.get("claim_type", ""),
        }
        for c in similar_claims_raw
    ]

    await session_service.create_session(
        app_name=APP_NAME,
        user_id="api_user",
        session_id=session_id,
        state={"similar_past_claims": similar_claims},
    )

    runner = Runner(
        agent=research_pipeline,
        app_name=APP_NAME,
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
        app_name=APP_NAME,
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

    from datetime import datetime, timezone
    def now(): return datetime.now(timezone.utc).isoformat()

    execution_trace = [
        {
            "agent": "planner_agent",
            "action": "sub_questions_created",
            "details": {"count": len(research_results), "questions": [r["question"] for r in research_results]},
            "timestamp": now(),
        },
        {
            "agent": "research_agent",
            "action": "sources_gathered",
            "details": {"source_count": len(set(url for r in research_results for url in r.get("sources", []))), "sub_questions": len(research_results)},
            "timestamp": now(),
        },
        {
            "agent": "claim_extractor_agent",
            "action": "claims_extracted",
            "details": {"claim_count": len(extracted_claims), "topics": list({c.get("topic") for c in extracted_claims})},
            "timestamp": now(),
        },
        {
            "agent": "verification_agent",
            "action": "claims_verified",
            "details": {
                "supported": sum(1 for v in verifications if v.get("status") == "SUPPORTED"),
                "disputed": sum(1 for v in verifications if v.get("status") == "DISPUTED"),
                "uncertain": sum(1 for v in verifications if v.get("status") == "UNCERTAIN"),
            },
            "timestamp": now(),
        },
        {
            "agent": "contradiction_agent",
            "action": "contradictions_detected",
            "details": {
                "total_relationships": len(contradictions),
                "conflicts": sum(1 for c in contradictions if c.get("relation") == "CONTRADICTS"),
                "topic_clusters": len(topic_clusters),
            },
            "timestamp": now(),
        },
    ]

    original_count = len(extracted_claims)
    extracted_claims = deduplicate_claims(extracted_claims)

    extracted_claims = extracted_claims[:12]
    duplicates_removed = original_count - len(extracted_claims)

    if verifications and extracted_claims:
        dedup_texts = {c["claim"] for c in extracted_claims}
        verifications = [v for v in verifications if v.get("claim") in dedup_texts]
        verifications = enhance_verifications(verifications, extracted_claims)

    ml_candidate_pairs = []
    if extracted_claims:
        pairs = ml_filter_contradictions(extracted_claims)
        ml_candidate_pairs = [
            {"claim_a": p[0].get("claim"), "claim_b": p[1].get("claim"), "similarity": p[2]}
            for p in pairs
        ]

    execution_trace.append({
        "agent": "ml_layer",
        "action": "stance_analysis_complete",
        "details": {
            "claims_analyzed": len(verifications),
            "candidate_pairs_filtered": len(ml_candidate_pairs),
            "avg_ml_confidence": round(
                sum(v.get("ml_stance_confidence", 0) for v in verifications) / len(verifications), 3
            ) if verifications else 0.0,
        },
        "timestamp": now(),
    })

    stored_ids = add_claims(extracted_claims, task_id=session_id) if extracted_claims else []

    execution_trace.append({
        "agent": "writer_agent",
        "action": "report_generated",
        "details": {
            "claims_stored": len(stored_ids),
            "duplicates_removed": duplicates_removed,
            "session_id": session_id,
        },
        "timestamp": now(),
    })

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
        "execution_trace": execution_trace,
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
        "similar_past_claims": similar_claims_raw,
        "all_sources": all_sources,
        "session_id": session_id,
    }
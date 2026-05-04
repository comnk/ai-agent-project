import json, uuid

from google.adk.agents import SequentialAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from agents.planner import planner_agent
from agents.research import research_agent
from agents.writer import writer_agent

research_pipeline = SequentialAgent(
    name="ResearchPipeline",
    description="Full research pipeline: plan sub-questions, research each, write final answer",
    sub_agents=[planner_agent, research_agent, writer_agent]
)

session_service = InMemorySessionService()

async def run_pipeline(query: str) -> dict:
    """Runs the research pipeline on the given query and returns the final answer."""
    session_id = str(uuid.uuid4())
    
    session = await session_service.create_session(app_name="ResearchPipeline", user_id="api_user", session_id=session_id)
    
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
        "all_sources": all_sources,
        "session_id": session_id,
    }
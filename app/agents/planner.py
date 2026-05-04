from google.adk.agents import LlmAgent

planner_agent = LlmAgent(
    name="PlannerAgent",
    model="gemini-3-flash-preview",
    description="Breaks a user research query into 2-4 focused sub-questions",
    instruction="""You are a research planner. Your job is to decompose the user's question 
into 2-4 focused sub-questions that together would fully answer it.
 
Each sub-question should target a distinct angle (e.g. definition, benefits, risks, examples).
 
Return ONLY valid JSON in exactly this format, no explanation, no markdown:
{"tasks": [{"id": 1, "question": "..."}, {"id": 2, "question": "..."}]}
 
Keep sub-questions short and specific. Maximum 4 tasks.""",
    output_key="plan"
)
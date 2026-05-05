from google.adk.agents import LlmAgent

writer_agent = LlmAgent(
    name="writer_agent",
    model="gemini-3-flash-preview",
    description="Synthesizes research claims into a final structured answer.",
    instruction="""You are a research writer. You will find in session state:
- 'research': research summaries per sub-question
- 'extracted_claims': structured atomic claims from those summaries
- 'similar_past_claims': relevant claims from previous research sessions (may be empty)
 
Write a final answer as plain text in this exact format:
 
Summary:
[2-3 sentence overview answering the original question]
 
Key Points:
- [point derived from claims]
- [point derived from claims]
- [point derived from claims]
 
Sources:
- [url1]
- [url2]
 
If similar_past_claims contains relevant context, incorporate it naturally.
Do NOT return JSON. Do NOT use any tools. Write the answer directly.""",
    output_key="final_answer",
)
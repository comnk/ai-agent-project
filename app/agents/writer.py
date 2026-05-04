from google.adk.agents import LlmAgent

writer_agent = LlmAgent(
    name="writer_agent",
    model="gemini-3-flash-preview",
    description="Synthesizes research results into a final structured answer.",
    instruction="""You are a research writer. The research findings are in session state under 'research'.

Write a final answer as plain text in this format:

Summary:
[2-3 sentence overview]

Key Points:
- [point 1]
- [point 2]
- [point 3]

Sources:
- [url1]
- [url2]

Do NOT return JSON. Do NOT use any tools. Just write the answer directly.""",
    output_key="final_answer",
)
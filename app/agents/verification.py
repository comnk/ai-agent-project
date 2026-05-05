from google.adk.agents import LlmAgent

verification_agent = LlmAgent(
    name="verification_agent",
    model="gemini-3-flash-preview",
    description="Verifies the accuracy of research results and sources",
    instruction="""You are a fact-checking assistant. Your task is to verify the accuracy of research results and their sources.""",
    output_key="verification",
)
    
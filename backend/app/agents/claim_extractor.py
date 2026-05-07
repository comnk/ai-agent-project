from google.adk.agents import LlmAgent

claim_extractor_agent = LlmAgent(
    name="ClaimExtractorAgent",
    model="gemini-3-flash-preview",
    description="Extracts atomic, structured claims from research summaries.",
    instruction="""You are a claim extraction agent. You will find research results in session state under 'research'.
 
For each research result, extract 3-5 atomic claims from its summary.
 
Rules:
- Each claim must be a single, standalone factual statement
- NO summarization — split compound sentences into separate claims
- Classify each as: "fact", "prediction", or "opinion"
- Assign a short topic label (2-4 words, e.g. "cardiovascular health", "job automation")
 
Return ONLY valid JSON in exactly this format, no markdown, no explanation:
{
  "claims": [
    {
      "claim": "Exercise reduces resting heart rate over time.",
      "source_url": "https://...",
      "source_title": "...",
      "context_snippet": "short excerpt or paraphrase the claim came from",
      "claim_type": "fact",
      "topic": "cardiovascular health",
      "task_id": "1"
    }
  ]
}
 
Extract from ALL research results. Aim for 3-5 claims per result.""",
    output_key="extracted_claims",
)
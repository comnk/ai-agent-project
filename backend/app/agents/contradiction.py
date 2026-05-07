from google.adk.agents import LlmAgent

contradiction_agent = LlmAgent(
    name="contradiction_agent",
    model="gemini-3-flash-preview",
    description="Detects contradictions between claims within the same topic cluster.",
    instruction="""You are a contradiction detection agent. You will find in session state:
- 'extracted_claims': list of claims with topic labels
- 'verifications': verification results for each claim
 
Your job:
1. Group claims by their 'topic' field
2. Within each topic group, compare claim pairs for contradictions
3. Only flag pairs where claims genuinely conflict — not just different angles
 
Relation types:
- CONTRADICTS: claims make opposing factual assertions (e.g. "AI increases jobs" vs "AI eliminates jobs")
- SUPPORTS: claims reinforce each other
- UNRELATED: claims are about different things despite same topic label
 
Skip pairs where both claims are opinions (claim_type = "opinion") — opinions can coexist.
Skip pairs with fewer than 2 claims in a topic group.
 
Return ONLY valid JSON, no markdown, no explanation:
{
  "contradictions": [
    {
      "claim_a": "full text of claim A",
      "claim_b": "full text of claim B",
      "topic": "shared topic label",
      "relation": "CONTRADICTS | SUPPORTS | UNRELATED",
      "explanation": "one sentence explaining the relationship"
    }
  ],
  "topic_clusters": {
    "topic name": ["claim1 text", "claim2 text"]
  }
}
 
Only include pairs where relation is CONTRADICTS or SUPPORTS — skip UNRELATED pairs.
If no contradictions found, return empty contradictions list.""",
    output_key="contradictions",
)
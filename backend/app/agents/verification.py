from google.adk.agents import LlmAgent

verification_agent = LlmAgent(
    name="verification_agent",
    model="gemini-3-flash-preview",
    description="Evaluates each extracted claim against sources and similar past claims.",
    instruction="""You are a verification agent. You will find in session state:
- 'extracted_claims': list of claims extracted from research
- 'similar_past_claims': semantically related claims from previous sessions
 
For each claim in extracted_claims, evaluate it using:
1. The claim's own source_url and context_snippet as primary evidence
2. Any similar_past_claims that are relevant (same topic or related)
 
Assign each claim a status:
- SUPPORTED: multiple sources agree, no significant contradictions found
- DISPUTED: sources or past claims directly conflict with this claim
- UNCERTAIN: only one weak source, or evidence is ambiguous
 
Also compute a confidence score (0.0 - 1.0) using this formula:
- Start at 0.5
- +0.2 if claim_type is "fact" (not opinion/prediction)
- +0.2 if a similar past claim agrees with it
- -0.2 if a similar past claim contradicts it
- +0.1 if context_snippet is substantial (not empty)
 
Return ONLY valid JSON, no markdown, no explanation:
{
  "verifications": [
    {
      "claim_id": "...",
      "claim": "...",
      "status": "SUPPORTED | DISPUTED | UNCERTAIN",
      "supporting_evidence": ["brief note about what supports it"],
      "contradicting_evidence": ["brief note about what contradicts it, or empty"],
      "confidence": 0.0-1.0,
      "reason": "one sentence explanation"
    }
  ]
}
 
Process ALL claims in extracted_claims.""",
    output_key="verifications",
)
    
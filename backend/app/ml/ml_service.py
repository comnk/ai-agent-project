from ml.stance_classifier import predict_stance_batch
from ml.similarity import score_similarity, filter_claim_pairs, SIMILARITY_THRESHOLD

def enhance_verifications(
    verifications: list[dict],
    extracted_claims: list[dict],
) -> list[dict]:
    claims_by_text = {c["claim"]: c for c in extracted_claims}

    pairs = []
    for v in verifications:
        claim_text = v.get("claim", "")
        meta = claims_by_text.get(claim_text, {})
        evidence = meta.get("context_snippet", "") or " ".join(v.get("supporting_evidence", []))
        pairs.append({"claim": claim_text, "evidence": evidence})

    stance_results = predict_stance_batch(pairs)

    enhanced = []
    for v, stance in zip(verifications, stance_results):
        claim_text = v.get("claim", "")
        meta = claims_by_text.get(claim_text, {})
        context = meta.get("context_snippet", "")

        similarity_score = score_similarity(claim_text, context) if context else 0.5

        status_score = {"SUPPORTED": 0.8, "UNCERTAIN": 0.5, "DISPUTED": 0.2}.get(
            v.get("status", "UNCERTAIN"), 0.5
        )

        stance_score = {"SUPPORTS": 0.9, "NEUTRAL": 0.5, "OPPOSES": 0.1}.get(
            stance.get("stance", "NEUTRAL"), 0.5
        ) * stance.get("confidence", 0.5)

        final_confidence = round(
            0.5 * status_score + 0.3 * stance_score + 0.2 * similarity_score, 3
        )

        enhanced.append({
            **v,
            "ml_stance": stance.get("stance"),
            "ml_stance_confidence": stance.get("confidence"),
            "ml_similarity": round(similarity_score, 3),
            "ml_confidence": final_confidence,
            "confidence": final_confidence,
        })

    return enhanced


def ml_filter_contradictions(claims: list[dict]) -> list[tuple]:
    """
    Use semantic similarity to pre-filter claim pairs before LLM contradiction check.
    Only returns pairs above SIMILARITY_THRESHOLD — saves LLM calls.

    Returns list of (claim_a, claim_b, similarity) tuples.
    """
    return filter_claim_pairs(claims, threshold=SIMILARITY_THRESHOLD)
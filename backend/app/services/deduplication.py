from ml.similarity import score_similarity

DEDUP_THRESHOLD = 0.92


def deduplicate_claims(claims: list[dict]) -> list[dict]:
    if len(claims) <= 1:
        return claims

    kept = []
    kept_texts = []

    for claim in claims:
        claim_text = claim.get("claim", "")
        if not claim_text:
            continue

        is_duplicate = False
        for existing_text in kept_texts:
            sim = score_similarity(claim_text, existing_text)
            if sim >= DEDUP_THRESHOLD:
                is_duplicate = True
                break

        if not is_duplicate:
            kept.append(claim)
            kept_texts.append(claim_text)

    return kept
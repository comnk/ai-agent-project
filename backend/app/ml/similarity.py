import numpy as np
from sentence_transformers import SentenceTransformer

_model = None
SIMILARITY_THRESHOLD = 0.45


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))


def score_similarity(text_a: str, text_b: str) -> float:
    """
    Compute cosine similarity between two texts.
    Returns 0.0-1.0, where 1.0 = identical meaning.
    """
    model = _get_model()
    embeddings = model.encode([text_a, text_b], normalize_embeddings=True)
    return round(cosine_similarity(embeddings[0], embeddings[1]), 3)


def filter_claim_pairs(claims: list[dict], threshold: float = SIMILARITY_THRESHOLD) -> list[tuple]:
    """
    Given a list of claims, return pairs that are semantically similar enough
    to be worth comparing for contradictions.

    Returns list of (claim_a, claim_b, similarity_score) tuples.
    """
    if len(claims) < 2:
        return []

    model = _get_model()
    texts = [c.get("claim", "") for c in claims]
    embeddings = model.encode(texts, normalize_embeddings=True)

    pairs = []
    for i in range(len(claims)):
        for j in range(i + 1, len(claims)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            if sim >= threshold:
                pairs.append((claims[i], claims[j], round(sim, 3)))

    return pairs
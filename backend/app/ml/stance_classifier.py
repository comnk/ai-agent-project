import hashlib
import json
from pathlib import Path

from transformers import pipeline

MODEL_NAME = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
CACHE_PATH = Path("./ml_cache/stance_cache.json")

_classifier = None


def get_classifier():
    global _classifier
    if _classifier is None:
        print(f"[StanceClassifier] Loading {MODEL_NAME} (first run only)...")
        _classifier = pipeline(
            "zero-shot-classification",
            model=MODEL_NAME,
            device=-1,
        )
        print("[StanceClassifier] Model loaded.")
    return _classifier


def load_cache() -> dict:
    if CACHE_PATH.exists():
        with open(CACHE_PATH) as f:
            return json.load(f)
    return {}


def save_cache(cache: dict):
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f)


def cache_key(claim: str, evidence: str) -> str:
    return hashlib.md5(f"{claim.strip()}|||{evidence.strip()}".encode()).hexdigest()


NLI_TO_STANCE = {
    "entailment": "SUPPORTS",
    "neutral": "NEUTRAL",
    "contradiction": "OPPOSES",
}


def predict_stance(claim: str, evidence: str) -> dict:
    """
    Predict the stance of evidence toward a claim.

    Returns:
        {
            "stance": "SUPPORTS | OPPOSES | NEUTRAL",
            "confidence": 0.0-1.0,
            "raw_scores": {"entailment": ..., "neutral": ..., "contradiction": ...}
        }
    """
    if not claim.strip() or not evidence.strip():
        return {"stance": "NEUTRAL", "confidence": 0.0, "raw_scores": {}}

    key = cache_key(claim, evidence)
    cache = load_cache()

    if key in cache:
        return cache[key]

    classifier = get_classifier()

    result = classifier(
        sequences=evidence,
        candidate_labels=["entailment", "neutral", "contradiction"],
        hypothesis_template="This text {}s the claim: " + claim,
    )

    scores = dict(zip(result["labels"], result["scores"]))
    top_label = result["labels"][0]

    output = {
        "stance": NLI_TO_STANCE.get(top_label, "NEUTRAL"),
        "confidence": round(scores[top_label], 3),
        "raw_scores": {NLI_TO_STANCE[k]: round(v, 3) for k, v in scores.items()},
    }

    cache[key] = output
    save_cache(cache)

    return output


def predict_stance_batch(pairs: list[dict]) -> list[dict]:
    """
    Run stance prediction for a list of {claim, evidence} dicts.
    Loads cache once, saves once — efficient for batch use.
    """
    cache = load_cache()
    results = []
    uncached = []

    for i, pair in enumerate(pairs):
        claim = pair.get("claim", "")
        evidence = pair.get("evidence", "")
        key = cache_key(claim, evidence)
        if key in cache:
            results.append((i, cache[key]))
        else:
            uncached.append((i, claim, evidence, key))

    if uncached:
        classifier = get_classifier()
        for i, claim, evidence, key in uncached:
            if not claim.strip() or not evidence.strip():
                output = {"stance": "NEUTRAL", "confidence": 0.0, "raw_scores": {}}
            else:
                result = classifier(
                    sequences=evidence,
                    candidate_labels=["entailment", "neutral", "contradiction"],
                    hypothesis_template="This text {}s the claim: " + claim,
                )
                scores = dict(zip(result["labels"], result["scores"]))
                top_label = result["labels"][0]
                output = {
                    "stance": NLI_TO_STANCE.get(top_label, "NEUTRAL"),
                    "confidence": round(scores[top_label], 3),
                    "raw_scores": {NLI_TO_STANCE[k]: round(v, 3) for k, v in scores.items()},
                }
                cache[key] = output
            results.append((i, output))

        save_cache(cache)

    results.sort(key=lambda x: x[0])
    return [r for _, r in results]
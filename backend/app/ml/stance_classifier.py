import hashlib
import json
from pathlib import Path
from transformers import pipeline

MODEL_NAME = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
CACHE_PATH = Path("./ml_cache/stance_cache.json")
MAX_CACHE_ENTRIES = 2000

NLI_TO_STANCE = {
    "entailment": "SUPPORTS",
    "neutral": "NEUTRAL",
    "contradiction": "OPPOSES",
}

classifier = None
cache: dict | None = None


def get_classifier():
    global classifier
    if classifier is None:
        print(f"[StanceClassifier] Loading {MODEL_NAME}...")
        classifier = pipeline(
            "zero-shot-classification",
            model=MODEL_NAME,
            device=-1,
            batch_size=8,
        )
        print("[StanceClassifier] Model loaded.")
    return classifier


def get_cache() -> dict:
    """Load cache from disk once, then keep in memory."""
    global cache
    if cache is None:
        if CACHE_PATH.exists():
            with open(CACHE_PATH) as f:
                cache = json.load(f)
        else:
            cache = {}
    return cache


def save_cache():
    global cache
    if cache is None:
        return
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if len(cache) > MAX_CACHE_ENTRIES:
        keys_to_drop = list(cache.keys())[: len(cache) - MAX_CACHE_ENTRIES]
        for k in keys_to_drop:
            del cache[k]
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f)


def cache_key(claim: str, evidence: str) -> str:
    return hashlib.md5(f"{claim.strip()}|||{evidence.strip()}".encode()).hexdigest()


def parse_result(result: dict) -> dict:
    scores = dict(zip(result["labels"], result["scores"]))
    top_label = result["labels"][0]
    return {
        "stance": NLI_TO_STANCE.get(top_label, "NEUTRAL"),
        "confidence": round(scores[top_label], 3),
        "raw_scores": {NLI_TO_STANCE[k]: round(v, 3) for k, v in scores.items()},
    }


def predict_stance(claim: str, evidence: str) -> dict:
    if not claim.strip() or not evidence.strip():
        return {"stance": "NEUTRAL", "confidence": 0.0, "raw_scores": {}}

    cache = get_cache()
    key = cache_key(claim, evidence)
    if key in cache:
        return cache[key]

    result = get_classifier()(
        sequences=evidence,
        candidate_labels=["entailment", "neutral", "contradiction"],
        hypothesis_template="This text {}s the following statement.",
    )
    output = parse_result(result)
    cache[key] = output
    save_cache()
    return output


def predict_stance_batch(pairs: list[dict]) -> list[dict]:
    cache = get_cache()
    results: list[dict | None] = [None] * len(pairs)
    uncached_indices = []
    uncached_sequences = []
    uncached_claims = []

    for i, pair in enumerate(pairs):
        claim = pair.get("claim", "")
        evidence = pair.get("evidence", "")

        if not claim.strip() or not evidence.strip():
            results[i] = {"stance": "NEUTRAL", "confidence": 0.0, "raw_scores": {}}
            continue

        key = cache_key(claim, evidence)
        if key in cache:
            results[i] = cache[key]
        else:
            uncached_indices.append(i)
            uncached_sequences.append(evidence)
            uncached_claims.append(claim)

    if uncached_sequences:
        classifier = get_classifier()

        batch_results = classifier(
            sequences=uncached_sequences,
            candidate_labels=["entailment", "neutral", "contradiction"],
            hypothesis_template="This text {}s the following statement.",
        )

        if isinstance(batch_results, dict):
            batch_results = [batch_results]

        for idx, (orig_i, claim, result) in enumerate(
            zip(uncached_indices, uncached_claims, batch_results)
        ):
            output = parse_result(result)
            key = cache_key(claim, uncached_sequences[idx])
            cache[key] = output
            results[orig_i] = output

        save_cache()

    return [r or {"stance": "NEUTRAL", "confidence": 0.0, "raw_scores": {}} for r in results]
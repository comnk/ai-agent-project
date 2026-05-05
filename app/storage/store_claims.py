import uuid

from datetime import datetime, timezone
from .chroma_client import get_claims_collection


def add_claims(claims: list[dict], task_id: str = "") -> list[str]:
    collection = get_claims_collection()
    
    documents = []
    metadatas = []
    ids = []
    
    for claim in claims:
        claim_id = str(uuid.uuid4())
        documents.append(claim["claim"])
        metadatas.append({
            "claim_id": claim_id,
            "topic": claim.get("topic", "general"),
            "source_url": claim.get("source_url", ""),
            "source_title": claim.get("source_title", ""),
            "context_snippet": claim.get("context_snippet", "")[:500],
            "claim_type": claim.get("claim_type", "fact"),
            "task_id": task_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        ids.append(claim_id)
    
    if documents:
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
        )
    
    return ids

def query_similar_claims(query: str, n_results: int = 5) -> list[dict]:
    collection = get_claims_collection()
    
    count = collection.count()
    
    if count == 0:
        return []
    
    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, count),
        include=["documents", "metadatas", "distances"],
    )
    
    claims = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        claims.append({
            "claim": doc,
            "similarity": round(1 - dist, 3),
            **meta,
        })
 
    return claims

def get_all_claims(limit: int = 100) -> list[dict]:
    collection = get_claims_collection()
    
    count = collection.count()
    
    if count == 0:
        return []
    
    results = collection.get(
        limit=min(limit, count),
        include=["documents", "metadatas"],
    )
 
    return [
        {"claim": doc, **meta}
        for doc, meta in zip(results["documents"], results["metadatas"])
    ]
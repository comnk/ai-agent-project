import chromadb

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

chroma_client = None
embedding_function = None

def get_chroma_client():
    global chroma_client
    if chroma_client is None:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
    return chroma_client

def get_embedding_function():
    global embedding_function
    if embedding_function is None:
        embedding_function = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    return embedding_function

def get_claims_collection() -> chromadb.Collection:
    client = get_chroma_client()
    return client.get_or_create_collection(
        name="claims",
        embedding_function=get_embedding_function(),
        metadata={"hnsw:space": "cosine"},
    )
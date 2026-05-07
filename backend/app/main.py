import os

from dotenv import load_dotenv
from fastapi import FastAPI

from routers.routes import router
from routers.ml import ml_router

load_dotenv()
 
for key in ("TAVILY_API_KEY", "GOOGLE_API_KEY", "CHROMA_DB_KEY"):
    if not os.getenv(key):
        raise RuntimeError(f"{key} not set in environment")


app = FastAPI(title="Research API - Week 1 MVP")
app.include_router(router)
app.include_router(ml_router)
    

@app.get("/health")
def health_check():
    return {"status": "ok"}
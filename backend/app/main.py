import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routers.routes import router
from app.routers.ml import ml_router

from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
 
for key in ("TAVILY_API_KEY", "GOOGLE_API_KEY", "CHROMA_DB_KEY"):
    if not os.getenv(key):
        raise RuntimeError(f"{key} not set in environment")


app = FastAPI(title="Research API - Week 1 MVP")
app.include_router(router)
app.include_router(ml_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}
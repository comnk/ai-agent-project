import os

from dotenv import load_dotenv
from fastapi import FastAPI

from routers.routes import router

load_dotenv()
 
for key in ("TAVILY_API_KEY", "GOOGLE_API_KEY"):
    if not os.getenv(key):
        raise RuntimeError(f"{key} not set in environment")


app = FastAPI(title="Research API - Week 1 MVP")
app.include_router(router)
    

@app.get("/health")
def health_check():
    return {"status": "ok"}
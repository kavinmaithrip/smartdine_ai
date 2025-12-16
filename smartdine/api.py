import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# --------------------------------------------------
# Path setup
# --------------------------------------------------

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

# --------------------------------------------------
# Logging
# --------------------------------------------------

from backend.logging import logger

# --------------------------------------------------
# Core recommender
# --------------------------------------------------

from src.recommender import SmartDineRecommender


# ============================================================
# Initialize FastAPI app
# ============================================================

app = FastAPI(
    title="SmartDine Recommendation API",
    description="AI-powered, city-aware, mood-based food recommendation engine",
    version="1.3.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load recommender once (singleton)
logger.info("[API] Loading SmartDine Recommender...")
recommender = SmartDineRecommender()
logger.info("[API] SmartDine Recommender ready.")


# ============================================================
# Request schema
# ============================================================

class RecommendRequest(BaseModel):
    query: str
    city: str
    surprise: Optional[bool] = False
    session_id: Optional[str] = "default"  # ✅ NEW (safe fallback)


# ============================================================
# Routes
# ============================================================

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "SmartDine",
        "message": "SmartDine API is running"
    }


@app.get("/cities")
def get_cities():
    cities = sorted(recommender.df["City"].unique().tolist())
    return {"cities": cities}


@app.post("/recommend")
def recommend(req: RecommendRequest):
    """
    Main recommendation endpoint.
    """
    try:
        city = req.city.strip().lower()
        query = req.query.strip()
        session_id = req.session_id or "default"

        logger.info(
            f"[REQUEST] session={session_id} | city='{city}' | query='{query}' | surprise={req.surprise}"
        )

        response = recommender.recommend(
            query=query,
            city=city,
            surprise=req.surprise,
            session_id=session_id   # ✅ PASSED THROUGH
        )

        logger.info(
            f"[RESPONSE] session={session_id} | city='{city}' | results={len(response.get('results', []))}"
        )

        return response

    except Exception as e:
        logger.exception("[ERROR] Recommendation failed")
        return {
            "error": str(e),
            "message": "Failed to generate recommendation"
        }


# ============================================================
# Run server
# ============================================================

if __name__ == "__main__":
    uvicorn.run(
        "backend.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

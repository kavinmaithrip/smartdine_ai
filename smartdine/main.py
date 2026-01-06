from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from api import recommend_food, surprise_food   # wrapper layer

# ---------------- LOGGING ----------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("smartdine")

# ---------------- APP ----------------
app = FastAPI(title="SmartDine API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MODELS ----------------
class RecommendRequest(BaseModel):
    city: str
    query: str

class SurpriseRequest(BaseModel):
    city: str

# ---------------- ROUTES ----------------
@app.post("/recommend")
def recommend(req: RecommendRequest):
    logger.info(f"Query='{req.query}' | City='{req.city}'")
    return recommend_food(
        city=req.city,
        query=req.query
    )

@app.post("/surprise")
def surprise(req: SurpriseRequest):
    logger.info(f"Surprise request | City='{req.city}'")

    return surprise_food(req.city)

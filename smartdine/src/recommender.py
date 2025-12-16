import os
import sys
import random
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv


load_dotenv()

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.append(SRC_DIR)



from mood_model import MoodModel
from faiss_index import search_city
from utils import load_csv
from weather import get_weather
from llm_explainer import LLMExplainer
from memory import SessionMemory   

DATA_PATH = "D:/Deltaforge/smartdine/data/processed/smartdine_preprocessed.csv"
SENTENCE_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

FAISS_TOP_K = 40
RETURN_K = 3
MIN_RATING = 4.0


class SmartDineRecommender:

    def __init__(self):
        print("[SmartDine] Initializing recommender...")
        self.df = load_csv(DATA_PATH)
        self.model = SentenceTransformer(SENTENCE_MODEL)
        self.mood_model = MoodModel()
        self.explainer = LLMExplainer()
        self.memory = SessionMemory()   
        print("[SmartDine] Ready.")

    
    def encode_query(self, query: str) -> np.ndarray:
        return self.model.encode([query], convert_to_numpy=True).astype("float32")

   
    def surprise_recommend(self, city: str, session_id: str):
        city_df = self.df[self.df["City"].str.lower() == city]

        if city_df.empty:
            return None

        weather = get_weather(city)
        category = weather.get("category")

        if category in ["cold", "rainy"]:
            pool = city_df[city_df["Cuisine"].str.contains("spicy|tandoor|grill|soup", case=False, na=False)]
        elif category == "hot":
            pool = city_df[city_df["Cuisine"].str.contains("salad|juice|light|cool", case=False, na=False)]
        else:
            pool = city_df

        if pool.empty:
            pool = city_df

        item = pool.sample(1).iloc[0].to_dict()

        use_weather = random.random() < 0.6

        item["explanation"] = self.explainer.explain(
            item=item,
            city=city.title(),
            mood="surprise",
            weather=weather if use_weather else None,
            surprise=True
        )

        return item


    def feature_score(self, item, intents, weather, memory):
        score = 0.0

        score += 0.4 * (item.get("Average_Rating", 0) / 5)
        score += 0.2 * min(item.get("Restaurant_Popularity", 0) / 1000, 1)

        if item.get("Is_Bestseller") == 1:
            score += 0.2

        cuisine = str(item.get("Cuisine", "")).lower()

        if intents.get("cheesy") and any(k in cuisine for k in ["pizza", "italian", "cheese"]):
            score += 0.15

        if intents.get("spicy") and any(k in cuisine for k in ["spicy", "tandoor", "chilli"]):
            score += 0.15

        
        if memory:
            if item.get("Cuisine") in memory.get("cuisines", []):
                score += 0.1    
            if item.get("Item_Name") in memory.get("items", []):
                score -= 0.2    

        
        if weather:
            cat = weather.get("category")
            if cat in ["cold", "rainy"] and intents.get("spicy"):
                score += 0.1
            if cat == "hot" and intents.get("light"):
                score += 0.1

        return score


    def recommend(self, query: str, city: str, surprise: bool = False, session_id: str = "default"):
        city = city.lower().strip()
        weather = get_weather(city)

        memory = self.memory.get(session_id)

        
        if surprise or not query.strip():
            pick = self.surprise_recommend(city, session_id)
            return {
                "mood": "surprise",
                "weather": weather,
                "results": [pick] if pick else []
            }

        
        mood, mood_score, intents = self.mood_model.get_mood(query)

        
        q_emb = self.encode_query(query)
        candidates = search_city(q_emb, city, FAISS_TOP_K)

        candidates = [c for c in candidates if c.get("Average_Rating", 0) >= MIN_RATING]

        if not candidates:
            return {"mood": mood, "weather": weather, "results": []}

        
        for c in candidates:
            c["final_score"] = (
                0.6 * c["semantic_score"]
                + 0.4 * self.feature_score(c, intents, weather, memory)
                + random.uniform(0.03, 0.09)
            )

        ranked = sorted(candidates, key=lambda x: x["final_score"], reverse=True)
        top_pool = ranked[:10]

        weather_item = random.choice(top_pool)
        remaining = [c for c in top_pool if c is not weather_item]
        non_weather = random.sample(remaining, k=min(RETURN_K - 1, len(remaining)))

        final_items = [weather_item] + non_weather
        random.shuffle(final_items)

        
        for item in final_items:
            item["explanation"] = self.explainer.explain(
                item=item,
                city=city.title(),
                mood=mood,
                weather=weather if item is weather_item else None,
                surprise=False
            )

        
        self.memory.update(
            session_id=session_id,
            query=query,
            results=final_items,
            mood=mood,
            city=city
        )

        return {
            "mood": mood,
            "mood_score": round(float(mood_score), 2),
            "weather": weather,
            "results": final_items
        }


if __name__ == "__main__":
    r = SmartDineRecommender()
    sid = "test-session"

    print(r.recommend("something cheesy and italian", "chennai", session_id=sid))
    print(r.recommend("something cheesy and italian", "chennai", session_id=sid))

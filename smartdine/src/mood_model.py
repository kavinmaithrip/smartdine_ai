import re
from sentence_transformers import SentenceTransformer, util
import numpy as np


class MoodModel:
    """
    Extracts:
    - primary mood (comfort, party, healthy, premium, etc.)
    - intent signals (cheap, expensive, cheesy, spicy, sweet)
    """

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

        # ---------------- MOODS ---------------- #
        self.mood_phrases = {
            "comfort": [
                "comfort food", "feeling low", "rough day",
                "tired", "need something filling", "home style"
            ],
            "party": [
                "party", "snacks", "friends", "celebration",
                "fast food", "street food"
            ],
            "healthy": [
                "healthy", "light food", "low calorie",
                "fresh", "diet", "salad"
            ],
            "premium": [
                "luxury", "fine dining", "fancy",
                "premium", "expensive restaurant"
            ],
        }

        # ---------------- INTENTS ---------------- #
        self.intent_keywords = {
            "cheap": [
                "cheap", "affordable", "budget",
                "not expensive", "low price"
            ],
            "expensive": [
                "expensive", "premium", "costly", "luxury"
            ],
            "cheesy": [
                "cheesy", "cheese", "creamy"
            ],
            "spicy": [
                "spicy", "hot", "fiery", "masala"
            ],
            "sweet": [
                "sweet", "dessert", "chocolate", "sugar"
            ]
        }

        # Precompute mood embeddings
        self.mood_embeddings = {
            mood: self.model.encode(phrases, convert_to_tensor=True)
            for mood, phrases in self.mood_phrases.items()
        }

    # -------------------------------------------------
    # Keyword-based intent detection
    # -------------------------------------------------
    def extract_intents(self, text):
        text_lower = text.lower()
        intents = {}

        for intent, words in self.intent_keywords.items():
            intents[intent] = any(
                re.search(rf"\b{w}\b", text_lower) for w in words
            )

        # Handle negation: "not expensive"
        if "not expensive" in text_lower or "not costly" in text_lower:
            intents["cheap"] = True
            intents["expensive"] = False

        return intents

    # -------------------------------------------------
    # Embedding-based mood score
    # -------------------------------------------------
    def detect_mood(self, text):
        query_emb = self.model.encode(text, convert_to_tensor=True)

        scores = {}
        for mood, emb in self.mood_embeddings.items():
            scores[mood] = util.cos_sim(query_emb, emb).mean().item()

        best_mood = max(scores, key=scores.get)

        # Normalize mood score
        vals = list(scores.values())
        score = (scores[best_mood] - min(vals)) / (max(vals) - min(vals) + 1e-6)

        return best_mood, float(score)

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------
    def get_mood(self, text):
        """
        Returns:
        mood: str
        mood_score: float (0–1)
        intents: dict
        """
        mood, mood_score = self.detect_mood(text)
        intents = self.extract_intents(text)

        return mood, mood_score, intents

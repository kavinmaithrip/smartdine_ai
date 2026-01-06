import pandas as pd
import numpy as np


class CityReranker:
    """
    Lightweight, city-aware reranker.
    Refines FAISS candidates using structured features.
    """

    def __init__(self, city_stats_path):
        print(f"[Reranker] Loading city statistics from: {city_stats_path}")

        city_stats = pd.read_csv(city_stats_path)

        # Normalize city key (CRITICAL)
        city_stats["city"] = city_stats["city"].str.lower().str.strip()

        self.city_stats = city_stats.set_index("city").to_dict(orient="index")

        print("[Reranker] City statistics loaded.")

        # Balanced, non-dominating weights
        self.WEIGHTS = {
            "semantic": 0.40,
            "rating_z": 0.25,
            "popularity_z": 0.20,
            "bestseller": 0.10,
            "mood": 0.05
        }

    # -------------------------------------------------
    # City stats
    # -------------------------------------------------
    def get_city_stats(self, city):
        city = city.lower().strip()
        return self.city_stats.get(city, None)

    # -------------------------------------------------
    # Feature computation
    # -------------------------------------------------
    def compute_features(self, df, city, mood_score=0.0):
        stats = self.get_city_stats(city)
        df = df.copy()

        # Safe fallback if stats missing
        if stats is None:
            df["rating_z"] = 0.0
            df["popularity_z"] = 0.0
            df["price_z"] = 0.0
            df["mood_score"] = mood_score
            return df

        # City means
        mean_rating = stats["avg_rating_city"]
        mean_pop = stats["avg_popularity_city"]
        mean_price = stats["avg_price_city"]

        # Robust std (avoid explosion)
        def safe_std(series):
            std = series.std()
            return std if std and std > 1e-3 else 1.0

        std_rating = safe_std(df["Average_Rating"])
        std_pop = safe_std(df["Restaurant_Popularity"])
        std_price = safe_std(df["Prices"])

        df["rating_z"] = (df["Average_Rating"] - mean_rating) / std_rating
        df["popularity_z"] = (df["Restaurant_Popularity"] - mean_pop) / std_pop
        df["price_z"] = (df["Prices"] - mean_price) / std_price

        df["mood_score"] = mood_score

        return df

    # -------------------------------------------------
    # Final score
    # -------------------------------------------------
    def compute_final_score(self, df):
        w = self.WEIGHTS

        df["final_score"] = (
            w["semantic"] * df.get("semantic_score", 0) +
            w["rating_z"] * df["rating_z"] +
            w["popularity_z"] * df["popularity_z"] +
            w["bestseller"] * df["Is_Bestseller"] +
            w["mood"] * df["mood_score"]
        )

        return df

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------
    def rerank(self, df, city, mood_score=0.0):
        if df.empty:
            return df

        df = self.compute_features(df, city, mood_score)
        df = self.compute_final_score(df)

        return (
            df.sort_values("final_score", ascending=False)
              .reset_index(drop=True)
        )


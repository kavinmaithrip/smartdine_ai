import pandas as pd
import numpy as np
import os

# ---------------- PATHS ---------------- #

CLEANED_DATA_PATH = "D:/Deltaforge/smartdine/data/processed/smartdine_cleaned.csv"
CITY_STATS_OUTPUT = "D:/Deltaforge/smartdine/data/processed/city_stats.csv"
PROCESSED_OUTPUT = "D:/Deltaforge/smartdine/data/processed/smartdine_preprocessed.csv"

# ---------------- HELPERS ---------------- #

def normalize_city(city):
    if pd.isna(city):
        return None
    return city.strip().lower()

def price_bucket(is_expensive):
    return "expensive" if is_expensive == 1 else "affordable"

def rating_bucket(is_highly_rated):
    return "highly rated" if is_highly_rated == 1 else "average rated"

# Build conversational, feature-aware embedding text
def build_embedding_text(row):
    return (
        f"Dish: {row['Item_Name']}. "
        f"Cuisine: {row['Cuisine']}. "
        f"Restaurant: {row['Restaurant_Name']}. "
        f"City: {row['city']}. "
        f"Price: {price_bucket(row['Is_Expensive'])}. "
        f"Rating: {rating_bucket(row['Is_Highly_Rated'])}. "
        f"{'Bestseller dish.' if row['Is_Bestseller'] == 1 else 'Regular menu item.'} "
        f"Average restaurant rating {row['Avg_Rating_Restaurant']}. "
        f"Popular choice with {row['Votes']} votes."
    )

# ---------------- LOAD DATA ---------------- #

def load_clean_data(path=CLEANED_DATA_PATH):
    print(f"[INFO] Loading cleaned dataset from: {path}")
    df = pd.read_csv(path)

    required_cols = [
        "Restaurant_Name", "Item_Name", "Cuisine", "City",
        "Prices", "Average_Rating", "Votes",
        "Is_Bestseller", "Is_Expensive", "Is_Highly_Rated",
        "Restaurant_Popularity", "Avg_Rating_Restaurant"
    ]

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"ERROR: Missing required columns: {missing}")

    print(f"[INFO] Loaded dataset with {df.shape[0]} rows.")
    return df

# ---------------- CITY STATS ---------------- #

def compute_city_statistics(df):
    print("[INFO] Computing city-level statistics...")

    city_stats = (
        df.groupby("city")
        .agg(
            avg_price_city=("Prices", "mean"),
            avg_rating_city=("Average_Rating", "mean"),
            avg_popularity_city=("Restaurant_Popularity", "mean"),
            avg_votes_city=("Votes", "mean"),
            restaurant_count=("Restaurant_Name", "count")
        )
        .reset_index()
    )

    return city_stats

# ---------------- NORMALIZATION ---------------- #

def normalize_numeric_columns(df, columns):
    print("[INFO] Normalizing numeric columns...")

    for col in columns:
        if col in df.columns:
            std = df[col].std()
            mean = df[col].mean()
            df[col + "_norm"] = 0.0 if std == 0 else (df[col] - mean) / (std + 1e-8)

    return df

# ---------------- SAVE ---------------- #

def save_outputs(df, city_stats):
    os.makedirs(os.path.dirname(PROCESSED_OUTPUT), exist_ok=True)

    city_stats.to_csv(CITY_STATS_OUTPUT, index=False)
    print(f"[INFO] City statistics saved → {CITY_STATS_OUTPUT}")

    df.to_csv(PROCESSED_OUTPUT, index=False)
    print(f"[INFO] Preprocessed dataset saved → {PROCESSED_OUTPUT}")

# ---------------- MAIN ---------------- #

def preprocess():
    print("\n🚀 Starting SmartDine preprocessing pipeline...\n")

    df = load_clean_data()

    # Normalize city
    df["city"] = df["City"].apply(normalize_city)
    df = df.dropna(subset=["city"])

    print(f"[INFO] Unique cities: {df['city'].nunique()}")

    # Build conversational embedding text
    print("[INFO] Building conversational embedding text...")
    df["embedding_text"] = df.apply(build_embedding_text, axis=1)

    # City statistics
    city_stats = compute_city_statistics(df)

    # Normalize numeric columns (for hybrid ranking later)
    numeric_cols = [
        "Prices",
        "Average_Rating",
        "Restaurant_Popularity",
        "Votes"
    ]
    df = normalize_numeric_columns(df, numeric_cols)

    save_outputs(df, city_stats)

    print("\n✅ Preprocessing completed successfully!\n")

# ---------------- ENTRY ---------------- #

if __name__ == "__main__":
    preprocess()

import pandas as pd
import numpy as np
import re

# -------------------------------------------------
# NORMALIZATION UTILITIES
# -------------------------------------------------

def normalize_text(text):
    """Normalize text for embeddings and matching."""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9 ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def clean_numeric(x):
    """Convert numeric fields safely."""
    try:
        return float(str(x).replace(",", "").strip())
    except:
        return np.nan


def normalize_city(city):
    if pd.isna(city):
        return None
    return city.strip().lower()


def price_bucket(is_expensive):
    return "expensive" if is_expensive == 1 else "affordable"


def rating_bucket(is_highly_rated):
    return "highly rated" if is_highly_rated == 1 else "average rated"


# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

df = pd.read_csv(
    r"D:/Deltaforge/smartdine/data/enhanced_zomato_dataset_clean.csv"
)
print("[INFO] Loaded:", df.shape)

# Normalize column names
df.columns = (
    df.columns.str.strip()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# -------------------------------------------------
# CLEAN TEXT COLUMNS
# -------------------------------------------------

text_cols = [
    "Restaurant_Name",
    "Cuisine",
    "Place_Name",
    "City",
    "Item_Name"
]

for col in text_cols:
    if col in df.columns:
        df[col] = df[col].astype(str).fillna("").str.strip()
        df[col + "_clean"] = df[col].apply(normalize_text)

# Normalize city (CRITICAL for FAISS-per-city)
df["city"] = df["City"].apply(normalize_city)

# -------------------------------------------------
# CLEAN NUMERIC COLUMNS
# -------------------------------------------------

numeric_cols = [
    "Dining_Rating", "Delivery_Rating",
    "Dining_Votes", "Delivery_Votes",
    "Prices", "Votes", "Average_Rating",
    "Total_Votes", "Price_per_Vote",
    "Log_Price", "Restaurant_Popularity",
    "Avg_Rating_Restaurant", "Avg_Price_Restaurant",
    "Avg_Rating_Cuisine", "Avg_Price_Cuisine",
    "Avg_Rating_City", "Avg_Price_City"
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].apply(clean_numeric)

# Fill rating columns first
rating_cols = ["Dining_Rating", "Delivery_Rating", "Average_Rating"]
for col in rating_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

# Fill remaining numeric columns
for col in numeric_cols:
    if col in df.columns:
        df[col] = df[col].fillna(df[col].median())

# -------------------------------------------------
# CLEAN FLAG / BOOLEAN COLUMNS
# -------------------------------------------------

flag_cols = [
    "Is_Bestseller",
    "Best_Seller",
    "Is_Highly_Rated",
    "Is_Expensive"
]

flag_map = {
    "yes": 1, "true": 1, "1": 1, "y": 1, "bestseller": 1,
    "no": 0, "false": 0, "0": 0, "n": 0, "": 0, "nan": 0
}

for col in flag_cols:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.lower()
            .str.strip()
            .apply(lambda x: flag_map.get(x, 0))
            .astype(int)
        )

# -------------------------------------------------
# REMOVE DUPLICATES
# -------------------------------------------------

before = df.shape[0]
df.drop_duplicates(
    subset=["Restaurant_Name", "Item_Name", "Place_Name", "city"],
    keep="first",
    inplace=True
)
after = df.shape[0]
print(f"[INFO] Removed duplicates: {before - after}")

# -------------------------------------------------
# BUILD FEATURE-AWARE EMBEDDING TEXT (KEY CHANGE)
# -------------------------------------------------

def build_embedding_text(row):
    """
    Conversational, feature-aware text for semantic embeddings.
    """
    return normalize_text(
        f"""
        Dish {row['Item_Name']}
        from restaurant {row['Restaurant_Name']}
        serving {row['Cuisine']} cuisine
        located in {row['city']}
        price is {price_bucket(row['Is_Expensive'])}
        rating is {rating_bucket(row['Is_Highly_Rated'])}
        average rating {row['Average_Rating']}
        popular with {row['Votes']} votes
        {'bestseller item' if row['Is_Bestseller'] == 1 else ''}
        comfort food filling tasty
        """
    )

df["embedding_text"] = df.apply(build_embedding_text, axis=1)

# -------------------------------------------------
# FINAL SANITY CHECK
# -------------------------------------------------

df = df.dropna(subset=["embedding_text", "city"])

print("[INFO] Unique cities:", df["city"].nunique())

# -------------------------------------------------
# SAVE OUTPUT
# -------------------------------------------------

df.to_csv(
    r"D:/Deltaforge/smartdine/data/processed/smartdine_cleaned.csv",
    index=False
)

print("[SUCCESS] Final cleaned dataset shape:", df.shape)
print("Cleaning completed successfully.")

import os
import faiss
import pickle
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# ---------------- PATHS ---------------- #

DATA_PATH = "D:/Deltaforge/smartdine/data/processed/smartdine_preprocessed.csv"
FAISS_DIR = "D:/Deltaforge/smartdine/backend/faiss_indexes"
META_DIR = os.path.join(FAISS_DIR, "metadata")

EMBEDDING_DIM = 384
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# ---------------- UTILS ---------------- #

def ensure_dirs():
    os.makedirs(FAISS_DIR, exist_ok=True)
    os.makedirs(META_DIR, exist_ok=True)

# ---------------- BUILD INDEXES ---------------- #

def build_city_faiss_indexes():
    """
    Builds ONE FAISS index PER CITY.
    """
    ensure_dirs()

    print("[INFO] Loading preprocessed dataset...")
    df = pd.read_csv(DATA_PATH)

    if "embedding_text" not in df.columns or "city" not in df.columns:
        raise ValueError("Dataset must contain 'embedding_text' and 'city' columns")

    model = SentenceTransformer(MODEL_NAME)

    for city, city_df in df.groupby("city"):
        print(f"\n[INFO] Building FAISS index for city: {city}")

        texts = city_df["embedding_text"].tolist()

        embeddings = model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        ).astype("float32")

        if embeddings.shape[1] != EMBEDDING_DIM:
            raise ValueError(
                f"Embedding dim mismatch for city {city}. "
                f"Expected {EMBEDDING_DIM}, got {embeddings.shape[1]}"
            )

        # Normalize for cosine similarity
        faiss.normalize_L2(embeddings)

        index = faiss.IndexFlatIP(EMBEDDING_DIM)
        index.add(embeddings)

        # Save index
        index_path = os.path.join(FAISS_DIR, f"{city}.index")
        faiss.write_index(index, index_path)

        # Save metadata aligned with FAISS vectors
        meta_path = os.path.join(META_DIR, f"{city}.pkl")
        with open(meta_path, "wb") as f:
            pickle.dump(city_df.to_dict(orient="records"), f)

        print(f"[SUCCESS] {city}: indexed {index.ntotal} items")

    print("\n✅ FAISS city-wise indexing completed successfully!")

# ---------------- LOAD INDEX ---------------- #

def load_city_index(city):
    """
    Load FAISS index + metadata for a given city.
    """
    city = city.lower().strip()

    index_path = os.path.join(FAISS_DIR, f"{city}.index")
    meta_path = os.path.join(META_DIR, f"{city}.pkl")

    if not os.path.exists(index_path):
        raise ValueError(f"No FAISS index found for city: {city}")

    index = faiss.read_index(index_path)

    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata

# ---------------- SEARCH ---------------- #

def search_city(
    query_embedding: np.ndarray,
    city: str,
    top_k: int = 20
):
    """
    Search FAISS index for a specific city.
    """
    index, metadata = load_city_index(city)

    query_embedding = query_embedding.astype("float32").reshape(1, -1)
    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(query_embedding, top_k)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < len(metadata):
            item = metadata[idx]
            item["semantic_score"] = float(score)
            results.append(item)

    return results

# ---------------- ENTRY ---------------- #

if __name__ == "__main__":
    build_city_faiss_indexes()

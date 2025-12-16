import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import time
import os

DATA_PATH = "D:/Deltaforge/smartdine/data/processed/smartdine_cleaned.csv"
OUTPUT_EMB_PATH = "D:/Deltaforge/smartdine/data/processed/embeddings.npy"
MODEL_NAME = "all-MiniLM-L6-v2"

# Loading cleaned data
df = pd.read_csv(DATA_PATH)

if "embedding_text" not in df.columns:
    raise ValueError("The column 'embedding_text' is missing in your cleaned dataset.")

texts = df["embedding_text"].astype(str).tolist()
print(f"Total rows to embed: {len(texts)}")

#Loading model
print(f"Loading model: {MODEL_NAME} ...")
model = SentenceTransformer(MODEL_NAME)

#Generating embeddings
start_time = time.time()

embeddings = model.encode(
    texts,
    batch_size=64,
    show_progress_bar=True,
    convert_to_numpy=True
)

end_time = time.time()
print(f"Embedding generation completed in {round(end_time - start_time, 2)} seconds.")
print(f"Embedding shape: {embeddings.shape}")

#Save embeddings
os.makedirs(os.path.dirname(OUTPUT_EMB_PATH), exist_ok=True)

np.save(OUTPUT_EMB_PATH, embeddings)

print(f"Embeddings saved to: {OUTPUT_EMB_PATH}")
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Load dataset
df = pd.read_csv("data/cleaned_bookings.csv")

# Combine multiple columns for better semantic search
df["text_data"] = df["hotel"].astype(str) + " " + df["country"].astype(str) + " " + df["reservation_status"].astype(str)

# Convert text data into embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(df['text_data'].tolist())

# Store in FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

# Save the index
faiss.write_index(index, "data/faiss_index.bin")
print("FAISS index created and saved.")

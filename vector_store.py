import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Load Dataset
df = pd.read_csv("data/cleaned_bookings.csv")

# Convert Data to Meaningful Chunks
df['text_chunk'] = df.apply(lambda row: f"Hotel {row['hotel']} has an ADR of {row['adr']} on {row['reservation_status_date']}", axis=1)

# Generate Embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(df['text_chunk'].tolist())

# Build FAISS Index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(np.array(embeddings))

# Save Index
faiss.write_index(index, "data/faiss_index.bin")
print("FAISS index created and saved.")

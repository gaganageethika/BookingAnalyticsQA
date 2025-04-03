from fastapi import FastAPI
from fastapi.responses import FileResponse 
import faiss
import numpy as np
import pandas as pd
import json
from sentence_transformers import SentenceTransformer
import time
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

app = FastAPI()

# Load FAISS index
index = faiss.read_index("data/faiss_index.bin")
model = SentenceTransformer("all-MiniLM-L6-v2")
df = pd.read_csv("data/cleaned_bookings.csv")

# Load precomputed insights
with open("data/insights.json", "r") as f:
    insights = json.load(f)

df['arrival_date'] = pd.to_datetime(df['reservation_status_date'])

@app.get("/query")
async def ask_question(question: str):
    """Handles general question queries."""
    # Check if the question is about revenue trends
    if "revenue trend" in question.lower():
        return {"response": insights["revenue_trend"]}

    # Process question using FAISS
    query_embedding = model.encode([question])
    D, I = index.search(np.array(query_embedding), 1)
    result = df.iloc[I[0][0]]['hotel']
    
    return {"response": f"Closest match: {result}"}

@app.get("/analytics")
async def get_analytics():
    """Returns precomputed analytics."""
    return insights

@app.get("/analytics/plot")
async def get_revenue_plot():
    """Generates and serves the revenue trends visualization as an image"""
    
    # Compute revenue trends
    monthly_revenue = df.groupby(df['arrival_date'].dt.strftime("%Y-%m"))['adr'].sum()

    # Generate the plot
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=monthly_revenue.index, y=monthly_revenue.values, marker="o")
    
    plt.xticks(rotation=45)
    plt.title("Monthly Revenue Trends")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue (ADR)")
    plt.grid(True)
    
    # Save the plot
    plot_path = "data/revenue_trends.png"
    plt.savefig(plot_path)
    plt.close()

    # Return the image file
    return FileResponse(plot_path, media_type="image/png", filename="revenue_trends.png")

# Run the API
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

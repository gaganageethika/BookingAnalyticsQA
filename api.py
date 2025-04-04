from fastapi import FastAPI
from fastapi.responses import FileResponse 
import faiss
import numpy as np
import pandas as pd
import json
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import time
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re

app = FastAPI()

# Load FAISS Index
index = faiss.read_index("data/faiss_index.bin")
model = SentenceTransformer("all-MiniLM-L6-v2")
df = pd.read_csv("data/cleaned_bookings.csv")

# Load Precomputed Insights
with open("data/insights.json", "r") as f:
    insights = json.load(f)

df['arrival_date'] = pd.to_datetime(df['reservation_status_date'])

# Load Open-Source LLM (Choose Model: 'mistral' or 'gpt-neo' etc.)
llm = pipeline("text-generation", model="google/flan-t5-small")

@app.post("/ask")
async def ask_question(question: dict):
    user_question = question.get("question", "").lower()

    # Pattern: Revenue for a specific month/year
    match = re.search(r"revenue.*(?:in|for)\s+(\w+)\s+(\d{4})", user_question)
    if match:
        month, year = match.groups()
        month_map = {
            "january": "01", "february": "02", "march": "03", "april": "04",
            "may": "05", "june": "06", "july": "07", "august": "08",
            "september": "09", "october": "10", "november": "11", "december": "12"
        }

        if month.lower() in month_map:
            month_year = f"{year}-{month_map[month.lower()]}"
            revenue = insights.get("revenue_trend", {}).get(month_year)
            if revenue:
                return {"response": f"Total revenue in {month} {year} was ${revenue:.2f}"}
            else:
                return {"response": f"No revenue data found for {month} {year}."}

    # Pattern: Highest cancellations by location
    if "cancellation" in user_question and "location" in user_question:
        cancel_by_location = df[df['is_canceled'] == 1]['country'].value_counts()
        top_locations = cancel_by_location.head(3).to_dict()
        return {"response": f"Top 3 countries with highest cancellations: {top_locations}"}

    # Pattern: Average price of bookings
    if "average price" in user_question or "average adr" in user_question:
        avg_price = df['adr'].mean()
        return {"response": f"The average price (ADR) of a booking is ${avg_price:.2f}"}

    # No match found – fallback to LLM with FAISS context
    try:
        query_embedding = model.encode([user_question])
        D, I = index.search(np.array(query_embedding), 1)
        matched_row = df.iloc[I[0][0]]

        context = f"User asked: '{user_question}'. Closest booking record: {matched_row.to_dict()}"
        response = llm(context, max_new_tokens=50, do_sample=True)[0]['generated_text']

        return {"response": response}
    except Exception as e:
        return {"response": "Sorry, I couldn't process your question at the moment.", "error": str(e)}



@app.get("/analytics")
async def get_analytics():
    """Returns precomputed analytics."""
    return insights

@app.get("/analytics/plot")
async def get_revenue_plot():
    """Generates and serves the revenue trends visualization as an image"""
    monthly_revenue = df.groupby(df['arrival_date'].dt.strftime("%Y-%m"))['adr'].sum()

    plt.figure(figsize=(10, 5))
    sns.lineplot(x=monthly_revenue.index, y=monthly_revenue.values, marker="o")
    
    plt.xticks(rotation=45)
    plt.title("Monthly Revenue Trends")
    plt.xlabel("Month")
    plt.ylabel("Total Revenue (ADR)")
    plt.grid(True)

    plot_path = "data/revenue_trends.png"
    plt.savefig(plot_path)
    plt.close()

    return FileResponse(plot_path, media_type="image/png", filename="revenue_trends.png")

# Run API Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Load cleaned dataset
df = pd.read_csv("data/cleaned_bookings.csv")

# Revenue trends over time
df['arrival_date'] = pd.to_datetime(df['reservation_status_date'])
monthly_revenue = df.groupby(df['arrival_date'].dt.strftime("%Y-%m"))['adr'].sum().to_dict()


#plt.figure(figsize=(10,5))
#sns.lineplot(x=monthly_revenue.index.astype(str), y=monthly_revenue.values)
#plt.xticks(rotation=45)
#plt.title("Monthly Revenue Trends")
#plt.savefig("data/revenue_trends.png")
#plt.show()

insights = {
    "revenue_trend": monthly_revenue
}

with open("data/insights.json", "w") as f:
    json.dump(insights, f, indent=4)

print("Revenue trends stored in insights.json")

#  Generating the Revenue Trend Plot
plt.figure(figsize=(10, 5))
sns.lineplot(x=list(monthly_revenue.keys()), y=list(monthly_revenue.values()), marker="o")

plt.xticks(rotation=45)
plt.title("Monthly Revenue Trends")
plt.xlabel("Month")
plt.ylabel("Total Revenue (ADR)")
plt.grid(True)

# Save the figure
plt.savefig("data/revenue_trends.png")
plt.show()

print("Revenue trend plot saved as revenue_trends.png")
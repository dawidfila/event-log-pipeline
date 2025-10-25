import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Create output directory for charts and reports
output_dir = Path("data/outputs")
output_dir.mkdir(parents=True, exist_ok=True)

# Connect to MongoDB
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
database = os.getenv("MONGO_DATABASE")

client = MongoClient(
    f"mongodb://{username}:{password}@localhost:27017/{database}",
    authSource="admin"
)

db = client.logs_db
summary_collection = db.daily_summary

# Load aggregated data
logger.info("Loading data from daily_summary collection...")
summary_data = list(summary_collection.find())

if not summary_data:
    logger.warning("No data found in daily_summary collection.")
    client.close()
    exit()

# Convert to DataFrame
df = pd.DataFrame(summary_data)
df["date"] = pd.to_datetime(df["date"])

logger.info(f"Loaded {len(df)} aggregated records")

# ANALYSIS Total Events by Event Type
logger.info("Analysis Events by type")
events_by_type = df.groupby("event_type")["total_events"].sum().sort_values(ascending=False)

plt.figure(figsize=(10, 6))
events_by_type.plot(kind="bar", color="steelblue")
plt.title("Total Events by Event Type", fontsize=16, fontweight="bold")
plt.xlabel("Event Type", fontsize=12)
plt.ylabel("Total Events", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_dir / "events_by_type.png", dpi=300)
logger.info(f"Chart saved: {output_dir / 'events_by_type.png'}")
plt.close()

# ANALYSIS Top 10 Countries by Activity
logger.info("Analysis Top 10 countries")
top_countries = df.groupby("country")["total_events"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12, 6))
top_countries.plot(kind="barh", color="coral")
plt.title("Top 10 Countries by Total Events", fontsize=16, fontweight="bold")
plt.xlabel("Total Events", fontsize=12)
plt.ylabel("Country", fontsize=12)
plt.tight_layout()
plt.savefig(output_dir / "top_countries.png", dpi=300)
logger.info(f"Chart saved: {output_dir / 'top_countries.png'}")
plt.close()

# ANALYSIS Events Over Time
logger.info("Analysis Events over time")
events_over_time = df.groupby("date")["total_events"].sum().sort_index()

plt.figure(figsize=(12, 6))
events_over_time.plot(kind="line", marker="o", color="green", linewidth=2)
plt.title("Events Over Time", fontsize=16, fontweight="bold")
plt.xlabel("Date", fontsize=12)
plt.ylabel("Total Events", fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(output_dir / "events_over_time.png", dpi=300)
logger.info(f"Chart saved: {output_dir / 'events_over_time.png'}")
plt.close()

# ANALYSIS Event Type Distribution by Country (Top 5 countries)
logger.info("Analysis Event distribution by top countries")
top_5_countries = df.groupby("country")["total_events"].sum().sort_values(ascending=False).head(5).index

df_top5 = df[df["country"].isin(top_5_countries)]
event_distribution = df_top5.pivot_table(
    index="country",
    columns="event_type",
    values="total_events",
    aggfunc="sum",
    fill_value=0
)

plt.figure(figsize=(14, 7))
event_distribution.plot(kind="bar", stacked=True, colormap="viridis")
plt.title("Event Type Distribution by Top 5 Countries", fontsize=16, fontweight="bold")
plt.xlabel("Country", fontsize=12)
plt.ylabel("Total Events", fontsize=12)
plt.legend(title="Event Type", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_dir / "event_distribution_top5.png", dpi=300)
logger.info(f"Chart saved: {output_dir / 'event_distribution_top5.png'}")
plt.close()

# ANALYSIS Heatmap - Events by Date and Event Type
logger.info("Analysis Heatmap of events")
heatmap_data = df.pivot_table(
    index="date",
    columns="event_type",
    values="total_events",
    aggfunc="sum",
    fill_value=0
)

plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, annot=False, cmap="YlOrRd", linewidths=0.5)
plt.title("Events Heatmap: Date vs Event Type", fontsize=16, fontweight="bold")
plt.xlabel("Event Type", fontsize=12)
plt.ylabel("Date", fontsize=12)
plt.tight_layout()
plt.savefig(output_dir / "events_heatmap.png", dpi=300)
logger.info(f"Chart saved: {output_dir / 'events_heatmap.png'}")
plt.close()

# Export summary to CSV
logger.info("Exporting summary statistics...")

# Summary Events by type
events_by_type.to_csv(output_dir / "summary_events_by_type.csv")

# Summary Top countries
top_countries.to_csv(output_dir / "summary_top_countries.csv")

# Summary Daily totals
events_over_time.to_csv(output_dir / "summary_daily_events.csv")

logger.info(f"CSV reports saved in {output_dir}")

client.close()
logger.info("Analysis completed successfully!")
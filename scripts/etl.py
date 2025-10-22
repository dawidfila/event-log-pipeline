import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import pandas as pd

load_dotenv()

# Connect to MongoDB
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
database = os.getenv("MONGO_DATABASE")

client = MongoClient(
    f"mongodb://{username}:{password}@localhost:27017/{database}",
    authSource="admin"
)

db = client.logs_db
raw_collection = db.raw_logs
summary_collection = db.daily_summary

# Extract - Load all raw logs from MongoDB
raw_logs = list(raw_collection.find())

if not raw_logs:
    print("No logs found in raw_logs collection.")
    exit()

# Transform - Convert to DataFrame
df = pd.DataFrame(raw_logs)

# Ensure timestamp is datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Create a new column "date" (YYYY-MM-DD)
df["date"] = df["timestamp"].dt.date

# Extract nested fields
df["country"] = df["metadata"].apply(lambda x: x.get("country"))
df["device"] = df["metadata"].apply(lambda x: x.get("device"))

# Aggregate - count number of events per date, country, and event_type
summary_df = (
    df.groupby(["date", "country", "event_type"])
    .size()
    .reset_index(name="total_events")
)

# Load - Save aggregated data into MongoDB collection `daily_summary`
summary_collection.delete_many({})  # (optional) clear previous summary
summary_collection.insert_many(summary_df.to_dict("records"))

print(f"✅ Aggregated {len(summary_df)} records and saved to daily_summary.")
client.close()
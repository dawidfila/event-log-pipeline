import os
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import pandas as pd

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Connect to MongoDB
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
database = os.getenv("MONGO_DATABASE")
mongo_host = os.getenv("MONGO_HOST", "localhost")
mongo_port = os.getenv("MONGO_PORT", "27017")

client = MongoClient(
    f"mongodb://{username}:{password}@{mongo_host}:{mongo_port}/{database}",
    authSource="admin"
)

db = client.logs_db
raw_collection = db.raw_logs
summary_collection = db.daily_summary

# Extract - Load all raw logs from MongoDB
raw_logs = list(raw_collection.find())

if not raw_logs:
    logger.warning("No logs found in raw_logs collection.")
    client.close()
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

# LOAD - Save aggregated data using UPSERT
upsert_count = 0
update_count = 0
insert_count = 0

for record in summary_df.to_dict("records"):
    # Convert date (object datetime.date) to string for MongoDB
    record["date"] = str(record["date"])
    
    # Unique identifier for the record (composite key)
    filter_query = {
        "date": record["date"],
        "country": record["country"],
        "event_type": record["event_type"]
    }
    
    # Excecuting upsert operation
    result = summary_collection.update_one(
        filter_query,           # Find record by date + country + event_type
        {"$set": record},       # If exists - update, if not - insert
        upsert=True            
    )
    
    upsert_count += 1
    
    # Counting how many updates vs inserts
    if result.matched_count > 0:
        update_count += 1
    else:
        insert_count += 1

logger.info(f"Upsert completed: {upsert_count} operations")
logger.info(f"Updated: {update_count}")
logger.info(f"Inserted: {insert_count}")

client.close()
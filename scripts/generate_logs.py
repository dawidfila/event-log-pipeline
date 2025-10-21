import random
import datetime
from faker import Faker
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv() 

fake = Faker()

def generate_log(n=50):
    logs = []
    event_types = ["login", "logout", "purchase", "error", "click", "view"]
    device = ["Mobile", "PC", "Tablet"]
    
    for _ in range(n):
        log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": random.randint(1, 1000),
            "event_type": random.choice(event_types),
            "message": fake.sentence(nb_words=6),
            "metadata": {
                "ip": fake.ipv4(),
                "device": random.choice(device),
                "country": fake.country()
            }
        }
        logs.append(log)
    return logs

def save_to_mongo(logs):
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    database = os.getenv("MONGO_DATABASE")    
    
    client = MongoClient(
        f"mongodb://{username}:{password}@localhost:27017/{database}",
        authSource='admin'
    )
    
    db = client.logs_db
    raw_collection = db.raw_logs
    raw_collection.insert_many(logs)
    print(f"{len(logs)} logs saved in MongoDB")
    client.close()

if __name__ == "__main__":
    logs = generate_log(10)
    save_to_mongo(logs)
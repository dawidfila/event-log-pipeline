import random
import datetime
from faker import Faker

fake = Faker()

def generate_log(n=50):
    logs = []
    event_types = ["login", "logout", "purchase", "error", "click", "view"]
    device = ["Mobile", "PC", "Tablet"]

    for _ in range(n):
        log = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": random.randint(1,1000),
            "event_type": random.choice(event_types),
            "message": fake.sentence(nb_words=6),
            "metdata": {
                "ip": fake.ipv4(),
                "device": random.choice(device),
                "country": fake.country()
            }
        }
        logs.append(log)
    return logs


if __name__ == "__main__":
    logs = generate_log(10)
    for log in logs:
        print(log)
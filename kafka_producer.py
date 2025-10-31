from kafka import KafkaProducer
import json
import time
import random

# Kafka broker
BROKER = 'localhost:9092'
TOPIC = 'spark_test'

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers=BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Continuously send JSON messages
while True:
    message = {
        "user_id": random.randint(1, 1000),
        "event": random.choice(["login", "purchase", "logout"]),
        "amount": round(random.uniform(10, 500), 2)
    }
    producer.send(TOPIC, value=message)
    print(f"Sent: {message}")
    time.sleep(1)  # 1 message per second

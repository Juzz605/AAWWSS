import requests
import random
import time

BACKEND_URL = "http://127.0.0.1:5002/ingest"
MACHINE_ID = "M101"

def generate_sensor_data():
    return {
        "temperature": round(random.uniform(40, 100), 2),
        "vibration": round(random.uniform(1, 10), 2),
        "current": round(random.uniform(10, 50), 2),
        "acoustic": round(random.uniform(20, 90), 2),
        "oil_quality": round(random.uniform(40, 100), 2),
        "pressure": round(random.uniform(30, 110), 2)
    }

while True:
    payload = {
        "machine_id": MACHINE_ID,
        "sensor_values": generate_sensor_data()
    }

    try:
        r = requests.post(BACKEND_URL, json=payload, timeout=2)
        print("Sent:", payload, "Status:", r.status_code)
    except Exception as e:
        print("Error:", e)

    time.sleep(2)

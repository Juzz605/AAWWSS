import requests
import random
import time

BACKEND_URL = "http://127.0.0.1:5000/ingest"

MACHINES = ["M101", "M102", "M103"]

def generate_sensor_data(machine_id):
    return {
        "machine_id": machine_id,
        "temperature": round(random.uniform(40, 100), 2),
        "vibration": round(random.uniform(1, 12), 2),
        "current": round(random.uniform(10, 50), 2),
        "acoustic": round(random.uniform(20, 80), 2),
        "oil_quality": round(random.uniform(20, 90), 2),
        "pressure": round(random.uniform(30, 110), 2)
    }

while True:
    for machine in MACHINES:
        payload = generate_sensor_data(machine)
        try:
            r = requests.post(BACKEND_URL, json=payload, timeout=2)
            print(f"Sent data for {machine} → Status {r.status_code}")
        except Exception as e:
            print("Error:", e)
    time.sleep(2)

import requests
import random
import time

BACKEND = "http://127.0.0.1:5000/ingest"
MACHINES = ["M101", "M102", "M103"]

SENSORS = {
    "temperature": (30, 120),
    "vibration": (0, 15),
    "current": (5, 60),
    "acoustic": (10, 100),
    "oil_quality": (0, 100),
    "pressure": (20, 120)
}

def simulate(sensor):
    low, high = SENSORS[sensor]
    return round(random.uniform(low, high), 2)

while True:
    for m in MACHINES:
        payload = {
            "machine_id": m,
            "sensor_values": {s: simulate(s) for s in SENSORS}
        }
        requests.post(BACKEND, json=payload)
        print("Sent:", payload)
    time.sleep(2)

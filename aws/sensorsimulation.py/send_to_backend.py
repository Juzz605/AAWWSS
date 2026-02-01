import time
import requests
from generate_data import generate_sensor_data

URL = "http://127.0.0.1:5000/upload_sensor"

while True:
    data = generate_sensor_data()
    data["machine_id"] = "machine01"
    r = requests.post(URL, json=data)
    print("Sent:", data, "Status:", r.status_code)
    time.sleep(5)

from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import time

app = Flask(__name__)
CORS(app)

SENSORS = {
    "temperature": (30, 120),
    "vibration": (0, 15),
    "current": (5, 60),
    "acoustic": (10, 100),
    "oil_quality": (0, 100),
    "pressure": (20, 120)
}

WEIGHTS = {
    "temperature": 0.20,
    "vibration": 0.25,
    "current": 0.15,
    "acoustic": 0.15,
    "oil_quality": 0.15,
    "pressure": 0.10
}

WINDOW = 30
machines = {}

def normalize(sensor, value):
    low, high = SENSORS[sensor]
    return ((value - low) / (high - low)) * 100

def calculate_risk(values):
    return round(sum(normalize(s, values[s]) * WEIGHTS[s] for s in values), 2)

def estimate_rul(risk):
    if risk < 40: return "High (>30 days)"
    if risk < 70: return "Medium (10–30 days)"
    return "Low (<10 days)"

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.json
    machine_id = data["machine_id"]

    if machine_id not in machines:
        machines[machine_id] = {
            "sensor_history": {s: [] for s in SENSORS},
            "risk_history": []
        }

    values = data["sensor_values"]

    for s in values:
        machines[machine_id]["sensor_history"][s].append(values[s])
        machines[machine_id]["sensor_history"][s] = machines[machine_id]["sensor_history"][s][-WINDOW:]

    risk = calculate_risk(values)
    machines[machine_id]["risk_history"].append(risk)
    machines[machine_id]["risk_history"] = machines[machine_id]["risk_history"][-WINDOW:]

    return jsonify({"status": "ok"}), 200

@app.route("/live/<machine_id>")
def live(machine_id):
    if machine_id not in machines:
        return jsonify({"error": "No data yet"}), 404

    values = {s: machines[machine_id]["sensor_history"][s][-1] for s in SENSORS}
    risk = machines[machine_id]["risk_history"][-1]

    health = "NORMAL"
    if risk >= 70: health = "CRITICAL"
    elif risk >= 40: health = "WARNING"

    return jsonify({
        "machine_id": machine_id,
        "sensor_values": values,
        "risk_score": risk,
        "machine_health": health,
        "remaining_life": estimate_rul(risk),
        "risk_history": machines[machine_id]["risk_history"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
import numpy as np

app = Flask(__name__)
CORS(app)

# ---------------- CONFIG ----------------
REGION = "ap-south-1"  # change if needed
NAMESPACE = "MachineMonitoring"
WINDOW = 30

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

machines = {}

# CloudWatch client (uses EC2 IAM Role automatically)
cloudwatch = boto3.client("cloudwatch", region_name=REGION)

# ---------------- HELPERS ----------------
def normalize(sensor, value):
    low, high = SENSORS[sensor]
    return ((value - low) / (high - low)) * 100

def calculate_risk(values):
    return round(sum(normalize(s, values[s]) * WEIGHTS[s] for s in values), 2)

def estimate_rul(risk):
    if risk < 40:
        return "High (>30 days)"
    if risk < 70:
        return "Medium (10–30 days)"
    return "Low (<10 days)"

# ---------------- INGEST ROUTE ----------------
@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.json
    machine_id = data["machine_id"]
    values = data["sensor_values"]

    if machine_id not in machines:
        machines[machine_id] = {
            "sensor_history": {s: [] for s in SENSORS},
            "risk_history": []
        }

    # Store history
    for s in values:
        machines[machine_id]["sensor_history"][s].append(values[s])
        machines[machine_id]["sensor_history"][s] = machines[machine_id]["sensor_history"][s][-WINDOW:]

    # Calculate risk
    risk = calculate_risk(values)
    machines[machine_id]["risk_history"].append(risk)
    machines[machine_id]["risk_history"] = machines[machine_id]["risk_history"][-WINDOW:]

    # Push to CloudWatch
    metric_data = []

    for s in values:
        metric_data.append({
            "MetricName": s.capitalize(),
            "Dimensions": [{"Name": "MachineId", "Value": machine_id}],
            "Value": values[s]
        })

    metric_data.append({
        "MetricName": "HealthScore",
        "Dimensions": [{"Name": "MachineId", "Value": machine_id}],
        "Value": risk,
        "Unit": "Percent"
    })

    cloudwatch.put_metric_data(
        Namespace=NAMESPACE,
        MetricData=metric_data
    )

    return jsonify({"status": "ok"}), 200


# ---------------- LIVE ROUTE ----------------
@app.route("/live/<machine_id>")
def live(machine_id):
    if machine_id not in machines:
        return jsonify({"error": "No data yet"}), 404

    values = {s: machines[machine_id]["sensor_history"][s][-1] for s in SENSORS}
    risk = machines[machine_id]["risk_history"][-1]

    health = "NORMAL"
    if risk >= 70:
        health = "CRITICAL"
    elif risk >= 40:
        health = "WARNING"

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

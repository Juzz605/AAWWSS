from flask import Flask, request, jsonify
from dotenv import load_dotenv
from pathlib import Path
import os
import mysql.connector

from db_utils import insert_machine_state, get_latest_state

# =========================
# Load .env safely
# =========================
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# =========================
# Read env variables
# =========================
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = int(os.getenv("DB_PORT"))

print("DEBUG FROM PYTHON")
print("DB_HOST =", repr(DB_HOST))
print("DB_USER =", repr(DB_USER))
print("DB_PASSWORD =", repr(DB_PASSWORD))
print("DB_NAME =", repr(DB_NAME))
print("DB_PORT =", repr(DB_PORT))
# =========================
# Connect to MySQL
# =========================
try:
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    print("✅ MySQL connected successfully")
except mysql.connector.Error as err:
    print("❌ MySQL connection failed")
    print(err)
    exit(1)

# =========================
# Flask app
# =========================
app = Flask(__name__)

@app.route("/upload_sensor", methods=["POST"])
def upload_sensor():
    data = request.json
    insert_machine_state(
        machine_id=data.get("machine_id", "machine01"),
        temperature=data["temperature"],
        vibration=data["vibration"],
        health="Normal"
    )
    return jsonify({"status": "stored"})

@app.route("/machine_state", methods=["GET"])
def machine_state():
    machine_id = request.args.get("machine_id", "machine01")
    state = get_latest_state(machine_id)
    return jsonify(state) if state else ("No data", 404)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

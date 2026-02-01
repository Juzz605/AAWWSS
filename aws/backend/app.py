from flask import Flask, request, jsonify
from db_utils import insert_machine_state, get_latest_state

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

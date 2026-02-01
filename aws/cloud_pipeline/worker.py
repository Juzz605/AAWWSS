import time
import mysql.connector
from ml import detect_anomaly

DB_CONFIG = {
    "host": "localhost",
    "user": "dt_user",
    "password": "password123",
    "database": "digital_twin"
}

def get_latest_sensor():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM machine_state
        ORDER BY timestamp DESC
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    return row

def update_health(record_id, health):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE machine_state
        SET health=%s
        WHERE id=%s
    """, (health, record_id))
    conn.commit()
    conn.close()

while True:
    record = get_latest_sensor()
    if record:
        health = detect_anomaly(record["temperature"], record["vibration"])
        update_health(record["id"], health)
        print("Health updated:", health)
    time.sleep(10)

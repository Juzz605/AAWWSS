import mysql.connector
from datetime import datetime

DB_CONFIG = {
    "host": "localhost",
    "user": "dt_user",
    "password": "password123",
    "database": "digital_twin"
}

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def insert_machine_state(machine_id, temperature, vibration, health):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO machine_state
        (machine_id, timestamp, temperature, vibration, health)
        VALUES (%s, %s, %s, %s, %s)
    """, (machine_id, datetime.utcnow(), temperature, vibration, health))
    conn.commit()
    conn.close()

def get_latest_state(machine_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM machine_state
        WHERE machine_id = %s
        ORDER BY timestamp DESC
        LIMIT 1
    """, (machine_id,))
    row = cursor.fetchone()
    conn.close()
    return row

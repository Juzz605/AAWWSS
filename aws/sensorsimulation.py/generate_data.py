import numpy as np

def generate_sensor_data():
    return {
        "temperature": 60 + np.random.normal(0, 1),
        "vibration": 0.5 + np.random.normal(0, 0.05)
    }

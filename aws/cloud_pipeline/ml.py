import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# 1️⃣ Load sensor data
data = pd.read_csv("sensor_data.csv")
data = data[["temperature", "vibration"]]

# 2️⃣ Scale data
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(data)

# 3️⃣ Create sequences
def create_sequences(data, seq_len=20):
    X, y = [], []
    for i in range(len(data) - seq_len):
        X.append(data[i:i+seq_len])
        y.append(data[i+seq_len])
    return np.array(X), np.array(y)

SEQ_LEN = 20
X, y = create_sequences(scaled_data, SEQ_LEN)

print("X shape:", X.shape)
print("y shape:", y.shape)

# 4️⃣ LSTM model
model = Sequential([
    LSTM(64, input_shape=(SEQ_LEN, 2)),
    Dense(2)
])

model.compile(optimizer="adam", loss="mse")
model.summary()

# 5️⃣ Train (no shuffle for time series)
history = model.fit(
    X, y,
    epochs=25,
    batch_size=16,
    validation_split=0.2,
    shuffle=False,
    verbose=1
)

# 6️⃣ Predict
predictions = model.predict(X)
predicted = scaler.inverse_transform(predictions)
actual = data.iloc[SEQ_LEN:].values

# 7️⃣ Anomaly detection
error = np.mean(np.abs(predicted - actual), axis=1)
threshold = np.percentile(error, 97)
anomalies = error > threshold

# 8️⃣ Plot
plt.figure(figsize=(12,4))
plt.plot(error, label="Prediction Error")
plt.axhline(threshold, color="red", linestyle="--", label="Threshold")
plt.legend()
plt.title("LSTM-based Anomaly Detection")
plt.show()

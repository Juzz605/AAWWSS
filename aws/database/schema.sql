CREATE DATABASE IF NOT EXISTS digital_twin;
USE digital_twin;

CREATE TABLE machine_state (
    id INT AUTO_INCREMENT PRIMARY KEY,
    machine_id VARCHAR(50),
    timestamp DATETIME,
    temperature FLOAT,
    vibration FLOAT,
    health VARCHAR(20)
);

import random
from datetime import datetime, timedelta

ENDPOINTS = ["/api/login", "/api/payment", "/api/products", "/api/cart", "/api/logout"]
LOG_LEVELS = ["INFO", "WARN", "ERROR"]
STATUS_CODES = [200, 200, 200, 200, 201, 400, 404, 500]

def generate_log_line(timestamp, force_anomaly=False):
    endpoint = random.choice(ENDPOINTS)
    
    if force_anomaly and endpoint == "/api/payment":
        # inject anomaly: high latency + error
        status = 500
        level = "ERROR"
        latency = random.randint(2000, 3500)
    else:
        status = random.choice(STATUS_CODES)
        level = "ERROR" if status == 500 else ("WARN" if status in [400, 404] else "INFO")
        latency = random.randint(50, 600)
    
    return f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} {level} GET {endpoint} {status} {latency}"

def generate_logs(num_lines=5000, anomaly_window=(2000, 2100)):
    start_time = datetime(2026, 9, 13, 0, 0, 0)
    lines = []
    for i in range(num_lines):
        ts = start_time + timedelta(seconds=i * 2)
        force_anomaly = anomaly_window[0] <= i <= anomaly_window[1]
        lines.append(generate_log_line(ts, force_anomaly))
    return lines

if __name__ == "__main__":
    logs = generate_logs()
    with open("logs/server.log", "w") as f:
        f.write("\n".join(logs))
    print(f"Generated {len(logs)} log lines in logs/server.log")
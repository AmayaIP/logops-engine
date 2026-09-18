import re
import pandas as pd

LOG_PATTERN = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) '
    r'(?P<log_level>\w+) '
    r'GET '
    r'(?P<endpoint>/\S+) '
    r'(?P<status_code>\d+) '
    r'(?P<latency_ms>\d+)'
)

def parse_log_file(filepath):
    records = []
    with open(filepath, "r") as f:
        for line in f:
            match = LOG_PATTERN.match(line.strip())
            if match:
                records.append(match.groupdict())
    return records

if __name__ == "__main__":
    records = parse_log_file("logs/server.log")
    df = pd.DataFrame(records)
    df["status_code"] = df["status_code"].astype(int)
    df["latency_ms"] = df["latency_ms"].astype(int)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    print(f"Parsed {len(df)} log lines")
    print(df.head())
    print(df.dtypes)
    
    df.to_csv("logs/parsed_logs.csv", index=False)
    print("Saved cleaned data to logs/parsed_logs.csv")
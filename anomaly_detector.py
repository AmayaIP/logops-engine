import duckdb
import pandas as pd

con = duckdb.connect("logops.duckdb")

df = con.execute("SELECT * FROM logs ORDER BY timestamp").fetchdf()

# Calculate Z-score for latency
mean_latency = df["latency_ms"].mean()
std_latency = df["latency_ms"].std()
df["latency_zscore"] = (df["latency_ms"] - mean_latency) / std_latency

# Flag anomaly: Z-score above 3 (common threshold)
df["is_anomaly"] = df["latency_zscore"].abs() > 3

anomalies = df[df["is_anomaly"]]

print(f"Mean latency: {round(mean_latency, 2)} ms")
print(f"Std deviation: {round(std_latency, 2)} ms")
print(f"\nTotal anomalies detected: {len(anomalies)}")
print("\nAnomaly sample:")
print(anomalies[["timestamp", "endpoint", "status_code", "latency_ms", "latency_zscore"]].head(10))

# Save anomalies back to DuckDB
con.execute("CREATE OR REPLACE TABLE anomalies AS SELECT * FROM df WHERE is_anomaly = true")

# Also save full table with zscore column for dashboard use
con.execute("CREATE OR REPLACE TABLE logs_with_zscore AS SELECT * FROM df")

con.close()
print("\nSaved anomalies table + logs_with_zscore table to logops.duckdb")
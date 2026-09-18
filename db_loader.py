import duckdb

# Connect to a local DuckDB file (creates it if not exist)
con = duckdb.connect("logops.duckdb")

# Load CSV into a table
con.execute("""
    CREATE OR REPLACE TABLE logs AS
    SELECT * FROM read_csv_auto('logs/parsed_logs.csv')
""")

# Quick sanity check
total = con.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
print(f"Loaded {total} rows into DuckDB table 'logs'")

# Preview
print(con.execute("SELECT * FROM logs LIMIT 5").fetchdf())

# Core metrics
print("\n--- Core Metrics ---")

error_rate = con.execute("""
    SELECT ROUND(100.0 * SUM(CASE WHEN status_code = 500 THEN 1 ELSE 0 END) / COUNT(*), 2) AS error_rate_pct
    FROM logs
""").fetchone()[0]
print(f"Error Rate: {error_rate}%")

avg_latency = con.execute("SELECT ROUND(AVG(latency_ms), 2) FROM logs").fetchone()[0]
print(f"Average Latency: {avg_latency} ms")

p95 = con.execute("SELECT QUANTILE_CONT(latency_ms, 0.95) FROM logs").fetchone()[0]
p99 = con.execute("SELECT QUANTILE_CONT(latency_ms, 0.99) FROM logs").fetchone()[0]
print(f"P95 Latency: {round(p95, 2)} ms")
print(f"P99 Latency: {round(p99, 2)} ms")

top_failing = con.execute("""
    SELECT endpoint, COUNT(*) AS error_count
    FROM logs
    WHERE status_code = 500
    GROUP BY endpoint
    ORDER BY error_count DESC
    LIMIT 5
""").fetchdf()
print("\nTop Failing Endpoints:")
print(top_failing)

con.close()
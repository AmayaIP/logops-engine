# LogOps-Engine

Application Performance & Log Observability Pipeline

## Overview
LogOps-Engine is an end-to-end observability pipeline that ingests raw server logs, parses and cleans them, stores structured data in a fast analytical database, detects performance anomalies using statistical methods, and visualizes system health on an interactive dashboard.

Built as a lightweight version of tools like Datadog, Grafana, and Splunk.

## Pipeline
Raw Logs → Parse (Regex) → Store (DuckDB) → Metrics (SQL) → Anomaly Detection (Z-score) → Dashboard (Streamlit)


## Features
- **Log Parsing**: Extracts timestamp, log level, endpoint, status code, and latency from raw log lines using Regex
- **Analytical Storage**: DuckDB (columnar OLAP database) for fast SQL queries on structured log data
- **Performance Metrics**: Error rate, average latency, P95/P99 latency, throughput, top failing endpoints
- **Anomaly Detection**: Statistical Z-score method automatically flags latency and error spikes (>3 standard deviations)
- **Interactive Dashboard**: 4-page Streamlit app — Overview, Performance, Errors & Anomalies, Log Explorer

## Tech Stack
- Python
- Regex (`re`)
- Pandas
- DuckDB
- Streamlit
- Plotly

## How to Run
```bash
# Clone the repo
git clone https://github.com/AmayaIP/logops-engine.git
cd logops-engine

# Install dependencies
pip install pandas duckdb streamlit plotly

# Generate synthetic log data
python generator.py

# Parse logs
python parser.py

# Load into DuckDB + compute metrics
python db_loader.py

# Run anomaly detection
python anomaly_detector.py

# Launch dashboard
streamlit run app.py
```

## Project Structure
logops-engine/
├── generator.py # Generates synthetic server logs
├── parser.py # Parses raw logs into structured data
├── db_loader.py # Loads data into DuckDB, computes core metrics
├── anomaly_detector.py # Z-score based anomaly detection
├── app.py # Streamlit dashboard
├── logs/ # Generated log files
└── README.md


## Key Metrics Tracked
- Total Requests
- Error Rate (%)
- Average / P95 / P99 Latency
- Throughput (requests/sec)
- Top Failing Endpoints
- Detected Anomalies (Z-score > 3)

## Future Enhancements
- AI-generated incident explanations (LLM layer)
- Real-time log streaming
- Alerting/notification system
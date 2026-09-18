import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="LogOps-Engine", layout="wide")

con = duckdb.connect("logops.duckdb")
df = con.execute("SELECT * FROM logs_with_zscore ORDER BY timestamp").fetchdf()

st.title("🖥️ LogOps-Engine Dashboard")

page = st.sidebar.radio("Navigate", [" Overview", "📈 Performance", "🚨 Errors & Anomalies", "🔍 Log Explorer"])

# ---------------- OVERVIEW ----------------
if page == " Overview":
    total_requests = len(df)
    error_rate = round(100 * (df["status_code"] == 500).sum() / total_requests, 2)
    p95 = round(df["latency_ms"].quantile(0.95), 2)
    p99 = round(df["latency_ms"].quantile(0.99), 2)
    duration_sec = (df["timestamp"].max() - df["timestamp"].min()).total_seconds()
    throughput = round(total_requests / duration_sec, 2)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total Requests", total_requests)
    col2.metric("Error Rate", f"{error_rate}%")
    col3.metric("P95 Latency", f"{p95} ms")
    col4.metric("P99 Latency", f"{p99} ms")
    col5.metric("Throughput", f"{throughput} req/s")

    st.subheader("Requests Over Time")
    df_time = df.set_index("timestamp").resample("1min").size().reset_index(name="requests")
    fig = px.line(df_time, x="timestamp", y="requests")
    st.plotly_chart(fig, use_container_width=True)

# ---------------- PERFORMANCE ----------------
elif page == "📈 Performance":
    st.subheader("Latency Over Time")
    fig = px.line(df, x="timestamp", y="latency_ms", color="endpoint")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Slowest Endpoints (Avg Latency)")
    slow = df.groupby("endpoint")["latency_ms"].mean().reset_index().sort_values("latency_ms", ascending=False)
    fig2 = px.bar(slow, x="endpoint", y="latency_ms")
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- ERRORS & ANOMALIES ----------------
elif page == "🚨 Errors & Anomalies":
    st.subheader("Error Trend Over Time")
    err_df = df[df["status_code"] == 500]
    err_time = err_df.set_index("timestamp").resample("1min").size().reset_index(name="errors")
    fig3 = px.line(err_time, x="timestamp", y="errors")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Top Failing Endpoints")
    top_fail = err_df["endpoint"].value_counts().reset_index()
    top_fail.columns = ["endpoint", "error_count"]
    fig4 = px.bar(top_fail, x="endpoint", y="error_count")
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("🚨 Detected Anomalies (Z-score > 3)")
    anomalies = df[df["is_anomaly"] == True]
    st.dataframe(anomalies[["timestamp", "endpoint", "status_code", "latency_ms", "latency_zscore"]])

# ---------------- LOG EXPLORER ----------------
elif page == "🔍 Log Explorer":
    st.subheader("Filter Logs")
    col1, col2, col3 = st.columns(3)
    endpoint_filter = col1.multiselect("Endpoint", df["endpoint"].unique())
    level_filter = col2.multiselect("Log Level", df["log_level"].unique())
    status_filter = col3.multiselect("Status Code", df["status_code"].unique())

    filtered = df.copy()
    if endpoint_filter:
        filtered = filtered[filtered["endpoint"].isin(endpoint_filter)]
    if level_filter:
        filtered = filtered[filtered["log_level"].isin(level_filter)]
    if status_filter:
        filtered = filtered[filtered["status_code"].isin(status_filter)]

    st.write(f"Showing {len(filtered)} logs")
    st.dataframe(filtered)

con.close()
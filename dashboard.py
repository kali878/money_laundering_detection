# dashboard.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import plotly.express as px
from src.graph_analysis import build_transaction_graph, calculate_graph_features

st.set_page_config(page_title="Money Laundering Detection Dashboard", layout="wide")

st.title("💸 Money Laundering Detection Dashboard")

# 📂 Upload or load transactions
uploaded_file = st.file_uploader("Upload Transactions CSV", type=["csv"])
if uploaded_file:
    transactions = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload a CSV file with columns: from_account, to_account, amount, timestamp")
    st.stop()

st.subheader("📊 Transactions Data")
st.dataframe(transactions.head())

# 🔹 Transaction Amount Distribution
st.subheader("💰 Transaction Amount Distribution")
fig = px.histogram(
    transactions, 
    x="amount", 
    nbins=30, 
    title="Distribution of Transaction Amounts"
)
st.plotly_chart(fig, use_container_width=True)

# 🔹 Time Series of Transactions
if "timestamp" in transactions.columns:
    transactions["timestamp"] = pd.to_datetime(transactions["timestamp"])
    time_series = transactions.groupby("timestamp")["amount"].sum().reset_index()

    st.subheader("📈 Transactions Over Time")
    fig2 = px.line(
        time_series, 
        x="timestamp", 
        y="amount", 
        title="Total Transaction Amount Over Time"
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("⚠️ No 'timestamp' column found, skipping time-based visualization.")

# 🔹 Graph Visualization
st.subheader("🌐 Transaction Network Graph")
G = build_transaction_graph(transactions)

fig, ax = plt.subplots(figsize=(8, 6))
pos = nx.spring_layout(G, k=0.3)
nx.draw_networkx(
    G, pos, with_labels=True, 
    node_color="skyblue", node_size=600, 
    edge_color="gray", ax=ax
)
st.pyplot(fig)

# 🔹 Graph Features
st.subheader("📌 Graph Features")
features = calculate_graph_features(G)
st.json(features)

# 🔹 Suspicious Transaction Alerts (rule-based example)
st.subheader("🚨 Suspicious Transactions")
suspicious = transactions[transactions["amount"] > 100000]  # rule: > 1 Lakh
if not suspicious.empty:
    st.error("High-value suspicious transactions detected!")
    st.dataframe(suspicious)
else:
    st.success("No suspicious transactions found.")

import streamlit as st
import pandas as pd
import os

st.title("🚨 Alerts Dashboard")

if os.path.exists("data/batch_results.csv"):
    df = pd.read_csv("data/batch_results.csv")
    suspicious = df[df["Prediction"] == "suspicious"]
    st.write("### Suspicious Transactions")
    st.dataframe(suspicious)
else:
    st.warning("No alerts found. Run predictions first.")
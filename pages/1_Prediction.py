import streamlit as st
import pandas as pd
import sys
import os

# --- Fix path so "src" folder accessible ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.model import predict_transaction   # yeh tumhara model ka function

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="💸 MONEY LAUNDERING PATTERN DETECTION", page_icon="💰")

st.title("💸 MONEY LAUNDERING PATTERN DETECTION")
st.write("Yeh app transactions ko predict karega ki wo **Normal** hai ya **Suspicious**.")

# User inputs
amount = st.number_input("Enter Transaction Amount (₹)", min_value=0.0, step=100.0)
country = st.text_input("Enter Country")
account_number = st.text_input("Enter Account Number")
account_age = st.number_input("Enter Account Age (days)", min_value=0, step=1)

# Predict button
if st.button("🔍 Predict"):
    if country.strip() == "":
        st.warning("⚠️ Please enter a country name.")
    else:
        # Call model function
        result = predict_transaction(amount, country, account_number, account_age)
        st.success(f"Prediction Result: **{result}**")

# Show uploaded dataset option
st.subheader("📂 View Sample Transactions")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Uploaded Data Preview:")
    st.dataframe(df.head())
 
import streamlit as st
import pandas as pd
from src.model import predict_transaction
from src.rules import check_suspicious

st.title("🔍 Single & Batch Prediction")

# Single Transaction
st.subheader("Single Transaction")
amount = st.number_input("Transaction Amount", min_value=0)
country = st.text_input("Country")
account_age = st.number_input("Account Age (days)", min_value=0)

if st.button("Predict"):
    txn = {"amount": amount, "country": country, "account_age": account_age}
    result = check_suspicious(txn)
    st.write(f"Prediction: *{result}*")

# Batch Upload
st.subheader("CSV Batch Prediction")
uploaded = st.file_uploader("Upload CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded)
    df["Prediction"] = df.apply(
        lambda row: check_suspicious(row.to_dict()), axis=1
    )
    st.dataframe(df)
    df.to_csv("data/batch_results.csv", index=False)
    st.success("Results saved to data/batch_results.csv")
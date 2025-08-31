import streamlit as st
import pandas as pd
from src.model import predict_transaction   # ye function model.py se aayega

st.title("🔮 Transaction Prediction")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("data/transaction.csv")

df = load_data()

# Show sample transactions
st.subheader("📊 Sample Transactions")
st.dataframe(df.head(10))

# Select transaction for prediction
st.subheader("🔎 Select a Transaction")
txn_id = st.selectbox("Choose Transaction ID", df["transaction_id"].unique())

if st.button("Predict"):
    txn = df[df["transaction_id"] == txn_id].iloc[0].to_dict()
    result = predict_transaction(txn)   # yahan se model ko call karega
    st.write("### 🧾 Prediction Result")
    st.json(result)
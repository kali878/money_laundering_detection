import pandas as pd
import streamlit as st
from src.model import predict_transaction   # tumhara model ka function

# 🔹 Data loading function
def load_data(filename):
    return pd.read_csv(f"data/{filename}")

st.title("💸 Money Laundering Detection App")

# 🔹 Dataset selection
file_choice = st.selectbox(
    "Choose dataset",
    ["transaction.csv", "new_transactions.csv", "transactions_fixed.csv"]
)

# 🔹 Load selected dataset
df = load_data(file_choice)
st.write("📊 Preview of selected data:")
st.dataframe(df.head())

# 🔹 User input for prediction
amount = st.number_input("Transaction Amount", min_value=0.0)
country = st.text_input("Country")
account_age = st.number_input("Account Age (days)", min_value=0)

if st.button("Predict"):
    result = predict_transaction(amount, country, account_age)
    st.success(f"Prediction: {result}")

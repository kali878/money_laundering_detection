from src.scorer import AnomalyScorer
import streamlit as st
from src.model import predict_transaction, predict_from_csv

st.title("💸 Money Laundering Detection App")

choice = st.sidebar.radio("Choose option:", ["🔹 Single Prediction", "📂 Bulk CSV Prediction"])

if choice == "🔹 Single Prediction":
    st.subheader("Enter Transaction Details")

    amount = st.number_input("Transaction Amount", min_value=0.0, format="%.2f")
    country = st.text_input("Country (optional)")
    account_age = st.number_input("Account Age (in days)", min_value=0)

    if st.button("Predict"):
        result = predict_transaction(amount, country, account_age)
        st.success(f"Prediction: {result}")

elif choice == "📂 Bulk CSV Prediction":
    st.subheader("Upload CSV File for Prediction")
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        df = predict_from_csv(uploaded_file)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Predictions", csv, "predictions.csv", "text/csv")

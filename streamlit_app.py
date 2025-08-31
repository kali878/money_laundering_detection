import streamlit as st
import joblib
import pandas as pd

st.title("💸 Money Laundering Detection App")

# Agar aapke paas model.pkl hai to load karna:
# model = joblib.load("model.pkl")

# User inputs
amount = st.number_input("Transaction Amount", min_value=0)
country = st.text_input("Country")
account_age = st.number_input("Account Age (in days)", min_value=0)

if st.button("Predict"):
    # Dummy logic (aap apne model ka use kar sakte ho)
    if amount > 100000 or country.lower() in ["cayman islands", "panama"]:
        st.error("⚠️ Suspicious Transaction (Possible Money Laundering)")
    else:
        st.success("✅ Normal Transaction")

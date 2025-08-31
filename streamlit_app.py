import streamlit as st
import joblib
import pandas as pd

st.title("💸 Money Laundering Detection App")

# Agar aapke paas model.pkl hai to load karna:
# model = joblib.load("model.pkl")

# ------------------- Single Transaction Prediction -------------------
st.header("🔍 Single Transaction Prediction")

amount = st.number_input("Transaction Amount", min_value=0)
country = st.text_input("Country")
account_age = st.number_input("Account Age (in days)", min_value=0)

if st.button("Predict"):
    # Dummy logic (aap apne model ka use kar sakte ho)
    if amount > 100000 or country.lower() in ["cayman islands", "panama"]:
        st.error("⚠️ Suspicious Transaction (Possible Money Laundering)")
    else:
        st.success("✅ Normal Transaction")

# ------------------- Batch Prediction (CSV Upload) -------------------
st.header("📂 CSV Upload for Batch Prediction")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="csv_uploader")

if uploaded_file is not None:
    # Read CSV file
    df = pd.read_csv(uploaded_file)
    st.write("✅ File uploaded successfully!")
    st.write("Preview of your data:", df.head())

    if st.button("Run Batch Prediction"):
        # Example: model prediction
        # NOTE: model ko load karna zaroori hai, warna error aayega
        # predictions = model.predict(df)   
        # df["Prediction"] = predictions

        # Abhi demo ke liye random logic laga dete hain
        df["Prediction"] = ["Suspicious" if x > 100000 else "Normal" for x in df[df.columns[0]]]
        
        st.write("Predictions:", df)

        # Download option
        csv_output = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Predictions",
            data=csv_output,
            file_name="predictions.csv",
            mime="text/csv"
        )

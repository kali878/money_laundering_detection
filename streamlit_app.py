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
import streamlit as st
import pandas as pd

st.title("📂 CSV Upload for Batch Prediction")

# CSV upload option
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
   # CSV Upload
 uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV file
    df = pd.read_csv(uploaded_file)
    st.write("✅ File uploaded successfully!")
    st.write("Preview of your data:", df.head())

    # Agar aapke model ka predict function hai to yaha use kar sakte ho
    if st.button("Run Batch Prediction"):
        # Example: model prediction
        # NOTE: model ko load karna zaroori hai, warna error aayega
        predictions = model.predict(df)   
        df["Prediction"] = predictions
        st.write("Predictions:", df)

        # Agar download bhi karwana ho:
        csv_output = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Predictions",
            data=csv_output,
            file_name="predictions.csv",
            mime="text/csv"
        )

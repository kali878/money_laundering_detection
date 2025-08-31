import streamlit as st
import pandas as pd
import joblib
import os
from src.preprocessing import preprocess_data
from src.model import AnomalyScorer
import matplotlib.pyplot as plt

st.title("💰 Money Laundering Pattern Detection")

# Upload CSV
uploaded_file = st.file_uploader("Upload transactions CSV", type="csv")
if uploaded_file:
    df = preprocess_data(uploaded_file)
    
    # Ensure timestamp is datetime
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
    else:
        st.error("❌ CSV must contain 'timestamp' column")
        st.stop()

    # Check required columns
    required_cols = ["amount_abs", "is_offshore", "is_high_risk_country"]
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        st.error(f"❌ Missing columns: {', '.join(missing_cols)}")
        st.stop()

    st.success("✅ CSV loaded and preprocessed!")

    # Load or train model
    model_path = "reports/compliance/model.pkl"
    if os.path.exists(model_path):
        scorer = joblib.load(model_path)
        st.info("Trained model loaded.")
    else:
        st.warning("No trained model found. Training new model...")
        scorer = AnomalyScorer().fit(df)
        os.makedirs("reports/compliance", exist_ok=True)
        joblib.dump(scorer, model_path)
        st.success("Model trained and saved!")

    # Threshold slider
    threshold = st.slider("Set anomaly threshold", min_value=0.0, max_value=1.0, value=0.5)

    # Score transactions
    if st.button("Score Transactions"):
        df["anomaly_score"] = scorer.score(df)
        df["is_anomaly"] = df["anomaly_score"] > threshold
        st.success("✅ Transactions scored!")

        # Top 5 suspicious
        st.subheader("🚨 Top 5 Suspicious Transactions")
        top5 = df.sort_values("anomaly_score", ascending=False).head(5)
        st.dataframe(top5[["timestamp","amount_abs","is_offshore","is_high_risk_country","anomaly_score","is_anomaly"]])

        # Full table
        st.subheader("📊 All Transactions with Scores")
        st.dataframe(df)

        # Histogram of anomaly scores
        st.subheader("Histogram of Anomaly Scores")
        fig, ax = plt.subplots()
        ax.hist(df["anomaly_score"], bins=30, color='skyblue', edgecolor='black')
        ax.set_xlabel("Anomaly Score")
        ax.set_ylabel("Number of Transactions")
        st.pyplot(fig)

        # Download CSV
        st.download_button("Download Scored CSV", data=df.to_csv(index=False), file_name="scored_transactions.csv")

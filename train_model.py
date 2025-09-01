import pandas as pd
import joblib
import os
from src.scorer import AnomalyScorer

df = pd.read_csv("data/new_transactions.csv")  # ✔️ make sure this file exists

model = AnomalyScorer()

os.makedirs("reports/compliance", exist_ok=True)
joblib.dump(model, "reports/compliance/model.pkl")

print("✅ Model saved successfully.")

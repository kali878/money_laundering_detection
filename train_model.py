# train_model.py
import pandas as pd
import joblib
import os
from src.scorer import AnomalyScorer  # 👈 Make sure you import it from src.scorer

df = pd.read_csv("data/new_transactions.csv")

model = AnomalyScorer()

os.makedirs("reports/compliance", exist_ok=True)
joblib.dump(model, "reports/compliance/model.pkl")

print("✅ Model saved successfully.")

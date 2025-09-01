import pandas as pd
import joblib
from src.scorer import AnomalyScorer
import os

# Sample training data
df = pd.read_csv("data/new_transaction.csv")

# Initialize dummy model
model = AnomalyScorer()

# Save the model properly
os.makedirs("reports/compliance", exist_ok=True)
joblib.dump(model, "reports/compliance/model.pkl")

print("✅ Model saved successfully at reports/compliance/model.pkl")

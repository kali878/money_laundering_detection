import pandas as pd
import joblib
import os
from src.preprocessing import preprocess_data
from src.model import AnomalyScorer   # Important for joblib load

# Load new transactions
new_data_path = "data/new_transactions.csv"
df_new = preprocess_data(new_data_path)

# Ensure timestamp is datetime
df_new["timestamp"] = pd.to_datetime(df_new["timestamp"])

# Load trained anomaly scorer
model_path = "reports/compliance/model.pkl"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model not found at {model_path}, please train first.")

scorer = joblib.load(model_path)

# Score new transactions
df_new["anomaly_score"] = scorer.score(df_new)

# Mark anomalies based on a threshold
threshold = 0.5  # aap customize kar sakte ho
df_new["is_anomaly"] = df_new["anomaly_score"] > threshold

# Save results
output_path = "reports/compliance/new_transactions_scored.csv"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df_new.to_csv(output_path, index=False)

print(f"✅ Scoring complete! Results saved at {output_path}")

# Print top 5 most suspicious transactions
top5 = df_new.sort_values("anomaly_score", ascending=False).head(5)
print("\n🚨 Top 5 most suspicious transactions:")
print(top5[["timestamp", "amount_abs", "is_offshore", "is_high_risk_country", "anomaly_score", "is_anomaly"]])

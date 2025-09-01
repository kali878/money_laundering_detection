# src/model.py
import pandas as pd
import joblib
from src.scorer import AnomalyScorer  # 👈 again, ensure this matches

def predict_transaction(amount, country, account_age):
    model = joblib.load("reports/compliance/model.pkl")
    data = {
        "amount": [amount],
        "country": [country],
        "account_age": [account_age]
    }
    df = pd.DataFrame(data)
    predictions = model.predict(df)
    return predictions[0]

def predict_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    model = joblib.load("reports/compliance/model.pkl")
    predictions = model.predict(df)
    df["prediction"] = predictions
    return df

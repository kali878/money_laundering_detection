import pandas as pd
import joblib
from src.scorer import AnomalyScorer
from src.model import predict_transaction, predict_from_csv

# Single transaction prediction
def predict_transaction(amount, country, account_age):
    model = joblib.load('reports/compliance/model.pkl')
    # Create DataFrame for prediction - add all required features here
    data = {
        "amount": [amount],
        "country": [country],
        "account_age": [account_age]
    }
    df = pd.DataFrame(data)

    # Preprocess if needed (depends on your AnomalyScorer input)
    # Example: df = preprocess_data(df)

    prediction = model.predict(df)
    return prediction[0]

# Bulk CSV prediction
def predict_from_csv(csv_file):
    model = joblib.load('reports/compliance/model.pkl')
    df = pd.read_csv(csv_file)

    # Preprocess if needed
    # df = preprocess_data(df)

    predictions = model.predict(df)
    df['prediction'] = predictions
    return df

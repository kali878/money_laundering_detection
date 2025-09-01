import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "src/model.pkl"

# Train & save model (run once)
def train_and_save_model(csv_path="data/transactions_fixed.csv"):
    df = pd.read_csv(csv_path)

    # Example preprocessing (modify as per dataset)
    X = df[["amount", "account_age"]]  # features
    y = df["label"]  # target (0 = legit, 1 = suspicious)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print("✅ Model trained & saved!")

# Load trained model
def load_model():
    return joblib.load(MODEL_PATH)

# Predict single transaction
def predict_transaction(amount, country, account_age):
    model = load_model()

    # For simplicity, ignoring 'country' now
    X = pd.DataFrame([[amount, account_age]], columns=["amount", "account_age"])
    pred = model.predict(X)[0]
    return "🚨 Suspicious" if pred == 1 else "✅ Legitimate"

# Predict from CSV
def predict_from_csv(csv_file):
    model = load_model()
    df = pd.read_csv(csv_file)

    # Ensure correct columns
    X = df[["amount", "account_age"]]
    df["prediction"] = model.predict(X)
    df["prediction"] = df["prediction"].map({0: "✅ Legitimate", 1: "🚨 Suspicious"})
    return df

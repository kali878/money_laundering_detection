import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# ==========================
# 1️⃣ Model Training Function
# ==========================
def train_and_save_model(csv_path):
    # CSV load karo
    df = pd.read_csv(csv_path)
    print("Available columns:", df.columns.tolist())

    # Required features define karo
    columns_needed = ["amount", "account_age"]
    existing_columns = [col for col in columns_needed if col in df.columns]

    if not existing_columns:
        raise ValueError("None of the required columns are present in the CSV!")

    # Features aur target
    X = df[existing_columns]
    if "is_fraud" not in df.columns:
        raise ValueError("Target column 'is_fraud' not found in CSV!")
    y = df["is_fraud"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Model train karo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Model save karo
    joblib.dump(model, "model.pkl")
    print("Model trained and saved as 'model.pkl' successfully!")

    # Accuracy check (optional)
    acc = model.score(X_test, y_test)
    print(f"Model Accuracy: {acc*100:.2f}%")

# =================================
# 2️⃣ Single Transaction Prediction
# =================================
def predict_transaction(transaction_data):
    """
    transaction_data: dict, eg. {"amount": 5000, "account_age": 365}
    """
    model = joblib.load("model.pkl")
    df = pd.DataFrame([transaction_data])

    # Ensure columns match model training
    required_columns = ["amount", "account_age"]
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0  # default value if missing

    prediction = model.predict(df)
    return prediction[0]

# ================================
# 3️⃣ Batch Prediction from CSV
# ================================
def predict_from_csv(csv_path):
    model = joblib.load("model.pkl")
    df = pd.read_csv(csv_path)

    required_columns = ["amount", "account_age"]
    existing_columns = [col for col in required_columns if col in df.columns]

    if not existing_columns:
        raise ValueError("Required feature columns missing!")

    X = df[existing_columns]
    predictions = model.predict(X)
    df["prediction"] = predictions
    return df

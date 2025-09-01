import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_and_save_model(csv_path):
    # 1️⃣ CSV load karo
    df = pd.read_csv(csv_path)
    print("Available columns:", df.columns.tolist())

    # 2️⃣ Required features define karo
    columns_needed = ["amount", "account_age"]  # aapke model ke liye features
    # Jo columns exist karte hain sirf wahi use karo
    existing_columns = [col for col in columns_needed if col in df.columns]

    if not existing_columns:
        raise ValueError("None of the required columns are present in the CSV!")

    # 3️⃣ Features aur target
    X = df[existing_columns]
    if "is_fraud" not in df.columns:
        raise ValueError("Target column 'is_fraud' not found in CSV!")
    y = df["is_fraud"]

    # 4️⃣ Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 5️⃣ Model train karo
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 6️⃣ Model save karo
    joblib.dump(model, "model.pkl")
    print("Model trained and saved as 'model.pkl' successfully!")

    # 7️⃣ Accuracy check (optional)
    acc = model.score(X_test, y_test)
    print(f"Model Accuracy: {acc*100:.2f}%")

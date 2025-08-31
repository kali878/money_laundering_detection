import os
import pandas as pd
from sklearn.ensemble import IsolationForest
from config import settings
import joblib

class AnomalyScorer:
    def __init__(self):
        self.model = None

    def fit(self, df: pd.DataFrame):
        features = self._features(df)
        self.model = IsolationForest(
            contamination=settings.ANOMALY["contamination"],
            random_state=settings.ANOMALY["random_state"],
        ).fit(features)
        return self

    def score(self, df: pd.DataFrame) -> pd.Series:
        if self.model is None:
            self.fit(df)
        features = self._features(df)
        s = -self.model.score_samples(features)  # Lower score = more abnormal
        return pd.Series(s, index=df.index, name="anomaly_score")

    @staticmethod
    def _features(df: pd.DataFrame) -> pd.DataFrame:
        use_cols = ["amount_abs", "is_offshore", "is_high_risk_country"]
        X = df[use_cols].copy()
        X["hour"] = df["timestamp"].dt.hour
        X["dow"] = df["timestamp"].dt.dayofweek
        return X.fillna(0.0)

if __name__ == "__main__":
    print("🚀 Model training started...")

    from src.preprocessing import preprocess_data

    # Preprocess data
    df = preprocess_data("data/transactions_fixed.csv")

    # Ensure timestamp is datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Make sure folder exists
    os.makedirs("reports/compliance", exist_ok=True)

    # Train anomaly scorer
    scorer = AnomalyScorer().fit(df)

    # Save trained model
    joblib.dump(scorer, "reports/compliance/model.pkl")

    print("✅ Model training complete. Model saved at reports/compliance/model.pkl")

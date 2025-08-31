# src/preprocessing.py
import pandas as pd

def load_transactions(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    if "amount" in df.columns:
        df["amount_abs"] = df["amount"].abs()

    return df


def preprocess_data(path: str) -> pd.DataFrame:
    df = load_transactions(path)

    # Rolling transaction sum per account over 1 day
    if "account_id" in df.columns and "timestamp" in df.columns:
        df = df.sort_values(["account_id", "timestamp"])
        df["rolling_sum_1d"] = (
            df.groupby("account_id")
              .apply(lambda g: g.set_index("timestamp")["amount_abs"].rolling("1D").sum())
              .reset_index(level=0, drop=True)
        )

    # Encode currency
    if "currency" in df.columns:
        df["currency"] = df["currency"].astype("category").cat.codes

    # Encode channel
    if "channel" in df.columns:
        df["channel"] = df["channel"].astype("category").cat.codes

    # High-risk / offshore countries feature
    if "country_to" in df.columns:
        high_risk_countries = ["IR", "KP", "AF", "SY"]
        offshore_centers = ["KY", "PA", "VG", "BS"]

        df["is_high_risk_country"] = df["country_to"].isin(high_risk_countries).astype(int)
        df["is_offshore"] = df["country_to"].isin(offshore_centers).astype(int)
    else:
        df["is_high_risk_country"] = 0
        df["is_offshore"] = 0

    return df

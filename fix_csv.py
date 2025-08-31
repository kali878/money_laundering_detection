import pandas as pd

df = pd.read_csv("data/transactions.csv")

# --- Required columns banate hain agar missing ho ---
if "transaction_id" not in df.columns:
    df["transaction_id"] = [f"T{i}" for i in range(len(df))]

if "account_id" not in df.columns:
    df["account_id"] = [f"ACC_{i}" for i in range(len(df))]

if "counterparty_id" not in df.columns:
    df["counterparty_id"] = [f"CPTY_{i}" for i in range(len(df))]

if "amount" not in df.columns:
    df["amount"] = [1000 + i for i in range(len(df))]  # dummy amounts

if "currency" not in df.columns:
    df["currency"] = "INR"  # default currency

if "timestamp" not in df.columns:
    df["timestamp"] = pd.date_range("2025-01-01", periods=len(df), freq="h")

if "channel" not in df.columns:
    df["channel"] = "online"  # default channel

if "country_from" not in df.columns:
    df["country_from"] = "IN"

if "country_to" not in df.columns:
    df["country_to"] = "US"

# --- Columns ko required order me arrange karte hain ---
df = df[[
    "transaction_id",
    "account_id",
    "counterparty_id",
    "amount",
    "currency",
    "timestamp",
    "channel",
    "country_from",
    "country_to"
]]

df.to_csv("data/transactions_fixed.csv", index=False)
print("✅ Fixed CSV saved as data/transactions_fixed.csv")

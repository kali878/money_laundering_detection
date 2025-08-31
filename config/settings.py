from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
ALERTS_DIR = REPORTS_DIR / "alerts"
VIS_DIR = REPORTS_DIR / "visualizations"

# Column names expected in transactions.csv
REQUIRED_COLUMNS = [
    "transaction_id", "account_id", "counterparty_id", "amount",
    "currency", "timestamp", "channel", "country_from", "country_to"
]

# Detection thresholds (tune as needed)
THRESHOLDS = {
    "structuring_single_amount_max": 9500,   # e.g., under 10k reporting threshold
    "structuring_window_minutes": 1440,      # 1 day
    "structuring_count_min": 3,              # at least 3 such txns in window

    "rapid_turnover_window_minutes": 60,     # 1 hour
    "rapid_out_in_ratio": 0.8,               # outflow followed by inflow ~same size

    "round_tripping_window_days": 7,
    "round_tripping_min_hops": 3,

    "high_risk_amount_min": 20000,
}

# Country risk lists (illustrative; replace with real lists)
HIGH_RISK_COUNTRIES = {"IR", "KP", "AF", "MM"}
OFFSHORE_COUNTRIES = {"VG", "KY", "PA", "BS", "MU", "IM", "JE"}

# Anomaly model
ANOMALY = {
    "use_isolation_forest": True,
    "contamination": 0.02,
    "random_state": 42
}

# Output
ALERT_FILE = ALERTS_DIR / "alerts.csv"
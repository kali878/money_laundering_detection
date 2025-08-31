import pandas as pd
from datetime import timedelta
from config import settings

def flag_structuring(df: pd.DataFrame) -> pd.DataFrame:
    cfg = settings.THRESHOLDS
    max_amt = cfg["structuring_single_amount_max"]
    window = timedelta(minutes=cfg["structuring_window_minutes"])
    min_count = cfg["structuring_count_min"]

    df = df.copy()
    df["structuring_flag"] = 0
    df["structuring_reason"] = ""

    for acc, grp in df.groupby("account_id", group_keys=False):
        g = grp.sort_values("timestamp")
        # Consider small deposits only (positive amounts <= max_amt)
        small = g[(g["amount"] > 0) & (g["amount"] <= max_amt)]
        idx = small.index
        # Sliding window count
        left = 0
        for right in range(len(idx)):
            while small.loc[idx[right], "timestamp"] - small.loc[idx[left], "timestamp"] > window:
                left += 1
            count = right - left + 1
            if count >= min_count:
                hit_idx = idx[left:right+1]
                df.loc[hit_idx, "structuring_flag"] = 1
        # Reason text
        df.loc[df.index.isin(idx) & (df["structuring_flag"] == 1), "structuring_reason"] = (
            f"≥{min_count} small deposits within {window}"
        )
    return df

def flag_rapid_turnover(df: pd.DataFrame) -> pd.DataFrame:
    from datetime import timedelta
    cfg = settings.THRESHOLDS
    window = timedelta(minutes=cfg["rapid_turnover_window_minutes"])
    ratio = cfg["rapid_out_in_ratio"]

    df = df.copy()
    df["rapid_turnover_flag"] = 0
    df["rapid_turnover_reason"] = ""

    for acc, grp in df.groupby("account_id", group_keys=False):
        g = grp.sort_values("timestamp")
        outs = g[g["direction"] == "out"]
        for i, row in outs.iterrows():
            # find inbound within window of similar size
            cond = (
                (g["direction"] == "in") &
                (g["timestamp"].between(row["timestamp"], row["timestamp"] + window)) &
                (g["amount"].abs() >= ratio * abs(row["amount"]))
            )
            if cond.any():
                df.loc[i, "rapid_turnover_flag"] = 1
                df.loc[i, "rapid_turnover_reason"] = (
                    f"Outflow followed by inbound ≥{int(ratio*100)}% within {window}"
                )
    return df

def flag_round_tripping(df: pd.DataFrame) -> pd.DataFrame:
    cfg = settings.THRESHOLDS
    window_days = cfg["round_tripping_window_days"]
    min_hops = cfg["round_tripping_min_hops"]

    df = df.copy()
    df["round_tripping_flag"] = 0
    df["round_tripping_reason"] = ""

    # Heuristic: same amount bouncing among a small set of accounts/counterparties in short period
    df_sorted = df.sort_values("timestamp")
    for amt, grp in df_sorted.groupby(df_sorted["amount"].round(2)):
        g = grp[grp["timestamp"] >= (grp["timestamp"].min() - pd.Timedelta(days=window_days))]
        # count distinct nodes involved for that amount
        nodes = g["account_id"].astype(str) + "->" + g["counterparty_id"].astype(str)
        if g["timestamp"].max() - g["timestamp"].min() <= pd.Timedelta(days=window_days) and nodes.nunique() >= min_hops:
            df.loc[g.index, "round_tripping_flag"] = 1
            df.loc[g.index, "round_tripping_reason"] = (
                f"≈same amount circulated across ≥{min_hops} hops in {window_days}d"
            )
    return df

def flag_high_risk(df: pd.DataFrame) -> pd.DataFrame:
    cfg = settings.THRESHOLDS
    df = df.copy()
    cond = (
        (df["country_to"].isin(settings.HIGH_RISK_COUNTRIES | settings.OFFSHORE_COUNTRIES)) &
        (df["amount"].abs() >= cfg["high_risk_amount_min"])
    )
    df["high_risk_flag"] = cond.astype(int)
    df["high_risk_reason"] = "high amount to risk/offshore corridor"
    return df
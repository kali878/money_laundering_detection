import pandas as pd
from . import patterns
from .utils import get_logger
from .preprocessing import load_transactions
from config import settings

try:
    from .model import AnomalyScorer
except Exception:
    AnomalyScorer = None

logger = get_logger()


def run_detection(path=None) -> pd.DataFrame:
    df = load_transactions(path)

    # Rule-based flags
    df = patterns.flag_structuring(df)
    df = patterns.flag_rapid_turnover(df)
    df = patterns.flag_round_tripping(df)
    df = patterns.flag_high_risk(df)

    # Aggregate rule flags & reasons
    rule_flags = [
        "structuring_flag", "rapid_turnover_flag", "round_tripping_flag", "high_risk_flag"
    ]
    reason_cols = [c for c in df.columns if c.endswith("_reason")]

    df["rule_flag_sum"] = df[rule_flags].sum(axis=1)
    df["rule_reasons"] = df[reason_cols].replace("", pd.NA).stack().groupby(level=0).apply(lambda s: "; ".join(s.dropna().unique()))

    # Anomaly score (optional)
    if settings.ANOMALY["use_isolation_forest"] and AnomalyScorer is not None:
        scorer = AnomalyScorer().fit(df)
        df["anomaly_score"] = scorer.score(df)
    else:
        df["anomaly_score"] = 0.0

    # Final alert decision
    df["alert"] = (df["rule_flag_sum"] > 0) | (df["anomaly_score"] > 0.8)

    return df
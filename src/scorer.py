# src/scorer.py
class AnomalyScorer:
    def __init__(self):
        pass

    def predict(self, df):
        scores = df["amount"] / 10000
        return (scores > 0.5).astype(int).values

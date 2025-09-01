import numpy as np

class AnomalyScorer:
    def __init__(self):
        # initialize model parameters or load weights if any
        pass

    def predict(self, df):
        # Example: simple threshold on amount as dummy logic
        scores = df['amount'] / 10000  # Dummy scoring logic
        return (scores > 0.5).astype(int).values  # Return 0/1 prediction array

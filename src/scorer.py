# src/scorer.py
class AnomalyScorer:
    def __init__(self, model):
        self.model = model
    
    def predict(self, data):
        # Example: Assuming data is a DataFrame
        return self.model.predict(data)  # Adjust based on actual logic
    # ... other methods as needed ...
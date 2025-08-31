class AnomalyScorer:
    def __init__(self, model):
        self.model = model

    def score(self, X):
        return -self.model.decision_function(X)

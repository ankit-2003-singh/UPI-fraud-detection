import numpy as np
from sklearn.ensemble import IsolationForest

class FraudModel:
    def __init__(self):
        data = np.random.rand(1000,3)
        self.model = IsolationForest(contamination=0.04)
        self.model.fit(data)

    def score(self, amount, freq, hour):
        X = [[amount/50000, freq/20, hour/24]]
        s = self.model.decision_function(X)[0]
        return round(1 - s, 3)

fraud_model = FraudModel()

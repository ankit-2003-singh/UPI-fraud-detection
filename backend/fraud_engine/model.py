import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from data.dataset_loader import load_dataset

class FraudModel:
    def __init__(self):
        df = load_dataset()

        if df is not None and len(df) >= 100:
            print("[FraudModel] Training Random Forest and Isolation Forest on Kaggle dataset...")
            amounts = df["amount"].values.astype(float)
            freqs   = df["freq"].values.astype(float)
            hours   = df["hour"].values.astype(float)
            labels  = df["isFraud"].values.astype(int)

            # Max bounds for normalisation
            self.max_amount = max(amounts.max(), 50000.0)
            self.max_freq   = 20.0
            self.max_hour   = 24.0

            X_train = np.column_stack([
                amounts / self.max_amount,
                np.clip(freqs / self.max_freq, 0, 1),
                hours / self.max_hour
            ])
            y_train = labels

            # Isolation Forest (unsupervised anomaly detection)
            contamination = max(0.01, min(0.15, float(y_train.mean()) if y_train.sum() > 0 else 0.04))
            self.iso_model = IsolationForest(contamination=contamination, random_state=42)
            self.iso_model.fit(X_train)

            # Random Forest (supervised)
            # Ensure at least two classes present
            if len(np.unique(y_train)) > 1:
                self.rf_model = RandomForestClassifier(
                    n_estimators=100, max_depth=6, random_state=42, class_weight="balanced"
                )
                self.rf_model.fit(X_train, y_train)
                self.has_rf = True
            else:
                self.has_rf = False
        else:
            print("[FraudModel] Using calibrated synthetic dataset for ML training...")
            self.max_amount = 50000.0
            self.max_freq   = 20.0
            self.max_hour   = 24.0

            iso_data = np.random.rand(1000, 3)
            self.iso_model = IsolationForest(contamination=0.04, random_state=42)
            self.iso_model.fit(iso_data)

            np.random.seed(42)
            n = 2000
            X_legit = np.random.rand(int(n * 0.96), 3) * [0.5, 0.5, 1.0]
            y_legit = np.zeros(len(X_legit))

            X_fraud = np.random.rand(int(n * 0.04), 3)
            X_fraud[:, 0] *= 1.0
            X_fraud[:, 1] = X_fraud[:, 1] * 0.4 + 0.6
            X_fraud[:, 2] = X_fraud[:, 2] * 0.25
            y_fraud = np.ones(len(X_fraud))

            X_train = np.vstack([X_legit, X_fraud])
            y_train = np.concatenate([y_legit, y_fraud])

            self.rf_model = RandomForestClassifier(
                n_estimators=100, max_depth=6, random_state=42
            )
            self.rf_model.fit(X_train, y_train)
            self.has_rf = True

    def score(self, amount, freq, hour):
        """Return a blended fraud score in [0, 1]."""
        X = [[
            min(float(amount) / self.max_amount, 1.0),
            min(float(freq) / self.max_freq, 1.0),
            min(float(hour) / self.max_hour, 1.0)
        ]]

        iso_raw = self.iso_model.decision_function(X)[0]
        iso_score = round(float(1 - iso_raw), 3)

        if getattr(self, "has_rf", False):
            rf_score = float(self.rf_model.predict_proba(X)[0][1])
            blended = round(0.4 * iso_score + 0.6 * rf_score, 3)
        else:
            blended = iso_score

        return min(max(blended, 0.0), 1.0)

fraud_model = FraudModel()

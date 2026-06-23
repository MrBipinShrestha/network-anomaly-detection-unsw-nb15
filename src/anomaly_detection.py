"""
anomaly_detection.py
--------------------
Isolation Forest anomaly detection module.
Tier 2 of the SOC detection pipeline — unsupervised, label-free screening.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

N_ESTIMATORS  = 100
CONTAMINATION = 0.10
RANDOM_STATE  = 42


def train_isolation_forest(X_train: np.ndarray) -> IsolationForest:
    """
    Fit Isolation Forest on original (pre-SMOTE) training data.
    Contamination approximates the expected attack fraction in the dataset.
    """
    model = IsolationForest(
        n_estimators=N_ESTIMATORS,
        contamination=CONTAMINATION,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    model.fit(X_train)
    print(f"Isolation Forest trained | estimators={N_ESTIMATORS} | contamination={CONTAMINATION}")
    return model


def score_records(model: IsolationForest,
                  X: np.ndarray,
                  df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute anomaly score per record.
    More negative score = more anomalous = higher attack likelihood.
    """
    df = df.copy()
    df['anomaly_score'] = model.decision_function(X)
    df['iso_flag']      = (model.predict(X) == -1).astype(int)
    return df


def summarise_scores(df: pd.DataFrame) -> pd.DataFrame:
    """Return per-class anomaly score statistics for SOC reporting."""
    summary = (df.groupby('label')['anomaly_score']
                 .agg(['mean', 'median', 'std', 'min', 'max'])
                 .round(4))
    print("\n--- Anomaly Score Summary by Class ---")
    print(summary.to_string())
    return summary


def flagged_rates(df: pd.DataFrame) -> dict:
    """Return the percentage of each class flagged as anomalous."""
    rates = (df.groupby('label')['iso_flag']
               .mean()
               .mul(100)
               .round(2)
               .to_dict())
    for label, pct in rates.items():
        name = "Normal" if label == 0 else "Attack"
        print(f"  {name}: {pct:.1f}% flagged as anomalous")
    return rates


if __name__ == "__main__":
    print("Import and use via the main notebook pipeline.")

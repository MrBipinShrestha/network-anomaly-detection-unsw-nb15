"""
model_training.py
-----------------
Random Forest supervised classification module.
Tier 1 of the SOC detection pipeline — high-precision attack classification.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

N_ESTIMATORS = 100
RANDOM_STATE = 42


def train_random_forest(X_train: np.ndarray,
                        y_train: np.ndarray) -> RandomForestClassifier:
    """
    Train Random Forest on SMOTE-balanced training data.
    Gini criterion enables interpretable feature importance scores for SOC analysts.
    """
    model = RandomForestClassifier(
        n_estimators=N_ESTIMATORS,
        criterion="gini",
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    print(f"Random Forest trained | estimators={N_ESTIMATORS} | samples={len(y_train):,}")
    return model


def predict(model: RandomForestClassifier, X_test: np.ndarray):
    """Return class predictions and probability scores for ROC analysis."""
    y_pred       = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    return y_pred, y_pred_proba


def print_report(y_test: np.ndarray, y_pred: np.ndarray):
    """Print classification report with accuracy."""
    acc = accuracy_score(y_test, y_pred)
    print(f"\nOverall Accuracy : {acc:.4f}  ({acc*100:.2f}%)")
    print("\n--- Classification Report ---")
    print(classification_report(y_test, y_pred,
                                 target_names=["Normal (0)", "Attack (1)"]))


def get_feature_importance(model: RandomForestClassifier,
                            feature_names: list) -> pd.DataFrame:
    """
    Return features ranked by mean Gini impurity decrease.
    Use output to generate SIEM detection rules for top features.
    """
    df = pd.DataFrame({
        'Feature':    feature_names,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False).reset_index(drop=True)
    print("\n--- Top 10 Features ---")
    print(df.head(10).to_string(index=False))
    return df


if __name__ == "__main__":
    print("Import and use via the main notebook pipeline.")

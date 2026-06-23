"""
preprocessing.py
----------------
Data preprocessing module for the SOC Intrusion Detection Pipeline.
Handles categorical encoding, feature scaling, and SMOTE resampling.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE

CATEGORICAL_COLS = ['proto', 'service', 'state']
DROP_COLS        = ['id', 'label', 'attack_cat']
TARGET_COL       = 'label'
RANDOM_STATE     = 42


def load_data(train_path: str, test_path: str):
    """Load UNSW-NB15 training and test CSV files."""
    train_df = pd.read_csv(train_path)
    test_df  = pd.read_csv(test_path)
    print(f"Training set : {train_df.shape[0]:,} rows x {train_df.shape[1]} columns")
    print(f"Test set     : {test_df.shape[0]:,} rows x {test_df.shape[1]} columns")
    return train_df, test_df


def encode_categoricals(train_df, test_df):
    """
    Fit LabelEncoder on training data only, transform both splits.
    Prevents silent integer mapping mismatches between partitions.
    """
    encoders = {}
    for col in CATEGORICAL_COLS:
        le = LabelEncoder()
        train_df[col] = le.fit_transform(train_df[col].astype(str))
        test_df[col]  = test_df[col].astype(str).map(
            lambda x, le=le: le.transform([x])[0] if x in le.classes_ else 0
        )
        encoders[col] = le
    print(f"Encoded {len(CATEGORICAL_COLS)} categorical features.")
    return train_df, test_df, encoders


def split_features_target(train_df, test_df):
    """Separate feature matrix X from target vector y."""
    drop    = [c for c in DROP_COLS if c in train_df.columns]
    X_train = train_df.drop(columns=drop)
    y_train = train_df[TARGET_COL]
    X_test  = test_df.drop(columns=[c for c in DROP_COLS if c in test_df.columns])
    y_test  = test_df[TARGET_COL]
    return X_train, y_train, X_test, y_test


def scale_features(X_train, X_test):
    """
    Fit StandardScaler on training data, transform both splits.
    Avoids data leakage from test distribution into scaling parameters.
    """
    scaler         = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)
    print("StandardScaler fitted on training data, applied to both splits.")
    return X_train_scaled, X_test_scaled, scaler


def apply_smote(X_train_scaled, y_train):
    """
    Apply SMOTE to training data ONLY.
    Balances class distribution without inflating test metrics.
    """
    before = dict(y_train.value_counts())
    smote  = SMOTE(random_state=RANDOM_STATE)
    X_res, y_res = smote.fit_resample(X_train_scaled, y_train)
    after  = dict(pd.Series(y_res).value_counts())
    print(f"SMOTE | Before: {before}  ->  After: {after}")
    return X_res, y_res


def run_pipeline(train_path: str, test_path: str):
    """Execute the full preprocessing pipeline."""
    train_df, test_df           = load_data(train_path, test_path)
    train_df, test_df, encoders = encode_categoricals(train_df, test_df)
    X_train, y_train, X_test, y_test = split_features_target(train_df, test_df)
    X_train_sc, X_test_sc, scaler    = scale_features(X_train, X_test)
    X_res, y_res                     = apply_smote(X_train_sc, y_train)
    return {
        "X_train": X_res,    "y_train": y_res,
        "X_test":  X_test_sc, "y_test":  y_test,
        "X_train_orig":  X_train_sc,
        "feature_names": X_train.columns.tolist(),
        "train_df": train_df,
        "scaler": scaler, "encoders": encoders,
    }


if __name__ == "__main__":
    data = run_pipeline("UNSW_NB15_training-set.csv", "UNSW_NB15_testing-set.csv")
    print("Preprocessing complete.")

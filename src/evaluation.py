"""
evaluation.py
-------------
Model evaluation and SOC dashboard generation module.
Produces all figures for analyst briefings and report insertion.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, roc_curve, auc,
    precision_score, recall_score, f1_score, accuracy_score
)

OUTPUT_DPI = 150


def plot_confusion_matrix(y_test, y_pred, save_path: str = None):
    """Figure 6 — Confusion matrix with TP/FP/FN/TN annotation."""
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, ax=ax,
                xticklabels=['Pred Normal', 'Pred Attack'],
                yticklabels=['Actual Normal', 'Actual Attack'],
                linewidths=0.5, linecolor='white', annot_kws={'size': 13})
    ax.set_title('Confusion Matrix — Random Forest on UNSW-NB15',
                 fontsize=12, fontweight='bold')
    ax.text(0.5, -0.14, f'TP={tp:,}  FP={fp:,}  FN={fn:,}  TN={tn:,}',
            ha='center', transform=ax.transAxes, fontsize=9, color='gray')
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=OUTPUT_DPI)
        print(f"Saved: {save_path}")
    plt.show()
    return tn, fp, fn, tp


def plot_roc_curve(y_test, y_pred_proba, save_path: str = None):
    """Figure 7 — ROC curve with AUC and optimal threshold marker."""
    fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    optimal_idx = np.argmax(tpr - fpr)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(fpr, tpr, color='#E8674C', lw=2.5,
            label=f'Random Forest  AUC = {roc_auc:.4f}')
    ax.plot([0,1],[0,1], color='gray', lw=1.5, linestyle='--',
            label='Random Classifier  AUC = 0.50')
    ax.fill_between(fpr, tpr, alpha=0.08, color='#E8674C')
    ax.scatter(fpr[optimal_idx], tpr[optimal_idx], s=80, color='#E8674C',
               zorder=5, label=f'Optimal threshold = {thresholds[optimal_idx]:.3f}')
    ax.set_xlabel('False Positive Rate', fontsize=11)
    ax.set_ylabel('True Positive Rate (Recall)', fontsize=11)
    ax.set_title('ROC Curve — Random Forest on UNSW-NB15', fontsize=12, fontweight='bold')
    ax.legend(loc='lower right', fontsize=10)
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=OUTPUT_DPI)
        print(f"Saved: {save_path}")
    plt.show()
    print(f"ROC AUC: {roc_auc:.4f}")
    return roc_auc


def plot_feature_importance(importances_df: pd.DataFrame,
                             top_n: int = 10,
                             save_path: str = None):
    """Figure 8 — Top N features by mean Gini impurity decrease."""
    top    = importances_df.head(top_n)
    colors = plt.cm.Blues(np.linspace(0.4, 0.85, top_n))
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top['Feature'][::-1], top['Importance'][::-1],
            color=colors, edgecolor='white')
    for i, val in enumerate(top['Importance'][::-1]):
        ax.text(val + 0.001, i, f'{val:.4f}', va='center', fontsize=9)
    ax.set_title(f'Top {top_n} Feature Importances — Mean Gini Decrease',
                 fontsize=12, fontweight='bold')
    ax.set_xlabel('Mean Gini Impurity Decrease', fontsize=11)
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=OUTPUT_DPI)
        print(f"Saved: {save_path}")
    plt.show()


def print_soc_summary(y_test, y_pred, roc_auc: float,
                      tn: int, fp: int, fn: int, tp: int):
    """Print SOC-style operational results summary."""
    print("=" * 60)
    print("  SOC DETECTION SYSTEM — OPERATIONAL SUMMARY")
    print("=" * 60)
    print(f"  Overall Accuracy   : {accuracy_score(y_test, y_pred)*100:.2f}%")
    print(f"  ROC AUC            : {roc_auc:.4f}")
    print(f"  Attack Recall      : {recall_score(y_test, y_pred, pos_label=1):.4f}")
    print(f"  Attack Precision   : {precision_score(y_test, y_pred, pos_label=1):.4f}")
    print(f"  Normal Recall      : {recall_score(y_test, y_pred, pos_label=0):.4f}")
    print(f"  False Negatives    : {fn:,}  ({fn/(fn+tp)*100:.1f}% miss rate)")
    print(f"  False Positives    : {fp:,}  (analyst alert load)")
    print("=" * 60)


if __name__ == "__main__":
    print("Import and use via the main notebook pipeline.")

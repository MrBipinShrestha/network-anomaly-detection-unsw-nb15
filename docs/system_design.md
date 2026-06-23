# System Design — AI-Powered SOC Intrusion Detection System

**Author:** Bipin Shrestha  
**Dataset:** UNSW-NB15 (UNSW Cyber Range Lab)  

---

## 1. System Overview

This document describes the architecture and design decisions behind the SOC Intrusion Detection System. The system processes network flow records, applies a two-stage ML detection pipeline, and produces analyst-ready security intelligence outputs.

---

## 2. Architecture

```
Network Traffic Logs (UNSW-NB15)
            |
            v
+---------------------------+
|   Preprocessing Layer     |
|  - Label Encoding         |
|  - StandardScaler         |
|  - SMOTE Balancing        |
+------------+--------------+
             |
      +-------+-------+
      |               |
      v               v
+----------+    +--------------+
|Isolation |    |    Random    |
|  Forest  |    |    Forest    |
| Tier 2   |    |   Tier 1    |
| (Anomaly)|    |(Classifier)  |
+----+-----+    +------+-------+
     |                 |
     +---------+-------+
               |
               v
+---------------------------+
|  Security Intelligence    |
|  - Feature Importance     |
|  - Anomaly Scores         |
|  - Threat Scoring         |
+---------------------------+
               |
               v
+---------------------------+
|  SOC Dashboard & Alerts   |
|  - 6-Panel Dashboard      |
|  - Unified Threat View    |
+---------------------------+
```

---

## 3. Detection Tiers

### Tier 1 — Critical Alerts (Random Forest)
- **Purpose:** High-confidence binary classification of Attack vs Normal
- **Algorithm:** Random Forest (n=100, Gini criterion)
- **Training data:** SMOTE-balanced partition
- **Key metric:** Attack Recall = 0.98

### Tier 2 — Suspicious Activity (Isolation Forest)
- **Purpose:** Unsupervised anomaly screening without labels
- **Algorithm:** Isolation Forest (n=100, contamination=0.1)
- **Training data:** Pre-SMOTE scaled training data
- **Output:** Continuous anomaly score per record

### Tier 3 — Analyst Intelligence
- **Purpose:** Explain detections for investigation and SIEM rule design
- **Output:** Feature importance rankings, per-category anomaly profiles

---

## 4. Preprocessing Design Decisions

| Decision | Rationale |
|----------|-----------|
| LabelEncoder fitted on train only | Prevents integer mapping mismatches between splits |
| StandardScaler fitted on train only | Prevents data leakage of test statistics |
| SMOTE applied after scaling | Interpolation in normalised feature space |
| SMOTE applied to training only | Preserves realistic test class distribution |

---

## 5. Key Results

| Metric | Value |
|--------|-------|
| Overall Accuracy | 88.30% |
| ROC AUC | 0.9794 |
| Attack Recall | 0.98 |
| False Negative Rate | 1.9% |

---

## 6. Top Discriminative Features

Features ranked by mean Gini importance — directly usable as SIEM threshold rules:

1. `ct_state_ttl` — 0.1097
2. `sttl` — 0.0975
3. `rate` — 0.0728
4. `sload` — 0.0667
5. `dload` — 0.0597

---

## 7. SIEM Integration Concept

The pipeline output can be integrated into SIEM systems:

- **Splunk:** Ingest feature vectors as structured events; use feature importance scores to build correlation rules
- **Wazuh:** Deploy as active response module triggered by anomaly score threshold
- **Microsoft Sentinel:** Feed predictions as custom analytics rule outputs
- **ELK Stack:** Index detection scores for real-time Kibana dashboards

---

## 8. Limitations

- Dataset is synthetic/lab-generated (2015)
- Attack patterns may not reflect current threat landscape
- No hyperparameter optimisation performed
- Single train/test split (no k-fold cross-validation)

---

## 9. Future Work

- Bayesian hyperparameter optimisation
- LSTM/Transformer temporal sequence modelling
- Online learning with concept drift detection (ADWIN)
- Geometric SMOTE for improved minority sampling
- Real-time Kafka streaming pipeline
- SIEM rule auto-exporter from feature rankings

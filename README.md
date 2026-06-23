# 🚨 AI-Powered Network Intrusion Detection System for SOC Environments (UNSW-NB15)

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Machine Learning](https://img.shields.io/badge/Machine%20Learning-SOC%20Ready-red)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.2+-green?logo=scikit-learn)
![Status](https://img.shields.io/badge/Status-Production%20Simulation-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **This project simulates a real-world SOC intrusion detection pipeline that processes network traffic, detects anomalies, and classifies cyber attacks using machine learning — designed to mirror how enterprise security teams operate.**

---

## 👤 Author

**Bipin Shrestha**  
Cybersecurity Analyst | SOC Operations | Network Security  
Sydney, Australia

---

## 🧠 System Overview

Most machine learning projects train a model and report accuracy. This project goes further — it simulates an **end-to-end Security Operations Centre detection pipeline** from raw network traffic through to analyst-ready security intelligence.

The system answers the question every SOC team asks daily:

> *"Of the millions of network flows crossing our infrastructure, which ones are attacks — and why?"*

It does this through a two-stage detection architecture:
- **Stage 1 — Isolation Forest:** Flags statistically anomalous traffic without needing labels (catches unknown threats)
- **Stage 2 — Random Forest:** Classifies confirmed attack vs normal traffic with high recall (catches known threats)

---

## 🛡️ Security Architecture

```
Network Traffic Logs (UNSW-NB15)
            │
            ▼
┌─────────────────────────┐
│   Preprocessing Layer   │
│  Label Encoding         │
│  StandardScaler         │
│  SMOTE Balancing        │
└────────────┬────────────┘
             │
      ┌──────┴──────┐
      ▼             ▼
┌──────────┐  ┌──────────────┐
│Isolation │  │    Random    │
│  Forest  │  │    Forest    │
│          │  │              │
│Anomaly   │  │ Binary       │
│Detection │  │ Classifier   │
│(Tier 2)  │  │ (Tier 1)     │
└────┬─────┘  └──────┬───────┘
     │               │
     └───────┬───────┘
             ▼
┌─────────────────────────┐
│  Security Intelligence  │
│  Layer                  │
│  Feature Importance     │
│  Threat Scoring         │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│   SOC Dashboard &       │
│   Analyst Alerts        │
└─────────────────────────┘
```

---

## 🎯 SOC Use Cases

| Use Case | How This System Addresses It |
|----------|------------------------------|
| Unknown attack detection | Isolation Forest flags statistical anomalies without labels |
| Known threat classification | Random Forest classifies with 0.98 Attack recall |
| Alert prioritisation | Tiered output separates critical alerts from anomalies |
| Analyst investigation | Feature importance explains *why* traffic is malicious |
| SIEM integration | Output structured for Splunk / Wazuh / Microsoft Sentinel |
| Incident response | Confusion matrix quantifies operational risk in real-time |

---

## 🔴 Tiered SOC Detection Model

### 🔴 Tier 1 — Critical Alerts (Random Forest)
Confirmed malicious traffic. High-confidence classification for immediate incident response.

### 🟡 Tier 2 — Suspicious Activity (Isolation Forest)
Anomalous network behaviour. Flagged for analyst investigation — catches zero-day variants.

### 🔵 Tier 3 — Analyst Intelligence Layer
Feature importance scores show *which network characteristics* drove each detection — supporting forensic analysis, SIEM rule tuning, and threat hunting.

---

## 📊 Performance Results

The system achieved **0.98 Attack recall** — meaning only 858 of 45,332 attack flows were missed. In a SOC context, each false negative is an undetected intrusion.

| Metric | Value | SOC Interpretation |
|--------|-------|--------------------|
| **Attack Recall** | **0.98** | 98% of attacks detected — primary security goal |
| **ROC AUC** | **0.9794** | Strong discrimination across all alert thresholds |
| **Overall Accuracy** | 88.30% | Reflects inverted training distribution |
| **Attack Precision** | 0.84 | Manageable false alarm rate |
| **Normal Recall** | 0.76 | Tunable via ROC threshold |
| **True Positives** | 44,474 | Confirmed attacks correctly flagged |
| **False Negatives** | 858 | Missed attacks — 1.9% miss rate |
| **False Positives** | 8,776 | False alarms — analyst workload cost |
| **True Negatives** | 28,224 | Legitimate traffic correctly cleared |

---

## 🧠 Feature Intelligence

The following features were identified as the strongest indicators of malicious network behaviour — directly actionable as SIEM detection rules:

| Rank | Feature | Importance | Security Meaning |
|------|---------|-----------|-----------------|
| 1 | `ct_state_ttl` | 0.1097 | Connection state / TTL anomalies |
| 2 | `sttl` | 0.0975 | Source TTL deviation |
| 3 | `rate` | 0.0728 | Abnormal packet transmission rate |
| 4 | `sload` | 0.0667 | Source byte load spikes |
| 5 | `dload` | 0.0597 | Destination byte load spikes |

> These five features alone account for ~46% of the model's discriminative power and represent the core of a lightweight SIEM threshold rule set.

---

## 📊 Visual Intelligence Outputs

| Figure | Description | SOC Value |
|--------|-------------|-----------|
| Fig 1 | Class distribution before & after SMOTE | Validates resampling strategy |
| Fig 3 | Feature distributions by class | Identifies attack traffic signatures |
| Fig 4 | Feature correlation heatmap | Guides feature selection |
| Fig 5 | Dual-panel anomaly scores | Validates Isolation Forest separation |
| Fig 5b | Anomaly scores by attack category | Per-threat unsupervised detectability |
| Fig 6 | Confusion matrix | Operational TP/FP/FN breakdown |
| Fig 7 | ROC curve (AUC = 0.9794) | Threshold tuning reference |
| Fig 8 | Feature importance ranking | SIEM rule design input |
| Fig 9 | Six-panel SOC dashboard | Full analyst briefing output |
| Fig 10 | Unified threat dashboard | Management reporting layer |

---

## 📁 Dataset

**UNSW-NB15 — Australian Centre for Cyber Security (ACCS)**  
🔗 https://research.unsw.edu.au/projects/unsw-nb15-dataset

| Property | Training | Test |
|----------|----------|------|
| Records | 175,341 | 82,332 |
| Features | 45 | 45 |
| Normal (0) | 56,000 | 37,000 |
| Attack (1) | 119,341 | 45,332 |
| Attack Categories | 9 | 9 |

> Download both CSV files and place them in the project root before running.

---

## 🧪 Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Pandas / NumPy | Data processing |
| Scikit-learn | ML models & evaluation |
| Imbalanced-learn | SMOTE resampling |
| Matplotlib / Seaborn | Security visualisations |
| Jupyter Notebook | Pipeline environment |

---

## 🧰 Industry / SIEM Integration Potential

This pipeline architecture is compatible with:

- **Splunk** — ingest feature vectors as structured events
- **Wazuh** — extend active response with ML classification layer
- **Microsoft Sentinel** — feed anomaly scores as custom analytics rules
- **Apache Kafka** — stream network flow records for real-time scoring
- **ELK Stack** — index detection outputs for dashboarding

---

## 🚀 Future Work

| Direction | Description |
|-----------|-------------|
| **Bayesian Hyperparameter Tuning** | Optimise RF depth and IF contamination to recover Normal recall |
| **LSTM / Transformer IDS** | Capture temporal attack sequences invisible to flow-level features |
| **Online Learning + Drift Detection** | Adapt model as traffic baselines evolve (ADWIN, Page-Hinkley) |
| **Geometric SMOTE** | More diverse synthetic minority samples |
| **Live Streaming Pipeline** | Kafka → feature extraction → real-time scoring |
| **SIEM Rule Exporter** | Auto-generate Splunk/Sigma rules from feature importance rankings |

---

## ⚠️ Limitations

- Dataset is synthetically generated in a 2015 lab environment — modern attack techniques (encrypted C2, supply chain, AI-augmented phishing) are not represented
- Training set distribution was inverted (68% Attack) vs the documented benchmark — directly affected Normal recall
- No hyperparameter optimisation was applied — reported metrics are conservative
- Single train/test split — k-fold validation would yield more statistically robust estimates

---

## 💼 Project Impact

> This system demonstrates SOC-level intrusion detection capability by combining unsupervised anomaly screening with supervised classification — achieving **0.98 Attack recall** and **AUC of 0.9794** on 82,332 real-world network records. The feature intelligence layer produces directly actionable SIEM rules, bridging the gap between ML model outputs and operational security decisions.

---

## 📦 Setup & Usage

```bash
git clone https://github.com/MrBipinShrestha/network-anomaly-detection-unsw-nb15.git
cd network-anomaly-detection-unsw-nb15
pip install -r requirements.txt
jupyter notebook "Jupyter Notebook_CLEAN.ipynb"
```

Then select **Kernel → Restart & Run All**

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

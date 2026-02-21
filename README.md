# 🛡️ UPI Shield — AI-Powered Real-Time Fraud Detection System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-black.svg)](https://flask.palletsprojects.com/)
[![React.js](https://img.shields.io/badge/React.js-19.0-61dafb.svg)](https://react.dev/)
[![Random Forest](https://img.shields.io/badge/Random%20Forest-Scikit--Learn-green.svg)](https://scikit-learn.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-Graph%20Analytics-blueviolet.svg)](https://networkx.org/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)

> **UPI Shield** is a real-time UPI fraud detection and prevention platform that identifies and blocks fraudulent digital payment transactions before completion. It features a hybrid scoring engine that merges **Supervised Random Forest Machine Learning**, **Rule-Based Risk Analysis**, and **Graph Analytics** with an interactive **React.js dashboard** and **Flask REST APIs**.

---

## 📌 Resume Highlights & Core Capabilities

- **Real-Time Pre-Transaction Fraud Gate**: Identifies and blocks fraudulent UPI transactions **before completion** via a low-latency decision gate (`POST /api/check`).
- **Random Forest Machine Learning**: 100-tree ensemble with balanced class weighting, achieving **97.83% Accuracy** and **99.27% ROC-AUC** on real UPI transaction data.
- **Hybrid Fraud Scoring Engine**:
  $$\text{Final Risk Score} = \frac{\text{Random Forest Score} + \text{Rule-Based Score}}{2}$$
- **Graph Analytics (NetworkX)**: Real-time detection of circular **fraud rings** (via cycle detection) and **money mule accounts** (via in/out-degree fan-in/fan-out analysis).
- **Interactive React.js Dashboard**: Live transaction monitoring, real-time alerts, KPI cards, and canvas network graph visualization.
- **Flask REST API & Server-Sent Events (SSE)**: True push streaming of transactions and graph updates without client polling.

---

## 📊 Model Performance & Benchmarks

The core Machine Learning model is a supervised **Random Forest Classifier** trained on UPI payment records with balanced class weighting to handle severe real-world fraud class imbalance ($~1.4\%$ fraud rate).

| Metric | Holdout Test Set | 5-Fold Cross-Validation | Interpretation |
| :--- | :---: | :---: | :--- |
| **Accuracy** | **97.83%** | **97.33%** | Over 97 out of 100 transactions classified correctly. |
| **ROC-AUC** | **99.27%** | **98.87%** | Exceptional discriminative power between safe and fraudulent transfers. |
| **Recall (Sensitivity)** | **66.67%** | **81.67%** | Captures over 80% of rare fraudulent transactions. |
| **Precision** | **37.50%** | **33.71%** | Balanced to prioritize catching high-loss fraud. |
| **F1-Score** | **48.00%** | **47.35%** | Optimal harmonic mean on severely skewed transaction data. |

### Feature Importances (Random Forest)
1. **`amount`** (**50.39%**): Scaled transaction value.
2. **`is_high_amount`** (**44.12%**): Binary flag for large transaction thresholds ($> ₹25,000$).
3. **`freq`** (**3.17%**): Account transaction velocity in active window.
4. **`hour`** (**1.95%**): Time of day (0–23).
5. **`is_night`** (**0.38%**): Nocturnal activity indicator ($< 5\text{am}$ or $\ge 23\text{pm}$).

---

## 🧠 System Architecture

```
                 Incoming UPI Transaction (Sender, Receiver, Amount, Hour, Freq)
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
        [1] Random Forest ML Model                        [2] Rule-Based Risk Engine
          (Scikit-Learn, 100 Trees)                         (Velocity, Amount, Time)
                     │                                                 │
                     └────────────────────────┬────────────────────────┘
                                              ▼
                                   Blended Risk Score [0.0 - 1.0]
                                              │
                     ┌────────────────────────┴────────────────────────┐
                     ▼                                                 ▼
        [3] Graph Analytics Engine                         [4] Pre-Transaction Gate
           (Fraud Rings & Mules)                             (Allow / 403 Forbidden)
                                              │
                                              ▼
                         [5] Flask REST APIs + SSE Push Stream
                                              │
                                              ▼
                    [6] React.js Real-Time Monitoring Dashboard
```

---

## 🔍 The 3 Detection Engines

### 1. Random Forest Machine Learning Model
- **Algorithm**: `sklearn.ensemble.RandomForestClassifier` (100 estimators, max depth 8, balanced class weights).
- **Training Pipeline**: Automatically normalizes features, trains against `kaggle_upi_fraud.csv`, and outputs calibrated probability via `predict_proba`.

### 2. Rule-Based Risk Analysis
- **Monetary Thresholds**: Escalates risk for transactions $> ₹30,000$ and $> ₹40,000$.
- **Velocity Spikes**: Flags accounts exceeding $12$ and $18$ transactions in an active monitoring window.
- **Nocturnal Activity**: Evaluates late-night transfers (between 23:00 and 05:00).
- **Self-Transfer Heuristic**: Detects suspicious loopback transactions where sender equals receiver.

### 3. Graph Analytics (NetworkX)
- **Fraud Ring Detection**: Runs `nx.simple_cycles()` bounded to 3–6 nodes to identify circular money-routing schemes and layering.
- **Money Mule Detection**: Identifies accounts with high in-degree/out-degree ratios (fan-in from multiple victims and rapid fan-out to external accounts).
- **PageRank Centrality**: Evaluates node importance and structural hubs across payment networks.

---

## 💻 Tech Stack

- **Backend**: Python 3.10+, Flask 3.0+, Flask-CORS
- **Machine Learning**: Scikit-Learn (Random Forest Classifier), Pandas, NumPy
- **Graph Analytics**: NetworkX (Directed Graph, Cycle Detection, PageRank)
- **Frontend**: React.js 19, HTML5 Canvas, Modern CSS
- **Real-Time Streaming**: Server-Sent Events (SSE / EventSource)

---

## 📁 Project Structure

```plaintext
UPI-fraud-detection/
├── backend/
│   ├── api/
│   │   └── routes.py             # REST & SSE endpoints (/stream, /check, /sse, /graph, /model)
│   ├── data/
│   │   ├── dataset_loader.py     # CSV dataset loader & column normalizer
│   │   ├── kaggle_upi_fraud.csv  # UPI transaction dataset
│   │   ├── simulator.py          # Real-time transaction generator & simulator
│   │   └── storage.py            # In-memory recent transaction store
│   ├── fraud_engine/
│   │   ├── graph_engine.py       # NetworkX graph, cycle detection & mule detection
│   │   ├── model.py              # Pure Random Forest Classifier model
│   │   └── risk_rules.py         # Heuristic rules (amount, velocity, time of day)
│   ├── app.py                    # Flask application server
│   └── requirements.txt          # Python dependencies
├── frontend-react/
│   ├── public/                   # Public assets & index.html
│   ├── src/
│   │   ├── api/
│   │   │   └── fraudApi.js       # Client API and SSE connection service
│   │   ├── components/
│   │   │   ├── AlertFeed.jsx     # Live fraud alerts feed
│   │   │   ├── FraudIntelligence.jsx # Fraud rings & mule account cards
│   │   │   ├── KPICards.jsx      # Top metrics & active Random Forest badge
│   │   │   ├── NetworkGraph.jsx  # Interactive canvas network graph
│   │   │   ├── PreTxChecker.jsx  # Pre-transaction fraud tester widget
│   │   │   └── TransactionList.jsx # Recent transaction table
│   │   ├── hooks/
│   │   │   └── useSSE.js         # React hook for real-time SSE stream
│   │   ├── App.jsx               # Dashboard root component
│   │   ├── App.css               # Dark theme dashboard styles
│   │   └── index.js              # React entry point
│   └── package.json              # React dependencies & scripts
├── .gitignore                    # Python & Node exclusion rules
└── README.md                     # System documentation
```

---

## 🚀 Quickstart Guide

### 1. Start the Flask Backend

```powershell
cd backend

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1    # On Linux/macOS: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend
python app.py
```
> The backend will start on **`http://127.0.0.1:5000`** and automatically train the Random Forest model on boot.

---

### 2. Start the React.js Dashboard

Open a separate terminal:

```powershell
cd frontend-react

# Install packages
npm install

# Start development server
npm start
```
> The dashboard will open at **`http://localhost:3000`**.

---

## 📡 API Reference

### 1. Pre-Transaction Fraud Gate (`POST /api/check`)
Evaluates pending transactions **before completion**.

- **Endpoint**: `POST /api/check`
- **Request Body**:
  ```json
  {
    "sender": "Vikram",
    "receiver": "Pooja",
    "amount": 48000,
    "freq": 16,
    "hour": 3
  }
  ```
- **Response (Blocked - HTTP 403)**:
  ```json
  {
    "allowed": false,
    "model": "Random Forest Classifier",
    "risk": 0.84,
    "rf_score": 0.81,
    "rule_score": 0.87,
    "reason": "Risk score 0.84 exceeds threshold 0.75; Party is a flagged mule account",
    "involves_mule": true,
    "involves_ring": false
  }
  ```

---

### 2. Random Forest Model Information (`GET /api/model`)
Returns the model's architecture, parameters, and feature importances.

- **Endpoint**: `GET /api/model`
- **Response (HTTP 200)**:
  ```json
  {
    "algorithm": "Random Forest Classifier",
    "framework": "Scikit-Learn",
    "n_estimators": 100,
    "max_depth": 8,
    "class_weight": "balanced",
    "feature_importances": {
      "amount": 0.5039,
      "is_high_amount": 0.4412,
      "freq": 0.0317,
      "hour": 0.0195,
      "is_night": 0.0038
    }
  }
  ```

---

### 3. Real-Time Push Stream (`GET /api/sse`)
Server-Sent Events endpoint pushing live transaction updates, detected rings, and mules every 1.5 seconds.

- **Endpoint**: `GET /api/sse`
- **Headers**: `Content-Type: text/event-stream`

---

### 4. Graph Analytics Snapshot (`GET /api/graph`)
Returns active nodes, edges, PageRank scores, detected rings, and mule accounts.

- **Endpoint**: `GET /api/graph`

---

## 👥 Contributors

- **Team Code Blooded** / **Ankit Singh**
- GitHub: [@ankit-2003-singh](https://github.com/ankit-2003-singh)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

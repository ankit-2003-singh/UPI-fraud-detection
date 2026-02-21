# 🛡️ UPI Shield — Real-Time UPI Fraud Detection & Prevention System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-black.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-19.0-61dafb.svg)](https://react.dev/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4%2B-orange.svg)](https://scikit-learn.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-3.0%2B-blueviolet.svg)](https://networkx.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**UPI Shield** is an end-to-end, real-time fraud intelligence and prevention platform designed to detect and block fraudulent Unified Payments Interface (UPI) transactions before they settle. 

It combines **Ensemble Machine Learning** (Supervised + Unsupervised), **Network Graph Analytics**, **Rule-Based Heuristic Scoring**, and a **Pre-Transaction Fraud Gate API** backed by an interactive real-time dashboard.

---

## 📑 Table of Contents
- [Architecture & Detection Engines](#-architecture--detection-engines)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Backend Setup](#1-backend-setup)
  - [2. Frontend Setup (React Dashboard)](#2-frontend-setup-react-dashboard)
  - [3. Vanilla Frontend Setup (Alternative)](#3-vanilla-frontend-setup-alternative)
- [API Reference](#-api-reference)
  - [Pre-Transaction Check (`POST /api/check`)](#1-pre-transaction-check-post-apicheck)
  - [Real-Time Stream (`GET /api/stream`)](#2-real-time-stream-get-apistream)
  - [Server-Sent Events (`GET /api/sse`)](#3-server-sent-events-get-apisse)
  - [Network Graph & Analytics (`GET /api/graph`)](#4-network-graph--analytics-get-apigraph)
  - [Transaction History (`GET /api/history`)](#5-transaction-history-get-apihistory)
- [Machine Learning & Graph Details](#-machine-learning--graph-details)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧠 Architecture & Detection Engines

UPI Shield utilizes a defense-in-depth approach consisting of three distinct fraud evaluation engines:

```
 Incoming UPI Transaction
          │
          ├──► [1] Random Forest Machine Learning Model
          ├──► [2] Rule-Based Risk Engine (Velocity, Amount, Time)
          └──► [3] Graph Analytics (Fraud Rings & Money Mule Accounts)
          │
          ▼
    Blended Risk Score [0.0 - 1.0] ──► Allow (200) / Block (403)
```

1. **Supervised Random Forest Classifier (Machine Learning Engine)**:
   - **Architecture**: 100 Decision Trees (`n_estimators=100`, `max_depth=8`) from Scikit-Learn.
   - **Class Balancing**: Uses `class_weight="balanced"` to effectively learn from imbalanced fraud patterns.
   - **Feature Engineering**:
     - `amount`: Normalized transaction amount.
     - `freq`: Transaction velocity/frequency within the active window.
     - `hour`: Time of day (0–23).
     - `is_night`: Binary indicator for high-risk nocturnal hours ($<5\text{am}$ or $\ge 23\text{pm}$).
     - `is_high_amount`: Binary flag for high-value risk ($> ₹25,000$).
   - **Outputs**: Direct calibrated fraud probability $[0.0 - 1.0]$ via `predict_proba`.

2. **Rule-Based Heuristic Engine**:
   - Evaluates high monetary velocity (frequency $> 10$ transactions/window).
   - High-value transaction thresholds ($> ₹20,000$).
   - High-risk temporal patterns (unusual late-night activity between 23:00 and 05:00).

3. **Graph Intelligence Engine (NetworkX)**:
   - **Fraud Ring Detection**: Runs directed cycle algorithms (`nx.simple_cycles`) to detect circular fund routing and layering (chains of 3–6 linked accounts).
   - **Money Mule Detection**: Analyzes node in-degree vs. out-degree ratios and transaction velocity to spot mule accounts funneling illicit money.
   - **PageRank Centrality**: Ranks influence and routing hubs across the financial transaction graph.

4. **Pre-Transaction Fraud Gate (`/api/check`)**:
   - Allows payment aggregators or banking apps to verify an incoming transaction **before** it is committed.
   - Immediately returns a decision (`allowed: true` or `allowed: false` with specific reasons) to stop financial fraud in flight.

---

## ✨ Key Features

- ⚡ **Real-Time Push via Server-Sent Events (SSE)**: Streams live simulated and dataset-backed transactions without client polling.
- 🛑 **Pre-Transaction Blocking API**: Interactive interface and REST endpoint to simulate blocking suspicious transactions before money leaves an account.
- 🕸️ **Interactive Network Graph**: Live visualization of nodes (senders/receivers) and directed edges with risk-based color indicators.
- 🔍 **Mule & Ring Intelligence**: Real-time identification and listing of high-risk mule accounts and circular fraud rings.
- 📊 **Executive KPI Metrics**: Live counters for total transactions, flagged alerts, and dynamic average fraud risk.
- 📂 **Flexible Dataset Loader**: Automatically detects and trains against Kaggle UPI / PaySim CSV datasets, with seamless fallback to calibrated synthetic data.

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10+** / **Flask 3.0+**
- **Scikit-Learn**: Random Forest Classifier
- **NetworkX**: Directed graph analysis, cycle detection, PageRank
- **Pandas & NumPy**: Dataset loading, normalization, feature scaling
- **Flask-CORS**: Cross-Origin Resource Sharing

### Frontend (React Dashboard)
- **React 19**
- **Modern CSS / Flexbox / Grid**
- **EventSource (SSE)** for real-time live push updates
- **Canvas / Vis-Network** for network graph visualization

### Frontend (Vanilla)
- **HTML5, CSS3, Vanilla ES6+ JavaScript**
- **Vis-Network (CDN)** for standalone visualization

---

## 📁 Project Structure

```plaintext
UPI-fraud-detection/
├── backend/
│   ├── api/
│   │   └── routes.py             # REST & SSE API endpoints (/stream, /check, /sse, /graph)
│   ├── data/
│   │   ├── dataset_loader.py     # Kaggle CSV dataset loader & column normalizer
│   │   ├── kaggle_upi_fraud.csv  # UPI transaction dataset
│   │   ├── simulator.py          # Real-time transaction generator & simulator
│   │   └── storage.py            # In-memory recent transaction store
│   ├── fraud_engine/
│   │   ├── graph_engine.py       # NetworkX graph, cycle detection & mule detection
│   │   ├── model.py              # Random Forest fraud classification model
│   │   └── risk_rules.py         # Heuristic rules (amount, velocity, time of day)
│   ├── app.py                    # Flask server entry point
│   └── requirements.txt          # Python dependencies
├── frontend-react/
│   ├── public/                   # Static assets & index.html
│   ├── src/
│   │   ├── api/
│   │   │   └── fraudApi.js       # Client API and SSE connection service
│   │   ├── components/
│   │   │   ├── AlertFeed.jsx     # Live fraud alerts feed
│   │   │   ├── FraudIntelligence.jsx # Fraud rings & mule account widgets
│   │   │   ├── KPICards.jsx      # Top metrics & risk stats
│   │   │   ├── NetworkGraph.jsx  # Interactive transaction graph
│   │   │   ├── PreTxChecker.jsx  # Pre-transaction fraud tester widget
│   │   │   └── TransactionList.jsx # Recent transaction table
│   │   ├── hooks/
│   │   │   └── useSSE.js         # React hook for real-time SSE stream
│   │   ├── App.jsx               # Main React dashboard layout
│   │   ├── App.css               # Dashboard styling & dark UI theme
│   │   └── index.js              # React DOM bootstrap
│   └── package.json              # Node dependencies & npm scripts
├── frontend/                     # Vanilla HTML/CSS/JS frontend alternative
│   ├── CSS/style.css
│   ├── JS/
│   │   ├── api.js
│   │   ├── dashboard.js
│   │   └── graph.js
│   └── index.html
├── .gitignore                    # Git ignore file for Python & Node
└── README.md                     # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+** (with `pip` or Python Launcher `py`)
- **Node.js 18+** and **npm**

---

### 1. Backend Setup

1. Open a terminal and navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create and activate a Python virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
     *(If `python` is not in your PATH, use `py -m venv venv` and `.\venv\Scripts\Activate.ps1`)*
   - **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Launch the Flask API server:
   ```bash
   python app.py
   ```
   The backend API will start at **`http://127.0.0.1:5000`**. On startup, it automatically loads and trains the ML models on `kaggle_upi_fraud.csv`.

---

### 2. Frontend Setup (React Dashboard)

1. Open a **new terminal** and navigate to `frontend-react`:
   ```bash
   cd frontend-react
   ```

2. Install dependencies (if not already installed):
   ```bash
   npm install
   ```

3. Start the React development server:
   ```bash
   npm start
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

---

### 3. Vanilla Frontend Setup (Alternative)

If you prefer running the lightweight vanilla JavaScript frontend without Node.js:
1. Ensure the backend server is running on `http://127.0.0.1:5000`.
2. Open [`frontend/index.html`](frontend/index.html) directly in any web browser or serve it using Python:
   ```bash
   cd frontend
   python -m http.server 8000
   ```
3. Open `http://localhost:8000` in your browser.

---

## 📡 API Reference

### 1. Pre-Transaction Check (`POST /api/check`)
Evaluates a pending transaction and decides whether to authorize or block it.

- **URL**: `/api/check`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
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
    "risk": 0.84,
    "ml_score": 0.81,
    "rule_score": 0.87,
    "reason": "Risk score 0.84 exceeds threshold 0.75; Party is a flagged mule account",
    "involves_mule": true,
    "involves_ring": false,
    "details": {
      "sender": "Vikram",
      "receiver": "Pooja",
      "amount": 48000.0,
      "freq": 16,
      "hour": 3
    }
  }
  ```
- **Response (Safe - HTTP 200)**:
  ```json
  {
    "allowed": true,
    "risk": 0.18,
    "ml_score": 0.22,
    "rule_score": 0.14,
    "reason": "Transaction appears safe",
    "involves_mule": false,
    "involves_ring": false,
    "details": { ... }
  }
  ```

---

### 2. Real-Time Stream (`GET /api/stream`)
Simulates and returns a single transaction tick alongside updated history, graph nodes/edges, and fraud intelligence metrics.

- **URL**: `/api/stream`
- **Method**: `GET`
- **Response (HTTP 200)**:
  ```json
  {
    "tx": {
      "id": "5dab9472",
      "sender": "Vikram",
      "receiver": "Riya",
      "amount": 13585.33,
      "freq": 19,
      "hour": 16,
      "risk": 0.335,
      "timestamp": "23:24:01"
    },
    "history": [ ... ],
    "graph": [
      { "from": "Vikram", "to": "Riya", "weight": 1, "max_risk": 0.335 }
    ],
    "analytics": {
      "pagerank": { "Riya": 0.649, "Vikram": 0.351 },
      "in_degree": { "Riya": 1, "Vikram": 0 },
      "out_degree": { "Riya": 0, "Vikram": 1 }
    },
    "fraud_rings": [],
    "mule_accounts": []
  }
  ```

---

### 3. Server-Sent Events (`GET /api/sse`)
Subscribes the client to real-time transaction updates pushed every 1.5 seconds.

- **URL**: `/api/sse`
- **Method**: `GET`
- **Content-Type**: `text/event-stream`

---

### 4. Network Graph & Analytics (`GET /api/graph`)
Returns the complete graph topology, centrality metrics, detected fraud rings, and mule accounts.

- **URL**: `/api/graph`
- **Method**: `GET`

---

### 5. Transaction History (`GET /api/history`)
Returns the latest scored transactions stored in memory.

- **URL**: `/api/history`
- **Method**: `GET`

---

## 🔬 Machine Learning & Graph Details

| Metric / Model | Implementation | Purpose |
| :--- | :--- | :--- |
| **Random Forest** | `sklearn.ensemble.RandomForestClassifier` | Classifies transaction patterns against known fraud labels. |
| **Simple Cycles** | `networkx.simple_cycles` | Discovers circular fund movements indicative of money laundering. |
| **PageRank** | `networkx.pagerank` | Measures high-traffic settlement hubs and intermediate flow. |
| **In/Out Degree** | `DiGraph.in_degree` / `out_degree` | Pinpoints money mule aggregation and fan-out behavior. |

---

## 👥 Contributors

- **Team Code Blooded** / **Ankit Singh**
- GitHub: [@ankit-2003-singh](https://github.com/ankit-2003-singh)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

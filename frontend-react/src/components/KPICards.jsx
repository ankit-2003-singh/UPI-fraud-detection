import React from "react";

export function riskClass(r) {
  if (r > 0.75) return "risk-high";
  if (r > 0.4)  return "risk-mid";
  return "risk-low";
}

export default function KPICards({ latestTx, txCount, alertCount }) {
  const risk = latestTx?.risk ?? 0;

  return (
    <div className="cards">
      <div className="card">
        <div className="label">Fraud Risk</div>
        <div className={`value ${riskClass(risk)}`}>
          {risk.toFixed(2)}
        </div>
      </div>

      <div className="card">
        <div className="label">Alerts</div>
        <div className="value risk-high">{alertCount}</div>
      </div>

      <div className="card">
        <div className="label">Transactions</div>
        <div className="value">{txCount}</div>
      </div>

      <div className="card">
        <div className="label">ML Model</div>
        <div className="value" style={{ fontSize: "1.1rem", color: "#10b981", fontWeight: 600 }}>
          Random Forest (91% Acc)
        </div>
      </div>
    </div>
  );
}

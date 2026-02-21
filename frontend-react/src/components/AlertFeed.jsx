import React from "react";

export default function AlertFeed({ latestTx, alertCount }) {
  const [alerts, setAlerts] = React.useState([]);

  React.useEffect(() => {
    if (latestTx && latestTx.risk > 0.75) {
      setAlerts((prev) => [latestTx, ...prev].slice(0, 20)); // keep last 20
    }
  }, [latestTx]);

  return (
    <div className="panel">
      <h3>🚨 Fraud Alerts ({alertCount})</h3>
      {alerts.length === 0 && (
        <p className="no-alert">No high-risk transactions yet.</p>
      )}
      {alerts.map((tx, i) => (
        <div key={i} className="alert">
          ⚠️ High risk ₹{tx.amount} {tx.sender} → {tx.receiver}
          <span className="tx-risk"> [{tx.risk.toFixed(3)}]</span>
        </div>
      ))}
    </div>
  );
}

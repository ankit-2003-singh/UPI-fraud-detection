import React, { useState } from "react";
import { riskClass } from "./KPICards";

export default function TransactionList({ history }) {
  const [showAll, setShowAll] = useState(false);

  const display = showAll
    ? [...history].reverse()
    : [...history].reverse().slice(0, 5);

  return (
    <div className="panel">
      <h3>Recent Transactions</h3>

      {display.map((t, i) => (
        <div key={i} className={`tx ${riskClass(t.risk)}`}>
          <span>₹{t.amount} {t.sender} → {t.receiver}</span>
          <span className="tx-risk">risk {t.risk.toFixed(3)}</span>
        </div>
      ))}

      <button
        className="see-more"
        onClick={() => setShowAll((v) => !v)}
      >
        {showAll ? "Show less" : "See more transactions"}
      </button>
    </div>
  );
}

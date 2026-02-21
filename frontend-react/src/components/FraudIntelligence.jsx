import React from "react";

/**
 * FraudRings – displays detected fraud ring (circular money movement) groups.
 */
export function FraudRings({ rings }) {
  if (!rings || rings.length === 0)
    return (
      <div className="panel">
        <h3>🔵 Fraud Rings</h3>
        <p className="no-alert">No fraud rings detected yet.</p>
      </div>
    );

  return (
    <div className="panel">
      <h3>🔵 Fraud Rings ({rings.length})</h3>
      {rings.map((ring, i) => (
        <div key={i} className="alert ring-alert">
          Ring #{i + 1}: {ring.join(" → ")} → {ring[0]}
        </div>
      ))}
    </div>
  );
}

/**
 * MuleAccounts – displays flagged mule accounts based on graph centrality.
 */
export function MuleAccounts({ mules }) {
  if (!mules || mules.length === 0)
    return (
      <div className="panel">
        <h3>🟠 Mule Accounts</h3>
        <p className="no-alert">No mule accounts flagged yet.</p>
      </div>
    );

  return (
    <div className="panel">
      <h3>🟠 Mule Accounts ({mules.length})</h3>
      {mules.map((m, i) => (
        <div key={i} className="alert mule-alert">
          <strong>{m.account}</strong>
          <span className="tx-risk">
            &nbsp;| PageRank: {m.norm_pagerank.toFixed(2)} | 
            In: {m.in_degree} / Out: {m.out_degree}
          </span>
        </div>
      ))}
    </div>
  );
}

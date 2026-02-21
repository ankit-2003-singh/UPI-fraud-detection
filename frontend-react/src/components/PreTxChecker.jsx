import React, { useState } from "react";
import { checkTransaction } from "../api/fraudApi";

const DEFAULT = { sender: "", receiver: "", amount: "", freq: "", hour: "" };

/**
 * PreTxChecker – lets a user submit a pending transaction for pre-flight
 * fraud scoring (the "detect fraud before completion" feature).
 */
export default function PreTxChecker() {
  const [form, setForm] = useState(DEFAULT);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const res = await checkTransaction({
        sender:   form.sender,
        receiver: form.receiver,
        amount:   parseFloat(form.amount) || 0,
        freq:     parseInt(form.freq) || 1,
        hour:     parseInt(form.hour) || 12,
      });
      setResult(res);
    } catch (err) {
      setError("Could not reach backend. Is the Flask server running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel pre-tx-panel">
      <h3>🔒 Pre-Transaction Fraud Check</h3>
      <p className="sub-label">
        Submit a transaction before completing it — we'll block it if it's risky.
      </p>

      <form className="pre-tx-form" onSubmit={handleSubmit}>
        <input name="sender"   placeholder="Sender (e.g. Amit)"    value={form.sender}   onChange={handleChange} required />
        <input name="receiver" placeholder="Receiver (e.g. Neha)"  value={form.receiver} onChange={handleChange} required />
        <input name="amount"   placeholder="Amount (₹)"            value={form.amount}   onChange={handleChange} type="number" min="0" required />
        <input name="freq"     placeholder="Frequency (1–20)"       value={form.freq}     onChange={handleChange} type="number" min="1" max="20" />
        <input name="hour"     placeholder="Hour (0–23)"            value={form.hour}     onChange={handleChange} type="number" min="0" max="23" />
        <button type="submit" disabled={loading}>
          {loading ? "Checking…" : "Check Transaction"}
        </button>
      </form>

      {error && <p className="error-msg">{error}</p>}

      {result && (
        <div className={`pre-tx-result ${result.allowed ? "allowed" : "blocked"}`}>
          <div className="result-badge">
            {result.allowed ? "✅ ALLOWED" : "🚫 BLOCKED"}
          </div>
          <div>Model: <strong>{result.model || "Random Forest Classifier"}</strong></div>
          <div>Risk Score: <strong>{result.risk}</strong> (RF Score: {result.rf_score ?? result.ml_score})</div>
          <div>Reason: {result.reason}</div>
          {result.involves_mule && <div>⚠️ Party is a flagged mule account</div>}
          {result.involves_ring && <div>⚠️ Party is in a detected fraud ring</div>}
        </div>
      )}
    </div>
  );
}

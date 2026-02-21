import { useState, useEffect, useRef } from "react";
import { subscribeSSE } from "../api/fraudApi";

/**
 * useSSE – connects to the backend SSE stream and returns live state.
 * Falls back to polling /api/stream if SSE is not available.
 */
export function useSSE() {
  const [latestTx, setLatestTx]       = useState(null);
  const [history, setHistory]          = useState([]);
  const [graph, setGraph]              = useState([]);
  const [fraudRings, setFraudRings]   = useState([]);
  const [muleAccounts, setMuleAccounts] = useState([]);
  const [alertCount, setAlertCount]   = useState(0);
  const [txCount, setTxCount]         = useState(0);
  const sourceRef = useRef(null);

  useEffect(() => {
    sourceRef.current = subscribeSSE((data) => {
      const tx = data.tx;

      setLatestTx(tx);
      setHistory(data.history || []);
      setGraph(data.graph || []);
      setFraudRings(data.fraud_rings || []);
      setMuleAccounts(data.mule_accounts || []);
      setTxCount((c) => c + 1);

      if (tx.risk > 0.75) {
        setAlertCount((c) => c + 1);
      }
    });

    return () => sourceRef.current?.close();
  }, []);

  return { latestTx, history, graph, fraudRings, muleAccounts, alertCount, txCount };
}

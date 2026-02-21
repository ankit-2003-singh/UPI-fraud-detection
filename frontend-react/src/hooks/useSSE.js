import { useState, useEffect, useRef } from "react";
import { subscribeSSE, fetchStream } from "../api/fraudApi";

/**
 * useSSE – connects to the backend SSE stream and returns live state.
 * Includes immediate initial fetch and automatic fallback to polling /api/stream.
 */
export function useSSE() {
  const [latestTx, setLatestTx]         = useState(null);
  const [history, setHistory]           = useState([]);
  const [graph, setGraph]               = useState([]);
  const [fraudRings, setFraudRings]     = useState([]);
  const [muleAccounts, setMuleAccounts] = useState([]);
  const [alertCount, setAlertCount]     = useState(0);
  const [txCount, setTxCount]           = useState(0);
  const sourceRef = useRef(null);

  useEffect(() => {
    let pollInterval = null;

    const handleData = (data) => {
      if (!data || !data.tx) return;
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
    };

    // Immediate initial tick
    fetchStream()
      .then(handleData)
      .catch(() => {});

    // Subscribe to SSE
    try {
      sourceRef.current = subscribeSSE(handleData);
      sourceRef.current.onerror = () => {
        // Fallback to polling /api/stream if SSE connection encounters an issue
        if (!pollInterval) {
          pollInterval = setInterval(async () => {
            try {
              const data = await fetchStream();
              handleData(data);
            } catch (_) {}
          }, 1500);
        }
      };
    } catch (_) {
      pollInterval = setInterval(async () => {
        try {
          const data = await fetchStream();
          handleData(data);
        } catch (_) {}
      }, 1500);
    }

    return () => {
      sourceRef.current?.close();
      if (pollInterval) clearInterval(pollInterval);
    };
  }, []);

  return { latestTx, history, graph, fraudRings, muleAccounts, alertCount, txCount };
}

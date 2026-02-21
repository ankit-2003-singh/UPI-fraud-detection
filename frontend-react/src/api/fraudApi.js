const BASE = "http://127.0.0.1:5000";

/**
 * Poll /api/stream for one transaction tick.
 */
export async function fetchStream() {
  const res = await fetch(`${BASE}/api/stream`);
  if (!res.ok) throw new Error("Stream fetch failed");
  return res.json();
}

/**
 * PRE-TRANSACTION CHECK — blocks fraud before completion.
 * @param {{ sender, receiver, amount, freq, hour }} tx
 */
export async function checkTransaction(tx) {
  const res = await fetch(`${BASE}/api/check`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(tx),
  });
  return res.json();
}

/**
 * Subscribe to Server-Sent Events for true real-time updates.
 * Returns the EventSource so the caller can close it.
 * @param {(data: object) => void} onMessage
 */
export function subscribeSSE(onMessage) {
  const source = new EventSource(`${BASE}/api/sse`);
  source.onmessage = (e) => {
    try {
      onMessage(JSON.parse(e.data));
    } catch (_) {}
  };
  return source;
}

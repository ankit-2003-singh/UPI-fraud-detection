import React, { useEffect, useRef } from "react";

// vis-network is loaded from CDN via index.html; access via window.vis
export default function NetworkGraph({ graphData, latestTx }) {
  const containerRef = useRef(null);
  const networkRef   = useRef(null);
  const nodesRef     = useRef(null);
  const edgesRef     = useRef(null);

  // Initialise the network once
  useEffect(() => {
    if (!window.vis || !containerRef.current) return;
    const { DataSet, Network } = window.vis;

    nodesRef.current = new DataSet([]);
    edgesRef.current = new DataSet([]);

    networkRef.current = new Network(
      containerRef.current,
      { nodes: nodesRef.current, edges: edgesRef.current },
      {
        nodes: { shape: "dot", size: 12, font: { color: "#e2e8f0" }, borderWidth: 2 },
        edges: { color: "#64748b", arrows: "to" },
        physics: { stabilization: false },
      }
    );
  }, []);

  // Update nodes/edges whenever graph data changes
  useEffect(() => {
    if (!nodesRef.current || !edgesRef.current || !graphData) return;

    graphData.forEach((e) => {
      const isFraud =
        latestTx &&
        (e.from === latestTx.sender || e.to === latestTx.receiver);

      const color = isFraud ? "#ef4444" : "#38bdf8";

      nodesRef.current.update({ id: e.from, label: e.from, color });
      nodesRef.current.update({ id: e.to,   label: e.to,   color });

      edgesRef.current.update({
        id:    `${e.from}-${e.to}`,
        from:  e.from,
        to:    e.to,
        width: Math.min(e.weight || 1, 5),
        color: { color: isFraud ? "#ef4444" : "#64748b" },
      });
    });
  }, [graphData, latestTx]);

  return <div id="graph" ref={containerRef} style={{ width: "100%", height: "400px" }} />;
}

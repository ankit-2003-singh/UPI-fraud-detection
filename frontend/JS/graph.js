let nodes = new vis.DataSet([]);
let edges = new vis.DataSet([]);

let network = new vis.Network(
  document.getElementById("graph"),
  {nodes:nodes,edges:edges},
  {
    nodes:{
      shape:"dot",
      size:12,
      font:{color:"#e2e8f0"},
      borderWidth:2
    },
    edges:{color:"#64748b"}
  }
);

function updateGraph(graphData, riskTx){
  graphData.forEach(e=>{
    let isFraud = riskTx && (e.from===riskTx.sender || e.to===riskTx.receiver);

    nodes.update({
      id:e.from,
      label:e.from,
      color:isFraud ? "#ef4444" : "#38bdf8"
    });

    nodes.update({
      id:e.to,
      label:e.to,
      color:isFraud ? "#ef4444" : "#38bdf8"
    });

    edges.update({from:e.from,to:e.to});
  });
}

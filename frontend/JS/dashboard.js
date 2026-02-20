let alertCount = 0;
let txCount = 0;
let showAllTx = false;

function riskClass(r){
  if(r > 0.75) return "risk-high";
  if(r > 0.4) return "risk-mid";
  return "risk-low";
}

function addAlert(tx){
  alertCount++;
  document.getElementById("alertCount").innerText = alertCount;

  let el = document.createElement("div");
  el.className = "alert";
  el.innerText = `⚠️ High risk ₹${tx.amount} ${tx.sender} → ${tx.receiver}`;

  document.getElementById("alerts").prepend(el);
}

function updateHistory(list){
  let html = "";

  let data = showAllTx
    ? list.slice().reverse()
    : list.slice().reverse().slice(0,5);

  data.forEach(t=>{
    html += `
      <div class="tx ${riskClass(t.risk)}">
        <span>₹${t.amount} ${t.sender} → ${t.receiver}</span>
        <span class="tx-risk">risk ${t.risk.toFixed(3)}</span>
      </div>
    `;
  });

  document.getElementById("history").innerHTML = html;
}

function updateKPIs(data){
  txCount++;
  document.getElementById("txCount").innerText = txCount;

  const riskEl = document.getElementById("riskValue");
  riskEl.innerText = data.tx.risk.toFixed(2);
  riskEl.className = "value " + riskClass(data.tx.risk);
}

document.addEventListener("DOMContentLoaded", ()=>{
  const btn = document.getElementById("seeMoreBtn");

  if(btn){
    btn.addEventListener("click", ()=>{
      showAllTx = !showAllTx;
      btn.innerText = showAllTx
        ? "Show less"
        : "See more transactions";
    });
  }
});

async function loop(){
  try{
    const data = await fetchStream();

    updateKPIs(data);

    if(data.tx.risk > 0.75){
      addAlert(data.tx);
    }

    updateGraph(data.graph, data.tx);
    updateHistory(data.history);

  }catch(err){
    console.error(err);
  }
}

setInterval(loop, 1500);
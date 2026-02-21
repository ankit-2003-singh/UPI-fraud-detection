import networkx as nx
from collections import defaultdict

class GraphEngine:
    def __init__(self):
        self.G = nx.DiGraph()          # Directed graph for UPI flow direction
        self._tx_counts = defaultdict(int)   # sender → tx count
        self._recv_counts = defaultdict(int) # receiver → recv count

    # ── Add a new transaction edge ────────────────────────────────────────
    def add_tx(self, sender, receiver, amount=0, risk=0.0):
        """Record a transaction and update edge weights."""
        if self.G.has_edge(sender, receiver):
            self.G[sender][receiver]["weight"] += 1
            self.G[sender][receiver]["total_amount"] += amount
        else:
            self.G.add_edge(sender, receiver, weight=1,
                            total_amount=amount, max_risk=risk)

        self.G[sender][receiver]["max_risk"] = max(
            self.G[sender][receiver]["max_risk"], risk
        )
        self._tx_counts[sender] += 1
        self._recv_counts[receiver] += 1

    # ── Full graph analytics ──────────────────────────────────────────────
    def get_analytics(self):
        """Return centrality metrics and graph-level stats."""
        if len(self.G.nodes) == 0:
            return {}

        # PageRank – who receives the most flow (mule candidates)
        try:
            pr = nx.pagerank(self.G, alpha=0.85)
        except Exception:
            pr = {n: 0 for n in self.G.nodes}

        # In-degree centrality – high in-degree = many senders = potential mule
        in_deg = dict(self.G.in_degree())
        out_deg = dict(self.G.out_degree())

        return {
            "pagerank": {k: round(v, 4) for k, v in pr.items()},
            "in_degree": in_deg,
            "out_degree": out_deg,
        }

    # ── Fraud ring detection ──────────────────────────────────────────────
    def detect_fraud_rings(self):
        """
        Detect fraud rings as strongly-connected components (SCCs) with
        more than 2 nodes. Cyclic money movement is a classic fraud-ring
        pattern (A→B→C→A).
        """
        rings = []
        for scc in nx.strongly_connected_components(self.G):
            if len(scc) >= 3:                    # ring needs ≥3 participants
                rings.append(sorted(scc))
        return rings

    # ── Mule account detection ────────────────────────────────────────────
    def detect_mules(self, pagerank_threshold=0.25, recv_threshold=3):
        """
        Flag potential mule accounts:
          • High PageRank (many senders route money through them)
          • High in-degree relative to out-degree (receive more than send)
          • Receive from 3+ distinct senders
        """
        mules = []
        if not self.G.nodes:
            return mules

        try:
            pr = nx.pagerank(self.G, alpha=0.85)
        except Exception:
            pr = {n: 0 for n in self.G.nodes}

        max_pr = max(pr.values()) if pr else 1

        for node in self.G.nodes:
            in_d = self.G.in_degree(node)
            out_d = self.G.out_degree(node)
            node_pr = pr.get(node, 0)

            # Normalised PR score
            norm_pr = node_pr / max_pr if max_pr > 0 else 0

            is_mule = (
                norm_pr >= pagerank_threshold and
                in_d >= recv_threshold and
                in_d > out_d          # receives more than sends
            )
            if is_mule:
                mules.append({
                    "account": node,
                    "in_degree": in_d,
                    "out_degree": out_d,
                    "pagerank": round(node_pr, 4),
                    "norm_pagerank": round(norm_pr, 4),
                })

        return mules

    # ── Edge list for vis-network ─────────────────────────────────────────
    def edges(self):
        result = []
        for u, v, d in self.G.edges(data=True):
            result.append({
                "from": u,
                "to": v,
                "weight": d.get("weight", 1),
                "max_risk": d.get("max_risk", 0),
            })
        return result


graph_engine = GraphEngine()

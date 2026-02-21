from flask import jsonify, request, Response
import json, time
from fraud_engine.model import fraud_model
from fraud_engine.risk_rules import rule_based_risk
from fraud_engine.graph_engine import graph_engine
from data.simulator import generate_tx
from data.storage import save, recent

def _score_tx(tx):
    """Shared scoring logic used by both /api/stream and /api/check."""
    ml   = fraud_model.score(tx["amount"], tx["freq"], tx["hour"])
    rule = rule_based_risk(tx)
    risk = round((ml + rule) / 2, 3)
    return risk, ml, rule

def register_routes(app):

    # ── /api/stream  ── polling endpoint (existing dashboard loop) ─────────
    @app.route("/api/stream")
    def stream():
        tx = generate_tx()
        risk, ml, rule = _score_tx(tx)
        tx["risk"] = risk

        save(tx)
        graph_engine.add_tx(tx["sender"], tx["receiver"],
                            amount=tx["amount"], risk=risk)

        rings = graph_engine.detect_fraud_rings()
        mules = graph_engine.detect_mules()

        return jsonify({
            "tx":          tx,
            "history":     recent(),
            "graph":       graph_engine.edges(),
            "analytics":   graph_engine.get_analytics(),
            "fraud_rings": rings,
            "mule_accounts": mules,
        })

    # ── /api/check  ── PRE-TRANSACTION fraud gate ──────────────────────────
    #
    # POST body (JSON):
    #   { "sender": "Amit", "receiver": "Neha",
    #     "amount": 45000, "freq": 18, "hour": 3 }
    #
    # Response:
    #   { "allowed": true/false, "risk": 0.82,
    #     "reason": "High risk transaction blocked", "details": {...} }
    #
    @app.route("/api/check", methods=["POST"])
    def check_transaction():
        """
        Pre-transaction fraud gate.
        Scores a pending transaction BEFORE it is committed and returns
        an allow/block decision. This simulates blocking fraud before
        transaction completion.
        """
        body = request.get_json(force=True, silent=True) or {}

        tx = {
            "sender":   body.get("sender",   "unknown"),
            "receiver": body.get("receiver", "unknown"),
            "amount":   float(body.get("amount", 0)),
            "freq":     int(body.get("freq",   1)),
            "hour":     int(body.get("hour",   12)),
        }

        risk, ml_score, rule_score = _score_tx(tx)

        # Check if either party is a known mule account
        mules        = graph_engine.detect_mules()
        mule_ids     = {m["account"] for m in mules}
        involves_mule = tx["sender"] in mule_ids or tx["receiver"] in mule_ids

        # Check if either party is in a fraud ring
        rings             = graph_engine.detect_fraud_rings()
        ring_members      = {node for ring in rings for node in ring}
        involves_ring     = tx["sender"] in ring_members or tx["receiver"] in ring_members

        # Decision logic
        BLOCK_THRESHOLD = 0.75
        blocked = risk >= BLOCK_THRESHOLD or involves_mule or involves_ring

        reasons = []
        if risk >= BLOCK_THRESHOLD:
            reasons.append(f"Risk score {risk} exceeds threshold {BLOCK_THRESHOLD}")
        if involves_mule:
            reasons.append("Party is a flagged mule account")
        if involves_ring:
            reasons.append("Party belongs to a detected fraud ring")

        return jsonify({
            "allowed":       not blocked,
            "risk":          risk,
            "ml_score":      ml_score,
            "rule_score":    rule_score,
            "reason":        "; ".join(reasons) if blocked else "Transaction appears safe",
            "involves_mule": involves_mule,
            "involves_ring": involves_ring,
            "details": {
                "sender":   tx["sender"],
                "receiver": tx["receiver"],
                "amount":   tx["amount"],
                "freq":     tx["freq"],
                "hour":     tx["hour"],
            }
        }), (200 if not blocked else 403)

    # ── /api/sse  ── Server-Sent Events for true real-time push ───────────
    @app.route("/api/sse")
    def sse():
        """
        Server-Sent Events stream. The frontend connects once and receives
        a new transaction event every 1.5 s without polling.
        """
        def event_stream():
            while True:
                tx = generate_tx()
                risk, _, _ = _score_tx(tx)
                tx["risk"] = risk
                save(tx)
                graph_engine.add_tx(tx["sender"], tx["receiver"],
                                    amount=tx["amount"], risk=risk)

                payload = json.dumps({
                    "tx":            tx,
                    "history":       recent(),
                    "graph":         graph_engine.edges(),
                    "fraud_rings":   graph_engine.detect_fraud_rings(),
                    "mule_accounts": graph_engine.detect_mules(),
                })
                yield f"data: {payload}\n\n"
                time.sleep(1.5)

        return Response(event_stream(),
                        mimetype="text/event-stream",
                        headers={
                            "Cache-Control": "no-cache",
                            "X-Accel-Buffering": "no",
                        })

    # ── /api/history  ── retrieve recent transactions ─────────────────────
    @app.route("/api/history")
    def history():
        return jsonify({"history": recent()})

    # ── /api/graph  ── retrieve graph + analytics snapshot ────────────────
    @app.route("/api/graph")
    def graph_snapshot():
        return jsonify({
            "edges":         graph_engine.edges(),
            "analytics":     graph_engine.get_analytics(),
            "fraud_rings":   graph_engine.detect_fraud_rings(),
            "mule_accounts": graph_engine.detect_mules(),
        })

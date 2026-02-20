from flask import jsonify
from fraud_engine.model import fraud_model
from fraud_engine.risk_rules import rule_based_risk
from fraud_engine.graph_engine import graph_engine
from data.simulator import generate_tx
from data.storage import save, recent

def register_routes(app):

    @app.route("/api/stream")
    def stream():

        tx = generate_tx()

        ml = fraud_model.score(tx["amount"], tx["freq"], tx["hour"])
        rule = rule_based_risk(tx)

        risk = round((ml + rule)/2,3)
        tx["risk"] = risk

        save(tx)
        graph_engine.add_tx(tx["sender"], tx["receiver"])

        return jsonify({
            "tx": tx,
            "history": recent(),
            "graph": graph_engine.edges()
        })

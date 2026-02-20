def rule_based_risk(tx):
    risk = 0

    if tx["amount"] > 30000:
        risk += 0.3

    if tx["freq"] > 15:
        risk += 0.3

    if tx["hour"] < 5:
        risk += 0.2

    return min(risk, 1.0)

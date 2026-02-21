def rule_based_risk(tx):
    """
    Rule-based risk scorer.
    Returns a float in [0, 1] based on amount, frequency, and hour rules.
    """
    risk = 0.0

    # --- Amount thresholds ---
    if tx["amount"] > 40000:
        risk += 0.35
    elif tx["amount"] > 30000:
        risk += 0.20

    # --- Transaction frequency ---
    if tx["freq"] > 18:
        risk += 0.30
    elif tx["freq"] > 12:
        risk += 0.15

    # --- Odd hours (late night / early morning) ---
    if tx["hour"] < 4:
        risk += 0.25
    elif tx["hour"] < 6:
        risk += 0.10

    # --- Self-transfer (same sender & receiver is suspicious) ---
    if tx.get("sender") == tx.get("receiver"):
        risk += 0.40

    return min(risk, 1.0)

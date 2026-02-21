history = []

def save(tx):
    history.append(tx)
    # Keep memory bounded to last 500 transactions
    if len(history) > 500:
        history.pop(0)

def recent(n=50):
    return history[-n:]

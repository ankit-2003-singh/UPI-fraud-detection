history = []

def save(tx):
    history.append(tx)

def recent(n=20):
    return history[-n:]

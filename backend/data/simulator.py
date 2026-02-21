import random
import uuid
import datetime
from data.dataset_loader import load_dataset

# Fallback pool
default_users = ["Amit", "Neha", "Rahul", "Priya", "Karan", "Sneha", "Vikram", "Riya"]

# Try loading Kaggle dataset
_dataset = load_dataset()
_cursor = 0

def generate_tx():
    """
    Generate next transaction.
    Pulls real records sequentially from the Kaggle dataset if present,
    otherwise falls back to synthetic generation.
    """
    global _cursor, _dataset

    if _dataset is not None and len(_dataset) > 0:
        row = _dataset.iloc[_cursor]
        _cursor = (_cursor + 1) % len(_dataset)

        return {
            "id":        str(uuid.uuid4())[:8],
            "sender":    str(row["display_sender"]),
            "receiver":  str(row["display_receiver"]),
            "amount":    float(row["amount"]),
            "freq":      int(row["freq"]),
            "hour":      int(row["hour"]),
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "dataset_label": int(row.get("isFraud", 0))
        }

    # Fallback synthetic generator
    sender   = random.choice(default_users)
    receiver = random.choice([u for u in default_users if u != sender])
    hour     = random.randint(0, 23)

    return {
        "id":        str(uuid.uuid4())[:8],
        "sender":    sender,
        "receiver":  receiver,
        "amount":    random.randint(100, 50000),
        "freq":      random.randint(1, 20),
        "hour":      hour,
        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
    }

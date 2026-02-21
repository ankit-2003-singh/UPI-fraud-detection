import os
import glob
import pandas as pd
import numpy as np

DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def find_kaggle_dataset():
    """
    Search data directory for Kaggle dataset CSVs in priority order:
    1. Any file matching *kaggle* or *upi* or *paysim*
    2. Any .csv in data/
    """
    candidates = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    if not candidates:
        return None

    for c in candidates:
        low = os.path.basename(c).lower()
        if "kaggle" in low or "upi" in low or "paysim" in low:
            return c

    return candidates[0]

def load_dataset():
    """
    Load dataset from CSV, normalize columns, and return a clean DataFrame.
    Guarantees unique column names:
      - amount
      - sender
      - receiver
      - hour
      - freq
      - isFraud
      - display_sender
      - display_receiver
    """
    csv_file = find_kaggle_dataset()
    if not csv_file:
        return None

    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print(f"[DatasetLoader] Error reading {csv_file}: {e}")
        return None

    # Find the best column for each required field
    cols_lower = {col.lower(): col for col in df.columns}

    def pick_col(candidates):
        for c in candidates:
            if c in cols_lower:
                return cols_lower[c]
        return None

    sender_col   = pick_col(["nameorig", "sender", "from", "source", "sender_id"])
    receiver_col = pick_col(["namedest", "receiver", "to", "destination", "recipient_id"])
    amount_col   = pick_col(["amount", "amt", "tx_amount", "transaction_amount"])
    fraud_col    = pick_col(["isfraud", "is_fraud", "class", "label", "fraud"])
    hour_col     = pick_col(["hour", "step", "time"])
    freq_col     = pick_col(["freq", "frequency", "tx_count"])

    clean_df = pd.DataFrame()

    # Amount
    if amount_col:
        clean_df["amount"] = pd.to_numeric(df[amount_col], errors="coerce").fillna(100.0)
    else:
        clean_df["amount"] = np.random.uniform(100, 25000, size=len(df)).round(2)

    # Sender & Receiver
    clean_df["sender"] = df[sender_col].astype(str) if sender_col else "UserA"
    clean_df["receiver"] = df[receiver_col].astype(str) if receiver_col else "UserB"

    # Hour (0 - 23)
    if hour_col:
        clean_df["hour"] = (pd.to_numeric(df[hour_col], errors="coerce").fillna(12).astype(int)) % 24
    else:
        clean_df["hour"] = np.random.randint(0, 24, size=len(df))

    # Frequency
    if freq_col:
        clean_df["freq"] = pd.to_numeric(df[freq_col], errors="coerce").fillna(1).astype(int)
    else:
        sender_counts = clean_df["sender"].value_counts().to_dict()
        clean_df["freq"] = clean_df["sender"].map(lambda s: min(sender_counts.get(s, 1), 20))

    # Fraud label
    if fraud_col:
        clean_df["isFraud"] = pd.to_numeric(df[fraud_col], errors="coerce").fillna(0).astype(int)
    else:
        clean_df["isFraud"] = 0

    # Clean display names
    def clean_name(val):
        val_str = str(val).strip()
        if "@" in val_str:
            return val_str.split("@")[0].capitalize()
        if val_str.startswith("C") and val_str[1:].isdigit():  # PaySim style C123456789
            return "User_" + val_str[-4:]
        if val_str.startswith("M") and val_str[1:].isdigit():  # PaySim merchant M123456789
            return "Shop_" + val_str[-4:]
        return val_str[:14]

    clean_df["display_sender"] = clean_df["sender"].apply(clean_name)
    clean_df["display_receiver"] = clean_df["receiver"].apply(clean_name)

    print(f"[DatasetLoader] Loaded {len(clean_df)} transactions from {os.path.basename(csv_file)} (Fraud: {clean_df['isFraud'].sum()})")
    return clean_df

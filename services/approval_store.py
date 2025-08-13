import json
from pathlib import Path

DATA_FILE = Path("data/approved_reviews.json")

def load_approvals():
    if not DATA_FILE.exists():
        return set()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_approvals(approved_ids):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(list(approved_ids), f)
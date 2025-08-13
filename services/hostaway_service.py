import json
import requests
from datetime import datetime

def fetch_mock_reviews(path="data/mock_reviews.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def fetch_live_reviews(account_id, api_key):
    url = f"https://api.hostaway.com/api/v1/reviews?accountId={account_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[ERROR] Hostaway API request failed: {e}")
        return {"result": []}

def normalize_reviews(raw_data, approved_ids):
    normalized = []
    for r in raw_data.get("result", []):
        overall = r.get("rating")
        if overall is None and r.get("reviewCategory"):
            overall = round(sum(c["rating"] for c in r["reviewCategory"]) / len(r["reviewCategory"]), 2)

        normalized.append({
            "id": r.get("id"),
            "listing": r.get("listingName"),
            "type": r.get("type", "guest-to-host"),
            "channel": "Hostaway",
            "overall_rating": overall,
            "categories": {c["category"]: c["rating"] for c in r.get("reviewCategory", [])},
            "review_text": r.get("publicReview"),
            "submitted_at": datetime.strptime(r.get("submittedAt"), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d"),
            "guest_name": r.get("guestName"),
            "approved": r.get("id") in approved_ids
        })
    return normalized
import requests
from datetime import datetime

def fetch_google_reviews(api_key, property_name_or_address, approved_ids):
    if not api_key:
        print("GOOGLE_API_KEY missing — skipping Google reviews.")
        return []

    # Find Place ID
    find_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params_find = {
        "input": property_name_or_address,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": api_key
    }
    results = requests.get(find_url, params=params_find).json()
    if not results.get("candidates"):
        return []
    place_id = results["candidates"][0]["place_id"]

    # Get Place Details + Reviews
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params_details = {
        "place_id": place_id,
        "fields": "name,reviews,rating,user_ratings_total",
        "key": api_key
    }
    details = requests.get(details_url, params=params_details).json()
    reviews = details.get("result", {}).get("reviews", [])

    normalized = []
    for idx, r in enumerate(reviews):
        review_id = f"google_{place_id}_{idx}"
        normalized.append({
            "id": review_id,
            "listing": details["result"].get("name"),
            "type": "guest-to-host",
            "channel": "Google",
            "overall_rating": r.get("rating"),
            "categories": {},
            "review_text": r.get("text"),
            "submitted_at": datetime.utcfromtimestamp(r.get("time")).strftime("%Y-%m-%d"),
            "guest_name": r.get("author_name"),
            "approved": review_id in approved_ids
        })
    return normalized
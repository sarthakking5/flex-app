import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def fetch_google_reviews(property_address):
    # Step 1: Get Place ID
    place_search_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    params = {
        "input": property_address,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": GOOGLE_API_KEY
    }
    place_res = requests.get(place_search_url, params=params).json()
    if not place_res.get("candidates"):
        return {"error": "Place not found"}
    place_id = place_res["candidates"][0]["place_id"]

    # Step 2: Get Place Details
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,rating,reviews,user_ratings_total",
        "key": GOOGLE_API_KEY
    }
    details_res = requests.get(details_url, params=params).json()
    return details_res

if __name__ == "__main__":
    print(fetch_google_reviews("Safestay London Kensington Holland Park, Holland Park Ave, Holland Walk, London W8 7QU, United Kingdom"))

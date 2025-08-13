import os
from flask import Flask, jsonify, render_template, request, abort
from dotenv import load_dotenv

from services.hostaway_service import fetch_mock_reviews, fetch_live_reviews, normalize_reviews
from services.google_service import fetch_google_reviews
from services.approval_store import load_approvals, save_approvals
from utils.filters import filter_reviews

load_dotenv()

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
)

ACCOUNT_ID = os.getenv("HOSTAWAY_ACCOUNT_ID")
HOSTAWAY_API_KEY = os.getenv("HOSTAWAY_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@app.route("/")
def home():
    routes_info = [
        {"url": "/dashboard", "description": "View the Dashboard with aggregated review trends"},
        {"url": "/api/reviews/hostaway", "description": "Fetch all Hostaway reviews in JSON format"},
        {"url": "/property/<name>", "description": "View property details and reviews (replace <name> with a property name from mock data)"},
        {"url": "/placesapi", "description": "Fetch Google reviews for a hardcoded property."}

    ]
    return render_template("index.html", routes=routes_info)

@app.route("/api/reviews/hostaway")
def api_hostaway():
    approved_ids = load_approvals()
    data = fetch_mock_reviews()
    normalized = normalize_reviews(data, approved_ids)
    return jsonify({"status": "success", "reviews": filter_reviews(normalized, request.args)})

@app.route("/api/reviews/all")
def api_all_reviews():
    approved_ids = load_approvals()
    hostaway_data = normalize_reviews(fetch_mock_reviews(), approved_ids)
    google_data = fetch_google_reviews(GOOGLE_API_KEY, "Your Property Name or Address", approved_ids)
    all_reviews = hostaway_data + google_data
    return jsonify({"status": "success", "reviews": filter_reviews(all_reviews, request.args)})

@app.route("/api/reviews/approve", methods=["POST"])
def api_approve():
    data = request.get_json()
    review_id = data.get("id")
    approved = data.get("approved", False)
    approvals = load_approvals()
    if approved:
        approvals.add(review_id)
    else:
        approvals.discard(review_id)
    save_approvals(approvals)
    return jsonify({"status": "success"})

@app.route("/dashboard")
def dashboard():
    approved_ids = load_approvals()
    hostaway_reviews = normalize_reviews(fetch_mock_reviews(), approved_ids)
    trends = {}
    for r in hostaway_reviews:
        month = r["submitted_at"][:7]
        trends.setdefault(month, []).append(r["overall_rating"])
    avg_trends = {m: round(sum(v)/len(v), 2) for m, v in trends.items()}
    return render_template("dashboard.html", reviews=hostaway_reviews, avg_trends=avg_trends)

@app.route("/placesapi")
def places_api():
    property_address = "Safestay London Kensington Holland Park, Holland Park Ave, Holland Walk, London W8 7QU, United Kingdom"
    approved_ids = set()  # Or fill with IDs if needed
    
    reviews_data = fetch_google_reviews(GOOGLE_API_KEY, property_address, approved_ids)
    
    return jsonify(reviews_data)

@app.route("/property/<name>")
def property_page(name):
    # Load all mock reviews without approval filtering
    all_reviews = normalize_reviews(fetch_mock_reviews(), set())

    # Get unique property names
    property_names = sorted(set(r["listing"] for r in all_reviews))

    # If requested property doesn't exist, fallback to first one
    matching_name = next((p for p in property_names if p.lower() == name.lower()), None)
    if not matching_name and property_names:
        matching_name = property_names[0]

    # Filter reviews for that property
    property_reviews = [r for r in all_reviews if r["listing"].lower() == matching_name.lower()]

    if not property_reviews:
        abort(404, "No reviews available in mock data")

    property_details = {
        "name": matching_name,
        "address": "123 Main St, Example City",
        "description": "Beautiful property in the heart of the city.",
        "images": [
            "/static/images/property1.jpg",
            "/static/images/property2.jpg",
            "/static/images/property3.jpg"
        ],
        "available_properties": property_names  # optional for template navigation
    }

    return render_template("property.html", property=property_details, reviews=property_reviews)


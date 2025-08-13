def filter_reviews(reviews, params):
    filtered = reviews
    channel = params.get("channel")
    rating = params.get("rating")
    start_date = params.get("from")
    end_date = params.get("to")
    category = params.get("category")

    if channel:
        filtered = [r for r in filtered if r["channel"].lower() == channel.lower()]
    if rating:
        filtered = [r for r in filtered if r["overall_rating"] >= float(rating)]
    if start_date:
        filtered = [r for r in filtered if r["submitted_at"] >= start_date]
    if end_date:
        filtered = [r for r in filtered if r["submitted_at"] <= end_date]
    if category:
        filtered = [r for r in filtered if category in r.get("categories", {})]

    return filtered

# Flex App Documentation

## 1. Overview
Flex App is a Flask-based web application designed as a property dashboard and review aggregator. The application provides a centralized interface to view property details, guest reviews, and integrates Google Reviews for additional insights.

---

## 2. Tech Stack
- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, Bootstrap 5  
- **Hosting/Deployment:** Vercel (Python/Flask serverless functions)  
- **APIs:** Google Places API for fetching reviews  
- **Version Control:** Git + GitHub  

---

## 3. Key Design & Logic Decisions
1. **Flask Routing:**  
   - `/` → Main landing page, listing all routes and features.  
   - `/dashboard` → Dashboard page for aggregated property information.  
   - `/property/<name>` → Displays property details and guest reviews (mock data).  
   - `/placesapi` → Fetches live Google Reviews for a hardcoded property address.  

2. **Review Normalization:**  
   - All review sources (mock and Google) are normalized to a consistent structure:
     ```json
     {
       "id", "listing", "type", "channel", "overall_rating",
       "categories", "review_text", "submitted_at", "guest_name", "approved"
     }
     ```

3. **Static Assets:**  
   - Images, CSS, and JS files are stored in `/static`.  
   - Property images are referenced in the template via `{{ url_for('static', filename='images/...') }}`.

4. **Deployment Considerations:**  
   - Serverless functions on Vercel require all routes to be compatible with WSGI.  
   - Sensitive keys (e.g., `GOOGLE_API_KEY`) should be stored in Vercel environment variables, **not hardcoded**.

---

## 4. API Behaviors
### 4.1 /placesapi
- **Method:** GET  
- **Function:** Fetches Google Reviews for a specific property address (currently hardcoded).  
- **Response:** JSON object with normalized reviews.  
- **Error Handling:** Returns an empty list if Google API key is missing or property not found.  

### 4.2 /property/<name>
- **Method:** GET  
- **Function:** Displays a property page with details and mock reviews filtered by property name.  
- **Behavior:**  
  - Returns a 404 page if no reviews are available.  
  - Uses Bootstrap carousel to show property images.

### 4.3 /dashboard
- **Method:** GET  
- **Function:** Placeholder for aggregated property metrics.  
- **Behavior:** Currently renders a static page, can be expanded for analytics.

---

## 5. Google Reviews Integration
- **Findings:**  
  - Google Reviews API provides `name`, `rating`, `reviews`, and `user_ratings_total`.  
  - Reviews are normalized with consistent fields for easier frontend rendering.  
  - Rate limiting may occur if API calls exceed quota; caching or backend throttling is recommended for production.

- **Normalized Example Review:**
```json
{
  "id": "google_xyz_0",
  "listing": "Safestay London Kensington Holland Park",
  "type": "guest-to-host",
  "channel": "Google",
  "overall_rating": 5,
  "categories": {},
  "review_text": "Great stay, very clean and comfortable!",
  "submitted_at": "2025-08-12",
  "guest_name": "John Doe",
  "approved": true
}

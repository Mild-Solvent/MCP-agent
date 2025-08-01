from fastapi import FastAPI
import uvicorn

# Initialize the FastAPI app
app = FastAPI()

# Route for getting website traffic data
@app.get("/tools/get_website_traffic")
async def get_website_traffic():
    """
    Returns total users and bounce rate for the last 30 days.
    """
    return {
        "total_users": 28500, 
        "bounce_rate": 0.32,
        "session_duration": "4m 23s",
        "conversion_rate": 0.076,
        "status": "success",
        "period": "last_30_days"
    }

# Route for getting top pages data
@app.get("/tools/get_top_pages")
async def get_top_pages():
    """
    Returns a list of top 5 pages by views with engagement metrics.
    """
    return {
        "pages": [
            {"page_path": "/products", "page_title": "Product Catalog", "views": 12400, "avg_time": "3m 45s", "bounce_rate": 0.24},
            {"page_path": "/blog", "page_title": "Tech Blog", "views": 8900, "avg_time": "5m 12s", "bounce_rate": 0.18},
            {"page_path": "/home", "page_title": "Homepage", "views": 7200, "avg_time": "2m 30s", "bounce_rate": 0.35},
            {"page_path": "/pricing", "page_title": "Pricing Plans", "views": 4800, "avg_time": "4m 05s", "bounce_rate": 0.28},
            {"page_path": "/about", "page_title": "About Us", "views": 3100, "avg_time": "2m 15s", "bounce_rate": 0.42}
        ],
        "total_pageviews": 36400,
        "period": "last_30_days"
    }

# Route for getting traffic sources
@app.get("/tools/get_traffic_sources")
async def get_traffic_sources():
    """
    Returns a list of top 6 traffic sources by users with detailed metrics.
    """
    return {
        "sources": [
            {"source": "Organic Search", "users": 14200, "percentage": 49.8, "growth": "+15%"},
            {"source": "Social Media", "users": 6800, "percentage": 23.9, "growth": "+32%"},
            {"source": "Direct Traffic", "users": 4200, "percentage": 14.7, "growth": "+8%"},
            {"source": "Email Marketing", "users": 2100, "percentage": 7.4, "growth": "+45%"},
            {"source": "Referral Sites", "users": 800, "percentage": 2.8, "growth": "+12%"},
            {"source": "Paid Ads", "users": 400, "percentage": 1.4, "growth": "-5%"}
        ],
        "total_users": 28500,
        "period": "last_30_days",
        "top_performing_source": "Organic Search"
    }

# Instructions
"""
To run the server locally:
1. Make sure you have FastAPI and Uvicorn installed:
   pip install fastapi uvicorn

2. Run the server using the command:
   uvicorn mcp_server:app --reload

3. Access the endpoints on http://localhost:8000
"""

# Entry point
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

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
    return {"total_users": 15000, "bounce_rate": 0.45}

# Route for getting top pages data
@app.get("/tools/get_top_pages")
async def get_top_pages():
    """
    Returns a list of top 3 pages by views.
    """
    return {
        "pages": [
            {"page_path": "/home", "page_title": "Homepage", "views": 5000},
            {"page_path": "/about", "page_title": "About Us", "views": 3000},
            {"page_path": "/contact", "page_title": "Contact", "views": 2000}
        ]
    }

# Route for getting traffic sources
@app.get("/tools/get_traffic_sources")
async def get_traffic_sources():
    """
    Returns a list of top 3 traffic sources by users.
    """
    return {
        "sources": [
            {"source": "Organic Search", "users": 7000},
            {"source": "Direct", "users": 5000},
            {"source": "Referral", "users": 3000}
        ]
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

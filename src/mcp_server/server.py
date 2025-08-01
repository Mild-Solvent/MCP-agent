from fastapi import FastAPI

app = FastAPI()

# Simulated Google Analytics data
fake_data = {
    "sessions": 1000,
    "bounce_rate": 50,
    "average_session_duration": 200
}

@app.get("/analytics")
async def get_analytics_data():
    """
    Simulate Google Analytics API response with pre-defined static data.
    """
    return fake_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

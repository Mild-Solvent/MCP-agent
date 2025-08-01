import requests

class AIAgent:
    def __init__(self, server_url):
        self.server_url = server_url

    def fetch_data(self):
        """
        Connect to the local MCP server and retrieve analytics data.
        """
        try:
            response = requests.get(f"{self.server_url}/analytics")
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            print(f"Failed to fetch data: {e}")
            return None

    def analyze_data(self, data):
        """
        Analyze the data and return actionable insights.
        """
        if data:
            # Placeholder for analysis logic
            sessions = data.get('sessions', 0)
            bounce_rate = data.get('bounce_rate', 0)
            avg_duration = data.get('average_session_duration', 0)

            print(f"Sessions: {sessions}")
            print(f"Bounce Rate: {bounce_rate}%")
            print(f"Average Session Duration: {avg_duration} seconds")
            # More analysis logic goes here
        else:
            print("No data to analyze.")

if __name__ == "__main__":
    server_url = "http://localhost:8000"
    agent = AIAgent(server_url)
    data = agent.fetch_data()
    agent.analyze_data(data)

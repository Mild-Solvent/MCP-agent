#!/usr/bin/env python3
"""
Google Analytics MCP Server

This server simulates Google Analytics data using the Model Context Protocol (MCP).
It provides static, pre-defined analytics data for development and testing purposes.

The server exposes tools that an AI agent can use to retrieve various types of 
analytics data including:
- Traffic metrics (sessions, page views, users)
- Engagement metrics (bounce rate, session duration)
- Conversion metrics (goal completions, conversion rate)
- Demographic data (user locations, devices)
"""

import asyncio
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import random

# Simulated Google Analytics data store
class GADataStore:
    """
    Simulated Google Analytics data store containing static data
    for development and testing purposes.
    """
    
    def __init__(self):
        self.base_date = datetime.now() - timedelta(days=30)
        
    def get_traffic_metrics(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get traffic metrics like sessions, page views, and users."""
        return {
            "sessions": random.randint(800, 1200),
            "pageviews": random.randint(2000, 4000),
            "users": random.randint(600, 1000),
            "new_users": random.randint(200, 400),
            "pages_per_session": round(random.uniform(2.1, 3.5), 2),
            "date_range": {
                "start_date": start_date,
                "end_date": end_date
            }
        }
    
    def get_engagement_metrics(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Get engagement metrics like bounce rate and session duration."""
        return {
            "bounce_rate": round(random.uniform(35.0, 65.0), 2),
            "average_session_duration": random.randint(120, 300),
            "pages_per_session": round(random.uniform(2.0, 4.0), 2),
            "session_duration_distribution": {
                "0-30s": random.randint(20, 40),
                "30s-1m": random.randint(15, 25),
                "1m-3m": random.randint(20, 35),
                "3m+": random.randint(10, 25)
            },
            "date_range": {
                "start_date": start_date,
                "end_date": end_date
            }
        }
    
    def get_top_pages(self, limit: int = 10) -> Dict[str, Any]:
        """Get top performing pages by page views."""
        pages = [
            {"page": "/", "pageviews": random.randint(300, 600), "unique_pageviews": random.randint(250, 500)},
            {"page": "/about", "pageviews": random.randint(100, 200), "unique_pageviews": random.randint(80, 180)},
            {"page": "/products", "pageviews": random.randint(150, 300), "unique_pageviews": random.randint(120, 250)},
            {"page": "/contact", "pageviews": random.randint(50, 120), "unique_pageviews": random.randint(40, 100)},
            {"page": "/blog", "pageviews": random.randint(80, 180), "unique_pageviews": random.randint(60, 150)},
        ]
        return {
            "top_pages": sorted(pages, key=lambda x: x["pageviews"], reverse=True)[:limit],
            "total_pages_analyzed": len(pages)
        }
    
    def get_traffic_sources(self) -> Dict[str, Any]:
        """Get traffic source breakdown."""
        return {
            "channels": {
                "organic_search": round(random.uniform(40.0, 60.0), 2),
                "direct": round(random.uniform(20.0, 35.0), 2),
                "social": round(random.uniform(10.0, 20.0), 2),
                "referral": round(random.uniform(5.0, 15.0), 2),
                "paid_search": round(random.uniform(3.0, 10.0), 2),
                "email": round(random.uniform(2.0, 8.0), 2)
            },
            "top_referrers": [
                {"source": "google.com", "sessions": random.randint(200, 400)},
                {"source": "facebook.com", "sessions": random.randint(50, 150)},
                {"source": "twitter.com", "sessions": random.randint(30, 100)},
                {"source": "linkedin.com", "sessions": random.randint(20, 80)}
            ]
        }
    
    def get_demographic_data(self) -> Dict[str, Any]:
        """Get user demographic information."""
        return {
            "countries": [
                {"country": "United States", "sessions": random.randint(300, 500), "percentage": round(random.uniform(35.0, 50.0), 2)},
                {"country": "United Kingdom", "sessions": random.randint(100, 200), "percentage": round(random.uniform(10.0, 20.0), 2)},
                {"country": "Canada", "sessions": random.randint(50, 150), "percentage": round(random.uniform(5.0, 15.0), 2)},
                {"country": "Germany", "sessions": random.randint(40, 120), "percentage": round(random.uniform(4.0, 12.0), 2)},
                {"country": "Australia", "sessions": random.randint(30, 100), "percentage": round(random.uniform(3.0, 10.0), 2)}
            ],
            "devices": {
                "desktop": round(random.uniform(45.0, 65.0), 2),
                "mobile": round(random.uniform(30.0, 45.0), 2),
                "tablet": round(random.uniform(5.0, 15.0), 2)
            },
            "age_groups": {
                "18-24": round(random.uniform(15.0, 25.0), 2),
                "25-34": round(random.uniform(25.0, 35.0), 2),
                "35-44": round(random.uniform(20.0, 30.0), 2),
                "45-54": round(random.uniform(15.0, 25.0), 2),
                "55-64": round(random.uniform(10.0, 20.0), 2),
                "65+": round(random.uniform(5.0, 15.0), 2)
            }
        }


class GAMCPServer:
    """
    MCP Server implementation for Google Analytics data simulation.
    
    This server provides tools that can be called by MCP clients (like AI agents)
    to retrieve various types of analytics data.
    """
    
    def __init__(self):
        self.data_store = GADataStore()
        self.tools = {
            "get_traffic_metrics": {
                "description": "Get traffic metrics including sessions, page views, and users for a date range",
                "parameters": {
                    "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD format"},
                    "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format"}
                }
            },
            "get_engagement_metrics": {
                "description": "Get engagement metrics like bounce rate and session duration",
                "parameters": {
                    "start_date": {"type": "string", "description": "Start date in YYYY-MM-DD format"},
                    "end_date": {"type": "string", "description": "End date in YYYY-MM-DD format"}
                }
            },
            "get_top_pages": {
                "description": "Get top performing pages by page views",
                "parameters": {
                    "limit": {"type": "integer", "description": "Number of top pages to return (default: 10)"}
                }
            },
            "get_traffic_sources": {
                "description": "Get traffic source breakdown and top referrers",
                "parameters": {}
            },
            "get_demographic_data": {
                "description": "Get user demographic information including countries, devices, and age groups",
                "parameters": {}
            }
        }
    
    async def handle_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle tool calls from MCP clients.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool call
            
        Returns:
            Dictionary containing the tool execution results
        """
        try:
            if tool_name == "get_traffic_metrics":
                start_date = parameters.get("start_date", "2024-01-01")
                end_date = parameters.get("end_date", "2024-01-31")
                return self.data_store.get_traffic_metrics(start_date, end_date)
            
            elif tool_name == "get_engagement_metrics":
                start_date = parameters.get("start_date", "2024-01-01")
                end_date = parameters.get("end_date", "2024-01-31")
                return self.data_store.get_engagement_metrics(start_date, end_date)
            
            elif tool_name == "get_top_pages":
                limit = parameters.get("limit", 10)
                return self.data_store.get_top_pages(limit)
            
            elif tool_name == "get_traffic_sources":
                return self.data_store.get_traffic_sources()
            
            elif tool_name == "get_demographic_data":
                return self.data_store.get_demographic_data()
            
            else:
                return {"error": f"Unknown tool: {tool_name}"}
                
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}
    
    def get_available_tools(self) -> Dict[str, Any]:
        """Return list of available tools and their descriptions."""
        return self.tools


# Simple HTTP server for testing (not full MCP protocol implementation)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Google Analytics MCP Server", version="1.0.0")
server = GAMCPServer()

class ToolCallRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any] = {}

@app.get("/")
async def root():
    """Root endpoint with server information."""
    return {
        "name": "Google Analytics MCP Server",
        "version": "1.0.0",
        "description": "Simulated Google Analytics data server using MCP protocol",
        "available_tools": list(server.tools.keys())
    }

@app.get("/tools")
async def get_tools():
    """Get list of available tools."""
    return server.get_available_tools()

@app.post("/tools/{tool_name}")
async def call_tool(tool_name: str, request: ToolCallRequest):
    """Execute a specific tool."""
    if tool_name not in server.tools:
        raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")
    
    result = await server.handle_tool_call(tool_name, request.parameters)
    return result

@app.post("/call_tool")
async def call_tool_generic(request: ToolCallRequest):
    """Generic tool call endpoint."""
    result = await server.handle_tool_call(request.tool_name, request.parameters)
    return result

if __name__ == "__main__":
    import uvicorn
    print("Starting Google Analytics MCP Server...")
    print("Available tools:", list(server.tools.keys()))
    uvicorn.run(app, host="localhost", port=8000)

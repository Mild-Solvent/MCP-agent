#!/usr/bin/env python3
"""
Google Analytics AI Agent

This AI agent connects to the Google Analytics MCP server to retrieve
analytics data and provide intelligent insights and recommendations.

The agent can:
- Fetch various types of analytics data via MCP tools
- Analyze the data to identify trends and issues
- Generate actionable recommendations
- Create visualizations and reports
- Answer natural language questions about the data
"""

import asyncio
import httpx
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
from dataclasses import dataclass
from enum import Enum


class InsightType(Enum):
    """Types of insights the agent can generate."""
    PERFORMANCE = "performance"
    OPTIMIZATION = "optimization"
    TREND = "trend"
    ALERT = "alert"
    RECOMMENDATION = "recommendation"


@dataclass
class Insight:
    """Represents an analytical insight with recommendations."""
    type: InsightType
    title: str
    description: str
    severity: str  # "low", "medium", "high", "critical"
    recommendations: List[str]
    data_source: str
    confidence: float  # 0.0 to 1.0


class MCPClient:
    """
    MCP Client for communicating with the Google Analytics MCP Server.
    
    This client handles the communication with the MCP server, including
    tool discovery and execution.
    """
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.server_url = server_url
        self.available_tools = {}
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def initialize(self):
        """Initialize the MCP client by discovering available tools."""
        try:
            response = await self.client.get(f"{self.server_url}/tools")
            response.raise_for_status()
            self.available_tools = response.json()
            print(f"✓ Connected to MCP server. Available tools: {list(self.available_tools.keys())}")
        except Exception as e:
            print(f"✗ Failed to connect to MCP server: {e}")
            raise
    
    async def call_tool(self, tool_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Call a tool on the MCP server.
        
        Args:
            tool_name: Name of the tool to call
            parameters: Parameters to pass to the tool
            
        Returns:
            Tool execution results
        """
        if parameters is None:
            parameters = {}
            
        if tool_name not in self.available_tools:
            raise ValueError(f"Tool '{tool_name}' not available. Available tools: {list(self.available_tools.keys())}")
        
        try:
            payload = {
                "tool_name": tool_name,
                "parameters": parameters
            }
            response = await self.client.post(f"{self.server_url}/call_tool", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"✗ Tool call failed: {e}")
            return {"error": str(e)}
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


class AnalyticsIntelligence:
    """
    AI-powered analytics intelligence engine.
    
    This class contains the logic for analyzing Google Analytics data
    and generating insights and recommendations.
    """
    
    def analyze_traffic_metrics(self, data: Dict[str, Any]) -> List[Insight]:
        """Analyze traffic metrics and generate insights."""
        insights = []
        
        sessions = data.get("sessions", 0)
        pageviews = data.get("pageviews", 0)
        users = data.get("users", 0)
        pages_per_session = data.get("pages_per_session", 0)
        
        # Traffic volume analysis
        if sessions < 500:
            insights.append(Insight(
                type=InsightType.ALERT,
                title="Low Traffic Volume",
                description=f"Website received only {sessions} sessions. This is below typical benchmarks.",
                severity="high",
                recommendations=[
                    "Implement SEO optimization to improve organic search visibility",
                    "Consider paid advertising campaigns to drive more traffic",
                    "Analyze and improve content marketing strategy",
                    "Check for technical issues that might be affecting site accessibility"
                ],
                data_source="traffic_metrics",
                confidence=0.8
            ))
        elif sessions > 1000:
            insights.append(Insight(
                type=InsightType.PERFORMANCE,
                title="Strong Traffic Performance",
                description=f"Website achieved {sessions} sessions, indicating good traffic performance.",
                severity="low",
                recommendations=[
                    "Maintain current marketing strategies",
                    "Consider scaling successful campaigns",
                    "Focus on conversion optimization to maximize the high traffic"
                ],
                data_source="traffic_metrics",
                confidence=0.9
            ))
        
        # Pages per session analysis
        if pages_per_session < 2.0:
            insights.append(Insight(
                type=InsightType.OPTIMIZATION,
                title="Low Page Engagement",
                description=f"Average of {pages_per_session} pages per session suggests users aren't exploring the site deeply.",
                severity="medium",
                recommendations=[
                    "Improve internal linking between related content",
                    "Add 'related articles' or 'you might also like' sections",
                    "Review and optimize page loading speeds",
                    "Enhance navigation menu and site structure"
                ],
                data_source="traffic_metrics",
                confidence=0.7
            ))
        
        return insights
    
    def analyze_engagement_metrics(self, data: Dict[str, Any]) -> List[Insight]:
        """Analyze engagement metrics and generate insights."""
        insights = []
        
        bounce_rate = data.get("bounce_rate", 0)
        avg_duration = data.get("average_session_duration", 0)
        
        # Bounce rate analysis
        if bounce_rate > 70:
            insights.append(Insight(
                type=InsightType.ALERT,
                title="High Bounce Rate",
                description=f"Bounce rate of {bounce_rate}% is concerning and indicates users are leaving quickly.",
                severity="high",
                recommendations=[
                    "Improve page loading speed (target <3 seconds)",
                    "Ensure content matches user expectations from search results",
                    "Enhance page design and user experience",
                    "Add clear calls-to-action to guide user behavior",
                    "Review mobile responsiveness and mobile user experience"
                ],
                data_source="engagement_metrics",
                confidence=0.9
            ))
        elif bounce_rate < 40:
            insights.append(Insight(
                type=InsightType.PERFORMANCE,
                title="Good User Engagement",
                description=f"Bounce rate of {bounce_rate}% indicates good user engagement.",
                severity="low",
                recommendations=[
                    "Continue current content and UX strategies",
                    "Identify top-performing pages and replicate their success factors"
                ],
                data_source="engagement_metrics",
                confidence=0.8
            ))
        
        # Session duration analysis
        if avg_duration < 60:
            insights.append(Insight(
                type=InsightType.OPTIMIZATION,
                title="Short Session Duration",
                description=f"Average session duration of {avg_duration} seconds suggests limited engagement.",
                severity="medium",
                recommendations=[
                    "Add more engaging, interactive content",
                    "Improve content readability and structure",
                    "Include videos, images, and other media to increase engagement",
                    "Create compelling content that encourages further exploration"
                ],
                data_source="engagement_metrics",
                confidence=0.7
            ))
        
        return insights
    
    def analyze_traffic_sources(self, data: Dict[str, Any]) -> List[Insight]:
        """Analyze traffic sources and generate insights."""
        insights = []
        
        channels = data.get("channels", {})
        organic_search = channels.get("organic_search", 0)
        direct = channels.get("direct", 0)
        social = channels.get("social", 0)
        
        # Organic search dependency
        if organic_search > 70:
            insights.append(Insight(
                type=InsightType.ALERT,
                title="High Dependency on Organic Search",
                description=f"{organic_search}% of traffic comes from organic search. This creates vulnerability to search algorithm changes.",
                severity="medium",
                recommendations=[
                    "Diversify traffic sources through social media marketing",
                    "Invest in email marketing campaigns",
                    "Consider paid advertising to reduce organic dependency",
                    "Build direct traffic through brand awareness campaigns"
                ],
                data_source="traffic_sources",
                confidence=0.8
            ))
        
        # Low direct traffic
        if direct < 20:
            insights.append(Insight(
                type=InsightType.OPTIMIZATION,
                title="Low Brand Recognition",
                description=f"Only {direct}% direct traffic suggests limited brand awareness.",
                severity="medium",
                recommendations=[
                    "Invest in brand awareness campaigns",
                    "Improve brand recall through consistent messaging",
                    "Encourage repeat visits through email newsletters",
                    "Build a community around your brand"
                ],
                data_source="traffic_sources",
                confidence=0.7
            ))
        
        # Social media opportunity
        if social < 10:
            insights.append(Insight(
                type=InsightType.RECOMMENDATION,
                title="Social Media Growth Opportunity",
                description=f"Social traffic is only {social}%, indicating untapped potential.",
                severity="low",
                recommendations=[
                    "Develop a comprehensive social media strategy",
                    "Create shareable content optimized for each platform",
                    "Engage actively with your audience on social platforms",
                    "Consider social media advertising to expand reach"
                ],
                data_source="traffic_sources",
                confidence=0.6
            ))
        
        return insights
    
    def generate_summary_report(self, all_insights: List[Insight]) -> str:
        """Generate a comprehensive summary report from all insights."""
        if not all_insights:
            return "No significant insights found in the current data."
        
        # Categorize insights by severity
        critical = [i for i in all_insights if i.severity == "critical"]
        high = [i for i in all_insights if i.severity == "high"]
        medium = [i for i in all_insights if i.severity == "medium"]
        low = [i for i in all_insights if i.severity == "low"]
        
        report = ["🔍 GOOGLE ANALYTICS INSIGHTS REPORT", "=" * 50, ""]
        
        if critical:
            report.extend(["🚨 CRITICAL ISSUES:", ""])
            for insight in critical:
                report.append(f"• {insight.title}")
                report.append(f"  {insight.description}")
                report.append("")
        
        if high:
            report.extend(["⚠️  HIGH PRIORITY ITEMS:", ""])
            for insight in high:
                report.append(f"• {insight.title}")
                report.append(f"  {insight.description}")
                report.append("")
        
        if medium:
            report.extend(["📊 OPTIMIZATION OPPORTUNITIES:", ""])
            for insight in medium:
                report.append(f"• {insight.title}")
                report.append(f"  {insight.description}")
                report.append("")
        
        if low:
            report.extend(["✅ POSITIVE INDICATORS:", ""])
            for insight in low:
                report.append(f"• {insight.title}")
                report.append(f"  {insight.description}")
                report.append("")
        
        # Top recommendations
        all_recommendations = []
        for insight in high + medium:  # Focus on actionable items
            all_recommendations.extend(insight.recommendations)
        
        if all_recommendations:
            report.extend(["🎯 TOP RECOMMENDATIONS:", ""])
            for i, rec in enumerate(all_recommendations[:5], 1):  # Top 5 recommendations
                report.append(f"{i}. {rec}")
            report.append("")
        
        report.extend([
            "📈 Next Steps:",
            "1. Address critical and high priority issues first",
            "2. Implement quick wins from medium priority optimizations",
            "3. Monitor the impact of changes over 2-4 weeks",
            "4. Run this analysis regularly to track improvements"
        ])
        
        return "\n".join(report)


class AnalyticsAgent:
    """
    Main AI Agent for Google Analytics analysis.
    
    This agent orchestrates the entire analytics workflow:
    1. Connects to the MCP server
    2. Retrieves various types of analytics data
    3. Analyzes the data using AI intelligence
    4. Generates insights and recommendations
    5. Provides natural language responses to user queries
    """
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        self.mcp_client = MCPClient(server_url)
        self.intelligence = AnalyticsIntelligence()
        self.last_analysis_data = {}
    
    async def initialize(self):
        """Initialize the agent by connecting to the MCP server."""
        await self.mcp_client.initialize()
        print("🤖 Analytics Agent initialized and ready!")
    
    async def run_comprehensive_analysis(self, start_date: str = None, end_date: str = None) -> str:
        """
        Run a comprehensive analysis of the website's analytics data.
        
        Args:
            start_date: Analysis start date (YYYY-MM-DD format)
            end_date: Analysis end date (YYYY-MM-DD format)
            
        Returns:
            Comprehensive analysis report as a string
        """
        # Set default date range if not provided
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        print(f"🔍 Running comprehensive analysis for {start_date} to {end_date}...")
        
        all_insights = []
        
        try:
            # Fetch traffic metrics
            print("  📊 Analyzing traffic metrics...")
            traffic_data = await self.mcp_client.call_tool("get_traffic_metrics", {
                "start_date": start_date,
                "end_date": end_date
            })
            if "error" not in traffic_data:
                traffic_insights = self.intelligence.analyze_traffic_metrics(traffic_data)
                all_insights.extend(traffic_insights)
                self.last_analysis_data["traffic"] = traffic_data
            
            # Fetch engagement metrics
            print("  💪 Analyzing engagement metrics...")
            engagement_data = await self.mcp_client.call_tool("get_engagement_metrics", {
                "start_date": start_date,
                "end_date": end_date
            })
            if "error" not in engagement_data:
                engagement_insights = self.intelligence.analyze_engagement_metrics(engagement_data)
                all_insights.extend(engagement_insights)
                self.last_analysis_data["engagement"] = engagement_data
            
            # Fetch traffic sources
            print("  🚦 Analyzing traffic sources...")
            sources_data = await self.mcp_client.call_tool("get_traffic_sources")
            if "error" not in sources_data:
                sources_insights = self.intelligence.analyze_traffic_sources(sources_data)
                all_insights.extend(sources_insights)
                self.last_analysis_data["sources"] = sources_data
            
            # Generate summary report
            report = self.intelligence.generate_summary_report(all_insights)
            print("✅ Analysis complete!")
            return report
            
        except Exception as e:
            error_msg = f"❌ Analysis failed: {str(e)}"
            print(error_msg)
            return error_msg
    
    async def answer_question(self, question: str) -> str:
        """
        Answer natural language questions about the analytics data.
        
        Args:
            question: User's question about the analytics data
            
        Returns:
            Natural language answer based on the available data
        """
        question_lower = question.lower()
        
        try:
            # Traffic-related questions
            if any(word in question_lower for word in ["traffic", "visitors", "sessions", "users"]):
                data = await self.mcp_client.call_tool("get_traffic_metrics")
                if "error" not in data:
                    sessions = data.get("sessions", 0)
                    users = data.get("users", 0)
                    pageviews = data.get("pageviews", 0)
                    return f"Your website had {sessions:,} sessions from {users:,} users, generating {pageviews:,} page views. Each user viewed an average of {data.get('pages_per_session', 0):.1f} pages per session."
            
            # Engagement questions
            elif any(word in question_lower for word in ["engagement", "bounce", "duration", "time"]):
                data = await self.mcp_client.call_tool("get_engagement_metrics")
                if "error" not in data:
                    bounce_rate = data.get("bounce_rate", 0)
                    duration = data.get("average_session_duration", 0)
                    return f"Your website has a {bounce_rate}% bounce rate and users spend an average of {duration//60}:{duration%60:02d} minutes on the site. {'This indicates good engagement.' if bounce_rate < 50 else 'Consider improving page content and loading speed to reduce bounce rate.'}"
            
            # Traffic sources questions
            elif any(word in question_lower for word in ["source", "referral", "social", "search"]):
                data = await self.mcp_client.call_tool("get_traffic_sources")
                if "error" not in data:
                    channels = data.get("channels", {})
                    top_channel = max(channels.items(), key=lambda x: x[1])
                    return f"Your top traffic source is {top_channel[0].replace('_', ' ')} at {top_channel[1]}%. Other significant sources include: " + ", ".join([f"{k.replace('_', ' ')}: {v}%" for k, v in sorted(channels.items(), key=lambda x: x[1], reverse=True)[1:4]])
            
            # Top pages questions
            elif any(word in question_lower for word in ["pages", "content", "popular"]):
                data = await self.mcp_client.call_tool("get_top_pages")
                if "error" not in data:
                    top_pages = data.get("top_pages", [])[:3]
                    return f"Your top performing pages are: " + ", ".join([f"{page['page']} ({page['pageviews']} views)" for page in top_pages])
            
            # Demographics questions
            elif any(word in question_lower for word in ["demographics", "location", "country", "device", "mobile"]):
                data = await self.mcp_client.call_tool("get_demographic_data")
                if "error" not in data:
                    countries = data.get("countries", [])[:3]
                    devices = data.get("devices", {})
                    return f"Your top locations are: {', '.join([f'{c[\"country\"]} ({c[\"percentage\"]}%)' for c in countries])}. Device breakdown: Desktop {devices.get('desktop', 0)}%, Mobile {devices.get('mobile', 0)}%, Tablet {devices.get('tablet', 0)}%."
            
            else:
                return "I can help you analyze traffic metrics, engagement data, traffic sources, top pages, and demographics. Try asking: 'How is my website traffic?' or 'What's my bounce rate?' or 'Where do my visitors come from?'"
        
        except Exception as e:
            return f"I encountered an error while retrieving data: {str(e)}. Please make sure the MCP server is running."
    
    async def close(self):
        """Clean up resources."""
        await self.mcp_client.close()


# Command-line interface
async def main():
    """Main function for running the analytics agent."""
    import sys
    
    agent = AnalyticsAgent()
    
    try:
        await agent.initialize()
        
        if len(sys.argv) > 1 and sys.argv[1] == "analyze":
            # Run comprehensive analysis
            report = await agent.run_comprehensive_analysis()
            print("\n" + report)
        
        elif len(sys.argv) > 1 and sys.argv[1] == "interactive":
            # Interactive mode
            print("\n🤖 Analytics Agent - Interactive Mode")
            print("Ask me questions about your website analytics!")
            print("Type 'analyze' for a full report, or 'quit' to exit.\n")
            
            while True:
                try:
                    question = input("❓ Your question: ").strip()
                    if question.lower() in ['quit', 'exit', 'q']:
                        break
                    elif question.lower() == 'analyze':
                        report = await agent.run_comprehensive_analysis()
                        print("\n" + report + "\n")
                    elif question:
                        answer = await agent.answer_question(question)
                        print(f"🤖 {answer}\n")
                except KeyboardInterrupt:
                    break
            
            print("👋 Goodbye!")
        
        else:
            # Default: run analysis
            report = await agent.run_comprehensive_analysis()
            print("\n" + report)
    
    finally:
        await agent.close()


if __name__ == "__main__":
    asyncio.run(main())

"""
Website Analyzer AI Agent

This agent interacts with the local MCP server to fetch website analytics data
and provides actionable insights and recommendations for website improvement.

Author: Agent #2
"""

import requests
import json
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WebsiteAnalyzerAgent:
    """
    AI Agent for Website Analysis and Recommendations
    
    This agent connects to the MCP server to fetch website analytics data
    and provides comprehensive analysis with actionable recommendations.
    """
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        """
        Initialize the Website Analyzer Agent
        
        Args:
            server_url (str): URL of the MCP server
        """
        self.server_url = server_url
        
        # Tool mapping: Natural language requests to MCP server endpoints
        self.tools_map = {
            "website traffic": "/analytics",
            "traffic data": "/analytics",
            "analytics": "/analytics",
            "website analytics": "/analytics",
            "performance metrics": "/analytics",
            # Future endpoints can be added here
            # "top pages": "/tools/get_top_pages",
            # "user demographics": "/tools/get_demographics",
            # "traffic sources": "/tools/get_traffic_sources"
        }
        
        # System prompt defining the agent's role
        self.system_prompt = (
            "You are an expert website analyst. Your goal is to fetch website data "
            "using the MCP server and provide actionable insights and recommendations "
            "for improvement. You analyze traffic patterns, user behavior, and "
            "performance metrics to help optimize website performance and user experience."
        )
        
        # Recommendation thresholds
        self.thresholds = {
            "high_bounce_rate": 50.0,
            "low_session_duration": 180,  # seconds
            "low_pages_per_session": 2.0,
            "good_bounce_rate": 30.0,
            "good_session_duration": 300
        }
    
    def fetch_data(self, request_type: str) -> Optional[Dict[str, Any]]:
        """
        Fetch data from the MCP server based on request type
        
        Args:
            request_type (str): Natural language description of the data needed
            
        Returns:
            Optional[Dict]: JSON response from the server or None if failed
        """
        # Map natural language request to endpoint
        endpoint = self.tools_map.get(request_type.lower())
        if not endpoint:
            logger.error(f"No tool found for request type: {request_type}")
            print(f"❌ No tool found for request type: '{request_type}'")
            print(f"Available request types: {list(self.tools_map.keys())}")
            return None

        url = f"{self.server_url}{endpoint}"
        logger.info(f"Fetching data from: {url}")
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            logger.info("Data fetched successfully")
            return data
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to MCP server")
            print("❌ Failed to connect to MCP server. Please ensure the server is running on localhost:8000")
            return None
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            print("❌ Request timeout. The server might be overloaded.")
            return None
        except requests.RequestException as e:
            logger.error(f"HTTP request failed: {e}")
            print(f"❌ Failed to fetch data: {e}")
            return None
        except json.JSONDecodeError:
            logger.error("Invalid JSON response")
            print("❌ Received invalid JSON response from server")
            return None
    
    def analyze_traffic_metrics(self, data: Dict[str, Any]) -> List[str]:
        """
        Analyze traffic metrics and generate insights
        
        Args:
            data (Dict): Traffic data from the server
            
        Returns:
            List[str]: List of insights and observations
        """
        insights = []
        
        sessions = data.get('sessions', 0)
        bounce_rate = data.get('bounce_rate', 0)
        avg_duration = data.get('average_session_duration', 0)
        
        # Traffic volume insights
        if sessions > 1000:
            insights.append(f"✅ Good traffic volume with {sessions:,} sessions")
        elif sessions > 500:
            insights.append(f"⚠️ Moderate traffic volume with {sessions:,} sessions")
        else:
            insights.append(f"📈 Low traffic volume with {sessions:,} sessions - consider marketing efforts")
        
        # Bounce rate insights
        if bounce_rate <= self.thresholds['good_bounce_rate']:
            insights.append(f"✅ Excellent bounce rate at {bounce_rate}% - users are highly engaged")
        elif bounce_rate <= self.thresholds['high_bounce_rate']:
            insights.append(f"⚠️ Acceptable bounce rate at {bounce_rate}% - room for improvement")
        else:
            insights.append(f"❌ High bounce rate at {bounce_rate}% - immediate attention needed")
        
        # Session duration insights
        duration_minutes = avg_duration / 60
        if avg_duration >= self.thresholds['good_session_duration']:
            insights.append(f"✅ Excellent session duration of {duration_minutes:.1f} minutes")
        elif avg_duration >= self.thresholds['low_session_duration']:
            insights.append(f"⚠️ Moderate session duration of {duration_minutes:.1f} minutes")
        else:
            insights.append(f"❌ Short session duration of {duration_minutes:.1f} minutes - users leave quickly")
        
        return insights
    
    def generate_recommendations(self, data: Dict[str, Any]) -> List[str]:
        """
        Generate actionable recommendations based on the data
        
        Args:
            data (Dict): Analytics data from the server
            
        Returns:
            List[str]: List of actionable recommendations
        """
        recommendations = []
        
        sessions = data.get('sessions', 0)
        bounce_rate = data.get('bounce_rate', 0)
        avg_duration = data.get('average_session_duration', 0)
        
        # Traffic growth recommendations
        if sessions < 1000:
            recommendations.extend([
                "🚀 Implement SEO optimization to increase organic traffic",
                "📱 Consider social media marketing campaigns",
                "📧 Set up email marketing to drive repeat visits"
            ])
        
        # Bounce rate improvements
        if bounce_rate > self.thresholds['high_bounce_rate']:
            recommendations.extend([
                "🎨 Improve website design and user interface",
                "⚡ Optimize page loading speed (aim for <3 seconds)",
                "📝 Review and improve content quality and relevance",
                "📱 Ensure mobile-responsive design",
                "🔍 Improve internal linking structure"
            ])
        elif bounce_rate > self.thresholds['good_bounce_rate']:
            recommendations.extend([
                "✨ A/B test different landing page designs",
                "📊 Add compelling call-to-action buttons",
                "🎯 Improve content targeting for your audience"
            ])
        
        # Session duration improvements
        if avg_duration < self.thresholds['low_session_duration']:
            recommendations.extend([
                "📚 Create more engaging, in-depth content",
                "🎥 Add multimedia content (videos, images, infographics)",
                "🔗 Implement related content suggestions",
                "💬 Add interactive elements (polls, quizzes, comments)"
            ])
        elif avg_duration < self.thresholds['good_session_duration']:
            recommendations.extend([
                "📖 Optimize content structure with clear headings",
                "⏱️ Add estimated reading time to articles",
                "🎯 Create content series to encourage deeper engagement"
            ])
        
        # General optimization recommendations
        recommendations.extend([
            "📈 Set up conversion tracking to measure success",
            "🔍 Implement heat mapping tools to understand user behavior",
            "📊 Create regular analytics reports to track improvements"
        ])
        
        return recommendations
    
    def print_analysis_report(self, data: Dict[str, Any]) -> None:
        """
        Generate and print a comprehensive analysis report
        
        Args:
            data (Dict): Analytics data to analyze
        """
        if not data:
            print("❌ No data available for analysis.")
            return
        
        print("\n" + "="*80)
        print("🌐 WEBSITE ANALYTICS REPORT")
        print("="*80)
        
        # Basic metrics display
        print("\n📊 KEY METRICS:")
        print("-" * 40)
        sessions = data.get('sessions', 0)
        bounce_rate = data.get('bounce_rate', 0)
        avg_duration = data.get('average_session_duration', 0)
        
        print(f"Sessions: {sessions:,}")
        print(f"Bounce Rate: {bounce_rate}%")
        print(f"Average Session Duration: {avg_duration} seconds ({avg_duration/60:.1f} minutes)")
        
        # Analysis insights
        insights = self.analyze_traffic_metrics(data)
        print("\n🔍 ANALYSIS INSIGHTS:")
        print("-" * 40)
        for insight in insights:
            print(f"  {insight}")
        
        # Recommendations
        recommendations = self.generate_recommendations(data)
        print("\n💡 ACTIONABLE RECOMMENDATIONS:")
        print("-" * 40)
        for i, recommendation in enumerate(recommendations, 1):
            print(f"  {i}. {recommendation}")
        
        # Performance score
        score = self.calculate_performance_score(data)
        print(f"\n📈 OVERALL PERFORMANCE SCORE: {score}/100")
        print(self.get_score_interpretation(score))
        print("\n" + "="*80)
    
    def calculate_performance_score(self, data: Dict[str, Any]) -> int:
        """
        Calculate an overall performance score based on key metrics
        
        Args:
            data (Dict): Analytics data
            
        Returns:
            int: Performance score out of 100
        """
        score = 0
        
        bounce_rate = data.get('bounce_rate', 100)
        avg_duration = data.get('average_session_duration', 0)
        sessions = data.get('sessions', 0)
        
        # Bounce rate scoring (40 points max)
        if bounce_rate <= 30:
            score += 40
        elif bounce_rate <= 50:
            score += 30
        elif bounce_rate <= 70:
            score += 20
        else:
            score += 10
        
        # Session duration scoring (40 points max)
        if avg_duration >= 300:
            score += 40
        elif avg_duration >= 180:
            score += 30
        elif avg_duration >= 120:
            score += 20
        else:
            score += 10
        
        # Traffic volume scoring (20 points max)
        if sessions >= 1000:
            score += 20
        elif sessions >= 500:
            score += 15
        elif sessions >= 100:
            score += 10
        else:
            score += 5
        
        return min(score, 100)
    
    def get_score_interpretation(self, score: int) -> str:
        """
        Get interpretation of the performance score
        
        Args:
            score (int): Performance score
            
        Returns:
            str: Score interpretation
        """
        if score >= 80:
            return "🏆 Excellent! Your website is performing very well."
        elif score >= 60:
            return "👍 Good performance with room for optimization."
        elif score >= 40:
            return "⚠️ Average performance - focus on key improvements."
        else:
            return "🚨 Poor performance - immediate action required."
    
    def run_analysis(self, request_type: str = "website traffic") -> None:
        """
        Run a complete analysis for the given request type
        
        Args:
            request_type (str): Type of analysis to perform
        """
        print(f"🤖 {self.system_prompt}")
        print(f"\n🔄 Fetching {request_type} data from MCP server...")
        
        data = self.fetch_data(request_type)
        if data:
            self.print_analysis_report(data)
        else:
            print("\n❌ Analysis failed due to data fetch error.")
    
    def run_demo(self) -> None:
        """
        Run a demonstration of the agent with predefined requests
        """
        print("\n🚀 Starting Website Analysis Demo")
        print("=" * 50)
        
        # Demo request: website traffic and analysis
        demo_request = "website traffic and top pages analysis"
        print(f"\n📋 Demo Request: '{demo_request}'")
        
        self.run_analysis("website traffic")
        
        print("\n✅ Demo completed successfully!")
        print("\n💡 To use this agent:")
        print("   1. Ensure the MCP server is running on localhost:8000")
        print("   2. Create an instance: agent = WebsiteAnalyzerAgent()")
        print("   3. Run analysis: agent.run_analysis('website traffic')")


def main():
    """
    Main function to demonstrate the agent functionality
    """
    server_url = "http://localhost:8000"
    agent = WebsiteAnalyzerAgent(server_url)
    
    # Run the demonstration
    agent.run_demo()


if __name__ == "__main__":
    main()

import requests
import json
from datetime import datetime


class WebsiteAnalyzerAgent:
    """
    Advanced Website Analytics Agent
    
    This agent interacts with a local MCP server to fetch website analytics data
    and provides comprehensive analysis with actionable recommendations.
    """
    
    def __init__(self, server_url="http://localhost:8000"):
        """
        Initialize the Website Analyzer Agent
        
        Args:
            server_url (str): URL of the local MCP server
        """
        self.server_url = server_url
        
        # Tool mapping: Natural language requests to MCP server endpoints
        self.tools_map = {
            "website traffic": "/analytics",
            "traffic analysis": "/analytics",
            "website performance": "/analytics",
            "user engagement": "/analytics",
            "site analytics": "/analytics",
            "traffic metrics": "/analytics",
            "website data": "/analytics",
            "performance metrics": "/analytics",
            # Future endpoints can be added here
            # "top pages": "/tools/get_top_pages",
            # "traffic sources": "/tools/get_traffic_sources",
            # "user demographics": "/tools/get_demographics"
        }
        
        # System prompt defining the agent's role
        self.system_prompt = (
            "You are an expert website analyst. Your goal is to fetch website data "
            "using the MCP server and provide actionable insights and recommendations "
            "for improvement. You analyze traffic patterns, user behavior, and "
            "performance metrics to help optimize website performance."
        )
        
        print(f"✓ Website Analyzer Agent initialized")
        print(f"✓ Connected to MCP server: {self.server_url}")
        print(f"✓ Available request types: {list(self.tools_map.keys())}")
    
    def fetch_data(self, request_type):
        """
        Fetch data from the MCP server based on request type
        
        Args:
            request_type (str): Natural language description of data needed
            
        Returns:
            dict: JSON response from the MCP server, or None if failed
        """
        # Map natural language request to endpoint
        endpoint = self.tools_map.get(request_type.lower())
        
        if not endpoint:
            print(f"❌ No tool found for request type: '{request_type}'")
            print(f"Available request types: {list(self.tools_map.keys())}")
            return None
        
        # Construct full URL
        url = f"{self.server_url}{endpoint}"
        
        try:
            print(f"🔍 Fetching data from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            print(f"✓ Successfully retrieved data ({len(str(data))} characters)")
            return data
            
        except requests.exceptions.ConnectionError:
            print(f"❌ Failed to connect to MCP server at {url}")
            print("Please ensure the MCP server is running on localhost:8000")
            return None
        except requests.exceptions.Timeout:
            print(f"❌ Request timed out when connecting to {url}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP error occurred: {e}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return None
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response from server")
            return None
    
    def analyze_basic_metrics(self, data):
        """
        Analyze basic website metrics from the MCP server response
        
        Args:
            data (dict): Analytics data from the MCP server
        """
        if not data:
            print("❌ No data available for analysis.")
            return
        
        print("\n" + "="*60)
        print("📊 BASIC WEBSITE METRICS ANALYSIS")
        print("="*60)
        
        # Extract basic metrics (compatible with current MCP server)
        sessions = data.get('sessions', 0)
        bounce_rate = data.get('bounce_rate', 0)
        avg_duration = data.get('average_session_duration', 0)
        
        print(f"🔢 Total Sessions: {sessions:,}")
        print(f"⚡ Bounce Rate: {bounce_rate}%")
        print(f"⏱️  Average Session Duration: {avg_duration} seconds ({avg_duration/60:.1f} minutes)")
        
        # Calculate additional insights if data is available
        if sessions > 0:
            engaged_sessions = sessions * (1 - bounce_rate/100)
            print(f"👥 Engaged Sessions: {engaged_sessions:,.0f} ({(engaged_sessions/sessions*100):.1f}%)")
    
    def generate_recommendations(self, data):
        """
        Generate specific, actionable recommendations based on the data
        
        Args:
            data (dict): Analytics data from the MCP server
        """
        if not data:
            return
        
        print("\n" + "="*60)
        print("💡 ACTIONABLE RECOMMENDATIONS")
        print("="*60)
        
        recommendations = []
        
        # Extract metrics
        sessions = data.get('sessions', 0)
        bounce_rate = data.get('bounce_rate', 0)
        avg_duration = data.get('average_session_duration', 0)
        
        # Bounce Rate Analysis
        if bounce_rate > 70:
            recommendations.append({
                "priority": "HIGH",
                "category": "User Experience",
                "issue": f"Very high bounce rate ({bounce_rate}%)",
                "recommendation": "Immediately review page loading speed, content relevance, and navigation design. Consider A/B testing different landing page layouts."
            })
        elif bounce_rate > 50:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Content Optimization",
                "issue": f"Above-average bounce rate ({bounce_rate}%)",
                "recommendation": "Improve content quality, add internal linking, and ensure page content matches user intent. Industry average is 40-50%."
            })
        elif bounce_rate < 30:
            recommendations.append({
                "priority": "INFO",
                "category": "Performance",
                "issue": f"Excellent bounce rate ({bounce_rate}%)",
                "recommendation": "Great job! Your content is highly engaging. Consider scaling successful content strategies."
            })
        
        # Session Duration Analysis
        if avg_duration < 60:
            recommendations.append({
                "priority": "HIGH",
                "category": "Content Engagement",
                "issue": f"Very low session duration ({avg_duration}s)",
                "recommendation": "Add engaging multimedia content, improve readability, and create clear call-to-actions to keep users engaged longer."
            })
        elif avg_duration < 120:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Content Strategy",
                "issue": f"Below-average session duration ({avg_duration}s)",
                "recommendation": "Consider adding related content suggestions, improving page layout, and optimizing content structure for better readability."
            })
        elif avg_duration > 300:
            recommendations.append({
                "priority": "INFO",
                "category": "User Engagement",
                "issue": f"Excellent session duration ({avg_duration}s)",
                "recommendation": "Users are highly engaged! Consider adding conversion opportunities and newsletter signups to capture this engaged audience."
            })
        
        # Traffic Volume Analysis
        if sessions < 100:
            recommendations.append({
                "priority": "HIGH",
                "category": "Traffic Generation",
                "issue": f"Low traffic volume ({sessions} sessions)",
                "recommendation": "Invest in SEO optimization, content marketing, and social media presence to increase organic traffic."
            })
        elif sessions > 10000:
            recommendations.append({
                "priority": "INFO",
                "category": "Growth Opportunity",
                "issue": f"High traffic volume ({sessions:,} sessions)",
                "recommendation": "With this traffic level, focus on conversion optimization and user experience improvements for maximum ROI."
            })
        
        # Display recommendations
        if not recommendations:
            print("✅ Your website metrics look good! Keep monitoring for trends.")
        else:
            for i, rec in enumerate(recommendations, 1):
                priority_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "INFO": "🟢"}
                print(f"\n{i}. {priority_emoji.get(rec['priority'], '📌')} {rec['priority']} PRIORITY")
                print(f"   Category: {rec['category']}")
                print(f"   Issue: {rec['issue']}")
                print(f"   Action: {rec['recommendation']}")
    
    def comprehensive_analysis(self, request_type="website traffic"):
        """
        Perform comprehensive website analysis including data fetching,
        metric analysis, and recommendation generation
        
        Args:
            request_type (str): Type of analysis to perform
        """
        print(f"\n🚀 Starting comprehensive website analysis...")
        print(f"📅 Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Request Type: {request_type}")
        
        # Fetch data from MCP server
        data = self.fetch_data(request_type)
        
        if data:
            # Perform analysis
            self.analyze_basic_metrics(data)
            self.generate_recommendations(data)
            
            print("\n" + "="*60)
            print("✅ ANALYSIS COMPLETE")
            print("="*60)
            print("💬 For more detailed analysis, ensure your MCP server provides")
            print("   additional endpoints for top pages, traffic sources, and demographics.")
        else:
            print("❌ Analysis failed due to data retrieval issues.")
    
    def run_demo(self):
        """
        Run a demonstration of the website analyzer agent
        """
        print("\n" + "="*80)
        print("🤖 WEBSITE ANALYZER AI AGENT - DEMONSTRATION")
        print("="*80)
        print(f"Role: {self.system_prompt}")
        print("\n🔄 Running predefined analysis: 'Website Traffic and Performance'")
        
        # Run comprehensive analysis
        self.comprehensive_analysis("website traffic")
        
        print("\n🎉 Demo completed! The agent successfully:")
        print("   ✅ Connected to the MCP server")
        print("   ✅ Fetched website analytics data")
        print("   ✅ Analyzed traffic metrics")
        print("   ✅ Generated actionable recommendations")

if __name__ == "__main__":
    server_url = "http://localhost:8000"
    agent = WebsiteAnalyzerAgent(server_url)
    agent.run_demo()


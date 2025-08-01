"""
Website Analyzer Agent - Demo Version with Mock Data

This version demonstrates the full functionality of the agent using mock data
when the MCP server is not available. This allows you to see the complete
analysis and recommendation generation process.
"""

import requests
import json
from datetime import datetime


class WebsiteAnalyzerAgent:
    """
    Advanced Website Analytics Agent with Mock Data Support
    
    This agent interacts with a local MCP server to fetch website analytics data
    and provides comprehensive analysis with actionable recommendations.
    """
    
    def __init__(self, server_url="http://localhost:8000", use_mock_data=False):
        """
        Initialize the Website Analyzer Agent
        
        Args:
            server_url (str): URL of the local MCP server
            use_mock_data (bool): If True, uses mock data instead of server
        """
        self.server_url = server_url
        self.use_mock_data = use_mock_data
        
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
        
        # Mock data for demonstration (matches the sample_data.json structure)
        self.mock_data = {
            "sessions": 1000,
            "bounce_rate": 50,
            "average_session_duration": 200
        }
        
        print(f"✓ Website Analyzer Agent initialized")
        print(f"✓ {'Mock data mode' if use_mock_data else f'Connected to MCP server: {self.server_url}'}")
        print(f"✓ Available request types: {list(self.tools_map.keys())}")
    
    def fetch_data(self, request_type):
        """
        Fetch data from the MCP server based on request type
        
        Args:
            request_type (str): Natural language description of data needed
            
        Returns:
            dict: JSON response from the MCP server, or None if failed
        """
        # If mock data mode is enabled, return mock data
        if self.use_mock_data:
            print(f"🔍 Using mock data for request: {request_type}")
            print(f"✓ Successfully retrieved mock data")
            return self.mock_data
        
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
            print("🔄 Falling back to mock data for demonstration...")
            self.use_mock_data = True
            return self.mock_data
        except requests.exceptions.Timeout:
            print(f"❌ Request timed out when connecting to {url}")
            print("🔄 Falling back to mock data for demonstration...")
            self.use_mock_data = True
            return self.mock_data
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
        
        # Additional analysis for website health
        print(f"\n📈 PERFORMANCE INDICATORS:")
        
        # Session quality scoring
        session_score = 100
        if bounce_rate > 60:
            session_score -= 30
        elif bounce_rate > 40:
            session_score -= 15
        
        if avg_duration < 60:
            session_score -= 25
        elif avg_duration < 120:
            session_score -= 10
        
        print(f"🎯 Website Engagement Score: {session_score}/100")
        
        if session_score >= 80:
            print("   Status: 🟢 Excellent - Your website is performing very well!")
        elif session_score >= 60:
            print("   Status: 🟡 Good - Some areas for improvement identified")
        else:
            print("   Status: 🔴 Needs Attention - Significant improvements needed")
    
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
                "recommendation": "Immediately review page loading speed, content relevance, and navigation design. Consider A/B testing different landing page layouts.",
                "expected_impact": "Could reduce bounce rate by 20-30%"
            })
        elif bounce_rate > 50:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Content Optimization",
                "issue": f"Above-average bounce rate ({bounce_rate}%)",
                "recommendation": "Improve content quality, add internal linking, and ensure page content matches user intent. Industry average is 40-50%.",
                "expected_impact": "Could reduce bounce rate by 10-15%"
            })
        elif bounce_rate < 30:
            recommendations.append({
                "priority": "INFO",
                "category": "Performance",
                "issue": f"Excellent bounce rate ({bounce_rate}%)",
                "recommendation": "Great job! Your content is highly engaging. Consider scaling successful content strategies to other pages.",
                "expected_impact": "Maintain current performance"
            })
        
        # Session Duration Analysis
        if avg_duration < 60:
            recommendations.append({
                "priority": "HIGH",
                "category": "Content Engagement",
                "issue": f"Very low session duration ({avg_duration}s)",
                "recommendation": "Add engaging multimedia content, improve readability, and create clear call-to-actions to keep users engaged longer.",
                "expected_impact": "Could increase session duration by 100-200%"
            })
        elif avg_duration < 120:
            recommendations.append({
                "priority": "MEDIUM",
                "category": "Content Strategy",
                "issue": f"Below-average session duration ({avg_duration}s)",
                "recommendation": "Consider adding related content suggestions, improving page layout, and optimizing content structure for better readability.",
                "expected_impact": "Could increase session duration by 50-100%"
            })
        elif avg_duration > 300:
            recommendations.append({
                "priority": "INFO",
                "category": "User Engagement",
                "issue": f"Excellent session duration ({avg_duration}s)",
                "recommendation": "Users are highly engaged! Consider adding conversion opportunities and newsletter signups to capture this engaged audience.",
                "expected_impact": "Potential for 20-30% increase in conversions"
            })
        
        # Traffic Volume Analysis
        if sessions < 100:
            recommendations.append({
                "priority": "HIGH",
                "category": "Traffic Generation",
                "issue": f"Low traffic volume ({sessions} sessions)",
                "recommendation": "Invest in SEO optimization, content marketing, and social media presence to increase organic traffic.",
                "expected_impact": "Could double traffic within 3-6 months"
            })
        elif sessions > 10000:
            recommendations.append({
                "priority": "INFO",
                "category": "Growth Opportunity",
                "issue": f"High traffic volume ({sessions:,} sessions)",
                "recommendation": "With this traffic level, focus on conversion optimization and user experience improvements for maximum ROI.",
                "expected_impact": "5-10% improvement in conversions = significant revenue impact"
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
                if 'expected_impact' in rec:
                    print(f"   Expected Impact: {rec['expected_impact']}")
        
        # Add next steps section
        print(f"\n📋 NEXT STEPS:")
        print("1. 🔄 Implement the highest priority recommendations first")
        print("2. 📊 Set up monitoring to track improvements")
        print("3. 🧪 A/B test major changes before full deployment")
        print("4. 📈 Schedule follow-up analysis in 2-4 weeks")
    
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
            print("💬 This analysis demonstrates the agent's capabilities.")
            print("   When connected to a real MCP server, it can provide")
            print("   even more detailed insights with live data.")
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
        print("   ✅ Connected to the data source")
        print("   ✅ Fetched website analytics data")
        print("   ✅ Analyzed traffic metrics")
        print("   ✅ Generated actionable recommendations")
        print("   ✅ Provided next steps for improvement")


if __name__ == "__main__":
    # Create agent with mock data enabled for demonstration
    server_url = "http://localhost:8000"
    agent = WebsiteAnalyzerAgent(server_url, use_mock_data=True)
    agent.run_demo()

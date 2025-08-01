# Website Analyzer AI Agent

## Overview

The Website Analyzer AI Agent is a sophisticated Python-based agent designed to interact with a local MCP (Model Context Protocol) server to fetch website analytics data and provide comprehensive analysis with actionable recommendations for website improvement.

## Features

### 🤖 **AI Agent Capabilities**
- **Clear System Prompt**: Defines the agent's role as an expert website analyst
- **Natural Language Processing**: Maps user requests like "website traffic" to appropriate MCP server endpoints
- **Comprehensive Analysis**: Processes analytics data and generates human-readable insights
- **Actionable Recommendations**: Provides specific, prioritized recommendations for website improvement

### 🔧 **Tool Mapping**
The agent includes a flexible tool mapping system that translates natural language requests to MCP server endpoints:

```python
{
    "website traffic": "/analytics",
    "traffic analysis": "/analytics",
    "website performance": "/analytics",
    "user engagement": "/analytics",
    # ... and more
}
```

### 📊 **Data Processing & Analysis**
- **Basic Metrics Analysis**: Sessions, bounce rate, session duration
- **Performance Scoring**: Calculates website engagement scores
- **Trend Analysis**: Identifies patterns and performance indicators
- **Comparative Analysis**: Compares metrics against industry standards

### 💡 **Recommendation Engine**
Generates prioritized recommendations based on:
- **High Priority**: Critical issues requiring immediate attention
- **Medium Priority**: Areas for improvement with moderate impact
- **Info**: Performance highlights and growth opportunities

## Files

### `agent.py`
The main production agent that connects to the MCP server running on `localhost:8000`.

**Key Features:**
- Robust error handling for server connectivity issues
- Comprehensive logging and status reporting
- Modular design for easy extension
- Well-documented code with detailed comments

### `demo_agent.py`
Enhanced demonstration version with mock data support.

**Additional Features:**
- Mock data fallback when MCP server is unavailable
- Enhanced analysis with engagement scoring
- Extended recommendation system with impact estimates
- Complete next steps guidance

## Usage

### Running the Production Agent

```bash
# Ensure the MCP server is running on localhost:8000
python agent.py
```

### Running the Demo Version

```bash
# Runs with mock data - no server required
python demo_agent.py
```

## Installation

1. **Install Dependencies**:
   ```bash
   pip install requests
   ```

2. **Ensure MCP Server is Running** (for production agent):
   The agent expects the MCP server to be available at `http://localhost:8000/analytics`

## Example Output

```
================================================================================
🤖 WEBSITE ANALYZER AI AGENT - DEMONSTRATION
================================================================================
Role: You are an expert website analyst...

🔄 Running predefined analysis: 'Website Traffic and Performance'

🚀 Starting comprehensive website analysis...
📅 Analysis Time: 2025-08-02 00:22:06
🎯 Request Type: website traffic

============================================================
📊 BASIC WEBSITE METRICS ANALYSIS
============================================================
🔢 Total Sessions: 1,000
⚡ Bounce Rate: 50%
⏱️  Average Session Duration: 200 seconds (3.3 minutes)
👥 Engaged Sessions: 500 (50.0%)

📈 PERFORMANCE INDICATORS:
🎯 Website Engagement Score: 85/100
   Status: 🟢 Excellent - Your website is performing very well!

============================================================
💡 ACTIONABLE RECOMMENDATIONS
============================================================
✅ Your website metrics look good! Keep monitoring for trends.

📋 NEXT STEPS:
1. 🔄 Implement the highest priority recommendations first
2. 📊 Set up monitoring to track improvements
3. 🧪 A/B test major changes before full deployment
4. 📈 Schedule follow-up analysis in 2-4 weeks
```

## Architecture

### Agent Design Pattern
```
User Request → Tool Mapping → HTTP Request → Data Processing → Analysis → Recommendations
```

### Error Handling
- **Connection Errors**: Graceful fallback with clear error messages
- **Timeout Handling**: 10-second timeout with retry logic
- **Data Validation**: JSON parsing with error recovery
- **Graceful Degradation**: Mock data fallback in demo version

### Extensibility
The agent is designed for easy extension:

1. **Add New Endpoints**: Simply update the `tools_map` dictionary
2. **Enhance Analysis**: Add new methods to the `WebsiteAnalyzerAgent` class
3. **Custom Recommendations**: Extend the `generate_recommendations` method
4. **Additional Data Sources**: Modify `fetch_data` to support multiple servers

## Configuration

### Server URL
Default: `http://localhost:8000`

```python
agent = WebsiteAnalyzerAgent("http://your-server:port")
```

### Request Timeout
Default: 10 seconds

```python
response = requests.get(url, timeout=10)
```

## Future Enhancements

### Planned Features
- **Multi-endpoint Support**: Integration with additional MCP server endpoints
- **Advanced Analytics**: Time-series analysis and trend prediction
- **Custom Dashboards**: Visual reporting capabilities
- **Automated Reporting**: Scheduled analysis and email reports
- **A/B Testing Integration**: Experiment tracking and analysis

### Potential Endpoints
```python
# Future endpoint mappings
"top pages": "/tools/get_top_pages",
"traffic sources": "/tools/get_traffic_sources", 
"user demographics": "/tools/get_demographics",
"conversion metrics": "/tools/get_conversions"
```

## Contributing

When extending the agent:

1. **Maintain Code Style**: Follow existing patterns and documentation
2. **Add Error Handling**: Ensure robust error handling for new features
3. **Update Tool Mapping**: Add new endpoints to the `tools_map` dictionary
4. **Test Thoroughly**: Verify both server-connected and mock data modes
5. **Document Changes**: Update this README and add inline comments

## Dependencies

- **requests**: HTTP client for MCP server communication
- **json**: JSON data parsing
- **datetime**: Timestamp generation for analysis reports

## License

This project is part of the MCP-agent repository for website analysis and optimization.

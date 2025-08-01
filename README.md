# 🤖 MCP Agent Project - Website Analytics Simulator

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)

**A powerful AI-driven website analytics simulation tool with Google Analytics integration capabilities.**

This repository contains a complete MCP (Model Context Protocol) server that simulates Google Analytics data using FastAPI. It's designed to be easily adaptable for real Google Analytics integration and provides a responsive web dashboard for data visualization.

## 🎯 **Purpose & Use Cases**

- **🧪 Testing & Development**: Simulate website analytics during development
- **📊 Proof of Concept**: Demonstrate analytics dashboards without real data
- **🔌 API Foundation**: Ready-to-extend foundation for real Google Analytics integration
- **🎓 Learning**: Understand analytics API structure and data formats
- **🚀 Prototyping**: Quick setup for analytics-based applications

## 📁 **Project Structure**

```
MCP-agent/
├── 📄 main.py                              # Main application entry point
├── 📋 requirements.txt                     # Python dependencies
├── ⚙️ .env                                # Environment configuration
├── 🌐 website-analysis-dashboard.html     # Interactive web dashboard
├── 📂 website_analyzer/                   # Core MCP server
│   ├── 🖥️ mcp_server.py                  # FastAPI server with endpoints
│   ├── 🧪 test_server.py                 # Automated testing script
│   ├── 📖 MCP_SERVER_README.md           # Detailed server documentation
│   ├── 🤖 agent.py                       # AI agent implementation
│   └── 🎭 demo_agent.py                  # Demo agent examples
├── 📂 src/                               # Source code modules
├── 📂 data/                              # Sample data storage
├── 📂 tests/                             # Test suite
└── 📂 logs/                              # Application logs
```

## ✨ **Key Features**

### 🔄 **MCP Server Capabilities**
- **FastAPI-powered REST API** with automatic documentation
- **3 Core endpoints** simulating Google Analytics data:
  - `GET /tools/get_website_traffic` - User metrics & bounce rates
  - `GET /tools/get_top_pages` - Page performance analytics
  - `GET /tools/get_traffic_sources` - Traffic source breakdown
- **Real-time data updates** with hot-reload support
- **CORS-enabled** for cross-origin requests
- **Production-ready** with proper error handling

### 🎨 **Interactive Dashboard**
- **Responsive design** using Tailwind CSS
- **Real-time server status** monitoring
- **Live API testing** directly from the dashboard
- **Visual metrics display** with charts and cards
- **AI recommendations** based on analytics data
- **Mobile-friendly** responsive layout

### 🤖 **AI Agent Integration**
- **Intelligent data analysis** and recommendations
- **Workflow automation** for analytics tasks
- **Extensible agent framework** for custom behaviors

## 🚀 **Quick Start Guide**

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Server**:
   ```bash
   cd website_analyzer
   uvicorn mcp_server:app --reload --host 127.0.0.1 --port 8000
   ```

3. **Open the Dashboard**:
   Simply open `website-analysis-dashboard.html` in your web browser.

## Configuration

- Environment variables can be set in the `.env` file.
- Server configurations such as host and port can be adjusted directly in the FastAPI run command.

## Integrating with Google Analytics

To integrate with real Google Analytics:

1. **Google Analytics API Setup:**
   - Obtain credentials from Google Developer Console.
   - Use OAuth 2.0 to authenticate.

2. **Use Google Analytics Client Library:**
   - Utilize libraries like `google-api-python-client` to extract real data.

3. **Adapt MCP Server Endpoints:**
   - Modify endpoints in `mcp_server.py` to fetch real data instead of static data.

## Notes

- **Security**: Ensure that credentials and sensitive information are stored securely.
- **Performance**: Test the setup with real data to assess performance impacts.

## Support

For further assistance, please refer to the FastAPI and Uvicorn documentation, or contact [Your Contact Information].

Enjoy your seamless web analytics experience with the MCP Agent Project! 🎉

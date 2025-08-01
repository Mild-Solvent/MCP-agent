# MCP Server for Website Analytics

🚀 **TESTED & WORKING!** This is a FastAPI-based MCP (Model Context Protocol) server that simulates Google Analytics data for website analysis.

## ✅ Test Results Summary

**All endpoints tested successfully:**
- ✅ `/tools/get_website_traffic` - Returns traffic data
- ✅ `/tools/get_top_pages` - Returns top pages list  
- ✅ `/tools/get_traffic_sources` - Returns traffic sources
- ✅ FastAPI docs available at `/docs`
- ✅ Server runs on localhost:8000

## Features

The server provides three endpoints that return static JSON data simulating website analytics:

### Endpoints

1. **GET /tools/get_website_traffic**
   - Returns total users and bounce rate for the last 30 days
   - Response: `{"total_users": 15000, "bounce_rate": 0.45}`

2. **GET /tools/get_top_pages**
   - Returns top 3 pages by views
   - Response: 
   ```json
   {
     "pages": [
       {"page_path": "/home", "page_title": "Homepage", "views": 5000},
       {"page_path": "/about", "page_title": "About Us", "views": 3000},
       {"page_path": "/contact", "page_title": "Contact", "views": 2000}
     ]
   }
   ```

3. **GET /tools/get_traffic_sources**
   - Returns top 3 traffic sources by users
   - Response:
   ```json
   {
     "sources": [
       {"source": "Organic Search", "users": 7000},
       {"source": "Direct", "users": 5000},
       {"source": "Referral", "users": 3000}
     ]
   }
   ```

## Installation

1. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn
   ```

## Running the Server

### Option 1: Using Python directly
```bash
python mcp_server.py
```

### Option 2: Using Uvicorn (recommended for development)
```bash
uvicorn mcp_server:app --reload
```

The server will start on `http://localhost:8000`

## 🧪 Testing the Endpoints

### Quick Test Guide

1. **Start the server:**
   ```bash
   cd website_analyzer
   uvicorn mcp_server:app --reload
   ```
   You should see: `INFO: Uvicorn running on http://127.0.0.1:8000`

2. **Test endpoints** (choose your preferred method below)

### Method 1: Using PowerShell (Windows)
```powershell
# Test website traffic endpoint
Invoke-WebRequest -Uri "http://localhost:8000/tools/get_website_traffic" | Select-Object -ExpandProperty Content

# Test top pages endpoint
Invoke-WebRequest -Uri "http://localhost:8000/tools/get_top_pages" | Select-Object -ExpandProperty Content

# Test traffic sources endpoint
Invoke-WebRequest -Uri "http://localhost:8000/tools/get_traffic_sources" | Select-Object -ExpandProperty Content
```

### Method 2: Using curl (Linux/Mac/Windows with curl)
```bash
# Get website traffic
curl http://localhost:8000/tools/get_website_traffic

# Get top pages
curl http://localhost:8000/tools/get_top_pages

# Get traffic sources
curl http://localhost:8000/tools/get_traffic_sources
```

### Method 3: Using a web browser
Simply navigate to these URLs in your browser:
- http://localhost:8000/tools/get_website_traffic
- http://localhost:8000/tools/get_top_pages
- http://localhost:8000/tools/get_traffic_sources

### Method 4: Using FastAPI's Interactive Documentation
Visit **http://localhost:8000/docs** to see the interactive API documentation where you can:
- See all endpoints
- Test them directly in the browser
- View request/response examples
- Download OpenAPI schema

## 📊 Expected Test Results

### Endpoint 1: Website Traffic
```json
{"total_users": 15000, "bounce_rate": 0.45}
```

### Endpoint 2: Top Pages
```json
{
  "pages": [
    {"page_path": "/home", "page_title": "Homepage", "views": 5000},
    {"page_path": "/about", "page_title": "About Us", "views": 3000},
    {"page_path": "/contact", "page_title": "Contact", "views": 2000}
  ]
}
```

### Endpoint 3: Traffic Sources
```json
{
  "sources": [
    {"source": "Organic Search", "users": 7000},
    {"source": "Direct", "users": 5000},
    {"source": "Referral", "users": 3000}
  ]
}
```

## Server Configuration

- **Host**: 127.0.0.1 (localhost)
- **Port**: 8000
- **Reload**: Enabled (automatically restarts on code changes)

## 🔧 Troubleshooting

### Common Issues:

1. **"ModuleNotFoundError: No module named 'fastapi'"**
   - Solution: `pip install fastapi uvicorn`

2. **"Port 8000 is already in use"**
   - Solution: Use a different port: `uvicorn mcp_server:app --port 8001`
   - Or stop existing processes: `Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process`

3. **"Connection refused" when testing endpoints**
   - Make sure the server is running first
   - Check if you can access http://localhost:8000 in browser
   - Verify the server started without errors

4. **Server won't start**
   - Make sure you're in the `website_analyzer` directory
   - Check that `mcp_server.py` exists in current directory
   - Verify Python and pip are working: `python --version`

### Stopping the Server:
```powershell
# In PowerShell (Windows)
Get-Process | Where-Object {$_.ProcessName -eq "python"} | Stop-Process

# Or press Ctrl+C in the terminal where server is running
```

## 📋 Server Logs

When running, you should see logs like:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:51953 - "GET /tools/get_website_traffic HTTP/1.1" 200 OK
```

## Notes

- All data returned is static and simulated for demonstration purposes
- The server uses FastAPI which provides automatic API documentation
- The `--reload` flag enables hot reloading during development
- Server tested successfully on Windows with PowerShell

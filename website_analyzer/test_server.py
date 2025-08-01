#!/usr/bin/env python3
"""
Test script for MCP Server endpoints
This script tests all three endpoints and displays the results
"""

import requests
import json
import time
import sys

def test_endpoint(url, endpoint_name):
    """Test a single endpoint and display results"""
    try:
        print(f"\n🧪 Testing {endpoint_name}...")
        print(f"URL: {url}")
        
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            print(f"✅ Status: {response.status_code} OK")
            print(f"📊 Response:")
            # Pretty print JSON
            formatted_json = json.dumps(response.json(), indent=2)
            print(formatted_json)
            return True
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Error: Cannot connect to {url}")
        print("Make sure the server is running with: uvicorn mcp_server:app --reload")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ Timeout: Server took too long to respond")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 MCP Server Endpoint Test")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test server availability first
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
        else:
            print("⚠️  Server responds but docs endpoint returned:", response.status_code)
    except:
        print("❌ Cannot connect to server at http://localhost:8000")
        print("Please start the server first with: uvicorn mcp_server:app --reload")
        sys.exit(1)
    
    # Test all endpoints
    endpoints = [
        ("/tools/get_website_traffic", "Website Traffic"),
        ("/tools/get_top_pages", "Top Pages"),
        ("/tools/get_traffic_sources", "Traffic Sources")
    ]
    
    results = []
    for endpoint, name in endpoints:
        url = f"{base_url}{endpoint}"
        success = test_endpoint(url, name)
        results.append((name, success))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your MCP server is working perfectly!")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")
        sys.exit(1)

if __name__ == "__main__":
    # Check if requests is available
    try:
        import requests
    except ImportError:
        print("❌ Error: 'requests' library not found")
        print("Install it with: pip install requests")
        sys.exit(1)
    
    main()

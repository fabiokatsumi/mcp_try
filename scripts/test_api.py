#!/usr/bin/env python3
"""
Quick API test script for the MCP server.
This script tests the server endpoints with your API key.
"""

import requests
import json
import sys
import os

# Configuration
BASE_URL = "http://localhost:8080"
API_KEY = "LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4"  # Your API key

def test_health():
    """Test the health endpoint (no auth required)"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_tools():
    """Test the tools endpoint (auth required)"""
    print("\n🔧 Testing tools endpoint...")
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(f"{BASE_URL}/api/tools", headers=headers)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_mcp():
    """Test the MCP endpoint (auth required)"""
    print("\n🎯 Testing MCP endpoint...")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "jsonrpc": "2.0",
        "method": "tools/list", 
        "id": 1
    }
    try:
        response = requests.post(f"{BASE_URL}/mcp", headers=headers, json=data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def main():
    print("🧪 MCP Server API Test")
    print("=" * 50)
    
    # Test health endpoint
    health_ok = test_health()
    
    # Test authenticated endpoints
    tools_ok = test_tools()
    mcp_ok = test_mcp()
    
    print("\n📊 Test Results:")
    print(f"   Health endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"   Tools endpoint:  {'✅ PASS' if tools_ok else '❌ FAIL'}")
    print(f"   MCP endpoint:    {'✅ PASS' if mcp_ok else '❌ FAIL'}")
    
    if health_ok and tools_ok and mcp_ok:
        print("\n🎉 All tests passed! Your MCP server is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Check server status and configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

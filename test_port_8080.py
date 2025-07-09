#!/usr/bin/env python3
"""
Test script for port 8080 server (original one)
"""

import requests
import json

BASE_URL = "http://localhost:8080"
API_KEY = "LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health Error: {e}")
        return False

def test_tools():
    """Test tools endpoint"""
    try:
        headers = {"Authorization": f"Bearer {API_KEY}"}
        response = requests.get(f"{BASE_URL}/api/tools", headers=headers, timeout=5)
        print(f"Tools Status: {response.status_code}")
        print(f"Tools Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Tools Error: {e}")
        return False

def test_mcp():
    """Test MCP endpoint"""
    try:
        headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
        data = {"jsonrpc": "2.0", "method": "tools/list", "id": 1}
        response = requests.post(f"{BASE_URL}/mcp", headers=headers, json=data, timeout=5)
        print(f"MCP Status: {response.status_code}")
        print(f"MCP Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"MCP Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing original server on port 8080...")
    print("=" * 50)
    
    health_ok = test_health()
    print()
    tools_ok = test_tools()
    print()
    mcp_ok = test_mcp()
    
    print(f"\n📊 Results:")
    print(f"Health: {'✅' if health_ok else '❌'}")
    print(f"Tools: {'✅' if tools_ok else '❌'}")
    print(f"MCP: {'✅' if mcp_ok else '❌'}")

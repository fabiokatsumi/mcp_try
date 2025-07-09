#!/usr/bin/env python3
"""
Enhanced API test script that shows tool details.
"""

import requests
import json
import sys
import os

# Configuration
BASE_URL = "http://localhost:8080"
API_KEY = "LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4"

def test_health():
    """Test the health endpoint (no auth required)"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        data = response.json()
        print(f"   Server Status: {data.get('status')}")
        print(f"   Uptime: {data.get('uptime', 0):.1f}s")
        print(f"   Version: {data.get('version')}")
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
        data = response.json()
        tools = data.get('tools', [])
        print(f"   Number of tools: {len(tools)}")
        
        if tools:
            print("   Available tools:")
            for tool in tools:
                if isinstance(tool, dict):
                    name = tool.get('name', 'unknown')
                    desc = tool.get('description', 'No description')
                    print(f"     - {name}: {desc}")
                else:
                    print(f"     - {tool}")
        else:
            print("   ⚠️  No tools registered")
        
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
        result = response.json()
        
        if 'result' in result:
            tools = result['result'].get('tools', [])
            print(f"   MCP tools count: {len(tools)}")
            if tools:
                print("   MCP tools:")
                for tool in tools:
                    if isinstance(tool, dict):
                        name = tool.get('name', 'unknown')
                        desc = tool.get('description', 'No description')
                        print(f"     - {name}: {desc}")
        else:
            print(f"   Raw response: {result}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_tool_execution():
    """Test executing a tool via MCP"""
    print("\n⚙️  Testing tool execution...")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Test echo tool
    data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "echo",
            "arguments": {"message": "Hello from MCP!"}
        },
        "id": 2
    }
    
    try:
        response = requests.post(f"{BASE_URL}/mcp", headers=headers, json=data)
        print(f"   Echo tool status: {response.status_code}")
        result = response.json()
        
        if 'result' in result:
            print(f"   Echo result: {result['result']}")
        else:
            print(f"   Echo response: {result}")
            
        return response.status_code == 200
    except Exception as e:
        print(f"   Error: {e}")
        return False

def main():
    print("🧪 Enhanced MCP Server API Test")
    print("=" * 50)
    
    # Test all endpoints
    health_ok = test_health()
    tools_ok = test_tools()
    mcp_ok = test_mcp()
    execution_ok = test_tool_execution()
    
    print("\n📊 Test Results:")
    print(f"   Health endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"   Tools endpoint:  {'✅ PASS' if tools_ok else '❌ FAIL'}")
    print(f"   MCP endpoint:    {'✅ PASS' if mcp_ok else '❌ FAIL'}")
    print(f"   Tool execution:  {'✅ PASS' if execution_ok else '❌ FAIL'}")
    
    if all([health_ok, tools_ok, mcp_ok]):
        print("\n🎉 Server is working correctly!")
        if not execution_ok:
            print("⚠️  Tool execution failed - check tool registration")
    else:
        print("\n❌ Some tests failed. Check server status.")
    
    print("\n💡 Next steps:")
    print("   1. Restart your server to load tools")
    print("   2. Use: python start_server.py --api-keys YOUR_API_KEY")
    print("   3. Run this test again to see tools loaded")

if __name__ == "__main__":
    main()

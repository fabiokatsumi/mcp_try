#!/usr/bin/env python3
"""
Test the MCP server on port 8081 with tools loaded.
"""

import requests
import json
import sys

# Configuration for port 8081
BASE_URL = "http://localhost:8081"
API_KEY = "LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4"

def test_health():
    """Test the health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Server Status: {data.get('status')}")
            print(f"   Uptime: {data.get('uptime', 0):.1f}s")
            return True
        else:
            print(f"   Error: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_tools():
    """Test the tools endpoint"""
    print("\n🔧 Testing tools endpoint...")
    headers = {"Authorization": f"Bearer {API_KEY}"}
    try:
        response = requests.get(f"{BASE_URL}/api/tools", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            tools = data.get('tools', [])
            count = data.get('count', len(tools))
            
            print(f"   Tools found: {count}")
            
            if tools:
                print("   Available tools:")
                for tool in tools:
                    if isinstance(tool, dict):
                        name = tool.get('name', 'unknown')
                        desc = tool.get('description', 'No description')
                        print(f"     - {name}: {desc}")
                    else:
                        print(f"     - {tool}")
                return True
            else:
                print("   ⚠️  No tools found")
                return False
        else:
            print(f"   Error: HTTP {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_mcp():
    """Test the MCP endpoint"""
    print("\n🎯 Testing MCP tools/list...")
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
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=2)}")
            
            if 'result' in result:
                tools = result['result'].get('tools', [])
                count = result['result'].get('count', len(tools))
                print(f"   MCP tools found: {count}")
                return len(tools) > 0
            else:
                print("   No result in response")
                return False
        else:
            print(f"   Error: HTTP {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"   Error: {e}")
        return False

def test_echo_tool():
    """Test the echo tool execution"""
    print("\n⚙️  Testing echo tool execution...")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "echo",
            "arguments": {"message": "Hello MCP!"}
        },
        "id": 2
    }
    
    try:
        response = requests.post(f"{BASE_URL}/mcp", headers=headers, json=data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   Echo result: {json.dumps(result, indent=2)}")
            
            if 'result' in result:
                return True
            elif 'error' in result:
                print(f"   Tool execution error: {result['error']}")
                return False
        else:
            print(f"   Error: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   Error: {e}")
        return False

def main():
    print("🧪 MCP Server Test (Port 8081)")
    print("=" * 50)
    
    # Test all endpoints
    health_ok = test_health()
    tools_ok = test_tools()
    mcp_ok = test_mcp()
    echo_ok = test_echo_tool()
    
    print("\n📊 Test Results:")
    print(f"   Health endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"   Tools endpoint:  {'✅ PASS' if tools_ok else '❌ FAIL'}")
    print(f"   MCP endpoint:    {'✅ PASS' if mcp_ok else '❌ FAIL'}")
    print(f"   Echo tool:       {'✅ PASS' if echo_ok else '❌ FAIL'}")
    
    if all([health_ok, tools_ok, mcp_ok]):
        print("\n🎉 Server is working with tools!")
        return 0
    else:
        print("\n❌ Some tests failed.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

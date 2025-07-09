#!/usr/bin/env python3
"""
Test client for the HTTP MCP server
"""

import requests
import json
import sys

def test_http_mcp_server(base_url="http://localhost:8080"):
    """Test the HTTP MCP server"""
    
    print(f"🧪 Testing HTTP MCP Server at {base_url}")
    print("=" * 50)
    
    # Test 1: Initialize
    print("\n1️⃣ Testing initialization...")
    init_request = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "http-client", "version": "1.0.0"}
        }
    }
    
    try:
        response = requests.post(f"{base_url}/mcp", json=init_request, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Initialize: SUCCESS")
            print(f"   Server: {result['result']['serverInfo']['name']}")
        else:
            print(f"❌ Initialize: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Initialize: FAILED - {e}")
    
    # Test 2: List tools
    print("\n2️⃣ Testing tools list...")
    tools_request = {
        "jsonrpc": "2.0",
        "id": "2",
        "method": "tools/list"
    }
    
    try:
        response = requests.post(f"{base_url}/mcp", json=tools_request, timeout=10)
        if response.status_code == 200:
            result = response.json()
            tools = result["result"]["tools"]
            print(f"✅ Tools list: SUCCESS - Found {len(tools)} tools")
            for tool in tools:
                print(f"   🔧 {tool['name']}")
        else:
            print(f"❌ Tools list: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Tools list: FAILED - {e}")
    
    # Test 3: Get time
    print("\n3️⃣ Testing get_time tool...")
    time_request = {
        "jsonrpc": "2.0",
        "id": "3",
        "method": "tools/call",
        "params": {
            "name": "get_time",
            "arguments": {}
        }
    }
    
    try:
        response = requests.post(f"{base_url}/mcp", json=time_request, timeout=10)
        if response.status_code == 200:
            result = response.json()
            content = result["result"]["content"][0]["text"]
            print("✅ Get time: SUCCESS")
            print(f"   ⏰ {content}")
        else:
            print(f"❌ Get time: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Get time: FAILED - {e}")
    
    # Test 4: List directory
    print("\n4️⃣ Testing list_directory tool...")
    list_request = {
        "jsonrpc": "2.0",
        "id": "4",
        "method": "tools/call",
        "params": {
            "name": "list_directory",
            "arguments": {"directory_path": "."}
        }
    }
    
    try:
        response = requests.post(f"{base_url}/mcp", json=list_request, timeout=10)
        if response.status_code == 200:
            result = response.json()
            content = result["result"]["content"][0]["text"]
            print("✅ List directory: SUCCESS")
            print(f"   📁 Directory content retrieved")
        else:
            print(f"❌ List directory: FAILED - HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ List directory: FAILED - {e}")
    
    print("\n" + "=" * 50)
    print("🎉 HTTP MCP Server test completed!")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:8080"
    
    # Check if requests is available
    try:
        import requests
    except ImportError:
        print("❌ 'requests' library not found. Install it with:")
        print("   pip install requests")
        sys.exit(1)
    
    test_http_mcp_server(base_url)

if __name__ == "__main__":
    main()

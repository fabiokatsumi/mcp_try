#!/usr/bin/env python3
"""
Test client for the MCP server over HTTP/LAN
"""

import requests
import json
import sys

def test_mcp_http_server(host="192.168.254.95", port=8080):
    """Test the MCP server over HTTP"""
    
    base_url = f"http://{host}:{port}"
    endpoint = f"{base_url}/mcp"
    
    print(f"🧪 Testing MCP Server at {endpoint}")
    print("=" * 50)
    
    # Test 1: Initialize the server
    print("\n1️⃣ Testing server initialization...")
    init_request = {
        "jsonrpc": "2.0",
        "id": "1",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "lan-test-client", "version": "1.0.0"}
        }
    }
    
    try:
        response = requests.post(endpoint, json=init_request)
        result = response.json()
        print(f"✅ Initialize: {result}")
    except Exception as e:
        print(f"❌ Initialize failed: {e}")
        return
    
    # Test 2: List available tools
    print("\n2️⃣ Testing tools list...")
    tools_request = {
        "jsonrpc": "2.0",
        "id": "2",
        "method": "tools/list"
    }
    
    try:
        response = requests.post(endpoint, json=tools_request)
        result = response.json()
        print(f"✅ Tools list: {result}")
    except Exception as e:
        print(f"❌ Tools list failed: {e}")
        return
    
    # Test 3: Get current time
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
        response = requests.post(endpoint, json=time_request)
        result = response.json()
        print(f"✅ Get time: {result}")
    except Exception as e:
        print(f"❌ Get time failed: {e}")
    
    # Test 4: List directory
    print("\n4️⃣ Testing list_directory tool...")
    list_request = {
        "jsonrpc": "2.0",
        "id": "4",
        "method": "tools/call",
        "params": {
            "name": "list_directory",
            "arguments": {"path": "."}
        }
    }
    
    try:
        response = requests.post(endpoint, json=list_request)
        result = response.json()
        print(f"✅ List directory: {result}")
    except Exception as e:
        print(f"❌ List directory failed: {e}")
    
    # Test 5: Test web interface
    print("\n5️⃣ Testing web interface...")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print(f"✅ Web interface accessible at {base_url}")
            print(f"   Content-Type: {response.headers.get('content-type')}")
            print(f"   Response length: {len(response.text)} characters")
        else:
            print(f"❌ Web interface failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Web interface failed: {e}")
    
    print(f"\n🌐 Your MCP server is accessible at:")
    print(f"   • Web UI: {base_url}")
    print(f"   • API: {endpoint}")
    print(f"   • Network: Available to all devices on LAN")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        host = sys.argv[1]
        test_mcp_http_server(host)
    else:
        test_mcp_http_server()

if __name__ == "__main__":
    main()

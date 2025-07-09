#!/usr/bin/env python3
"""
Demo script to test the new dynamic tools
"""

import requests
import json

def test_new_tools():
    """Test the new tools that were added"""
    
    base_url = "http://192.168.254.95:8080/mcp"
    
    print("🧮 Testing Calculator Tool")
    print("=" * 30)
    
    # Test calculator
    calc_request = {
        "jsonrpc": "2.0",
        "id": "calc1",
        "method": "tools/call",
        "params": {
            "name": "calculate",
            "arguments": {"expression": "2 + 3 * 4"}
        }
    }
    
    response = requests.post(base_url, json=calc_request)
    result = response.json()
    print(f"Expression: 2 + 3 * 4")
    print(f"Result: {result}")
    
    print("\n💻 Testing System Info Tool")
    print("=" * 30)
    
    # Test system info
    sys_request = {
        "jsonrpc": "2.0",
        "id": "sys1",
        "method": "tools/call",
        "params": {
            "name": "system_info",
            "arguments": {}
        }
    }
    
    response = requests.post(base_url, json=sys_request)
    result = response.json()
    print(f"System Info: {result}")
    
    print("\n🌐 Tools API Test")
    print("=" * 30)
    
    # Test tools API
    response = requests.get("http://192.168.254.95:8080/api/tools")
    tools_data = response.json()
    
    print("Available tools:")
    for tool in tools_data['tools']:
        print(f"  • {tool['name']}: {tool['description']}")

if __name__ == "__main__":
    test_new_tools()

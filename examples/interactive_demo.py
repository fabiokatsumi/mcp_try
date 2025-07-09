#!/usr/bin/env python3
"""
Interactive demo for the MCP server
"""

import json
import subprocess
import sys

def interactive_demo():
    """Interactive demonstration of MCP server capabilities"""
    
    print("🎯 Interactive MCP Server Demo")
    print("=" * 40)
    print("This demo shows how to interact with the MCP server")
    print("using raw JSON-RPC requests.\n")
    
    while True:
        print("\nAvailable actions:")
        print("1. Initialize server")
        print("2. List tools")
        print("3. Get current time")
        print("4. List current directory")
        print("5. Write a file")
        print("6. Read a file")
        print("7. List resources")
        print("8. Read resource")
        print("9. Send custom request")
        print("0. Exit")
        
        choice = input("\nChoose an action (0-9): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            demo_initialize()
        elif choice == "2":
            demo_list_tools()
        elif choice == "3":
            demo_get_time()
        elif choice == "4":
            demo_list_directory()
        elif choice == "5":
            demo_write_file()
        elif choice == "6":
            demo_read_file()
        elif choice == "7":
            demo_list_resources()
        elif choice == "8":
            demo_read_resource()
        elif choice == "9":
            demo_custom_request()
        else:
            print("❌ Invalid choice. Please try again.")

def send_request(request):
    """Send a request to the MCP server and display the response"""
    print(f"\n📤 Sending request:")
    print(json.dumps(request, indent=2))
    
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
            response = json.loads(stdout.strip())
            print(f"\n📥 Response:")
            print(json.dumps(response, indent=2))
            return response
        else:
            print(f"❌ No response. Error: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def demo_initialize():
    request = {
        "jsonrpc": "2.0",
        "id": "init",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "demo-client", "version": "1.0.0"}
        }
    }
    send_request(request)

def demo_list_tools():
    request = {
        "jsonrpc": "2.0",
        "id": "tools",
        "method": "tools/list"
    }
    send_request(request)

def demo_get_time():
    request = {
        "jsonrpc": "2.0",
        "id": "time",
        "method": "tools/call",
        "params": {
            "name": "get_time",
            "arguments": {}
        }
    }
    send_request(request)

def demo_list_directory():
    path = input("Enter directory path (or press Enter for current directory): ").strip()
    if not path:
        path = "."
    
    request = {
        "jsonrpc": "2.0",
        "id": "listdir",
        "method": "tools/call",
        "params": {
            "name": "list_directory",
            "arguments": {"directory_path": path}
        }
    }
    send_request(request)

def demo_write_file():
    filename = input("Enter filename to write: ").strip()
    content = input("Enter content to write: ").strip()
    
    if not filename:
        print("❌ Filename cannot be empty")
        return
    
    request = {
        "jsonrpc": "2.0",
        "id": "write",
        "method": "tools/call",
        "params": {
            "name": "write_file",
            "arguments": {
                "file_path": filename,
                "content": content
            }
        }
    }
    send_request(request)

def demo_read_file():
    filename = input("Enter filename to read: ").strip()
    
    if not filename:
        print("❌ Filename cannot be empty")
        return
    
    request = {
        "jsonrpc": "2.0",
        "id": "read",
        "method": "tools/call",
        "params": {
            "name": "read_file",
            "arguments": {"file_path": filename}
        }
    }
    send_request(request)

def demo_list_resources():
    request = {
        "jsonrpc": "2.0",
        "id": "resources",
        "method": "resources/list"
    }
    send_request(request)

def demo_read_resource():
    request = {
        "jsonrpc": "2.0",
        "id": "readres",
        "method": "resources/read",
        "params": {"uri": "file://current_directory"}
    }
    send_request(request)

def demo_custom_request():
    print("\nEnter a custom JSON-RPC request:")
    print("Example: {\"jsonrpc\": \"2.0\", \"id\": \"custom\", \"method\": \"tools/list\"}")
    
    try:
        request_str = input("JSON request: ").strip()
        request = json.loads(request_str)
        send_request(request)
    except json.JSONDecodeError:
        print("❌ Invalid JSON format")

if __name__ == "__main__":
    interactive_demo()

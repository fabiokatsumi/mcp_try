#!/usr/bin/env python3
"""
Simple MCP client for testing the MCP server
"""

import asyncio
import json
import sys
import subprocess
from typing import Dict, Any


class SimpleMCPClient:
    """A simple MCP client for testing"""
    
    def __init__(self, server_command: str):
        self.server_command = server_command
        self.process = None
    
    async def start_server(self):
        """Start the MCP server process"""
        self.process = await asyncio.create_subprocess_exec(
            *self.server_command.split(),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    
    async def send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a request to the server and get response"""
        if not self.process:
            raise RuntimeError("Server not started")
        
        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json.encode())
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        response = json.loads(response_line.decode().strip())
        
        return response
    
    async def close(self):
        """Close the server process"""
        if self.process:
            self.process.terminate()
            await self.process.wait()


async def test_mcp_server():
    """Test the MCP server with various requests"""
    client = SimpleMCPClient("python app.py")
    
    try:
        print("Starting MCP server...")
        await client.start_server()
        
        # Test 1: Initialize
        print("\n1. Testing initialization...")
        init_request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        response = await client.send_request(init_request)
        print(f"Initialize response: {json.dumps(response, indent=2)}")
        
        # Test 2: List tools
        print("\n2. Testing tools list...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "tools/list"
        }
        
        response = await client.send_request(tools_request)
        print(f"Tools list response: {json.dumps(response, indent=2)}")
        
        # Test 3: Call get_time tool
        print("\n3. Testing get_time tool...")
        time_request = {
            "jsonrpc": "2.0",
            "id": "3",
            "method": "tools/call",
            "params": {
                "name": "get_time",
                "arguments": {}
            }
        }
        
        response = await client.send_request(time_request)
        print(f"Get time response: {json.dumps(response, indent=2)}")
        
        # Test 4: List current directory
        print("\n4. Testing list_directory tool...")
        list_request = {
            "jsonrpc": "2.0",
            "id": "4",
            "method": "tools/call",
            "params": {
                "name": "list_directory",
                "arguments": {
                    "directory_path": "."
                }
            }
        }
        
        response = await client.send_request(list_request)
        print(f"List directory response: {json.dumps(response, indent=2)}")
        
        # Test 5: Write and read a test file
        print("\n5. Testing write_file tool...")
        write_request = {
            "jsonrpc": "2.0",
            "id": "5",
            "method": "tools/call",
            "params": {
                "name": "write_file",
                "arguments": {
                    "file_path": "test_file.txt",
                    "content": "Hello from MCP server!\nThis is a test file."
                }
            }
        }
        
        response = await client.send_request(write_request)
        print(f"Write file response: {json.dumps(response, indent=2)}")
        
        print("\n6. Testing read_file tool...")
        read_request = {
            "jsonrpc": "2.0",
            "id": "6",
            "method": "tools/call",
            "params": {
                "name": "read_file",
                "arguments": {
                    "file_path": "test_file.txt"
                }
            }
        }
        
        response = await client.send_request(read_request)
        print(f"Read file response: {json.dumps(response, indent=2)}")
        
        # Test 7: List resources
        print("\n7. Testing resources list...")
        resources_request = {
            "jsonrpc": "2.0",
            "id": "7",
            "method": "resources/list"
        }
        
        response = await client.send_request(resources_request)
        print(f"Resources list response: {json.dumps(response, indent=2)}")
        
        # Test 8: Read resource
        print("\n8. Testing resource read...")
        resource_request = {
            "jsonrpc": "2.0",
            "id": "8",
            "method": "resources/read",
            "params": {
                "uri": "file://current_directory"
            }
        }
        
        response = await client.send_request(resource_request)
        print(f"Resource read response: {json.dumps(response, indent=2)}")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
    
    finally:
        await client.close()


if __name__ == "__main__":
    print("Simple MCP Client Test")
    print("=" * 50)
    asyncio.run(test_mcp_server())

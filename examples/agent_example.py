#!/usr/bin/env python3
"""
Example AI agent that uses the cloud-deployed MCP server
"""

import requests
import json
from typing import Dict, Any, List

class CloudMCPAgent:
    """An AI agent that uses a cloud-deployed MCP server"""
    
    def __init__(self, mcp_url: str):
        """Initialize with the cloud MCP server URL"""
        self.mcp_url = mcp_url.rstrip('/') + '/mcp'
        self.request_id = 0
        
        # Test connection
        if not self._test_connection():
            raise ConnectionError(f"Cannot connect to MCP server at {self.mcp_url}")
    
    def _test_connection(self) -> bool:
        """Test if the MCP server is accessible"""
        try:
            response = requests.get(self.mcp_url.replace('/mcp', '/health'), timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def _send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a request to the MCP server"""
        self.request_id += 1
        
        request = {
            "jsonrpc": "2.0",
            "id": str(self.request_id),
            "method": method
        }
        
        if params:
            request["params"] = params
        
        try:
            response = requests.post(
                self.mcp_url,
                json=request,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": str(self.request_id),
                "error": {"code": -1, "message": str(e)}
            }
    
    def initialize(self) -> bool:
        """Initialize the MCP session"""
        response = self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "cloud-mcp-agent",
                "version": "1.0.0"
            }
        })
        
        return "result" in response
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools"""
        response = self._send_request("tools/list")
        
        if "result" in response:
            return response["result"].get("tools", [])
        return []
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any] = None) -> Any:
        """Call a specific tool"""
        if arguments is None:
            arguments = {}
        
        response = self._send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        
        if "result" in response:
            content = response["result"].get("content", [])
            if content and len(content) > 0:
                return content[0].get("text", "")
        elif "error" in response:
            return f"Error: {response['error']['message']}"
        
        return "No response"
    
    def calculate(self, expression: str) -> str:
        """Use the calculator tool"""
        return self.call_tool("calculate", {"expression": expression})
    
    def get_time(self) -> str:
        """Get current time"""
        return self.call_tool("get_time")
    
    def get_system_info(self) -> str:
        """Get system information"""
        return self.call_tool("system_info")
    
    def read_file(self, file_path: str) -> str:
        """Read a file"""
        return self.call_tool("read_file", {"file_path": file_path})
    
    def write_file(self, file_path: str, content: str) -> str:
        """Write to a file"""
        return self.call_tool("write_file", {"file_path": file_path, "content": content})
    
    def list_directory(self, directory_path: str = ".") -> str:
        """List directory contents"""
        return self.call_tool("list_directory", {"directory_path": directory_path})

def demo_agent(server_url: str):
    """Demonstrate the cloud MCP agent"""
    print(f"🤖 Connecting to MCP server at: {server_url}")
    print("=" * 60)
    
    try:
        # Create agent
        agent = CloudMCPAgent(server_url)
        
        # Initialize
        if agent.initialize():
            print("✅ Successfully connected to MCP server")
        else:
            print("❌ Failed to initialize MCP connection")
            return
        
        # Get available tools
        print("\n🛠️ Available Tools:")
        tools = agent.get_available_tools()
        for tool in tools:
            print(f"  • {tool['name']}: {tool['description']}")
        
        # Test calculator
        print("\n🧮 Testing Calculator:")
        result = agent.calculate("2**10 + 5 * 3")
        print(f"  Result: {result}")
        
        # Test time
        print("\n⏰ Getting Current Time:")
        time_result = agent.get_time()
        print(f"  Time: {time_result}")
        
        # Test system info
        print("\n💻 Getting System Info:")
        sys_info = agent.get_system_info()
        print(f"  Info: {sys_info[:100]}...")
        
        # Test file operations
        print("\n📁 Testing File Operations:")
        write_result = agent.write_file("agent_test.txt", "Hello from cloud agent!")
        print(f"  Write: {write_result}")
        
        read_result = agent.read_file("agent_test.txt")
        print(f"  Read: {read_result}")
        
        print("\n✅ All agent tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Agent error: {e}")

def main():
    """Main function"""
    print("🤖 Cloud MCP Agent Demo")
    print("=" * 40)
    
    # You can test with different URLs
    test_urls = [
        "http://localhost:8080",  # Local development
        # "https://your-app.railway.app",  # Railway deployment
        # "https://your-app.herokuapp.com",  # Heroku deployment
        # "https://your-app.onrender.com",  # Render deployment
    ]
    
    for url in test_urls:
        print(f"\n🔗 Testing with: {url}")
        try:
            demo_agent(url)
            break  # Stop on first successful connection
        except ConnectionError as e:
            print(f"❌ Connection failed: {e}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

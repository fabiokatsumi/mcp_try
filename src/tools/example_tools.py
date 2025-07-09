#!/usr/bin/env python3
"""
Example MCP tool for demonstration purposes.
This tool provides basic system information.
"""

import platform
import psutil
import json
import time
from typing import Dict, Any, List

class SystemInfoTool:
    """Example MCP tool that provides system information."""
    
    def __init__(self):
        self.name = "system_info"
        self.description = "Get system information including OS, CPU, memory, and disk usage"
        self.version = "1.0.0"
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the tool schema for MCP protocol."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "detail_level": {
                            "type": "string",
                            "description": "Level of detail: 'basic' or 'detailed'",
                            "enum": ["basic", "detailed"],
                            "default": "basic"
                        }
                    },
                    "required": []
                }
            }
        }
    
    def execute(self, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the system info tool."""
        if parameters is None:
            parameters = {}
        
        detail_level = parameters.get("detail_level", "basic")
        
        try:
            # Basic system info
            basic_info = {
                "system": platform.system(),
                "platform": platform.platform(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count(),
                "memory_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
                "disk_usage_gb": round(psutil.disk_usage('/').total / (1024**3), 2) if platform.system() != "Windows" else round(psutil.disk_usage('C:').total / (1024**3), 2)
            }
            
            if detail_level == "detailed":
                # Detailed system info
                memory = psutil.virtual_memory()
                cpu_percent = psutil.cpu_percent(interval=1)
                disk_path = '/' if platform.system() != "Windows" else 'C:'
                disk = psutil.disk_usage(disk_path)
                
                detailed_info = {
                    **basic_info,
                    "cpu_usage_percent": cpu_percent,
                    "memory_usage_percent": memory.percent,
                    "memory_available_gb": round(memory.available / (1024**3), 2),
                    "disk_usage_percent": round((disk.used / disk.total) * 100, 2),
                    "disk_free_gb": round(disk.free / (1024**3), 2),
                    "boot_time": psutil.boot_time(),
                    "network_interfaces": len(psutil.net_if_addrs())
                }
                
                return {
                    "success": True,
                    "data": detailed_info,
                    "detail_level": detail_level
                }
            else:
                return {
                    "success": True,
                    "data": basic_info,
                    "detail_level": detail_level
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "detail_level": detail_level
            }

class EchoTool:
    """Simple echo tool for testing."""
    
    def __init__(self):
        self.name = "echo"
        self.description = "Echo back the input message"
        self.version = "1.0.0"
    
    def get_schema(self) -> Dict[str, Any]:
        """Get the tool schema for MCP protocol."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message to echo back"
                        }
                    },
                    "required": ["message"]
                }
            }
        }
    
    def execute(self, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute the echo tool."""
        if parameters is None:
            parameters = {}
        
        message = parameters.get("message", "")
        
        return {
            "success": True,
            "echoed_message": message,
            "timestamp": str(time.time())
        }

# Available tools for registration
AVAILABLE_TOOLS = [
    SystemInfoTool(),
    EchoTool()
]

def get_tools_list() -> List[Dict[str, Any]]:
    """Get list of available tools with their schemas."""
    return [tool.get_schema() for tool in AVAILABLE_TOOLS]

def execute_tool(tool_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
    """Execute a specific tool by name."""
    for tool in AVAILABLE_TOOLS:
        if tool.name == tool_name:
            return tool.execute(parameters)
    
    return {
        "success": False,
        "error": f"Tool '{tool_name}' not found",
        "available_tools": [tool.name for tool in AVAILABLE_TOOLS]
    }

if __name__ == "__main__":
    # Demo the tools
    print("🔧 Available MCP Tools:")
    for tool in AVAILABLE_TOOLS:
        print(f"  - {tool.name}: {tool.description}")
    
    print("\n🧪 Testing Echo Tool:")
    echo_result = execute_tool("echo", {"message": "Hello, MCP!"})
    print(json.dumps(echo_result, indent=2))
    
    print("\n🧪 Testing System Info Tool:")
    system_result = execute_tool("system_info", {"detail_level": "basic"})
    print(json.dumps(system_result, indent=2))

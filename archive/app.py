#!/usr/bin/env python3
"""
A simple MCP (Model Context Protocol) server example.
This server provides basic tools for file operations and system information.
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import os
import datetime


@dataclass
class Tool:
    """Represents an MCP tool"""
    name: str
    description: str
    input_schema: Dict[str, Any]


@dataclass
class Resource:
    """Represents an MCP resource"""
    uri: str
    name: str
    description: str
    mime_type: str


class SimpleMCPServer:
    """A simple MCP server implementation"""
    
    def __init__(self):
        self.tools = self._register_tools()
        self.resources = self._register_resources()
    
    def _register_tools(self) -> List[Tool]:
        """Register available tools"""
        return [
            Tool(
                name="get_time",
                description="Get current date and time",
                input_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            ),
            Tool(
                name="read_file",
                description="Read contents of a file",
                input_schema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to read"
                        }
                    },
                    "required": ["file_path"]
                }
            ),
            Tool(
                name="list_directory",
                description="List contents of a directory",
                input_schema={
                    "type": "object",
                    "properties": {
                        "directory_path": {
                            "type": "string",
                            "description": "Path to the directory to list"
                        }
                    },
                    "required": ["directory_path"]
                }
            ),
            Tool(
                name="write_file",
                description="Write content to a file",
                input_schema={
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to the file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            ),
            Tool(
                name="calculate",
                description="Perform basic mathematical calculations",
                input_schema={
                    "type": "object",
                    "properties": {
                        "expression": {
                            "type": "string",
                            "description": "Mathematical expression to evaluate (e.g., '2 + 3 * 4')"
                        }
                    },
                    "required": ["expression"]
                }
            ),
            Tool(
                name="system_info",
                description="Get system information",
                input_schema={
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            )
        ]
    
    def _register_resources(self) -> List[Resource]:
        """Register available resources"""
        return [
            Resource(
                uri="file://current_directory",
                name="Current Directory",
                description="Contents of the current working directory",
                mime_type="text/plain"
            )
        ]
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                return await self._handle_initialize(request_id, params)
            elif method == "tools/list":
                return await self._handle_tools_list(request_id)
            elif method == "tools/call":
                return await self._handle_tools_call(request_id, params)
            elif method == "resources/list":
                return await self._handle_resources_list(request_id)
            elif method == "resources/read":
                return await self._handle_resources_read(request_id, params)
            else:
                return self._error_response(request_id, -32601, f"Method not found: {method}")
        
        except Exception as e:
            return self._error_response(request_id, -32603, f"Internal error: {str(e)}")
    
    async def _handle_initialize(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {}
                },
                "serverInfo": {
                    "name": "simple-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
    
    async def _handle_tools_list(self, request_id: str) -> Dict[str, Any]:
        """Handle tools list request"""
        tools_data = []
        for tool in self.tools:
            tools_data.append({
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            })
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": tools_data
            }
        }
    
    async def _handle_tools_call(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "get_time":
            result = await self._tool_get_time()
        elif tool_name == "read_file":
            result = await self._tool_read_file(arguments.get("file_path"))
        elif tool_name == "list_directory":
            # Support both 'directory_path' and 'path' parameter names
            path = arguments.get("directory_path") or arguments.get("path") or "."
            result = await self._tool_list_directory(path)
        elif tool_name == "write_file":
            result = await self._tool_write_file(
                arguments.get("file_path"), 
                arguments.get("content")
            )
        elif tool_name == "calculate":
            result = await self._tool_calculate(arguments.get("expression"))
        elif tool_name == "system_info":
            result = await self._tool_system_info()
        else:
            return self._error_response(request_id, -32602, f"Unknown tool: {tool_name}")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": result
                    }
                ]
            }
        }
    
    async def _handle_resources_list(self, request_id: str) -> Dict[str, Any]:
        """Handle resources list request"""
        resources_data = []
        for resource in self.resources:
            resources_data.append({
                "uri": resource.uri,
                "name": resource.name,
                "description": resource.description,
                "mimeType": resource.mime_type
            })
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resources": resources_data
            }
        }
    
    async def _handle_resources_read(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle resource read request"""
        uri = params.get("uri")
        
        if uri == "file://current_directory":
            content = await self._resource_current_directory()
        else:
            return self._error_response(request_id, -32602, f"Unknown resource: {uri}")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "contents": [
                    {
                        "uri": uri,
                        "mimeType": "text/plain",
                        "text": content
                    }
                ]
            }
        }
    
    # Tool implementations
    async def _tool_get_time(self) -> str:
        """Get current date and time"""
        now = datetime.datetime.now()
        return f"Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    async def _tool_read_file(self, file_path: str) -> str:
        """Read file contents"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"File contents of {file_path}:\n\n{content}"
        except FileNotFoundError:
            return f"Error: File not found: {file_path}"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    async def _tool_list_directory(self, directory_path: str) -> str:
        """List directory contents"""
        try:
            items = os.listdir(directory_path)
            items.sort()
            
            result = f"Contents of directory {directory_path}:\n\n"
            for item in items:
                item_path = os.path.join(directory_path, item)
                if os.path.isdir(item_path):
                    result += f"📁 {item}/\n"
                else:
                    result += f"📄 {item}\n"
            
            return result
        except FileNotFoundError:
            return f"Error: Directory not found: {directory_path}"
        except Exception as e:
            return f"Error listing directory: {str(e)}"
    
    async def _tool_write_file(self, file_path: str, content: str) -> str:
        """Write content to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote content to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    async def _tool_calculate(self, expression: str) -> str:
        """Perform basic mathematical calculations"""
        try:
            # Only allow safe mathematical operations
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return "Error: Only basic mathematical operations are allowed (+, -, *, /, parentheses)"
            
            # Evaluate the expression safely
            result = eval(expression)
            return f"Result: {expression} = {result}"
        except Exception as e:
            return f"Error calculating expression: {str(e)}"
    
    async def _tool_system_info(self) -> str:
        """Get system information"""
        try:
            import platform
            import psutil
            
            info = []
            info.append(f"System: {platform.system()} {platform.release()}")
            info.append(f"Architecture: {platform.architecture()[0]}")
            info.append(f"Processor: {platform.processor()}")
            info.append(f"Python: {platform.python_version()}")
            info.append(f"CPU Cores: {psutil.cpu_count()}")
            info.append(f"Memory: {psutil.virtual_memory().total // (1024**3)} GB")
            
            return "\n".join(info)
        except ImportError:
            return "System info requires 'psutil' package. Install with: pip install psutil"
        except Exception as e:
            return f"Error getting system info: {str(e)}"
    
    # Resource implementations
    async def _resource_current_directory(self) -> str:
        """Get current directory contents as a resource"""
        try:
            cwd = os.getcwd()
            items = os.listdir(cwd)
            items.sort()
            
            result = f"Current working directory: {cwd}\n\n"
            for item in items:
                item_path = os.path.join(cwd, item)
                if os.path.isdir(item_path):
                    result += f"📁 {item}/\n"
                else:
                    result += f"📄 {item}\n"
            
            return result
        except Exception as e:
            return f"Error accessing current directory: {str(e)}"
    
    def _error_response(self, request_id: str, code: int, message: str) -> Dict[str, Any]:
        """Create an error response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }


async def main():
    """Main server loop"""
    server = SimpleMCPServer()
    
    print("Simple MCP Server started. Waiting for requests...", file=sys.stderr)
    print("Send JSON-RPC requests to stdin, responses will be sent to stdout.", file=sys.stderr)
    
    while True:
        try:
            # Read request from stdin
            line = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            
            if not line:
                break
            
            # Parse JSON request
            try:
                request = json.loads(line.strip())
            except json.JSONDecodeError:
                continue
            
            # Handle request
            response = await server.handle_request(request)
            
            # Send response to stdout
            print(json.dumps(response), flush=True)
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error in main loop: {e}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())

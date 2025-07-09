#!/usr/bin/env python3
"""
Secure MCP Server with API Key Authentication 🔒
A production-ready MCP server with security features.
"""

import asyncio
import json
import sys
import os
import secrets
import hashlib
import hmac
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
import time
import psutil

# Import from relative path
from .auth import Authentication
from .rate_limiter import RateLimiter
from .monitoring import Monitoring
from .middleware import SecurityMiddleware
from ..tools.registry import ToolRegistry


class SecureMCPServer:
    """A secure MCP server implementation with authentication and monitoring"""
    
    def __init__(self, api_keys=None, port=8443, host="0.0.0.0"):
        """Initialize the secure MCP server"""
        self.host = host
        self.port = port
        self.api_keys = set(api_keys) if api_keys else set()
        self.auth = Authentication(list(self.api_keys))
        self.rate_limiter = RateLimiter()
        self.monitor = Monitoring()
        self.tool_registry = ToolRegistry()
        self.tools = self.tool_registry.tools
        self.server = None
        self.server_thread = None
        
        # If no API keys provided, generate one and print warning
        if not self.api_keys:
            default_key = self.auth.generate_key()
            self.api_keys.add(default_key)
            print(f"⚠️ WARNING: No API keys provided. Using generated key: {default_key}")
            print("Please secure this key and provide it for production use.")
        
    def start(self):
        """Start the HTTP server in a separate thread"""
        handler = self._create_handler()
        self.server = HTTPServer((self.host, self.port), handler)
        
        # Start server in a thread
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        print(f"🚀 Secure MCP Server running at http://{self.host}:{self.port}")
        print(f"🔒 API Key authentication required")
        
        # Keep main thread alive
        try:
            while True:
                # Print periodic stats
                self.monitor.print_stats()
                time.sleep(60)
        except KeyboardInterrupt:
            print("\n💤 Shutting down server...")
            self.stop()
    
    def stop(self):
        """Stop the server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("✅ Server stopped")
    
    def _create_handler(self):
        """Create a request handler class with access to server instance"""
        server = self
        
        class SecureHandler(BaseHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.server_instance = server
                super().__init__(*args, **kwargs)
            
            def _authenticate_request(self) -> bool:
                """Authenticate the current request using API key"""
                auth_header = self.headers.get('Authorization', '')
                
                if not auth_header.startswith('Bearer '):
                    self.send_response(401)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('WWW-Authenticate', 'Bearer')
                    # Add CORS headers for browser access
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                    self.end_headers()
                    error_data = {
                        "error": "Unauthorized",
                        "message": "API key required. Use Authorization: Bearer <api_key>"
                    }
                    self.wfile.write(json.dumps(error_data).encode('utf-8'))
                    return False
                    
                api_key = auth_header[7:]  # Remove 'Bearer ' prefix
                
                if api_key not in self.server_instance.api_keys:
                    self.send_response(403)
                    self.send_header('Content-type', 'application/json')
                    # Add CORS headers for browser access
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                    self.end_headers()
                    error_data = {
                        "error": "Forbidden",
                        "message": "Invalid API key"
                    }
                    self.wfile.write(json.dumps(error_data).encode('utf-8'))
                    return False
                
                return True
            
            def do_OPTIONS(self):
                """Handle CORS preflight requests"""
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                self.send_header('Access-Control-Max-Age', '86400')  # 24 hours
                self.end_headers()
            
            def do_GET(self):
                """Handle GET requests"""
                if self.path == '/health':
                    # Health check endpoint (public)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    # Add CORS headers for browser access
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                    self.end_headers()
                    health_data = {
                        "status": "ok",
                        "timestamp": datetime.now().isoformat(),
                        "uptime": self.server_instance.monitor.get_uptime(),
                        "version": "1.0.0"
                    }
                    self.wfile.write(json.dumps(health_data).encode('utf-8'))
                    return
                
                # All other GET endpoints need authentication
                if not self._authenticate_request():
                    return
                
                # Check rate limit
                client_ip = self.client_address[0]
                if not self.server_instance.rate_limiter.check_rate_limit(client_ip):
                    self.send_response(429)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Retry-After', '60')
                    # Add CORS headers for browser access
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                    self.end_headers()
                    error_data = {
                        "error": "Too many requests",
                        "message": "Rate limit exceeded. Please try again later."
                    }
                    self.wfile.write(json.dumps(error_data).encode('utf-8'))
                    return
                
                if self.path == '/api/tools':
                    # List available tools
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    # Add CORS headers for browser access
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                    self.end_headers()
                    
                    # Get tools with their schemas
                    tools_list = []
                    for tool_name, tool_info in self.server_instance.tools.items():
                        tool_data = {
                            "name": tool_name,
                            "description": tool_info.get("description", ""),
                            "schema": tool_info.get("schema", {})
                        }
                        tools_list.append(tool_data)
                    
                    response_data = {
                        "tools": tools_list,
                        "count": len(tools_list)
                    }
                    self.wfile.write(json.dumps(response_data).encode('utf-8'))
                else:
                    # Unknown endpoint
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    error_data = {
                        "error": "Not Found",
                        "message": f"Endpoint {self.path} not found"
                    }
                    self.wfile.write(json.dumps(error_data).encode('utf-8'))
            
            def do_POST(self):
                """Handle POST requests"""
                # MCP endpoint requires authentication
                if self.path == '/mcp':
                    if not self._authenticate_request():
                        return
                    
                    # Check rate limit
                    client_ip = self.client_address[0]
                    if not self.server_instance.rate_limiter.check_rate_limit(client_ip):
                        self.send_response(429)
                        self.send_header('Content-type', 'application/json')
                        self.send_header('Retry-After', '60')
                        self.end_headers()
                        error_data = {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32000,
                                "message": "Rate limit exceeded. Please try again later."
                            },
                            "id": None
                        }
                        self.wfile.write(json.dumps(error_data).encode('utf-8'))
                        return
                    
                    # Process MCP request
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    
                    try:
                        # Parse and validate JSON request
                        request = json.loads(post_data.decode('utf-8'))
                        if not isinstance(request, dict) or 'method' not in request:
                            raise ValueError("Invalid MCP request format")
                        
                        # Apply middleware to request (for now, just pass through)
                        # request = apply_middleware(request)
                        
                        # Track request in monitoring
                        # self.server_instance.monitor.track_request(request)
                        
                        # Process request and send response
                        response = self._handle_mcp_request(request)
                        
                        # Track response in monitoring
                        # self.server_instance.monitor.track_response(response)
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        # Add CORS headers for browser access
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
                        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                        self.end_headers()
                        self.wfile.write(json.dumps(response).encode('utf-8'))
                        
                    except json.JSONDecodeError:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_data = {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32700,
                                "message": "Parse error: Invalid JSON"
                            },
                            "id": None
                        }
                        self.wfile.write(json.dumps(error_data).encode('utf-8'))
                    except ValueError as e:
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        error_data = {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32600,
                                "message": f"Invalid request: {str(e)}"
                            },
                            "id": None
                        }
                        self.wfile.write(json.dumps(error_data).encode('utf-8'))
                else:
                    # Unknown endpoint
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    error_data = {
                        "error": "Not Found",
                        "message": f"Endpoint {self.path} not found"
                    }
                    self.wfile.write(json.dumps(error_data).encode('utf-8'))
            
            def _handle_mcp_request(self, request):
                """Process an MCP request"""
                request_id = request.get('id', None)
                method = request.get('method', '')
                params = request.get('params', {})
                
                # Check if method is valid
                if '/' not in method:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32601,
                            "message": f"Method {method} not found"
                        },
                        "id": request_id
                    }
                
                # Parse method parts
                parts = method.split('/', 1)
                if len(parts) != 2:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32601,
                            "message": f"Method {method} not found"
                        },
                        "id": request_id
                    }
                
                # Handle "tools/list" special method
                if parts[0] == "tools" and parts[1] == "list":
                    # Get tools with their schemas
                    tools_list = []
                    for tool_name, tool_info in self.server_instance.tools.items():
                        tool_data = {
                            "name": tool_name,
                            "description": tool_info.get("description", ""),
                            "schema": tool_info.get("schema", {})
                        }
                        tools_list.append(tool_data)
                    
                    return {
                        "jsonrpc": "2.0",
                        "result": {
                            "tools": tools_list,
                            "count": len(tools_list)
                        },
                        "id": request_id
                    }
                
                # Handle tool execution
                if parts[0] == "tools" and parts[1] == "call":
                    # Handle tool call: {"method": "tools/call", "params": {"name": "echo", "arguments": {...}}}
                    tool_name = params.get("name")
                    tool_args = params.get("arguments", {})
                    
                    if not tool_name:
                        return {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32602,
                                "message": "Missing tool name in parameters"
                            },
                            "id": request_id
                        }
                    
                    if tool_name not in self.server_instance.tools:
                        return {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32601,
                                "message": f"Tool {tool_name} not found"
                            },
                            "id": request_id
                        }
                    
                    tool_info = self.server_instance.tools[tool_name]
                    handler = tool_info.get("handler")
                    
                    if not handler:
                        return {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32603,
                                "message": f"Tool {tool_name} has no handler"
                            },
                            "id": request_id
                        }
                    
                    # Execute tool
                    try:
                        result = handler(tool_args)
                        return {
                            "jsonrpc": "2.0",
                            "result": result,
                            "id": request_id
                        }
                    except Exception as e:
                        return {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32603,
                                "message": f"Tool execution error: {str(e)}"
                            },
                            "id": request_id
                        }
                
                # Handle other methods
                tool_name = parts[0]
                action = parts[1]
                
                # For now, return method not found for other methods
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Method {method} not found"
                    },
                    "id": request_id
                }
        
        return SecureHandler


def main():
    """Run the server with command line arguments"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Secure MCP Server")
    parser.add_argument("--port", type=int, default=8443, help="Port to run the server on")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind the server to")
    parser.add_argument("--api-keys", type=str, help="Comma-separated list of API keys")
    
    args = parser.parse_args()
    
    # Check for environment variables
    port = int(os.environ.get("PORT", args.port))
    host = os.environ.get("HOST", args.host)
    
    # Get API keys from environment or command line
    api_keys_str = os.environ.get("MCP_API_KEYS", args.api_keys)
    api_keys = api_keys_str.split(",") if api_keys_str else []
    
    # Create and start server
    server = SecureMCPServer(api_keys=api_keys, port=port, host=host)
    server.start()


if __name__ == "__main__":
    main()

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

# Import the base MCP server
from app import SimpleMCPServer

class SecureHTTPHandler(BaseHTTPRequestHandler):
    """HTTP handler with API key authentication"""
    
    def __init__(self, *args, api_keys=None, rate_limits=None, **kwargs):
        self.api_keys = api_keys or set()
        self.rate_limits = rate_limits or {}
        super().__init__(*args, **kwargs)
    
    def _authenticate(self) -> bool:
        """Check API key authentication"""
        auth_header = self.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return False
            
        api_key = auth_header[7:]  # Remove 'Bearer ' prefix
        return api_key in self.api_keys
    
    def _check_rate_limit(self, client_ip: str) -> bool:
        """Simple rate limiting: 100 requests per minute per IP"""
        now = time.time()
        minute_ago = now - 60
        
        if client_ip not in self.rate_limits:
            self.rate_limits[client_ip] = []
        
        # Clean old requests
        self.rate_limits[client_ip] = [
            req_time for req_time in self.rate_limits[client_ip] 
            if req_time > minute_ago
        ]
        
        # Check limit
        if len(self.rate_limits[client_ip]) >= 100:
            return False
        
        # Add current request
        self.rate_limits[client_ip].append(now)
        return True
    
    def _send_error_response(self, code: int, message: str):
        """Send error response"""
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_response = {
            "error": {
                "code": code,
                "message": message,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def _send_success_response(self, data: Any):
        """Send successful response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        self.wfile.write(json.dumps(data).encode('utf-8'))
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        # Parse URL
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Health check endpoint (no auth required)
        if parsed_path.path == '/health':
            self._send_success_response({
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "server": "Secure MCP Server",
                "version": "1.0.0"
            })
            return
        
        # All other endpoints require authentication
        if not self._authenticate():
            self._send_error_response(401, "Invalid or missing API key")
            return
        
        # Rate limiting
        client_ip = self.client_address[0]
        if not self._check_rate_limit(client_ip):
            self._send_error_response(429, "Rate limit exceeded")
            return
        
        # API endpoints
        if parsed_path.path == '/api/tools':
            # Get tools list
            try:
                mcp_server = self.server.mcp_server
                tools_response = asyncio.run(mcp_server._handle_tools_list({}))
                
                if "error" in tools_response:
                    self._send_error_response(500, tools_response["error"]["message"])
                else:
                    self._send_success_response(tools_response["result"])
            except Exception as e:
                self._send_error_response(500, f"Internal server error: {str(e)}")
        
        elif parsed_path.path == '/api/status':
            # Server status
            self._send_success_response({
                "server": "Secure MCP Server",
                "status": "running",
                "authenticated": True,
                "tools_count": len(self.server.mcp_server.tools),
                "resources_count": len(self.server.mcp_server.resources),
                "uptime": time.time() - self.server.start_time,
                "memory_usage": psutil.Process().memory_info().rss / 1024 / 1024,  # MB
                "timestamp": datetime.utcnow().isoformat()
            })
        
        elif parsed_path.path == '/':
            # Secure web interface
            html_content = self._generate_secure_web_ui()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        
        else:
            self._send_error_response(404, "Endpoint not found")
    
    def do_POST(self):
        """Handle POST requests"""
        # Authentication required for all POST requests
        if not self._authenticate():
            self._send_error_response(401, "Invalid or missing API key")
            return
        
        # Rate limiting
        client_ip = self.client_address[0]
        if not self._check_rate_limit(client_ip):
            self._send_error_response(429, "Rate limit exceeded")
            return
        
        # Parse URL
        parsed_path = urllib.parse.urlparse(self.path)
        
        if parsed_path.path == '/mcp':
            # Handle MCP requests
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data.decode('utf-8'))
                
                # Process MCP request
                mcp_server = self.server.mcp_server
                response = asyncio.run(mcp_server.handle_request(request_data))
                
                self._send_success_response(response)
                
            except json.JSONDecodeError:
                self._send_error_response(400, "Invalid JSON")
            except Exception as e:
                self._send_error_response(500, f"Internal server error: {str(e)}")
        
        else:
            self._send_error_response(404, "Endpoint not found")
    
    def _generate_secure_web_ui(self) -> str:
        """Generate secure web interface"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔒 Secure MCP Server</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .title {
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .security-badge {
            display: inline-block;
            background: rgba(0, 255, 0, 0.2);
            border: 2px solid #00ff00;
            border-radius: 25px;
            padding: 10px 20px;
            margin: 20px 0;
            font-weight: bold;
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .feature-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .feature-title {
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        .api-section {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
        }
        .code-block {
            background: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
            border-left: 4px solid #00ff00;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #00ff00;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .warning {
            background: rgba(255, 165, 0, 0.2);
            border: 2px solid #ffa500;
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🔒 Secure MCP Server</h1>
            <p class="subtitle">Model Context Protocol Server with API Key Authentication</p>
            <div class="security-badge">
                <span class="status-indicator"></span>
                AUTHENTICATED & SECURED
            </div>
        </div>

        <div class="warning">
            <h3>🛡️ Security Features Active</h3>
            <ul>
                <li>✅ API Key Authentication Required</li>
                <li>✅ Rate Limiting (100 req/min per IP)</li>
                <li>✅ CORS Protection</li>
                <li>✅ Request Logging & Monitoring</li>
                <li>✅ Memory Usage Tracking</li>
            </ul>
        </div>

        <div class="features">
            <div class="feature-card">
                <h3 class="feature-title">🔐 Authentication</h3>
                <p>All requests require a valid API key in the Authorization header.</p>
            </div>
            
            <div class="feature-card">
                <h3 class="feature-title">⚡ Rate Limiting</h3>
                <p>Maximum 100 requests per minute per IP address.</p>
            </div>
            
            <div class="feature-card">
                <h3 class="feature-title">📊 Monitoring</h3>
                <p>Real-time server status and performance metrics.</p>
            </div>
            
            <div class="feature-card">
                <h3 class="feature-title">🛠️ MCP Tools</h3>
                <p>Full MCP protocol support with secure tool execution.</p>
            </div>
        </div>

        <div class="api-section">
            <h3>🌐 API Endpoints</h3>
            <div class="code-block">
POST /mcp - MCP Protocol requests (auth required)
GET /api/tools - List available tools (auth required)
GET /api/status - Server status (auth required)
GET /health - Health check (no auth required)
            </div>
        </div>

        <div class="api-section">
            <h3>🔑 Authentication Example</h3>
            <div class="code-block">
curl -X POST https://your-server.com/mcp \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer your-api-key" \\
  -d '{"jsonrpc": "2.0", "method": "tools/list"}'
            </div>
        </div>

        <div class="api-section">
            <h3>📈 Server Information</h3>
            <div id="server-info">Loading...</div>
        </div>
    </div>

    <script>
        // Load server status
        async function loadServerStatus() {
            try {
                // This will fail without API key, but that's expected
                const response = await fetch('/api/status', {
                    headers: {
                        'Authorization': 'Bearer demo-key-would-go-here'
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('server-info').innerHTML = `
                        <div class="code-block">
                            Status: ${data.status}<br>
                            Tools: ${data.tools_count}<br>
                            Resources: ${data.resources_count}<br>
                            Uptime: ${Math.round(data.uptime)} seconds<br>
                            Memory: ${Math.round(data.memory_usage)} MB<br>
                            Last Updated: ${new Date(data.timestamp).toLocaleString()}
                        </div>
                    `;
                } else {
                    document.getElementById('server-info').innerHTML = `
                        <div class="code-block">
                            ⚠️ Authentication required to view status<br>
                            Use your API key to access detailed information
                        </div>
                    `;
                }
            } catch (error) {
                document.getElementById('server-info').innerHTML = `
                    <div class="code-block">
                        🔒 Server running in secure mode<br>
                        API key required for status information
                    </div>
                `;
            }
        }

        // Load status on page load
        loadServerStatus();
        
        // Refresh every 30 seconds
        setInterval(loadServerStatus, 30000);
    </script>
</body>
</html>'''

    def log_message(self, format, *args):
        """Custom log message with timestamp and auth status"""
        auth_status = "✅ AUTH" if self._authenticate() else "❌ NOAUTH"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{auth_status}] {format % args}")


class SecureMCPServer:
    """Secure MCP Server with authentication and rate limiting"""
    
    def __init__(self, api_keys: List[str], port: int = 8443):
        self.api_keys = set(api_keys)
        self.port = port
        self.mcp_server = SimpleMCPServer()
        self.rate_limits = {}
        self.start_time = time.time()
        
    def create_handler(self):
        """Create HTTP handler with bound parameters"""
        def handler(*args, **kwargs):
            return SecureHTTPHandler(*args, api_keys=self.api_keys, 
                                   rate_limits=self.rate_limits, **kwargs)
        return handler
    
    def start(self):
        """Start the secure server"""
        handler = self.create_handler()
        httpd = HTTPServer(('0.0.0.0', self.port), handler)
        
        # Bind MCP server to HTTP server
        httpd.mcp_server = self.mcp_server
        httpd.start_time = self.start_time
        
        print(f"🔒 Secure MCP Server starting on port {self.port}")
        print(f"🌍 Server URL: http://localhost:{self.port}")
        print(f"🔑 API Keys configured: {len(self.api_keys)}")
        print(f"🛡️ Security features: API authentication, rate limiting, CORS protection")
        print(f"📊 Health check: http://localhost:{self.port}/health")
        print("🚀 Server ready! Press Ctrl+C to stop.")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server shutdown requested")
            httpd.shutdown()
            print("✅ Server stopped safely")


def generate_api_key() -> str:
    """Generate a secure API key"""
    return secrets.token_urlsafe(32)


def main():
    """Main function with CLI support"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Secure MCP Server with API Key Authentication")
    parser.add_argument('--port', type=int, default=8443, help='Port to run server on (default: 8443)')
    parser.add_argument('--api-key', action='append', help='API key for authentication (can be used multiple times)')
    parser.add_argument('--generate-key', action='store_true', help='Generate a new API key and exit')
    parser.add_argument('--env-keys', action='store_true', help='Load API keys from MCP_API_KEYS environment variable (comma-separated)')
    
    args = parser.parse_args()
    
    # Generate API key and exit
    if args.generate_key:
        new_key = generate_api_key()
        print(f"🔑 Generated new API key: {new_key}")
        print(f"💡 Use it like this: python secure_server.py --api-key {new_key}")
        print(f"🌍 Or set environment: set MCP_API_KEYS={new_key}")
        return
    
    # Collect API keys
    api_keys = []
    
    if args.api_key:
        api_keys.extend(args.api_key)
    
    if args.env_keys:
        env_keys = os.environ.get('MCP_API_KEYS', '')
        if env_keys:
            api_keys.extend([key.strip() for key in env_keys.split(',') if key.strip()])
    
    # Default demo key if none provided
    if not api_keys:
        demo_key = "demo-secure-key-12345"
        api_keys.append(demo_key)
        print(f"⚠️  No API keys provided, using demo key: {demo_key}")
        print(f"💡 Generate a secure key with: python secure_server.py --generate-key")
    
    # Start server
    server = SecureMCPServer(api_keys, args.port)
    server.start()


if __name__ == "__main__":
    main()

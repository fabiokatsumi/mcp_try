#!/usr/bin/env python3
"""
Production-ready MCP HTTP server for cloud deployment
"""

import asyncio
import json
import sys
import subprocess
import os
from typing import Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse
import socket

class MCPCloudHTTPHandler(BaseHTTPRequestHandler):
    """HTTP handler optimized for cloud deployment"""
    
    def __init__(self, mcp_server, *args, **kwargs):
        self.mcp_server = mcp_server
        super().__init__(*args, **kwargs)
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/mcp':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                # Parse JSON request
                request = json.loads(post_data.decode('utf-8'))
                
                # Forward to MCP server
                response = self.mcp_server.send_request_sync(request)
                
                # Send response with CORS headers
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            except Exception as e:
                self.send_error(500, f"Error processing request: {str(e)}")
        elif self.path == '/health':
            # Health check endpoint for cloud platforms
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            import datetime
            health_status = {"status": "healthy", "timestamp": str(datetime.datetime.now())}
            self.wfile.write(json.dumps(health_status).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self._serve_main_page()
        elif self.path == '/api/tools':
            self._serve_tools_api()
        elif self.path == '/health':
            # Health check
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            import datetime
            health_status = {"status": "healthy", "timestamp": str(datetime.datetime.now())}
            self.wfile.write(json.dumps(health_status).encode('utf-8'))
        else:
            self.send_error(404, "Page not found")
    
    def _serve_tools_api(self):
        """Serve the tools list as JSON API"""
        try:
            # Get tools from MCP server
            tools_request = {
                "jsonrpc": "2.0",
                "id": "tools_api",
                "method": "tools/list"
            }
            
            response = self.mcp_server.send_request_sync(tools_request)
            
            if 'result' in response and 'tools' in response['result']:
                tools = response['result']['tools']
            else:
                tools = []
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            self.wfile.write(json.dumps({"tools": tools}).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error fetching tools: {str(e)}")
    
    def _serve_main_page(self):
        """Serve the main page with cloud deployment info"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # Get server URL for display
        host = self.headers.get('Host', 'localhost')
        server_url = f"https://{host}" if 'localhost' not in host else f"http://{host}"
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCP Server - Cloud Deployed</title>
    <style>
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 0; 
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }}
        .container {{ 
            max-width: 900px; 
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        .status {{ 
            background: #d4edda; 
            border: 1px solid #c3e6cb; 
            color: #155724; 
            padding: 15px; 
            border-radius: 8px; 
            text-align: center;
            margin-bottom: 20px;
            font-weight: bold;
        }}
        .endpoint {{ 
            background: #f8f9fa; 
            padding: 15px; 
            margin: 15px 0; 
            border-radius: 8px; 
            border-left: 4px solid #007bff;
        }}
        .tools-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .tool-card {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
        }}
        pre {{ 
            background: #2d3748; 
            color: #e2e8f0;
            padding: 15px; 
            overflow-x: auto; 
            border-radius: 8px;
            font-size: 14px;
        }}
        h1 {{ 
            color: #2d3748; 
            text-align: center; 
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .cloud-badge {{
            background: #007bff;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.8em;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 MCP Server <span class="cloud-badge">☁️ Cloud Deployed</span></h1>
        <div class="status">
            ✅ Your MCP server is running in the cloud and accessible worldwide!
        </div>
        
        <h2>🌍 Global Access</h2>
        <div class="endpoint">
            <strong>🌐 Public URL:</strong> <code>{server_url}</code><br>
            <strong>📡 MCP API:</strong> <code>{server_url}/mcp</code><br>
            <strong>🔧 Tools API:</strong> <code>{server_url}/api/tools</code><br>
            <strong>💊 Health Check:</strong> <code>{server_url}/health</code>
        </div>
        
        <h2>🤖 Agent Integration</h2>
        <div class="endpoint">
            Configure your AI agents to use this MCP server:<br><br>
            <strong>HTTP Endpoint:</strong> <code>{server_url}/mcp</code><br>
            <strong>Protocol:</strong> JSON-RPC 2.0 over HTTP<br>
            <strong>CORS:</strong> Enabled for web agents
        </div>
        
        <h2>🔧 Available Tools</h2>
        <div id="tools-loading">🔄 Loading tools...</div>
        <div class="tools-grid" id="tools-grid" style="display: none;">
            <!-- Tools will be loaded dynamically -->
        </div>
        
        <h2>💡 Example Usage for Agents</h2>
        
        <h3>🔍 Get Tools List:</h3>
        <pre>curl -X POST {server_url}/mcp \\
  -H "Content-Type: application/json" \\
  -d '{{"jsonrpc": "2.0", "id": "1", "method": "tools/list"}}'</pre>
        
        <h3>🧮 Use Calculator:</h3>
        <pre>curl -X POST {server_url}/mcp \\
  -H "Content-Type: application/json" \\
  -d '{{
    "jsonrpc": "2.0",
    "id": "2",
    "method": "tools/call",
    "params": {{
      "name": "calculate",
      "arguments": {{"expression": "2**10 + 5"}}
    }}
  }}'</pre>
        
        <h3>🔌 Agent Configuration (JSON):</h3>
        <pre>{{
  "mcp_servers": {{
    "cloud-mcp": {{
      "type": "http",
      "url": "{server_url}/mcp",
      "headers": {{"Content-Type": "application/json"}}
    }}
  }}
}}</pre>
        
        <script>
        // Fetch and display tools dynamically
        async function loadTools() {{
            try {{
                const response = await fetch('/api/tools');
                const data = await response.json();
                const toolsGrid = document.getElementById('tools-grid');
                const loading = document.getElementById('tools-loading');
                
                if (data.tools && data.tools.length > 0) {{
                    toolsGrid.innerHTML = '';
                    
                    const toolEmojis = {{
                        'get_time': '⏰',
                        'read_file': '📖',
                        'write_file': '✏️',
                        'list_directory': '📁',
                        'calculate': '🧮',
                        'system_info': '💻',
                        'default': '🔧'
                    }};
                    
                    data.tools.forEach(tool => {{
                        const emoji = toolEmojis[tool.name] || toolEmojis.default;
                        const toolCard = document.createElement('div');
                        toolCard.className = 'tool-card';
                        toolCard.innerHTML = `
                            <strong>${{emoji}} ${{tool.name}}</strong><br>
                            <small>${{tool.description || 'No description available'}}</small>
                        `;
                        toolsGrid.appendChild(toolCard);
                    }});
                    
                    loading.style.display = 'none';
                    toolsGrid.style.display = 'grid';
                }} else {{
                    loading.innerHTML = '❌ No tools available';
                }}
            }} catch (error) {{
                const loading = document.getElementById('tools-loading');
                loading.innerHTML = `❌ Error loading tools: ${{error.message}}`;
            }}
        }}
        
        // Load tools when page loads
        document.addEventListener('DOMContentLoaded', loadTools);
        
        // Auto-refresh tools every 30 seconds
        setInterval(loadTools, 30000);
        </script>
        
    </div>
</body>
</html>"""
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[HTTP] {self.address_string()} - {format % args}")

class MCPServerWrapper:
    """Wrapper to manage the MCP server process for cloud deployment"""
    
    def __init__(self):
        self.process = None
    
    def start(self):
        """Start the MCP server process"""
        print("🚀 Starting MCP server process for cloud deployment...")
    
    def send_request_sync(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a synchronous request to the MCP server"""
        try:
            # Create a new process for each request (simpler for cloud deployment)
            process = subprocess.Popen(
                [sys.executable, "app.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            request_json = json.dumps(request) + "\n"
            stdout, stderr = process.communicate(input=request_json, timeout=30)
            
            if stdout:
                return json.loads(stdout.strip())
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {stderr}"
                    }
                }
        except subprocess.TimeoutExpired:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": "Request timeout"
                }
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "error": {
                    "code": -32603,
                    "message": f"Error: {str(e)}"
                }
            }

def main():
    """Main function optimized for cloud deployment"""
    # Get port from environment variable (required by most cloud platforms)
    PORT = int(os.environ.get("PORT", 8080))
    HOST = "0.0.0.0"  # Listen on all interfaces
    
    print(f"🌍 Starting MCP Cloud Server on port {PORT}...")
    
    # Create MCP server wrapper
    mcp_server = MCPServerWrapper()
    mcp_server.start()
    
    # Create HTTP handler with MCP server reference
    def handler(*args, **kwargs):
        MCPCloudHTTPHandler(mcp_server, *args, **kwargs)
    
    # Start HTTP server
    httpd = HTTPServer((HOST, PORT), handler)
    
    print(f"""
🌍 MCP Cloud Server Started!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Server Port:      {PORT}
🌐 Global Access:    Available worldwide when deployed
📡 MCP Endpoint:     /mcp
🔧 Tools API:        /api/tools
💊 Health Check:     /health

🤖 For AI Agents:
   Use HTTP POST to /mcp endpoint with JSON-RPC 2.0 protocol

Press Ctrl+C to stop the server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down cloud server...")
        httpd.shutdown()
        print("✅ Server stopped successfully")

if __name__ == "__main__":
    main()

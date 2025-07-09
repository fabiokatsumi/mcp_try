#!/usr/bin/env python3
"""
HTTP wrapper for the MCP server to make it accessible over LAN
"""

import asyncio
import json
import sys
import subprocess
from typing import Dict, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import urllib.parse
import socket

class MCPHTTPHandler(BaseHTTPRequestHandler):
    """HTTP handler that forwards requests to the MCP server"""
    
    def __init__(self, mcp_server, *args, **kwargs):
        self.mcp_server = mcp_server
        super().__init__(*args, **kwargs)
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
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
                
                # Send response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # Enable CORS
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            except Exception as e:
                self.send_error(500, f"Error processing request: {str(e)}")
        else:
            self.send_error(404, "Endpoint not found")
    
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self._serve_main_page()
        elif self.path == '/api/tools':
            self._serve_tools_api()
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
            
            import json
            self.wfile.write(json.dumps({"tools": tools}).encode('utf-8'))
            
        except Exception as e:
            self.send_error(500, f"Error fetching tools: {str(e)}")
    
    def _serve_main_page(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MCP Server</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            margin: 40px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        .container { 
            max-width: 900px; 
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .endpoint { 
            background: #f8f9fa; 
            padding: 15px; 
            margin: 15px 0; 
            border-radius: 8px; 
            border-left: 4px solid #007bff;
        }
        pre { 
            background: #2d3748; 
            color: #e2e8f0;
            padding: 15px; 
            overflow-x: auto; 
            border-radius: 8px;
            font-size: 14px;
        }
        h1 { 
            color: #2d3748; 
            text-align: center; 
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        h2 { 
            color: #4a5568; 
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 8px;
        }
        .status { 
            background: #d4edda; 
            border: 1px solid #c3e6cb; 
            color: #155724; 
            padding: 10px; 
            border-radius: 5px; 
            text-align: center;
            margin-bottom: 20px;
        }
        .tools-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .tool-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #28a745;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 MCP Server</h1>
        <div class="status">
            ✅ Your MCP server is running and accessible over the network!
        </div>
        
        <h2>📡 Available Endpoints</h2>
        <div class="endpoint">
            <strong>POST /mcp</strong> - Send MCP requests to the server
        </div>
        
        <h2>🔧 Available Tools</h2>
        <div id="tools-loading">🔄 Loading tools...</div>
        <div class="tools-grid" id="tools-grid" style="display: none;">
            <!-- Tools will be loaded dynamically -->
        </div>
        
        <script>
        // Fetch and display tools dynamically
        async function loadTools() {
            try {
                const response = await fetch('/api/tools');
                const data = await response.json();
                const toolsGrid = document.getElementById('tools-grid');
                const loading = document.getElementById('tools-loading');
                
                if (data.tools && data.tools.length > 0) {
                    toolsGrid.innerHTML = '';
                    
                    // Define emoji mapping for tools
                    const toolEmojis = {
                        'get_time': '⏰',
                        'read_file': '📖',
                        'write_file': '✏️',
                        'list_directory': '📁',
                        'calculate': '🧮',
                        'system_info': '💻',
                        'default': '🔧'
                    };
                    
                    data.tools.forEach(tool => {
                        const emoji = toolEmojis[tool.name] || toolEmojis.default;
                        const toolCard = document.createElement('div');
                        toolCard.className = 'tool-card';
                        toolCard.innerHTML = `
                            <strong>${emoji} ${tool.name}</strong><br>
                            <small>${tool.description || 'No description available'}</small>
                        `;
                        toolsGrid.appendChild(toolCard);
                    });
                    
                    loading.style.display = 'none';
                    toolsGrid.style.display = 'grid';
                } else {
                    loading.innerHTML = '❌ No tools available';
                }
            } catch (error) {
                const loading = document.getElementById('tools-loading');
                loading.innerHTML = `❌ Error loading tools: ${error.message}`;
            }
        }
        
        // Load tools when page loads
        document.addEventListener('DOMContentLoaded', loadTools);
        
        // Auto-refresh tools every 30 seconds
        setInterval(loadTools, 30000);
        </script>
        
        <h2>💡 Quick Test Examples</h2>
        
        <h3>🔍 List Available Tools:</h3>
        <pre>curl -X POST http://""" + self.get_server_ip() + """:8080/mcp \\
  -H "Content-Type: application/json" \\
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/list"
  }'</pre>
        
        <h3>⏰ Get Current Time:</h3>
        <pre>curl -X POST http://""" + self.get_server_ip() + """:8080/mcp \\
  -H "Content-Type: application/json" \\
  -d '{
    "jsonrpc": "2.0",
    "id": "2",
    "method": "tools/call",
    "params": {
      "name": "get_time",
      "arguments": {}
    }
  }'</pre>
        
        <h3>📁 List Directory:</h3>
        <pre>curl -X POST http://""" + self.get_server_ip() + """:8080/mcp \\
  -H "Content-Type: application/json" \\
  -d '{
    "jsonrpc": "2.0",
    "id": "3",
    "method": "tools/call",
    "params": {
      "name": "list_directory",
      "arguments": {"directory_path": "."}
    }
  }'</pre>
        
        <h2>🌐 Network Access</h2>
        <div class="endpoint">
            <strong>Local:</strong> <code>http://localhost:8080</code><br>
            <strong>LAN:</strong> <code>http://""" + self.get_server_ip() + """:8080</code><br>
            <strong>API:</strong> <code>http://""" + self.get_server_ip() + """:8080/mcp</code>
        </div>
        
    </div>
</body>
</html>"""
            self.wfile.write(html.encode('utf-8'))
    
    def get_server_ip(self):
        """Get the server's IP address"""
        try:
            # Connect to a remote address to determine local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "localhost"
    
    def log_message(self, format, *args):
        """Override to customize logging"""
        print(f"[HTTP] {self.address_string()} - {format % args}")

class MCPServerWrapper:
    """Wrapper to manage the MCP server process"""
    
    def __init__(self):
        self.process = None
    
    def start(self):
        """Start the MCP server process"""
        self.process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("🚀 MCP server process started")
    
    def send_request_sync(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Send a synchronous request to the MCP server"""
        if not self.process:
            raise RuntimeError("MCP server not started")
        
        try:
            # Create a new process for each request (simpler but less efficient)
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
    
    def stop(self):
        """Stop the MCP server process"""
        if self.process:
            self.process.terminate()
            self.process.wait()

def get_local_ip():
    """Get the local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    """Main function to start the HTTP server"""
    HOST = "0.0.0.0"  # Listen on all interfaces
    PORT = 8080
    
    # Create MCP server wrapper
    mcp_server = MCPServerWrapper()
    mcp_server.start()
    
    # Create HTTP handler with MCP server reference
    def handler(*args, **kwargs):
        MCPHTTPHandler(mcp_server, *args, **kwargs)
    
    # Start HTTP server
    httpd = HTTPServer((HOST, PORT), handler)
    
    local_ip = get_local_ip()
    
    print(f"""
🌐 MCP HTTP Server Started!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Local Access:     http://localhost:{PORT}
🌍 Network Access:   http://{local_ip}:{PORT}
📡 API Endpoint:     http://{local_ip}:{PORT}/mcp

💡 Quick Test:
curl -X POST http://{local_ip}:{PORT}/mcp \\
  -H "Content-Type: application/json" \\
  -d '{{"jsonrpc": "2.0", "id": "1", "method": "tools/list"}}'

Press Ctrl+C to stop the server
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down server...")
        httpd.shutdown()
        mcp_server.stop()
        print("✅ Server stopped successfully")

if __name__ == "__main__":
    main()

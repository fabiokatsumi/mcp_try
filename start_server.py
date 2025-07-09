#!/usr/bin/env python3
"""
Start the MCP server with tools loaded.
"""

import sys
import os
import argparse

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.server.secure_server import SecureMCPServer

def main():
    parser = argparse.ArgumentParser(description='Start the Secure MCP Server')
    parser.add_argument('--api-keys', type=str, required=True, help='Comma-separated API keys')
    parser.add_argument('--port', type=int, default=8080, help='Port to run the server on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
    
    args = parser.parse_args()
    
    # Parse API keys
    api_keys = [key.strip() for key in args.api_keys.split(',')]
    
    print(f"🚀 Starting MCP Server...")
    print(f"   Host: {args.host}")
    print(f"   Port: {args.port}")
    print(f"   API Keys: {len(api_keys)} key(s) configured")
    
    # Create and start server
    server = SecureMCPServer(api_keys=api_keys, port=args.port, host=args.host)
    
    try:
        server.start()
        print(f"✅ Server started at http://{args.host}:{args.port}")
        print(f"🔧 Available tools: {list(server.tools.keys())}")
        print(f"🔑 Health check: http://{args.host}:{args.port}/health")
        print(f"📋 API tools: http://{args.host}:{args.port}/api/tools (requires auth)")
        print(f"🎯 MCP endpoint: http://{args.host}:{args.port}/mcp (requires auth)")
        print("\n🛑 Press Ctrl+C to stop the server")
        
        # Keep the server running
        while True:
            try:
                import time
                time.sleep(1)
            except KeyboardInterrupt:
                break
                
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
    finally:
        server.stop()
        print("✅ Server stopped")

if __name__ == "__main__":
    main()

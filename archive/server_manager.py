#!/usr/bin/env python3
"""
Quick server manager for MCP LAN access
"""

import subprocess
import sys
import os
import signal
import time

def get_server_info():
    """Display server information"""
    print("""
🌐 MCP Server LAN Manager
========================

This script helps you manage your MCP server for LAN access.

Available commands:
  1. start    - Start the HTTP server
  2. test     - Test the server
  3. status   - Check if server is running
  4. stop     - Stop the server (if running in background)

""")

def start_server():
    """Start the HTTP server"""
    print("🚀 Starting MCP HTTP Server...")
    try:
        # Start the server
        subprocess.run([sys.executable, "http_server.py"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def test_server():
    """Test the server"""
    print("🧪 Testing MCP Server...")
    try:
        subprocess.run([sys.executable, "test_lan_client.py"])
    except Exception as e:
        print(f"❌ Error testing server: {e}")

def main():
    """Main function"""
    if len(sys.argv) < 2:
        get_server_info()
        return
    
    command = sys.argv[1].lower()
    
    if command == "start":
        start_server()
    elif command == "test":
        test_server()
    elif command == "status":
        print("📊 Checking server status...")
        test_server()
    elif command == "help":
        get_server_info()
    else:
        print(f"❌ Unknown command: {command}")
        get_server_info()

if __name__ == "__main__":
    main()

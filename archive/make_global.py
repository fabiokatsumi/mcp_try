#!/usr/bin/env python3
"""
Quick tunnel solution using ngrok for immediate global access
"""

import subprocess
import sys
import os
import requests
import json
import time

def install_ngrok():
    """Instructions to install ngrok"""
    print("""
🌍 Ngrok Setup Instructions:

1. Go to https://ngrok.com/signup
2. Sign up for free account
3. Download ngrok for your platform
4. Install and authenticate:
   
   Windows:
   - Download ngrok.exe
   - Put it in your PATH or project folder
   - Run: ngrok authtoken YOUR_TOKEN
   
   Mac/Linux:
   - brew install ngrok (Mac)
   - sudo apt install ngrok (Ubuntu)
   - Run: ngrok authtoken YOUR_TOKEN

5. Run this script again
""")

def start_tunnel(port=8080):
    """Start ngrok tunnel"""
    try:
        # Start ngrok tunnel
        print(f"🚀 Starting ngrok tunnel on port {port}...")
        
        # Start ngrok in background
        ngrok_process = subprocess.Popen(
            ["ngrok", "http", str(port), "--log=stdout"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a moment for ngrok to start
        time.sleep(3)
        
        # Get tunnel URL from ngrok API
        try:
            response = requests.get("http://localhost:4040/api/tunnels")
            data = response.json()
            
            if data.get("tunnels"):
                tunnel_url = data["tunnels"][0]["public_url"]
                print(f"""
🌍 SUCCESS! Your MCP server is now globally accessible!

📍 Public URL: {tunnel_url}
📡 MCP Endpoint: {tunnel_url}/mcp
🔧 Tools API: {tunnel_url}/api/tools
💊 Health Check: {tunnel_url}/health

🤖 For AI Agents:
   Use: {tunnel_url}/mcp

🌐 Web Interface:
   Open: {tunnel_url}

⚠️  This tunnel will stay active as long as this script runs.
   Press Ctrl+C to stop the tunnel.
""")
                
                # Keep the tunnel alive
                try:
                    ngrok_process.wait()
                except KeyboardInterrupt:
                    print("\n🛑 Stopping tunnel...")
                    ngrok_process.terminate()
                    print("✅ Tunnel stopped")
            else:
                print("❌ Failed to get tunnel URL. Check ngrok installation.")
        except requests.exceptions.RequestException:
            print("❌ Failed to connect to ngrok API. Is ngrok running?")
            
    except FileNotFoundError:
        print("❌ ngrok not found in PATH")
        install_ngrok()
    except Exception as e:
        print(f"❌ Error starting tunnel: {e}")

def main():
    """Main function"""
    print("🌍 MCP Server Global Tunnel")
    print("=" * 40)
    
    # Check if HTTP server is running
    try:
        response = requests.get("http://localhost:8080/health", timeout=2)
        print("✅ Local MCP server is running")
    except:
        print("❌ Local MCP server not running. Please start it first:")
        print("   python http_server.py")
        return
    
    start_tunnel()

if __name__ == "__main__":
    main()

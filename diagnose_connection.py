#!/usr/bin/env python3
"""
MCP Server Connection Diagnostic Tool
Tests various connection methods to help troubleshoot browser issues
"""

import requests
import json
import socket
import time
import subprocess
import sys
from urllib.parse import urlparse

def check_port_open(host, port):
    """Check if a port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def test_url(url, description=""):
    """Test a URL and return results"""
    print(f"\n🔍 Testing {description}: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"   ✅ Status: {response.status_code}")
        print(f"   📊 Headers: {dict(response.headers)}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            data = response.json()
            print(f"   📄 Response: {json.dumps(data, indent=2)}")
        else:
            print(f"   📄 Response: {response.text[:200]}...")
        
        return True, response
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ Connection Error: {e}")
        return False, None
    except requests.exceptions.Timeout as e:
        print(f"   ⏰ Timeout Error: {e}")
        return False, None
    except Exception as e:
        print(f"   💥 Error: {e}")
        return False, None

def get_local_ips():
    """Get local IP addresses"""
    ips = []
    try:
        # Get hostname
        hostname = socket.gethostname()
        
        # Get local IP
        local_ip = socket.gethostbyname(hostname)
        ips.append(local_ip)
        
        # Get all network interfaces (Windows/Linux compatible)
        try:
            import subprocess
            if sys.platform.startswith('win'):
                result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'IPv4' in line and ':' in line:
                        ip = line.split(':')[1].strip()
                        if ip and ip != '127.0.0.1' and ip not in ips:
                            ips.append(ip)
            else:
                result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
                for ip in result.stdout.split():
                    if ip and ip != '127.0.0.1' and ip not in ips:
                        ips.append(ip)
        except:
            pass
    except:
        pass
    
    return ips

def main():
    print("🔒 MCP Server Connection Diagnostic Tool")
    print("=" * 50)
    
    # Default configuration
    port = 8080
    api_key = "LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4"
    
    # Test configurations
    hosts_to_test = ['localhost', '127.0.0.1']
    
    # Add local IPs
    local_ips = get_local_ips()
    hosts_to_test.extend(local_ips)
    
    print(f"🌐 Testing hosts: {hosts_to_test}")
    print(f"🔑 Using API key: {api_key[:20]}...")
    
    # Check port availability
    print(f"\n🔌 Checking port {port} availability...")
    for host in hosts_to_test:
        is_open = check_port_open(host, port)
        status = "✅ OPEN" if is_open else "❌ CLOSED"
        print(f"   {host}:{port} - {status}")
    
    # Test health endpoints
    print(f"\n🏥 Testing health endpoints...")
    working_urls = []
    
    for host in hosts_to_test:
        url = f"http://{host}:{port}/health"
        success, response = test_url(url, f"Health check ({host})")
        if success:
            working_urls.append((host, url))
    
    if not working_urls:
        print("\n❌ No working URLs found!")
        print("\n🔧 Troubleshooting steps:")
        print("1. Make sure server is running: python start_server.py --api-keys YOUR_KEY")
        print("2. Check firewall settings")
        print("3. Try a different port: python start_server.py --api-keys YOUR_KEY --port 8081")
        return
    
    print(f"\n✅ Found {len(working_urls)} working URL(s)!")
    
    # Test authenticated endpoints
    print(f"\n🔐 Testing authenticated endpoints...")
    
    for host, base_url in working_urls:
        # Test tools endpoint
        tools_url = f"http://{host}:{port}/api/tools"
        print(f"\n🔧 Testing tools endpoint: {tools_url}")
        
        try:
            response = requests.get(tools_url, 
                                  headers={'Authorization': f'Bearer {api_key}'}, 
                                  timeout=10)
            print(f"   ✅ Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   📊 Tools found: {len(data.get('tools', []))}")
                if data.get('tools'):
                    for tool in data['tools']:
                        print(f"      - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
            else:
                print(f"   📄 Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Test MCP endpoint
        mcp_url = f"http://{host}:{port}/mcp"
        print(f"\n📡 Testing MCP endpoint: {mcp_url}")
        
        mcp_request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 1
        }
        
        try:
            response = requests.post(mcp_url,
                                   json=mcp_request,
                                   headers={'Authorization': f'Bearer {api_key}'},
                                   timeout=10)
            print(f"   ✅ Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   📊 MCP Response: {json.dumps(data, indent=2)}")
            else:
                print(f"   📄 Response: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Browser recommendations
    print(f"\n🌐 Browser Testing Recommendations:")
    print(f"   Best URLs to try in browser:")
    for host, url in working_urls:
        print(f"   • {url}")
    
    print(f"\n📋 Browser JavaScript test code:")
    for host, url in working_urls:
        print(f"""
   // Test {host}
   fetch('{url}')
     .then(r => r.json())
     .then(console.log)
     .catch(console.error);
        """)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Diagnostic stopped by user")
    except Exception as e:
        print(f"\n💥 Diagnostic failed: {e}")

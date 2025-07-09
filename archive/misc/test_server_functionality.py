#!/usr/bin/env python3
"""
Test script to verify the secure server functionality
"""

import sys
sys.path.append('.')

import time
import threading
import requests
from src.server.secure_server import SecureMCPServer

def test_server():
    """Test the secure server functionality"""
    print("🧪 Starting Secure Server Test")
    print("=" * 50)
    
    # Test 1: Server instantiation
    try:
        server = SecureMCPServer(api_keys=['test-api-key-123'], port=8444)
        print("✅ Server instantiated successfully")
    except Exception as e:
        print(f"❌ Server instantiation failed: {e}")
        return False
    
    # Test 2: Server startup
    try:
        # Start server in background
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()
        
        # Give server time to start
        time.sleep(2)
        print("✅ Server started successfully")
        
        # Test 3: Health check endpoint
        try:
            response = requests.get('http://localhost:8444/health', timeout=5)
            if response.status_code == 200:
                print("✅ Health check endpoint working")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Health check failed with status: {response.status_code}")
        except Exception as e:
            print(f"❌ Health check request failed: {e}")
        
        # Test 4: Authentication test
        try:
            response = requests.get(
                'http://localhost:8444/api/tools',
                headers={'Authorization': 'Bearer test-api-key-123'},
                timeout=5
            )
            if response.status_code == 200:
                print("✅ Authentication working")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Authentication test failed with status: {response.status_code}")
        except Exception as e:
            print(f"❌ Authentication request failed: {e}")
        
        # Test 5: Invalid authentication test
        try:
            response = requests.get(
                'http://localhost:8444/api/tools',
                headers={'Authorization': 'Bearer invalid-key'},
                timeout=5
            )
            if response.status_code == 403:
                print("✅ Invalid authentication properly rejected")
            else:
                print(f"⚠️ Invalid auth returned unexpected status: {response.status_code}")
        except Exception as e:
            print(f"❌ Invalid auth test failed: {e}")
        
        # Test 6: MCP endpoint test
        try:
            response = requests.post(
                'http://localhost:8444/mcp',
                headers={
                    'Authorization': 'Bearer test-api-key-123',
                    'Content-Type': 'application/json'
                },
                json={"jsonrpc": "2.0", "id": "1", "method": "tools/list"},
                timeout=5
            )
            if response.status_code == 200:
                print("✅ MCP endpoint working")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ MCP endpoint failed with status: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ MCP endpoint test failed: {e}")
        
        # Stop server
        server.stop()
        print("✅ Server stopped successfully")
        
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        return False
    
    print("\n🎉 All tests completed!")
    return True

if __name__ == "__main__":
    test_server()

#!/usr/bin/env python3
"""
Simple test for MCP server
"""

import json
import subprocess
import sys

def test_basic_functionality():
    """Test basic MCP server functionality"""
    
    # Test 1: Start server and send a simple request
    print("Testing MCP server...")
    
    try:
        # Start the server process
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        # Send request
        request_json = json.dumps(init_request) + "\n"
        stdout, stderr = process.communicate(input=request_json, timeout=5)
        
        print(f"Return code: {process.returncode}")
        print(f"Stdout: {stdout}")
        print(f"Stderr: {stderr}")
        
        if stdout:
            try:
                response = json.loads(stdout.strip())
                print(f"Parsed response: {json.dumps(response, indent=2)}")
                print("✅ Server responded correctly!")
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse response: {e}")
        else:
            print("❌ No response received")
            
    except subprocess.TimeoutExpired:
        print("❌ Server timed out")
        process.kill()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_basic_functionality()

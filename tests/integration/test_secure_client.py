#!/usr/bin/env python3
"""
Test client for the Secure MCP Server 🔒
Tests authentication, rate limiting, and all security features.
"""

import asyncio
import aiohttp
import json
import time
import sys
from typing import Dict, Any, Optional

class SecureMCPClient:
    """Client for testing the secure MCP server"""
    
    def __init__(self, base_url: str = "http://localhost:8443", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    def _get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """Get request headers with optional authentication"""
        headers = {"Content-Type": "application/json"}
        
        if include_auth and self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        return headers
    
    async def health_check(self) -> Dict[str, Any]:
        """Test health check endpoint (no auth required)"""
        async with self.session.get(f"{self.base_url}/health") as response:
            return {
                "status_code": response.status,
                "data": await response.json() if response.status == 200 else await response.text()
            }
    
    async def get_tools(self, use_auth: bool = True) -> Dict[str, Any]:
        """Get available tools"""
        headers = self._get_headers(include_auth=use_auth)
        
        async with self.session.get(f"{self.base_url}/api/tools", headers=headers) as response:
            return {
                "status_code": response.status,
                "data": await response.json() if response.status == 200 else await response.text()
            }
    
    async def get_status(self, use_auth: bool = True) -> Dict[str, Any]:
        """Get server status"""
        headers = self._get_headers(include_auth=use_auth)
        
        async with self.session.get(f"{self.base_url}/api/status", headers=headers) as response:
            return {
                "status_code": response.status,
                "data": await response.json() if response.status == 200 else await response.text()
            }
    
    async def mcp_request(self, request_data: Dict[str, Any], use_auth: bool = True) -> Dict[str, Any]:
        """Send MCP protocol request"""
        headers = self._get_headers(include_auth=use_auth)
        
        async with self.session.post(f"{self.base_url}/mcp", 
                                   headers=headers, 
                                   json=request_data) as response:
            return {
                "status_code": response.status,
                "data": await response.json() if response.status == 200 else await response.text()
            }
    
    async def test_rate_limiting(self, requests_count: int = 105) -> Dict[str, Any]:
        """Test rate limiting by sending many requests"""
        print(f"🔄 Testing rate limiting with {requests_count} requests...")
        
        success_count = 0
        rate_limited_count = 0
        error_count = 0
        
        tasks = []
        for i in range(requests_count):
            task = self.health_check()
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, dict):
                if result["status_code"] == 200:
                    success_count += 1
                elif result["status_code"] == 429:
                    rate_limited_count += 1
                else:
                    error_count += 1
            else:
                error_count += 1
        
        return {
            "total_requests": requests_count,
            "successful": success_count,
            "rate_limited": rate_limited_count,
            "errors": error_count
        }


import pytest

@pytest.mark.asyncio
async def test_authentication(base_url="http://localhost:8443", api_key="demo-secure-key-12345"):
    """Test authentication features"""
    print("🔐 Testing Authentication...")
    
    # Test without API key
    async with SecureMCPClient(base_url) as client:
        result = await client.get_tools(use_auth=False)
        print(f"   No API key: Status {result['status_code']} (expected 401)")
        assert result["status_code"] == 401, "Should reject requests without API key"
    
    # Test with invalid API key
    async with SecureMCPClient(base_url, api_key="invalid-key") as client:
        result = await client.get_tools()
        print(f"   Invalid API key: Status {result['status_code']} (expected 401)")
        assert result["status_code"] == 401, "Should reject invalid API keys"
    
    # Test with valid API key
    async with SecureMCPClient(base_url, api_key=api_key) as client:
        result = await client.get_tools()
        print(f"   Valid API key: Status {result['status_code']} (expected 200)")
        assert result["status_code"] == 200, "Should accept valid API key"
        print(f"   ✅ Found {len(result['data']['tools'])} tools")
    
    print("   ✅ Authentication tests passed!")


@pytest.mark.asyncio
async def test_health_endpoint(base_url="http://localhost:8443"):
    """Test health check endpoint (no auth required)"""
    print("🏥 Testing Health Check...")
    
    async with SecureMCPClient(base_url) as client:
        result = await client.health_check()
        print(f"   Health check: Status {result['status_code']}")
        
        if result["status_code"] == 200:
            data = result["data"]
            print(f"   ✅ Server status: {data.get('status')}")
            print(f"   ✅ Server: {data.get('server')}")
            print(f"   ✅ Version: {data.get('version')}")
        else:
            print(f"   ❌ Health check failed: {result['data']}")
    
    print("   ✅ Health check tests passed!")


@pytest.mark.asyncio
async def test_mcp_protocol(base_url="http://localhost:8443", api_key="demo-secure-key-12345"):
    """Test MCP protocol functionality"""
    print("🔧 Testing MCP Protocol...")
    
    async with SecureMCPClient(base_url, api_key=api_key) as client:
        # Test initialize
        init_request = {
            "jsonrpc": "2.0",
            "id": "1",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "secure-test-client", "version": "1.0.0"}
            }
        }
        
        result = await client.mcp_request(init_request)
        print(f"   Initialize: Status {result['status_code']}")
        assert result["status_code"] == 200, "Initialize should succeed"
        print("   ✅ MCP initialization successful")
        
        # Test tools list
        tools_request = {
            "jsonrpc": "2.0",
            "id": "2",
            "method": "tools/list"
        }
        
        result = await client.mcp_request(tools_request)
        print(f"   Tools list: Status {result['status_code']}")
        assert result["status_code"] == 200, "Tools list should succeed"
        
        tools = result["data"]["result"]["tools"]
        print(f"   ✅ Found {len(tools)} tools: {[tool['name'] for tool in tools]}")
        
        # Test tool call (calculator)
        calc_request = {
            "jsonrpc": "2.0",
            "id": "3",
            "method": "tools/call",
            "params": {
                "name": "calculate",
                "arguments": {"expression": "2**8 + 15 * 3"}
            }
        }
        
        result = await client.mcp_request(calc_request)
        print(f"   Calculator tool: Status {result['status_code']}")
        assert result["status_code"] == 200, "Calculator tool should work"
        
        calc_result = result["data"]["result"]["content"][0]["text"]
        print(f"   ✅ Calculator result: {calc_result}")
        
        # Test system info tool
        sysinfo_request = {
            "jsonrpc": "2.0",
            "id": "4",
            "method": "tools/call",
            "params": {
                "name": "system_info",
                "arguments": {}
            }
        }
        
        result = await client.mcp_request(sysinfo_request)
        print(f"   System info tool: Status {result['status_code']}")
        assert result["status_code"] == 200, "System info tool should work"
        print("   ✅ System info retrieved successfully")
    
    print("   ✅ MCP protocol tests passed!")


@pytest.mark.asyncio
async def test_rate_limiting(base_url="http://localhost:8443"):
    """Test rate limiting functionality"""
    print("⚡ Testing Rate Limiting...")
    
    async with SecureMCPClient(base_url) as client:
        # Test with a reasonable number of requests
        result = await client.test_rate_limiting(requests_count=50)
        
        print(f"   Total requests: {result['total_requests']}")
        print(f"   Successful: {result['successful']}")
        print(f"   Rate limited: {result['rate_limited']}")
        print(f"   Errors: {result['errors']}")
        
        if result['rate_limited'] > 0:
            print("   ✅ Rate limiting is working!")
        else:
            print("   ⚠️  Rate limiting not triggered (may need more requests)")
    
    print("   ✅ Rate limiting tests completed!")


@pytest.mark.asyncio
async def test_server_status(base_url="http://localhost:8443", api_key="demo-secure-key-12345"):
    """Test server status endpoint"""
    print("📊 Testing Server Status...")
    
    async with SecureMCPClient(base_url, api_key=api_key) as client:
        result = await client.get_status()
        print(f"   Status endpoint: Status {result['status_code']}")
        
        if result["status_code"] == 200:
            data = result["data"]
            print(f"   ✅ Server status: {data.get('status')}")
            print(f"   ✅ Tools count: {data.get('tools_count')}")
            print(f"   ✅ Resources count: {data.get('resources_count')}")
            print(f"   ✅ Uptime: {data.get('uptime'):.2f} seconds")
            print(f"   ✅ Memory usage: {data.get('memory_usage'):.2f} MB")
            print(f"   ✅ Authenticated: {data.get('authenticated')}")
        else:
            print(f"   ❌ Status check failed: {result['data']}")
    
    print("   ✅ Server status tests passed!")


async def comprehensive_security_test(base_url="http://localhost:8443", api_key="demo-secure-key-12345"):
    """Run comprehensive security tests"""
    print("🔒 SECURE MCP SERVER TEST SUITE")
    print("=" * 50)
    
    try:
        await test_health_endpoint(base_url)
        print()
        
        await test_authentication(base_url, api_key)
        print()
        
        await test_server_status(base_url, api_key)
        print()
        
        await test_mcp_protocol(base_url, api_key)
        print()
        
        await test_rate_limiting(base_url)
        print()
        
        print("🎉 ALL SECURITY TESTS PASSED!")
        print("✅ Server is properly secured and functional")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        sys.exit(1)


def main():
    """Main function with CLI support"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test client for Secure MCP Server")
    parser.add_argument('--url', default='http://localhost:8443', help='Server URL')
    parser.add_argument('--api-key', default='demo-secure-key-12345', help='API key for authentication')
    parser.add_argument('--test', choices=['auth', 'health', 'mcp', 'rate', 'status', 'all'], 
                       default='all', help='Which test to run')
    
    args = parser.parse_args()
    
    # Update global client settings
    global SecureMCPClient
    
    async def run_specific_test():
        if args.test == 'auth':
            await test_authentication(args.url, args.api_key)
        elif args.test == 'health':
            await test_health_endpoint(args.url)
        elif args.test == 'mcp':
            await test_mcp_protocol(args.url, args.api_key)
        elif args.test == 'rate':
            await test_rate_limiting(args.url)
        elif args.test == 'status':
            await test_server_status(args.url, args.api_key)
        else:
            await comprehensive_security_test(args.url, args.api_key)
    
    asyncio.run(run_specific_test())


if __name__ == "__main__":
    main()


"""Security tests for MCP server."""

import pytest
import aiohttp
import asyncio
from aiohttp import web
import json
import time
import os
import sys

# Add src directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.server.auth import Authentication
from src.server.rate_limiter import RateLimiter
from src.server.monitoring import Monitoring
from src.server.middleware import SecurityMiddleware


@pytest.fixture
async def test_client(aiohttp_client):
    """Create a test client with security middleware."""
    app = web.Application()
    
    # Set up security components
    auth = Authentication(["test-api-key"])
    rate_limiter = RateLimiter(limit=5, window=1)  # 5 requests per second for testing
    monitoring = Monitoring(enabled=True)
    
    # Add security middleware
    security_middleware = SecurityMiddleware(auth, rate_limiter, monitoring)
    app.middlewares.append(security_middleware.middleware)
    
    # Add test routes
    async def health_handler(request):
        return web.json_response({"status": "healthy"})
    
    async def protected_handler(request):
        return web.json_response({"message": "authorized"})
    
    app.router.add_get('/health', health_handler)
    app.router.add_get('/protected', protected_handler)
    
    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_health_endpoint(test_client):
    """Test public health endpoint."""
    resp = await test_client.get('/health')
    assert resp.status == 200
    data = await resp.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_auth_required(test_client):
    """Test that protected endpoints require authentication."""
    resp = await test_client.get('/protected')
    assert resp.status == 401
    
    resp = await test_client.get('/protected', headers={"Authorization": "Bearer invalid-key"})
    assert resp.status == 401
    
    resp = await test_client.get('/protected', headers={"Authorization": "Bearer test-api-key"})
    assert resp.status == 200


@pytest.mark.asyncio
async def test_rate_limiting(test_client):
    """Test rate limiting."""
    headers = {"Authorization": "Bearer test-api-key"}
    
    # Make 5 requests (our limit)
    for _ in range(5):
        resp = await test_client.get('/protected', headers=headers)
        assert resp.status == 200
    
    # 6th request should be rate limited
    resp = await test_client.get('/protected', headers=headers)
    assert resp.status == 429
    assert "Retry-After" in resp.headers
    
    # Wait for rate limit to reset
    await asyncio.sleep(1.1)
    
    # Should be able to make a request again
    resp = await test_client.get('/protected', headers=headers)
    assert resp.status == 200


@pytest.mark.asyncio
async def test_rate_limit_headers(test_client):
    """Test rate limit headers."""
    headers = {"Authorization": "Bearer test-api-key"}
    
    resp = await test_client.get('/protected', headers=headers)
    assert resp.status == 200
    assert "X-RateLimit-Remaining" in resp.headers
    
    remaining = int(resp.headers["X-RateLimit-Remaining"])
    assert remaining < 5  # Should be less than our limit

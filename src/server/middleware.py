
"""Middleware for the secure MCP server."""

from typing import Callable, Dict, Tuple, Optional, Any
import json
import time
import asyncio
from aiohttp import web

from .auth import Authentication
from .rate_limiter import RateLimiter
from .monitoring import Monitoring


class SecurityMiddleware:
    """Implements security middleware for the secure MCP server."""

    def __init__(self, 
                auth: Authentication, 
                rate_limiter: RateLimiter,
                monitoring: Monitoring,
                public_paths: Optional[list] = None):
        """Initialize the security middleware.
        
        Args:
            auth: Authentication instance
            rate_limiter: RateLimiter instance
            monitoring: Monitoring instance
            public_paths: List of paths that don't require authentication
        """
        self.auth = auth
        self.rate_limiter = rate_limiter
        self.monitoring = monitoring
        self.public_paths = public_paths or ['/health']
    
    @web.middleware
    async def middleware(self, request: web.Request, handler: Callable) -> web.Response:
        """Apply security middleware to incoming requests.
        
        Args:
            request: The incoming request
            handler: The request handler
        
        Returns:
            The response from the handler or an error response
        """
        start_time = time.time()
        client_ip = request.remote
        path = request.path
        
        # Check rate limit
        allowed, retry_after, remaining = self.rate_limiter.check_rate_limit(client_ip)
        if not allowed:
            response = web.json_response(
                {"error": "Too many requests", "retry_after": retry_after}, 
                status=429
            )
            response.headers['Retry-After'] = str(retry_after)
            response.headers['X-RateLimit-Remaining'] = '0'
            
            self.monitoring.log_request(
                client_id=client_ip,
                endpoint=path,
                status=429,
                authenticated=False,
                duration=time.time() - start_time
            )
            return response
        
        # Check authentication for protected paths
        authenticated = False
        if path not in self.public_paths:
            auth_header = request.headers.get('Authorization')
            api_key = self.auth.extract_api_key(auth_header)
            authenticated = self.auth.verify_key(api_key)
            
            if not authenticated:
                response = web.json_response(
                    {"error": "Unauthorized. API key required"}, 
                    status=401
                )
                response.headers['WWW-Authenticate'] = 'Bearer'
                
                self.monitoring.log_request(
                    client_id=client_ip,
                    endpoint=path,
                    status=401,
                    authenticated=False,
                    duration=time.time() - start_time
                )
                return response
        else:
            # Public path, no authentication needed
            authenticated = True
        
        # Add rate limit headers
        if remaining is not None:
            request['X-RateLimit-Remaining'] = remaining
        
        # Process the request
        try:
            response = await handler(request)
            
            # Add rate limit headers to response
            if remaining is not None:
                response.headers['X-RateLimit-Remaining'] = str(remaining)
                response.headers['X-RateLimit-Limit'] = str(self.rate_limiter.limit)
            
            # Log the request
            self.monitoring.log_request(
                client_id=client_ip,
                endpoint=path,
                status=response.status,
                authenticated=authenticated,
                duration=time.time() - start_time
            )
            
            return response
            
        except web.HTTPException as ex:
            # Handle HTTP exceptions
            self.monitoring.log_request(
                client_id=client_ip,
                endpoint=path,
                status=ex.status,
                authenticated=authenticated,
                duration=time.time() - start_time
            )
            raise
            
        except Exception as ex:
            # Handle unexpected exceptions
            self.monitoring.log_request(
                client_id=client_ip,
                endpoint=path,
                status=500,
                authenticated=authenticated,
                duration=time.time() - start_time
            )
            return web.json_response(
                {"error": "Internal server error"}, 
                status=500
            )

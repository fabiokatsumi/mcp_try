
"""Rate limiting implementation for the secure MCP server."""

import time
from typing import Dict, Tuple, Optional
from collections import defaultdict, deque


class RateLimiter:
    """Implements rate limiting for the secure MCP server."""

    def __init__(self, limit: int = 100, window: int = 60):
        """Initialize the rate limiter.
        
        Args:
            limit: Maximum number of requests per window
            window: Time window in seconds
        """
        self.limit = limit
        self.window = window
        self.requests = defaultdict(lambda: deque(maxlen=limit+1))
    
    def check_rate_limit(self, client_id: str) -> Tuple[bool, Optional[int], Optional[int]]:
        """Check if a client has exceeded their rate limit.
        
        Args:
            client_id: Identifier for the client (e.g., IP address)
        
        Returns:
            Tuple of (allowed, retry_after, remaining)
            - allowed: True if request is allowed, False otherwise
            - retry_after: Seconds to wait before retrying (if exceeded)
            - remaining: Number of requests remaining in the window
        """
        now = time.time()
        client_requests = self.requests[client_id]
        
        # Remove expired timestamps
        while client_requests and client_requests[0] < now - self.window:
            client_requests.popleft()
        
        # Check if limit is exceeded
        if len(client_requests) >= self.limit:
            retry_after = int(client_requests[0] - (now - self.window)) + 1
            return False, retry_after, 0
        
        # Add current request timestamp
        client_requests.append(now)
        
        # Return allowed with remaining count
        remaining = self.limit - len(client_requests)
        return True, None, remaining
    
    def clear_old_entries(self):
        """Clear old entries to prevent memory growth."""
        now = time.time()
        expired_clients = []
        
        for client_id, timestamps in self.requests.items():
            # Check if all timestamps are expired
            if all(ts < now - self.window for ts in timestamps):
                expired_clients.append(client_id)
        
        # Remove expired clients
        for client_id in expired_clients:
            del self.requests[client_id]

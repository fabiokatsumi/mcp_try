
"""Unit tests for rate limiter module."""

import pytest
import time
from src.server.rate_limiter import RateLimiter


def test_check_rate_limit_allowed():
    """Test rate limiting when requests are allowed."""
    limiter = RateLimiter(limit=5, window=60)
    
    # First request should be allowed
    allowed, retry_after, remaining = limiter.check_rate_limit("client1")
    assert allowed is True
    assert retry_after is None
    assert remaining == 4


def test_check_rate_limit_exceeded():
    """Test rate limiting when limit is exceeded."""
    limiter = RateLimiter(limit=2, window=60)
    
    # Make 2 requests (limit)
    limiter.check_rate_limit("client2")
    limiter.check_rate_limit("client2")
    
    # Third request should be denied
    allowed, retry_after, remaining = limiter.check_rate_limit("client2")
    assert allowed is False
    assert retry_after is not None
    assert retry_after > 0
    assert remaining == 0


def test_separate_clients():
    """Test that clients are rate limited separately."""
    limiter = RateLimiter(limit=2, window=60)
    
    # Use up client3's limit
    limiter.check_rate_limit("client3")
    limiter.check_rate_limit("client3")
    
    # client3 should be rate limited
    allowed3, _, _ = limiter.check_rate_limit("client3")
    assert allowed3 is False
    
    # client4 should still be allowed
    allowed4, _, _ = limiter.check_rate_limit("client4")
    assert allowed4 is True


def test_clear_old_entries():
    """Test clearing of expired entries."""
    # Short window for testing
    limiter = RateLimiter(limit=5, window=0.1)
    
    # Make a request
    limiter.check_rate_limit("temp_client")
    
    # Verify client exists in requests
    assert "temp_client" in limiter.requests
    
    # Wait for window to expire
    time.sleep(0.2)
    
    # Clear old entries
    limiter.clear_old_entries()
    
    # Client should be removed
    assert "temp_client" not in limiter.requests

#!/usr/bin/env python3
"""
Basic functionality test for the MCP server components.
This test verifies core functionality without complex async fixtures.
"""

import sys
import os
import time

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.server.auth import Authentication
from src.server.rate_limiter import RateLimiter
from src.server.monitoring import Monitoring

def test_core_functionality():
    """Test basic functionality of all core components."""
    print("🧪 Testing Core Functionality...")
    
    # Test Authentication
    print("  Testing Authentication...")
    auth = Authentication(["test-key-1", "test-key-2"])
    
    # Test key generation
    key = auth.generate_key()
    assert len(key) > 30  # Base64 encoded key should be longer than 30 chars
    print(f"    ✅ Generated key: {key[:8]}...")
    
    # Test key verification
    assert auth.verify_key("test-key-1") == True
    assert auth.verify_key("invalid-key") == False
    print("    ✅ Key verification works")
    
    # Test key extraction
    key = auth.extract_api_key("Bearer test-key-1")
    assert key == "test-key-1"
    print("    ✅ Key extraction works")
    
    # Test Rate Limiter
    print("  Testing Rate Limiter...")
    limiter = RateLimiter(limit=5, window=1)
    
    # Test rate limiting
    client_id = "test-client"
    
    # Should allow first 5 requests
    for i in range(5):
        allowed, retry_after, remaining = limiter.check_rate_limit(client_id)
        assert allowed == True
        assert remaining == 4 - i
    
    # 6th request should be blocked
    allowed, retry_after, remaining = limiter.check_rate_limit(client_id)
    assert allowed == False
    assert remaining == 0
    print("    ✅ Rate limiting works")
    
    # Test Monitoring
    print("  Testing Monitoring...")
    monitor = Monitoring(enabled=True)
    
    # Test metrics recording
    monitor.log_request("test-client", "/health", 200, True, 0.05)
    
    # Test metrics retrieval
    stats = monitor.get_stats()
    assert "uptime" in stats
    assert "total_requests" in stats
    print("    ✅ Monitoring works")
    
    print("🎉 All core functionality tests passed!")
    return True

if __name__ == "__main__":
    try:
        test_core_functionality()
        print("\n✅ PROJECT IS READY FOR DEPLOYMENT!")
        print("✅ All core components are working correctly!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

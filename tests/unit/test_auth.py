
"""Unit tests for authentication module."""

import pytest
from src.server.auth import Authentication


def test_generate_key():
    """Test API key generation."""
    key = Authentication.generate_key()
    assert isinstance(key, str)
    assert len(key) > 16  # Should be reasonably long for security


def test_verify_key():
    """Test API key verification."""
    auth = Authentication(["valid-key", "another-key"])
    
    # Valid keys
    assert auth.verify_key("valid-key") is True
    assert auth.verify_key("another-key") is True
    
    # Invalid keys
    assert auth.verify_key("invalid-key") is False
    assert auth.verify_key("") is False
    assert auth.verify_key(None) is False


def test_extract_api_key():
    """Test API key extraction from Authorization header."""
    auth = Authentication(["valid-key"])
    
    # Valid header format
    assert auth.extract_api_key("Bearer valid-key") == "valid-key"
    
    # Invalid header format
    assert auth.extract_api_key("Token valid-key") is None
    assert auth.extract_api_key("valid-key") is None
    assert auth.extract_api_key("") is None
    assert auth.extract_api_key(None) is None


def test_empty_api_keys():
    """Test authentication with no API keys."""
    auth = Authentication([])
    assert auth.verify_key("any-key") is False

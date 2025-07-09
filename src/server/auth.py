
"""Authentication module for the secure MCP server."""

import hmac
import secrets
from typing import List, Optional, Tuple


class Authentication:
    """Handles API key authentication for the secure MCP server."""

    def __init__(self, api_keys: List[str]):
        """Initialize with a list of valid API keys.
        
        Args:
            api_keys: List of valid API keys
        """
        self.api_keys = api_keys
    
    @staticmethod
    def generate_key() -> str:
        """Generate a secure API key.
        
        Returns:
            A secure random API key
        """
        return secrets.token_urlsafe(32)
    
    def verify_key(self, api_key: str) -> bool:
        """Verify if the provided API key is valid.
        
        Args:
            api_key: The API key to verify
        
        Returns:
            True if the API key is valid, False otherwise
        """
        if not api_key or not self.api_keys:
            return False
            
        # Use constant time comparison to prevent timing attacks
        return any(
            hmac.compare_digest(key, api_key)
            for key in self.api_keys
            if key and api_key
        )
    
    def extract_api_key(self, authorization_header: Optional[str]) -> Optional[str]:
        """Extract API key from Authorization header.
        
        Args:
            authorization_header: The Authorization header value
        
        Returns:
            The API key if valid format, None otherwise
        """
        if not authorization_header:
            return None
            
        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
            
        return parts[1]

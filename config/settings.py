
"""Configuration settings for the MCP server."""

import os
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

# Use absolute import for utils
from src.utils.helpers import get_env_var, get_env_var_bool


class Settings:
    """Configuration settings for the MCP server."""

    def __init__(self, config_file: Optional[str] = None):
        """Initialize settings from config file and environment variables.
        
        Args:
            config_file: Path to configuration file
        """
        self.config: Dict[str, Any] = {}
        
        # Load configuration file if provided
        if config_file and os.path.isfile(config_file):
            try:
                with open(config_file, 'r') as f:
                    self.config = json.load(f)
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON in config file: {config_file}")
            except Exception as e:
                logging.error(f"Error reading config file: {e}")
        
        # Load default configuration if no file provided or loading failed
        if not self.config:
            default_config_path = Path(__file__).parent / "mcp_config.json"
            try:
                if os.path.isfile(default_config_path):
                    with open(default_config_path, 'r') as f:
                        self.config = json.load(f)
            except Exception:
                # Start with empty config if even default fails
                self.config = {}
    
    @property
    def api_keys(self) -> List[str]:
        """Get API keys from environment or config.
        
        Returns:
            List of API keys
        """
        # Environment variable has precedence
        keys_env = get_env_var("MCP_API_KEYS", None)
        if keys_env:
            return [k.strip() for k in keys_env.split(',') if k.strip()]
        
        # Fall back to config file
        return self.config.get("api_keys", [])
    
    @property
    def port(self) -> int:
        """Get server port.
        
        Returns:
            Server port number
        """
        port_env = get_env_var("PORT", None)
        if port_env and port_env.isdigit():
            return int(port_env)
        return self.config.get("port", 8443)
    
    @property
    def log_level(self) -> str:
        """Get log level.
        
        Returns:
            Log level
        """
        return get_env_var("MCP_LOG_LEVEL", 
                         self.config.get("log_level", "INFO"))
    
    @property
    def enable_monitoring(self) -> bool:
        """Check if monitoring is enabled.
        
        Returns:
            True if monitoring is enabled
        """
        return get_env_var_bool("MCP_ENABLE_MONITORING", 
                              self.config.get("enable_monitoring", True))
    
    @property
    def rate_limit(self) -> int:
        """Get rate limit.
        
        Returns:
            Rate limit per minute
        """
        limit_env = get_env_var("MCP_RATE_LIMIT", None)
        if limit_env and limit_env.isdigit():
            return int(limit_env)
        return self.config.get("rate_limit", 100)
    
    @property
    def cors_origins(self) -> List[str]:
        """Get CORS origins.
        
        Returns:
            List of allowed origins
        """
        origins_env = get_env_var("MCP_CORS_ORIGINS", None)
        if origins_env:
            return [o.strip() for o in origins_env.split(',') if o.strip()]
        return self.config.get("cors_origins", ["*"])
    
    @property
    def tools_directory(self) -> str:
        """Get tools directory.
        
        Returns:
            Path to tools directory
        """
        return get_env_var("MCP_TOOLS_DIRECTORY", 
                         self.config.get("tools_directory", "./tools"))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary.
        
        Returns:
            Dictionary of settings
        """
        return {
            "port": self.port,
            "log_level": self.log_level,
            "enable_monitoring": self.enable_monitoring,
            "rate_limit": self.rate_limit,
            "cors_origins": self.cors_origins,
            "tools_directory": self.tools_directory,
            # Don't include API keys for security
        }


"""Common utility functions for MCP server."""

import os
import json
import logging
from typing import Dict, Any, Optional


def load_json_file(filepath: str) -> Dict[str, Any]:
    """Load JSON from a file.
    
    Args:
        filepath: Path to the JSON file
    
    Returns:
        The parsed JSON data
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json_file(filepath: str, data: Dict[str, Any]) -> None:
    """Save JSON to a file.
    
    Args:
        filepath: Path to the JSON file
        data: The data to save
    
    Raises:
        IOError: If the file can't be written
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def get_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get an environment variable with a default value.
    
    Args:
        name: The name of the environment variable
        default: The default value if the variable is not set
    
    Returns:
        The value of the environment variable or the default
    """
    return os.environ.get(name, default)


def get_env_var_bool(name: str, default: bool = False) -> bool:
    """Get a boolean environment variable.
    
    Args:
        name: The name of the environment variable
        default: The default value if the variable is not set
    
    Returns:
        True if the variable is set to 'true', 'yes', '1', or 'y' (case-insensitive)
        False otherwise or if the variable is not set and default is False
    """
    val = get_env_var(name, None)
    if val is None:
        return default
    return val.lower() in ('true', 'yes', '1', 'y')


def setup_logger(name: str, level: str = 'INFO') -> logging.Logger:
    """Set up a logger with the specified name and level.
    
    Args:
        name: The name of the logger
        level: The logging level
    
    Returns:
        The configured logger
    """
    logger = logging.getLogger(name)
    
    # Set level
    numeric_level = getattr(logging, level.upper(), None)
    if isinstance(numeric_level, int):
        logger.setLevel(numeric_level)
    
    # Add handler if not already added
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

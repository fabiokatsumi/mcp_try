# Migration Script for MCP Server Project Reorganization

"""
This script assists in the migration of the MCP Server project to the new structure.
It creates directories, moves files, and sets up the new project organization.

To run:
python migration_script.py

Note: Run this from the root of the old project (mcp_try)
"""

import os
import shutil
from pathlib import Path
import sys


def print_step(message):
    """Print a step message with formatting."""
    print("\n" + "=" * 80)
    print(f"🚀 {message}")
    print("=" * 80)


def print_success(message):
    """Print a success message with formatting."""
    print(f"✅ {message}")


def print_warning(message):
    """Print a warning message with formatting."""
    print(f"⚠️ {message}")


def print_error(message):
    """Print an error message with formatting."""
    print(f"❌ {message}")


def create_directory(path):
    """Create a directory if it doesn't exist."""
    try:
        os.makedirs(path, exist_ok=True)
        print_success(f"Created directory: {path}")
    except Exception as e:
        print_error(f"Failed to create directory {path}: {e}")
        return False
    return True


def create_file(path, content=""):
    """Create a file with optional content."""
    try:
        with open(path, 'w') as f:
            f.write(content)
        print_success(f"Created file: {path}")
    except Exception as e:
        print_error(f"Failed to create file {path}: {e}")
        return False
    return True


def copy_file(src, dest):
    """Copy a file from src to dest."""
    try:
        shutil.copy2(src, dest)
        print_success(f"Copied file: {src} -> {dest}")
    except Exception as e:
        print_error(f"Failed to copy file {src} to {dest}: {e}")
        return False
    return True


def create_init_files(directory):
    """Create __init__.py files in directory and all subdirectories."""
    for root, dirs, files in os.walk(directory):
        init_file = os.path.join(root, "__init__.py")
        if not os.path.exists(init_file):
            create_file(init_file, "")


def main():
    """Execute the migration process."""
    # Confirm we are in the right location
    if not os.path.exists('server/secure_server.py'):
        print_error("Cannot find server/secure_server.py. Are you in the MCP project root?")
        return

    # Backup original project
    print_step("Creating backup of original project")
    backup_dir = "../mcp_try_backup_" + os.path.basename(os.getcwd())
    if os.path.exists(backup_dir):
        print_warning(f"Backup directory {backup_dir} already exists. Skipping backup.")
    else:
        shutil.copytree(".", backup_dir)
        print_success(f"Backup created at {backup_dir}")

    # Create base directory structure
    print_step("Creating new directory structure")
    
    directories = [
        # Main directories
        "src",
        "config",
        "deployment",
        "docs",
        "tests",
        "scripts",
        
        # Subdirectories
        "src/server",
        "src/tools",
        "src/tools/implementations",
        "src/utils",
        "deployment/dokploy",
        "deployment/env",
        "docs/deployment",
        "docs/security",
        "docs/api",
        "tests/unit",
        "tests/integration",
        "tests/security"
    ]
    
    for directory in directories:
        create_directory(directory)
    
    # Create package markers (__init__.py files)
    print_step("Creating package markers")
    create_init_files("src")
    create_init_files("config")
    create_init_files("tests")

    # Migrate core server files
    print_step("Migrating core server files")
    
    # Secure server
    if os.path.exists("secure_server.py"):
        copy_file("secure_server.py", "src/server/secure_server.py")
    else:
        print_warning("Could not find secure_server.py")
        
    # Extract common content for auth.py
    auth_content = """
\"\"\"Authentication module for the secure MCP server.\"\"\"

import hmac
import secrets
from typing import List, Optional, Tuple


class Authentication:
    \"\"\"Handles API key authentication for the secure MCP server.\"\"\"

    def __init__(self, api_keys: List[str]):
        \"\"\"Initialize with a list of valid API keys.
        
        Args:
            api_keys: List of valid API keys
        \"\"\"
        self.api_keys = api_keys
    
    @staticmethod
    def generate_key() -> str:
        \"\"\"Generate a secure API key.
        
        Returns:
            A secure random API key
        \"\"\"
        return secrets.token_urlsafe(32)
    
    def verify_key(self, api_key: str) -> bool:
        \"\"\"Verify if the provided API key is valid.
        
        Args:
            api_key: The API key to verify
        
        Returns:
            True if the API key is valid, False otherwise
        \"\"\"
        if not api_key or not self.api_keys:
            return False
            
        # Use constant time comparison to prevent timing attacks
        return any(
            hmac.compare_digest(key, api_key)
            for key in self.api_keys
            if key and api_key
        )
    
    def extract_api_key(self, authorization_header: Optional[str]) -> Optional[str]:
        \"\"\"Extract API key from Authorization header.
        
        Args:
            authorization_header: The Authorization header value
        
        Returns:
            The API key if valid format, None otherwise
        \"\"\"
        if not authorization_header:
            return None
            
        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
            
        return parts[1]
"""
    create_file("src/server/auth.py", auth_content)
    
    # Extract common content for rate_limiter.py
    rate_limiter_content = """
\"\"\"Rate limiting implementation for the secure MCP server.\"\"\"

import time
from typing import Dict, Tuple, Optional
from collections import defaultdict, deque


class RateLimiter:
    \"\"\"Implements rate limiting for the secure MCP server.\"\"\"

    def __init__(self, limit: int = 100, window: int = 60):
        \"\"\"Initialize the rate limiter.
        
        Args:
            limit: Maximum number of requests per window
            window: Time window in seconds
        \"\"\"
        self.limit = limit
        self.window = window
        self.requests = defaultdict(lambda: deque(maxlen=limit+1))
    
    def check_rate_limit(self, client_id: str) -> Tuple[bool, Optional[int], Optional[int]]:
        \"\"\"Check if a client has exceeded their rate limit.
        
        Args:
            client_id: Identifier for the client (e.g., IP address)
        
        Returns:
            Tuple of (allowed, retry_after, remaining)
            - allowed: True if request is allowed, False otherwise
            - retry_after: Seconds to wait before retrying (if exceeded)
            - remaining: Number of requests remaining in the window
        \"\"\"
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
        \"\"\"Clear old entries to prevent memory growth.\"\"\"
        now = time.time()
        expired_clients = []
        
        for client_id, timestamps in self.requests.items():
            # Check if all timestamps are expired
            if all(ts < now - self.window for ts in timestamps):
                expired_clients.append(client_id)
        
        # Remove expired clients
        for client_id in expired_clients:
            del self.requests[client_id]
"""
    create_file("src/server/rate_limiter.py", rate_limiter_content)
    
    # Extract common content for monitoring.py
    monitoring_content = """
\"\"\"Monitoring module for the secure MCP server.\"\"\"

import time
import logging
import os
from typing import Dict, List, Optional, Any
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class Monitoring:
    \"\"\"Handles monitoring and logging for the secure MCP server.\"\"\"

    def __init__(self, enabled: bool = True, log_level: str = "INFO"):
        \"\"\"Initialize the monitoring system.
        
        Args:
            enabled: Whether monitoring is enabled
            log_level: The logging level to use
        \"\"\"
        self.enabled = enabled
        self.process = psutil.Process(os.getpid())
        self.start_time = time.time()
        self.requests = []
        self.max_requests = 1000  # Maximum number of requests to store
        
        # Set log level
        numeric_level = getattr(logging, log_level.upper(), None)
        if isinstance(numeric_level, int):
            logging.getLogger().setLevel(numeric_level)
    
    def log_request(self, client_id: str, endpoint: str, status: int, 
                   authenticated: bool, duration: float):
        \"\"\"Log a request to the monitoring system.
        
        Args:
            client_id: Client identifier (e.g., IP address)
            endpoint: The requested endpoint
            status: HTTP status code of the response
            authenticated: Whether the request was authenticated
            duration: Request processing duration in seconds
        \"\"\"
        if not self.enabled:
            return
            
        # Log to system logger
        log_level = logging.INFO if status < 400 else logging.WARNING
        logging.log(log_level, 
                   f"Request: {endpoint} from {client_id} - "
                   f"Status: {status}, Auth: {authenticated}, Time: {duration:.4f}s")
        
        # Store for statistics
        self.requests.append({
            'timestamp': time.time(),
            'client_id': client_id,
            'endpoint': endpoint,
            'status': status,
            'authenticated': authenticated,
            'duration': duration
        })
        
        # Trim requests list if necessary
        if len(self.requests) > self.max_requests:
            self.requests = self.requests[-self.max_requests:]
    
    def get_system_stats(self) -> Dict[str, Any]:
        \"\"\"Get system statistics.
        
        Returns:
            Dictionary with system statistics
        \"\"\"
        if not self.enabled:
            return {'monitoring': 'disabled'}
            
        uptime = time.time() - self.start_time
        hours, remainder = divmod(uptime, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        
        memory_info = self.process.memory_info()
        
        return {
            'uptime': uptime_str,
            'memory_usage_mb': round(memory_info.rss / (1024 * 1024), 2),
            'cpu_percent': self.process.cpu_percent(interval=0.1),
            'request_count': len(self.requests),
            'request_rate': round(len(self.requests) / uptime if uptime > 0 else 0, 2),
            'monitoring_enabled': self.enabled
        }
    
    def get_recent_errors(self, limit: int = 10) -> List[Dict[str, Any]]:
        \"\"\"Get recent error requests.
        
        Args:
            limit: Maximum number of errors to return
        
        Returns:
            List of error requests
        \"\"\"
        if not self.enabled:
            return []
            
        errors = [r for r in self.requests if r['status'] >= 400]
        errors.sort(key=lambda x: x['timestamp'], reverse=True)
        return errors[:limit]
"""
    create_file("src/server/monitoring.py", monitoring_content)
    
    # Create middleware.py
    middleware_content = """
\"\"\"Middleware for the secure MCP server.\"\"\"

from typing import Callable, Dict, Tuple, Optional, Any
import json
import time
import asyncio
from aiohttp import web

from .auth import Authentication
from .rate_limiter import RateLimiter
from .monitoring import Monitoring


class SecurityMiddleware:
    \"\"\"Implements security middleware for the secure MCP server.\"\"\"

    def __init__(self, 
                auth: Authentication, 
                rate_limiter: RateLimiter,
                monitoring: Monitoring,
                public_paths: Optional[list] = None):
        \"\"\"Initialize the security middleware.
        
        Args:
            auth: Authentication instance
            rate_limiter: RateLimiter instance
            monitoring: Monitoring instance
            public_paths: List of paths that don't require authentication
        \"\"\"
        self.auth = auth
        self.rate_limiter = rate_limiter
        self.monitoring = monitoring
        self.public_paths = public_paths or ['/health']
    
    @web.middleware
    async def middleware(self, request: web.Request, handler: Callable) -> web.Response:
        \"\"\"Apply security middleware to incoming requests.
        
        Args:
            request: The incoming request
            handler: The request handler
        
        Returns:
            The response from the handler or an error response
        \"\"\"
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
"""
    create_file("src/server/middleware.py", middleware_content)
    
    # Create tools module
    tools_registry_content = """
\"\"\"Tool registry for MCP server.\"\"\"

from typing import Dict, List, Any, Callable, Optional
import importlib
import os
import sys
import json
import inspect


class ToolRegistry:
    \"\"\"Registry for MCP tools.\"\"\"

    def __init__(self):
        \"\"\"Initialize an empty tool registry.\"\"\"
        self.tools: Dict[str, Dict[str, Any]] = {}
    
    def register_tool(self, name: str, handler: Callable, description: str, schema: Dict[str, Any]):
        \"\"\"Register a new tool.
        
        Args:
            name: The name of the tool
            handler: The function that implements the tool
            description: A description of the tool
            schema: The JSON schema for the tool's parameters
        \"\"\"
        self.tools[name] = {
            'name': name,
            'handler': handler,
            'description': description,
            'schema': schema
        }
    
    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        \"\"\"Get a tool by name.
        
        Args:
            name: The name of the tool
        
        Returns:
            The tool definition or None if not found
        \"\"\"
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        \"\"\"List all available tools.
        
        Returns:
            List of tool definitions (without handlers)
        \"\"\"
        return [
            {
                'name': tool['name'],
                'description': tool['description'],
                'schema': tool['schema']
            }
            for tool in self.tools.values()
        ]
    
    def load_from_directory(self, directory: str) -> int:
        \"\"\"Load tools from a directory.
        
        Args:
            directory: The directory to load tools from
        
        Returns:
            The number of tools loaded
        \"\"\"
        count = 0
        
        # Add directory to path temporarily
        sys.path.insert(0, os.path.abspath(os.path.dirname(directory)))
        
        try:
            # Walk through the directory
            for root, _, files in os.walk(directory):
                for filename in files:
                    if filename.endswith('.py') and not filename.startswith('__'):
                        # Convert path to module name
                        file_path = os.path.join(root, filename)
                        module_name = os.path.relpath(file_path, os.path.dirname(directory))
                        module_name = os.path.splitext(module_name)[0].replace(os.path.sep, '.')
                        
                        try:
                            # Import the module
                            module = importlib.import_module(module_name)
                            
                            # Look for tool definitions
                            for name, obj in inspect.getmembers(module):
                                if hasattr(obj, '_mcp_tool') and obj._mcp_tool:
                                    self.register_tool(
                                        name=obj._mcp_tool_name,
                                        handler=obj,
                                        description=obj._mcp_tool_description,
                                        schema=obj._mcp_tool_schema
                                    )
                                    count += 1
                        except Exception as e:
                            print(f"Error loading module {module_name}: {e}")
        finally:
            # Remove directory from path
            sys.path.pop(0)
        
        return count


def tool(name: str, description: str, schema: Dict[str, Any]):
    \"\"\"Decorator to mark a function as an MCP tool.
    
    Args:
        name: The name of the tool
        description: A description of the tool
        schema: The JSON schema for the tool's parameters
    
    Returns:
        Decorator function
    \"\"\"
    def decorator(func):
        func._mcp_tool = True
        func._mcp_tool_name = name
        func._mcp_tool_description = description
        func._mcp_tool_schema = schema
        return func
    return decorator
"""
    create_file("src/tools/registry.py", tools_registry_content)
    
    # Create utilities
    utils_content = """
\"\"\"Common utility functions for MCP server.\"\"\"

import os
import json
import logging
from typing import Dict, Any, Optional


def load_json_file(filepath: str) -> Dict[str, Any]:
    \"\"\"Load JSON from a file.
    
    Args:
        filepath: Path to the JSON file
    
    Returns:
        The parsed JSON data
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    \"\"\"
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json_file(filepath: str, data: Dict[str, Any]) -> None:
    \"\"\"Save JSON to a file.
    
    Args:
        filepath: Path to the JSON file
        data: The data to save
    
    Raises:
        IOError: If the file can't be written
    \"\"\"
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def get_env_var(name: str, default: Optional[str] = None) -> Optional[str]:
    \"\"\"Get an environment variable with a default value.
    
    Args:
        name: The name of the environment variable
        default: The default value if the variable is not set
    
    Returns:
        The value of the environment variable or the default
    \"\"\"
    return os.environ.get(name, default)


def get_env_var_bool(name: str, default: bool = False) -> bool:
    \"\"\"Get a boolean environment variable.
    
    Args:
        name: The name of the environment variable
        default: The default value if the variable is not set
    
    Returns:
        True if the variable is set to 'true', 'yes', '1', or 'y' (case-insensitive)
        False otherwise or if the variable is not set and default is False
    \"\"\"
    val = get_env_var(name, None)
    if val is None:
        return default
    return val.lower() in ('true', 'yes', '1', 'y')


def setup_logger(name: str, level: str = 'INFO') -> logging.Logger:
    \"\"\"Set up a logger with the specified name and level.
    
    Args:
        name: The name of the logger
        level: The logging level
    
    Returns:
        The configured logger
    \"\"\"
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
"""
    create_file("src/utils/helpers.py", utils_content)

    # Create configuration module
    settings_content = """
\"\"\"Configuration settings for the MCP server.\"\"\"

import os
import json
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..utils.helpers import get_env_var, get_env_var_bool


class Settings:
    \"\"\"Configuration settings for the MCP server.\"\"\"

    def __init__(self, config_file: Optional[str] = None):
        \"\"\"Initialize settings from config file and environment variables.
        
        Args:
            config_file: Path to configuration file
        \"\"\"
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
        \"\"\"Get API keys from environment or config.
        
        Returns:
            List of API keys
        \"\"\"
        # Environment variable has precedence
        keys_env = get_env_var("MCP_API_KEYS", None)
        if keys_env:
            return [k.strip() for k in keys_env.split(',') if k.strip()]
        
        # Fall back to config file
        return self.config.get("api_keys", [])
    
    @property
    def port(self) -> int:
        \"\"\"Get server port.
        
        Returns:
            Server port number
        \"\"\"
        port_env = get_env_var("PORT", None)
        if port_env and port_env.isdigit():
            return int(port_env)
        return self.config.get("port", 8443)
    
    @property
    def log_level(self) -> str:
        \"\"\"Get log level.
        
        Returns:
            Log level
        \"\"\"
        return get_env_var("MCP_LOG_LEVEL", 
                         self.config.get("log_level", "INFO"))
    
    @property
    def enable_monitoring(self) -> bool:
        \"\"\"Check if monitoring is enabled.
        
        Returns:
            True if monitoring is enabled
        \"\"\"
        return get_env_var_bool("MCP_ENABLE_MONITORING", 
                              self.config.get("enable_monitoring", True))
    
    @property
    def rate_limit(self) -> int:
        \"\"\"Get rate limit.
        
        Returns:
            Rate limit per minute
        \"\"\"
        limit_env = get_env_var("MCP_RATE_LIMIT", None)
        if limit_env and limit_env.isdigit():
            return int(limit_env)
        return self.config.get("rate_limit", 100)
    
    @property
    def cors_origins(self) -> List[str]:
        \"\"\"Get CORS origins.
        
        Returns:
            List of allowed origins
        \"\"\"
        origins_env = get_env_var("MCP_CORS_ORIGINS", None)
        if origins_env:
            return [o.strip() for o in origins_env.split(',') if o.strip()]
        return self.config.get("cors_origins", ["*"])
    
    @property
    def tools_directory(self) -> str:
        \"\"\"Get tools directory.
        
        Returns:
            Path to tools directory
        \"\"\"
        return get_env_var("MCP_TOOLS_DIRECTORY", 
                         self.config.get("tools_directory", "./tools"))
    
    def to_dict(self) -> Dict[str, Any]:
        \"\"\"Convert settings to dictionary.
        
        Returns:
            Dictionary of settings
        \"\"\"
        return {
            "port": self.port,
            "log_level": self.log_level,
            "enable_monitoring": self.enable_monitoring,
            "rate_limit": self.rate_limit,
            "cors_origins": self.cors_origins,
            "tools_directory": self.tools_directory,
            # Don't include API keys for security
        }
"""
    create_file("config/settings.py", settings_content)
    
    # Create config/mcp_config.json
    if os.path.exists("secure_production_config.json"):
        copy_file("secure_production_config.json", "config/mcp_config.json")
    else:
        config_content = """{
  "port": 8443,
  "log_level": "INFO",
  "enable_monitoring": true,
  "rate_limit": 100,
  "cors_origins": ["*"],
  "tools_directory": "./src/tools/implementations"
}"""
        create_file("config/mcp_config.json", config_content)

    # Migrate deployment files
    print_step("Migrating deployment files")
    
    # Dokploy files
    dokploy_files = [
        ("Dockerfile.production", "deployment/dokploy/Dockerfile.production"),
        ("dokploy.config", "deployment/dokploy/dokploy.config"),
        ("docker-compose.dokploy.yml", "deployment/dokploy/docker-compose.dokploy.yml"),
        ("deploy_dokploy.sh", "deployment/dokploy/deploy_dokploy.sh"),
        ("dokploy-health-check.sh", "deployment/dokploy/dokploy-health-check.sh"),
        ("dokploy-health-check.ps1", "deployment/dokploy/dokploy-health-check.ps1")
    ]
    
    for src, dest in dokploy_files:
        if os.path.exists(src):
            copy_file(src, dest)
        else:
            print_warning(f"Could not find {src}")
    
    # Create environment templates
    env_example_content = """# Example environment variables for MCP server

# Server Configuration
PORT=8443
MCP_LOG_LEVEL=INFO
MCP_ENABLE_MONITORING=true
MCP_RATE_LIMIT=100
MCP_CORS_ORIGINS=*
MCP_TOOLS_DIRECTORY=./src/tools/implementations

# Security
# MCP_API_KEYS=key1,key2,key3

# Python Configuration
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
PYTHONOPTIMIZE=1
"""
    create_file("deployment/env/.env.example", env_example_content)
    
    env_production_content = """# Production environment variables template for MCP server

# Server Configuration
PORT=8443
MCP_LOG_LEVEL=INFO
MCP_ENABLE_MONITORING=true
MCP_RATE_LIMIT=100
MCP_CORS_ORIGINS=*
MCP_TOOLS_DIRECTORY=./src/tools/implementations

# Security
# IMPORTANT: Replace with your actual API keys
MCP_API_KEYS=REPLACE_WITH_SECURE_API_KEYS

# Python Configuration
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
PYTHONOPTIMIZE=1
"""
    create_file("deployment/env/.env.production.template", env_production_content)

    # Create Dockerfile in root
    root_dockerfile_content = """# Production Dockerfile for MCP Secure Server
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \\
    PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONOPTIMIZE=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    gcc \\
    && rm -rf /var/lib/apt/lists/* \\
    && apt-get clean

# Copy requirements first (for better Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \\
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 mcpuser && \\
    chown -R mcpuser:mcpuser /app
USER mcpuser

# Expose port
EXPOSE 8443

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8443/health || exit 1

# Start secure server
CMD ["python", "-m", "src.server.secure_server", "--port", "8443", "--env-keys"]
"""
    create_file("Dockerfile.production", root_dockerfile_content)
    
    # Create .dockerignore
    dockerignore_content = """# Git
.git
.gitignore
.github/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# IDE
.idea/
.vscode/
*.swp
*.swo
.DS_Store
Thumbs.db

# Project specific
tests/
docs/
*.md
*.log
.coverage
htmlcov/
.pytest_cache/
.tox/
deployment/*
!deployment/dokploy/Dockerfile.production
!deployment/env/.env.production.template
scripts/
.env*
"""
    create_file(".dockerignore", dockerignore_content)
    
    # Update requirements.txt
    if os.path.exists("requirements.txt"):
        copy_file("requirements.txt", "requirements.txt.bak")
        
    requirements_content = """# Production dependencies for MCP Server
aiohttp==3.9.1
psutil==7.0.0
python-dotenv==1.0.0
"""
    create_file("requirements.txt", requirements_content)
    
    # Create requirements-dev.txt
    requirements_dev_content = """# Development dependencies
# Includes all production dependencies
-r requirements.txt

# Testing
pytest==7.4.0
pytest-asyncio==0.21.1
pytest-cov==4.1.0

# Linting and formatting
black==23.9.1
isort==5.12.0
flake8==6.1.0

# Documentation
mkdocs==1.5.3
mkdocs-material==9.4.6

# Development tools
ipython==8.12.0
"""
    create_file("requirements-dev.txt", requirements_dev_content)
    
    # Create setup.py
    setup_py_content = """from setuptools import setup, find_packages

# Read requirements
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="mcp-server",
    version="1.0.0",
    description="Secure Model Context Protocol Server for VPS Deployment",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
"""
    create_file("setup.py", setup_py_content)

    # Migrate documentation
    print_step("Migrating documentation")
    
    doc_files = [
        ("DOKPLOY_DEPLOYMENT_GUIDE.md", "docs/deployment/DOKPLOY_DEPLOYMENT_GUIDE.md"),
        ("dokploy-quickstart.md", "docs/deployment/dokploy-quickstart.md"),
        ("dokploy-troubleshooting.md", "docs/deployment/dokploy-troubleshooting.md"),
        ("SECURITY.md", "docs/security/SECURITY.md"),
        ("SECURITY_IMPLEMENTATION.md", "docs/security/SECURITY_IMPLEMENTATION.md"),
        ("SECURITY_CHECKLIST.md", "docs/security/SECURITY_CHECKLIST.md"),
        ("DOCUMENTATION_INDEX.md", "docs/DOCUMENTATION_INDEX.md")
    ]
    
    for src, dest in doc_files:
        if os.path.exists(src):
            copy_file(src, dest)
        else:
            print_warning(f"Could not find {src}")
    
    # Create API documentation
    api_doc_content = """# 📚 MCP Server API Reference

## Overview

This document provides a complete reference for the MCP Server API endpoints.

## Authentication

All endpoints except `/health` require authentication using an API key in the 
`Authorization` header with the `Bearer` scheme:

```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### Health Check

**GET** `/health`

Check the server health. This endpoint does not require authentication.

#### Response

```json
{
  "status": "healthy",
  "timestamp": "2025-07-07T12:34:56Z",
  "uptime": "10:30:15"
}
```

### List Available Tools

**GET** `/api/tools`

List all available tools.

#### Response

```json
{
  "tools": [
    {
      "name": "calculate",
      "description": "Perform mathematical calculations",
      "schema": {
        "properties": {
          "expression": {
            "type": "string",
            "description": "The mathematical expression to calculate"
          }
        },
        "required": ["expression"]
      }
    },
    ...
  ]
}
```

### Call Tool

**POST** `/mcp`

Call a tool using the JSON-RPC 2.0 protocol.

#### Request

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/call",
  "params": {
    "name": "calculate",
    "arguments": {
      "expression": "2 + 2"
    }
  }
}
```

#### Response

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "result": 4
  }
}
```

### List Tools (JSON-RPC)

**POST** `/mcp`

List available tools using the JSON-RPC 2.0 protocol.

#### Request

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "method": "tools/list",
  "params": {}
}
```

#### Response

Same as `GET /api/tools`

### Server Status

**GET** `/api/status`

Get server status information (requires authentication).

#### Response

```json
{
  "status": "running",
  "version": "1.0.0",
  "uptime": "10:30:15",
  "memory_usage_mb": 42.5,
  "cpu_percent": 2.3,
  "request_count": 1503,
  "request_rate": 2.5,
  "monitoring_enabled": true
}
```

## Error Handling

All errors are returned with appropriate HTTP status codes and a JSON body:

```json
{
  "error": "Error description"
}
```

JSON-RPC errors follow the JSON-RPC 2.0 specification:

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "error": {
    "code": -32000,
    "message": "Error description"
  }
}
```

## Rate Limiting

The server imposes a rate limit of 100 requests per minute per IP address.
When the rate limit is exceeded, the server returns a 429 status code with
a `Retry-After` header indicating the number of seconds to wait before retrying.

## CORS

The server supports CORS with the following headers:

- `Access-Control-Allow-Origin`: Configurable, defaults to `*`
- `Access-Control-Allow-Methods`: `GET, POST, OPTIONS`
- `Access-Control-Allow-Headers`: `Content-Type, Authorization`
- `Access-Control-Max-Age`: `86400` (24 hours)

## Monitoring

The server includes monitoring features that track:

- Request counts and rates
- Error rates
- Resource usage (memory, CPU)
- Authentication attempts

This data is available through the `/api/status` endpoint.
"""
    create_file("docs/api/API.md", api_doc_content)
    
    # Update main README.md
    readme_content = """# 🔒 Secure MCP Server

A production-ready, secure Model Context Protocol (MCP) server for VPS deployment with
enterprise-grade security features.

## 📋 Overview

This package provides a secure implementation of the Model Context Protocol (MCP) server
designed for production deployment on VPS using Dokploy. It includes:

- 🔐 **API Key Authentication** - Bearer token protection
- ⚡ **Rate Limiting** - Configurable requests per IP
- 🛡️ **CORS Protection** - Secure cross-origin policies
- 📊 **Request Monitoring** - Complete audit trail
- 🔍 **Input Validation** - Request sanitization
- 🚫 **Error Protection** - No information disclosure

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/mcp-server.git
cd mcp-server

# Install dependencies
pip install -r requirements.txt
```

### 2. Local Development

```bash
# Generate API key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Start secure server
python -m src.server.secure_server --api-key YOUR_API_KEY

# Test server
curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8443/api/tools
```

### 3. Production Deployment

For detailed deployment instructions, see:

- [📘 Complete Dokploy Guide](./docs/deployment/DOKPLOY_DEPLOYMENT_GUIDE.md)
- [⚡ Quick Start Guide](./docs/deployment/dokploy-quickstart.md)

## 📚 Documentation

- [📖 Documentation Index](./docs/DOCUMENTATION_INDEX.md) - Start here
- [🔒 Security Documentation](./docs/security/SECURITY.md) - Security overview
- [📡 API Reference](./docs/api/API.md) - API documentation
- [🛠️ Troubleshooting](./docs/deployment/dokploy-troubleshooting.md) - Fix issues

## 🏗️ Project Structure

```
mcp-server/
├── src/                   # Application source code
│   ├── server/            # Server implementation
│   ├── tools/             # MCP tools implementation
│   └── utils/             # Utilities
├── config/                # Configuration
├── deployment/            # Deployment files
│   └── dokploy/           # Dokploy VPS deployment
├── docs/                  # Documentation
└── tests/                 # Test suite
```

## 🧪 Testing

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=src
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
"""
    create_file("README.md", readme_content)

    # Migrate tests
    print_step("Migrating tests")
    
    if os.path.exists("test_secure_client.py"):
        copy_file("test_secure_client.py", "tests/integration/test_secure_client.py")
    
    # Create sample unit tests
    test_auth_content = """
\"\"\"Unit tests for authentication module.\"\"\"

import pytest
from src.server.auth import Authentication


def test_generate_key():
    \"\"\"Test API key generation.\"\"\"
    key = Authentication.generate_key()
    assert isinstance(key, str)
    assert len(key) > 16  # Should be reasonably long for security


def test_verify_key():
    \"\"\"Test API key verification.\"\"\"
    auth = Authentication(["valid-key", "another-key"])
    
    # Valid keys
    assert auth.verify_key("valid-key") is True
    assert auth.verify_key("another-key") is True
    
    # Invalid keys
    assert auth.verify_key("invalid-key") is False
    assert auth.verify_key("") is False
    assert auth.verify_key(None) is False


def test_extract_api_key():
    \"\"\"Test API key extraction from Authorization header.\"\"\"
    auth = Authentication(["valid-key"])
    
    # Valid header format
    assert auth.extract_api_key("Bearer valid-key") == "valid-key"
    
    # Invalid header format
    assert auth.extract_api_key("Token valid-key") is None
    assert auth.extract_api_key("valid-key") is None
    assert auth.extract_api_key("") is None
    assert auth.extract_api_key(None) is None


def test_empty_api_keys():
    \"\"\"Test authentication with no API keys.\"\"\"
    auth = Authentication([])
    assert auth.verify_key("any-key") is False
"""
    create_file("tests/unit/test_auth.py", test_auth_content)
    
    test_rate_limiter_content = """
\"\"\"Unit tests for rate limiter module.\"\"\"

import pytest
import time
from src.server.rate_limiter import RateLimiter


def test_check_rate_limit_allowed():
    \"\"\"Test rate limiting when requests are allowed.\"\"\"
    limiter = RateLimiter(limit=5, window=60)
    
    # First request should be allowed
    allowed, retry_after, remaining = limiter.check_rate_limit("client1")
    assert allowed is True
    assert retry_after is None
    assert remaining == 4


def test_check_rate_limit_exceeded():
    \"\"\"Test rate limiting when limit is exceeded.\"\"\"
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
    \"\"\"Test that clients are rate limited separately.\"\"\"
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
    \"\"\"Test clearing of expired entries.\"\"\"
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
"""
    create_file("tests/unit/test_rate_limiter.py", test_rate_limiter_content)
    
    # Create security tests
    test_security_content = """
\"\"\"Security tests for MCP server.\"\"\"

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
    \"\"\"Create a test client with security middleware.\"\"\"
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


async def test_health_endpoint(test_client):
    \"\"\"Test public health endpoint.\"\"\"
    resp = await test_client.get('/health')
    assert resp.status == 200
    data = await resp.json()
    assert data["status"] == "healthy"


async def test_auth_required(test_client):
    \"\"\"Test that protected endpoints require authentication.\"\"\"
    resp = await test_client.get('/protected')
    assert resp.status == 401
    
    resp = await test_client.get('/protected', headers={"Authorization": "Bearer invalid-key"})
    assert resp.status == 401
    
    resp = await test_client.get('/protected', headers={"Authorization": "Bearer test-api-key"})
    assert resp.status == 200


async def test_rate_limiting(test_client):
    \"\"\"Test rate limiting.\"\"\"
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


async def test_rate_limit_headers(test_client):
    \"\"\"Test rate limit headers.\"\"\"
    headers = {"Authorization": "Bearer test-api-key"}
    
    resp = await test_client.get('/protected', headers=headers)
    assert resp.status == 200
    assert "X-RateLimit-Remaining" in resp.headers
    
    remaining = int(resp.headers["X-RateLimit-Remaining"])
    assert remaining < 5  # Should be less than our limit
"""
    create_file("tests/security/test_security.py", test_security_content)

    # Create scripts
    print_step("Creating utility scripts")
    
    # Key generator script
    key_generator_content = """
\"\"\"Generate secure API keys for MCP server.\"\"\"

import secrets
import argparse
import sys


def generate_key(length: int = 32) -> str:
    \"\"\"Generate a secure API key.
    
    Args:
        length: Minimum length of the key in bytes
    
    Returns:
        A secure random API key
    \"\"\"
    return secrets.token_urlsafe(length)


def main():
    \"\"\"Generate API keys based on command line arguments.\"\"\"
    parser = argparse.ArgumentParser(description="Generate secure API keys for MCP server")
    parser.add_argument("-n", "--num-keys", type=int, default=1, 
                       help="Number of keys to generate")
    parser.add_argument("-l", "--length", type=int, default=32,
                       help="Minimum key length in bytes")
    parser.add_argument("-f", "--format", choices=["plain", "env", "json"],
                       default="plain", help="Output format")
    
    args = parser.parse_args()
    
    if args.num_keys < 1:
        print("Number of keys must be at least 1", file=sys.stderr)
        sys.exit(1)
    
    if args.length < 16:
        print("WARNING: Short keys are less secure. Recommended length is 32+.",
             file=sys.stderr)
    
    # Generate keys
    keys = [generate_key(args.length) for _ in range(args.num_keys)]
    
    # Output in specified format
    if args.format == "plain":
        for i, key in enumerate(keys, 1):
            print(f"Key {i}: {key}")
    
    elif args.format == "env":
        print(f"MCP_API_KEYS={','.join(keys)}")
    
    elif args.format == "json":
        import json
        print(json.dumps({"api_keys": keys}, indent=2))


if __name__ == "__main__":
    main()
"""
    create_file("scripts/key_generator.py", key_generator_content)

    # Clean up
    print_step("Cleaning up unused files")
    cleanup_files = [
        "app.py",
        "http_server.py",
        "cloud_server.py",
        "make_global.py"
    ]
    
    for file in cleanup_files:
        if os.path.exists(file):
            print_warning(f"Consider removing: {file}")
    
    # Verify setup
    print_step("Verifying structure")
    
    try:
        # Create a minimal __main__.py for testing
        main_content = """
\"\"\"Entry point for package execution.\"\"\"

if __name__ == "__main__":
    print("Package structure verified successfully!")
"""
        create_file("src/__main__.py", main_content)
        
        # Test importing
        import_success = False
        try:
            sys.path.insert(0, os.path.abspath('.'))
            import src
            import_success = True
        except Exception as e:
            print_error(f"Failed to import package: {e}")
        
        if import_success:
            print_success("Package structure verified successfully!")
        
    except Exception as e:
        print_error(f"Failed to verify structure: {e}")

    # Final message
    print_step("Migration completed")
    print_success("Project structure has been reorganized!")
    print("Next steps:")
    print("1. Review the changes and verify everything works correctly")
    print("2. Update import paths in your source files")
    print("3. Run tests to ensure functionality is preserved")
    print("4. Commit the changes to your repository")


if __name__ == "__main__":
    main()

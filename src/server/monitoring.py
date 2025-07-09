"""Monitoring module for the secure MCP server."""

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
    """Handles monitoring and logging for the secure MCP server."""

    def __init__(self, enabled: bool = True, log_level: str = "INFO"):
        """Initialize the monitoring system.
        
        Args:
            enabled: Whether monitoring is enabled
            log_level: The logging level to use
        """
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
        """Log a request to the monitoring system.
        
        Args:
            client_id: Client identifier (e.g., IP address)
            endpoint: The requested endpoint
            status: HTTP status code of the response
            authenticated: Whether the request was authenticated
            duration: Request processing duration in seconds
        """
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
        """Get system statistics.
        
        Returns:
            Dictionary with system statistics
        """
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
        """Get recent error requests.
        
        Args:
            limit: Maximum number of errors to return
        
        Returns:
            List of error requests
        """
        if not self.enabled:
            return []
            
        errors = [r for r in self.requests if r['status'] >= 400]
        errors.sort(key=lambda x: x['timestamp'], reverse=True)
        return errors[:limit]

    def get_uptime(self) -> float:
        """Get the server uptime in seconds."""
        return time.time() - self.start_time
    
    def print_stats(self):
        """Print monitoring statistics."""
        if not self.enabled:
            return
        
        uptime = self.get_uptime()
        total_requests = len(self.requests)
        memory_usage = self.process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"📊 Server Stats - Uptime: {uptime:.1f}s, Requests: {total_requests}, Memory: {memory_usage:.1f}MB")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get monitoring statistics as a dictionary."""
        if not self.enabled:
            return {}
        
        uptime = self.get_uptime()
        total_requests = len(self.requests)
        memory_usage = self.process.memory_info().rss / 1024 / 1024  # MB
        
        return {
            "uptime": uptime,
            "total_requests": total_requests,
            "memory_usage_mb": memory_usage,
            "start_time": self.start_time
        }

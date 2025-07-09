
"""Tool registry for MCP server."""

from typing import Dict, List, Any, Callable, Optional
import importlib
import os
import sys
import json
import inspect


class ToolRegistry:
    """Registry for MCP tools."""

    def __init__(self):
        """Initialize the tool registry and load available tools."""
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._load_default_tools()
    
    def _load_default_tools(self):
        """Load default tools from the example_tools module."""
        try:
            # Try to import and load example tools
            from .example_tools import AVAILABLE_TOOLS
            
            for tool in AVAILABLE_TOOLS:
                self.register_tool_instance(tool)
                
            print(f"✅ Loaded {len(AVAILABLE_TOOLS)} default tools")
            
        except ImportError as e:
            print(f"⚠️ Could not load default tools: {e}")
        except Exception as e:
            print(f"⚠️ Error loading default tools: {e}")
    
    def register_tool_instance(self, tool_instance):
        """Register a tool instance that has get_schema() and execute() methods.
        
        Args:
            tool_instance: An instance of a tool class with get_schema() and execute() methods
        """
        if not hasattr(tool_instance, 'get_schema') or not hasattr(tool_instance, 'execute'):
            raise ValueError("Tool instance must have get_schema() and execute() methods")
        
        schema = tool_instance.get_schema()
        tool_name = tool_instance.name
        
        self.tools[tool_name] = {
            'name': tool_name,
            'handler': tool_instance.execute,
            'description': tool_instance.description,
            'schema': schema,
            'instance': tool_instance
        }
    
    def register_tool(self, name: str, handler: Callable, description: str, schema: Dict[str, Any]):
        """Register a new tool.
        
        Args:
            name: The name of the tool
            handler: The function that implements the tool
            description: A description of the tool
            schema: The JSON schema for the tool's parameters
        """
        self.tools[name] = {
            'name': name,
            'handler': handler,
            'description': description,
            'schema': schema
        }
    
    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a tool by name.
        
        Args:
            name: The name of the tool
        
        Returns:
            The tool definition or None if not found
        """
        return self.tools.get(name)
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools.
        
        Returns:
            List of tool definitions (without handlers)
        """
        return [
            {
                'name': tool['name'],
                'description': tool['description'],
                'schema': tool['schema']
            }
            for tool in self.tools.values()
        ]
    
    def load_from_directory(self, directory: str) -> int:
        """Load tools from a directory.
        
        Args:
            directory: The directory to load tools from
        
        Returns:
            The number of tools loaded
        """
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
    """Decorator to mark a function as an MCP tool.
    
    Args:
        name: The name of the tool
        description: A description of the tool
        schema: The JSON schema for the tool's parameters
    
    Returns:
        Decorator function
    """
    def decorator(func):
        func._mcp_tool = True
        func._mcp_tool_name = name
        func._mcp_tool_description = description
        func._mcp_tool_schema = schema
        return func
    return decorator

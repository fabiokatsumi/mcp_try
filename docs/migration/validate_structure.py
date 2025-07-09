#!/usr/bin/env python3
"""
Validation script to verify the new project structure and check for import errors
"""

import os
import importlib
import sys
import inspect


def print_status(message, success=True):
    """Print a status message with color coding."""
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")


def check_directory_exists(path):
    """Check if a directory exists."""
    exists = os.path.isdir(path)
    print_status(f"Directory '{path}' exists", success=exists)
    return exists


def check_file_exists(path):
    """Check if a file exists."""
    exists = os.path.isfile(path)
    print_status(f"File '{path}' exists", success=exists)
    return exists


def try_import(module_name):
    """Try to import a module and report success or failure."""
    try:
        module = importlib.import_module(module_name)
        print_status(f"Successfully imported {module_name}")
        return module
    except ImportError as e:
        print_status(f"Failed to import {module_name}: {e}", success=False)
        return None


def check_import_relationships():
    """Check if modules can import each other correctly."""
    # Add the project root to the path to enable imports
    sys.path.insert(0, ".")

    # Check core server modules
    auth = try_import("src.server.auth")
    rate_limiter = try_import("src.server.rate_limiter")
    monitoring = try_import("src.server.monitoring")
    middleware = try_import("src.server.middleware")
    secure_server = try_import("src.server.secure_server")

    # Check tool registry
    registry = try_import("src.tools.registry")

    # Check utility modules
    helpers = try_import("src.utils.helpers")

    # Check configuration module
    config = try_import("config.settings")


def validate_directory_structure():
    """Validate the directory structure."""
    print("\n=== Directory Structure Validation ===\n")
    
    directories = [
        "src",
        "src/server",
        "src/tools",
        "src/tools/implementations",
        "src/utils",
        "config",
        "deployment",
        "deployment/dokploy",
        "deployment/env",
        "docs",
        "docs/deployment",
        "docs/security",
        "docs/api",
        "tests",
        "tests/unit",
        "tests/integration",
        "tests/security",
        "scripts"
    ]
    
    all_exist = True
    for directory in directories:
        if not check_directory_exists(directory):
            all_exist = False
    
    return all_exist


def validate_core_files():
    """Validate core files."""
    print("\n=== Core Files Validation ===\n")
    
    files = [
        "src/server/secure_server.py",
        "src/server/auth.py",
        "src/server/rate_limiter.py",
        "src/server/monitoring.py",
        "src/server/middleware.py",
        "src/tools/registry.py",
        "deployment/dokploy/deploy_dokploy.sh",
        "deployment/dokploy/docker-compose.dokploy.yml",
        "deployment/env/.env.production.template",
        "Dockerfile.production",
        "requirements.txt",
        "README.md"
    ]
    
    all_exist = True
    for file in files:
        if not check_file_exists(file):
            all_exist = False
    
    return all_exist


def main():
    """Run the validation script."""
    print("=== MCP Server Project Structure Validation ===\n")
    
    dir_valid = validate_directory_structure()
    files_valid = validate_core_files()
    
    print("\n=== Import Validation ===\n")
    check_import_relationships()
    
    print("\n=== Validation Summary ===\n")
    if dir_valid:
        print_status("Directory structure is valid")
    else:
        print_status("Directory structure has issues", success=False)
    
    if files_valid:
        print_status("Core files are present")
    else:
        print_status("Some core files are missing", success=False)
    
    print("\nValidation complete!")


if __name__ == "__main__":
    main()

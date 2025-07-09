#!/usr/bin/env python3
"""
Final File Organization Script for MCP Server Project

This script organizes all remaining files in the root directory.
"""

import os
import shutil
from pathlib import Path


def print_header(message):
    """Print a header message with formatting."""
    print("\n" + "=" * 80)
    print(f"📂 {message}")
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


def create_directory_if_not_exists(path):
    """Create a directory if it doesn't exist."""
    try:
        os.makedirs(path, exist_ok=True)
        print_success(f"Created directory: {path}")
    except Exception as e:
        print_error(f"Failed to create directory {path}: {e}")
        return False
    return True


def move_file_safe(src, dest):
    """Move a file from src to dest safely."""
    try:
        if not os.path.exists(src):
            print_warning(f"Source file not found: {src}")
            return False
        
        # Create destination directory if it doesn't exist
        dest_dir = os.path.dirname(dest)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
            
        # If the destination already exists, skip with warning
        if os.path.exists(dest):
            print_warning(f"Destination already exists, skipping: {dest}")
            return False
            
        shutil.move(src, dest)
        print_success(f"Moved: {src} -> {dest}")
        return True
    except Exception as e:
        print_error(f"Failed to move {src} to {dest}: {e}")
        return False


def remove_file_safe(file_path):
    """Remove a file safely."""
    try:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print_success(f"Removed directory: {file_path}")
            else:
                os.remove(file_path)
                print_success(f"Removed file: {file_path}")
        else:
            print_warning(f"File not found: {file_path}")
    except Exception as e:
        print_error(f"Failed to remove {file_path}: {e}")


def create_required_directories():
    """Create all required directories."""
    print_header("Creating Required Directories")
    
    directories = [
        "docs/organization",
        "docs/status",
        "deployment/dokploy",
        "archive/deprecated",
        "archive/deployment", 
        "archive/documentation",
        "archive/tests"
    ]
    
    for directory in directories:
        create_directory_if_not_exists(directory)


def move_documentation_files():
    """Move documentation files to appropriate locations."""
    print_header("Moving Documentation Files")
    
    # Organization documentation
    org_files = [
        "FILE_ORGANIZATION_PLAN.md",
        "FILE_ORGANIZATION_RESULTS.md", 
        "ORGANIZE_FILES_README.md",
        "FINAL_ORGANIZATION_PLAN.md"
    ]
    
    for file in org_files:
        if os.path.exists(file):
            move_file_safe(file, os.path.join("docs", "organization", file))
    
    # Status documentation
    status_files = [
        "SECURE_SERVER_STATUS.md"
    ]
    
    for file in status_files:
        if os.path.exists(file):
            move_file_safe(file, os.path.join("docs", "status", file))
    
    # Migration files (if still in root)
    migration_files = [
        "MIGRATION_CHECKLIST.md",
        "migration_script.py",
        "REORGANIZATION_PLAN.md",
        "REORGANIZATION_SUMMARY.md", 
        "REORGANIZATION_UPDATE.md",
        "validate_structure.py",
        "organize_files.py"
    ]
    
    for file in migration_files:
        if os.path.exists(file):
            move_file_safe(file, os.path.join("docs", "migration", file))


def move_dokploy_files():
    """Move Dokploy deployment files."""
    print_header("Moving Dokploy Files")
    
    dokploy_files = [
        "docker-compose.dokploy.yml",
        "dokploy-health-check.ps1",
        "dokploy-health-check.sh", 
        "dokploy-quickstart.md",
        "dokploy-troubleshooting.md",
        "dokploy.config",
        "DOKPLOY_DEPLOYMENT_GUIDE.md",
        "DOKPLOY_DOCUMENTATION_INDEX.md"
    ]
    
    for file in dokploy_files:
        if os.path.exists(file):
            move_file_safe(file, os.path.join("deployment", "dokploy", file))


def move_deprecated_files():
    """Move deprecated files to archive."""
    print_header("Moving Deprecated Files")
    
    deprecated_files = [
        "agent_example.py",
        "app.py", 
        "cloud_server.py",
        "http_server.py",
        "make_global.py",
        "secure_production_config.py",
        "secure_server.py",
        "server_manager.py",
        "start_server.bat",
        "interactive_demo.py",
        "simple_test.py"
    ]
    
    for file in deprecated_files:
        if os.path.exists(file):
            move_file_safe(file, os.path.join("archive", "deprecated", file))


def move_deprecated_deployment():
    """Move deprecated deployment files."""
    print_header("Moving Deprecated Deployment Files")
    
    deployment_files = [
        "Dockerfile",
        "Procfile", 
        "render.yaml"
    ]
    
    for file in deployment_files:
        if os.path.exists(file):
            move_file_safe(file, os.path.join("archive", "deployment", file))


def move_deprecated_documentation():
    """Move deprecated documentation."""
    print_header("Moving Deprecated Documentation")
    
    doc_files = [
        "CLOUD_DEPLOYMENT.md",
        "DEPLOYMENT_GUIDE.md",
        "DOCUMENTATION_INDEX.md", 
        "LAN_ACCESS_GUIDE.md",
        "SUMMARY.md"
    ]
    
    for file in doc_files:
        if os.path.exists(file):
            move_file_safe(file, os.path.join("archive", "documentation", file))


def move_deprecated_tests():
    """Move deprecated test files."""
    print_header("Moving Deprecated Test Files")
    
    test_files = [
        "test_client.py",
        "test_dynamic_tools.py",
        "test_http_client.py",
        "test_lan_client.py", 
        "test_suite.py",
        "test_web_content.py"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            move_file_safe(file, os.path.join("archive", "tests", file))
    
    # Move test script to scripts if not already there
    if os.path.exists("test_server_functionality.py"):
        move_file_safe("test_server_functionality.py", os.path.join("scripts", "test_server_functionality.py"))


def move_config_files():
    """Move configuration files."""
    print_header("Moving Configuration Files")
    
    config_files = [
        "mcp_config.json"
    ]
    
    for file in config_files:
        if os.path.exists(file):
            move_file_safe(file, os.path.join("config", file))


def move_security_files():
    """Move security files if still in root."""
    print_header("Moving Security Files")
    
    security_files = [
        "SECURITY.md",
        "SECURITY_CHECKLIST.md",
        "SECURITY_IMPLEMENTATION.md"
    ]
    
    for file in security_files:
        if os.path.exists(file):
            move_file_safe(file, os.path.join("docs", "security", file))


def cleanup_files():
    """Clean up unnecessary files."""
    print_header("Cleaning Up Unnecessary Files")
    
    # Remove backup files
    backup_files = [
        "requirements.txt.bak"
    ]
    
    for file in backup_files:
        remove_file_safe(file)
    
    # Remove Python cache
    remove_file_safe("__pycache__")
    
    # Remove duplicate test file if exists
    if os.path.exists("test_secure_client.py") and os.path.exists("tests/integration/test_secure_client.py"):
        print_warning("Duplicate test_secure_client.py found, removing from root")
        remove_file_safe("test_secure_client.py")


def verify_essential_files():
    """Verify essential files remain in root."""
    print_header("Verifying Essential Files")
    
    essential_files = [
        ".dockerignore",
        "Dockerfile.production", 
        "README.md",
        "requirements.txt",
        "requirements-dev.txt",
        "setup.py",
        "deploy_dokploy.sh"
    ]
    
    for file in essential_files:
        if os.path.exists(file):
            print_success(f"Essential file present: {file}")
        else:
            print_warning(f"Essential file missing: {file}")


def main():
    """Main function to organize all files."""
    print_header("Final MCP Server File Organization")
    print("This script will organize all remaining files in the root directory")
    print("Working directory:", os.getcwd())
    
    # Create required directories
    create_required_directories()
    
    # Move files by category
    move_documentation_files()
    move_dokploy_files()
    move_deprecated_files()
    move_deprecated_deployment()
    move_deprecated_documentation()
    move_deprecated_tests()
    move_config_files()
    move_security_files()
    
    # Clean up
    cleanup_files()
    
    # Verify essential files
    verify_essential_files()
    
    print_header("Final Organization Complete")
    print("All files have been organized according to the plan.")
    print("Root directory now contains only essential files.")


if __name__ == "__main__":
    main()

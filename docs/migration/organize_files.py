#!/usr/bin/env python3
"""
File Organization Script for MCP Server Project

This script implements the file organization plan documented in FILE_ORGANIZATION_PLAN.md.
It moves files from the root directory to appropriate subdirectories.
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


def move_file(src, dest):
    """Move a file from src to dest."""
    try:
        if not os.path.exists(src):
            print_warning(f"Source file not found: {src}")
            return False
        
        # Create destination directory if it doesn't exist
        dest_dir = os.path.dirname(dest)
        if dest_dir and not os.path.exists(dest_dir):
            os.makedirs(dest_dir, exist_ok=True)
            
        # If the destination already exists, warn and skip
        if os.path.exists(dest):
            print_warning(f"Destination already exists, skipping: {dest}")
            return False
            
        shutil.move(src, dest)
        print_success(f"Moved: {src} -> {dest}")
        return True
    except Exception as e:
        print_error(f"Failed to move {src} to {dest}: {e}")
        return False


def create_directories():
    """Create all required directories."""
    print_header("Creating Directories")
    
    directories = [
        "archive/deprecated",
        "archive/tests",
        "archive/deployment",
        "archive/documentation",
        "docs/migration",
        "examples",
        "scripts"
    ]
    
    for directory in directories:
        create_directory_if_not_exists(directory)


def move_to_docs_migration():
    """Move files to docs/migration directory."""
    print_header("Moving Files to docs/migration")
    
    files_to_move = [
        "MIGRATION_CHECKLIST.md",
        "migration_script.py",
        "REORGANIZATION_PLAN.md",
        "REORGANIZATION_SUMMARY.md",
        "REORGANIZATION_UPDATE.md",
        "validate_structure.py"
    ]
    
    for file in files_to_move:
        if os.path.exists(file):
            move_file(file, os.path.join("docs", "migration", file))


def move_to_examples():
    """Move files to examples directory."""
    print_header("Moving Files to examples")
    
    files_to_move = [
        "agent_example.py",
        "agent_test.txt",
        "interactive_demo.py",
        "simple_test.py"
    ]
    
    for file in files_to_move:
        if os.path.exists(file):
            move_file(file, os.path.join("examples", file))


def move_to_archive_deprecated():
    """Move files to archive/deprecated directory."""
    print_header("Moving Files to archive/deprecated")
    
    files_to_move = [
        "app.py",
        "cloud_server.py",
        "http_server.py",
        "make_global.py",
        "server_manager.py",
        "start_server.bat",
        "secure_production_config.py"
    ]
    
    for file in files_to_move:
        if os.path.exists(file):
            move_file(file, os.path.join("archive", "deprecated", file))


def move_to_archive_tests():
    """Move files to archive/tests directory."""
    print_header("Moving Files to archive/tests")
    
    files_to_move = [
        "test_client.py",
        "test_dynamic_tools.py",
        "test_http_client.py",
        "test_lan_client.py",
        "test_web_content.py",
        "test_suite.py"
    ]
    
    for file in files_to_move:
        if os.path.exists(file):
            move_file(file, os.path.join("archive", "tests", file))


def move_to_archive_deployment():
    """Move files to archive/deployment directory."""
    print_header("Moving Files to archive/deployment")
    
    files_to_move = [
        "deployment_.env.template",
        "deployment_cloud-run-service.yaml",
        "deployment_k8s-deployment.yaml",
        "deployment_Procfile",
        "deployment_railway_start.sh",
        "Dockerfile",
        "Procfile",
        "render.yaml"
    ]
    
    for file in files_to_move:
        if os.path.exists(file):
            move_file(file, os.path.join("archive", "deployment", file))


def move_to_archive_documentation():
    """Move files to archive/documentation directory."""
    print_header("Moving Files to archive/documentation")
    
    files_to_move = [
        "CLOUD_DEPLOYMENT.md",
        "DEPLOYMENT_GUIDE.md",
        "LAN_ACCESS_GUIDE.md",
        "SUMMARY.md",
        "DOCUMENTATION_INDEX.md"
    ]
    
    for file in files_to_move:
        if os.path.exists(file):
            move_file(file, os.path.join("archive", "documentation", file))
    
    # Move contents of documentation/ directory if it exists
    if os.path.exists("documentation") and os.path.isdir("documentation"):
        for file in os.listdir("documentation"):
            src = os.path.join("documentation", file)
            dest = os.path.join("archive", "documentation", file)
            move_file(src, dest)


def move_to_scripts():
    """Move files to scripts directory."""
    print_header("Moving Files to scripts")
    
    if os.path.exists("test_deployment.sh"):
        move_file("test_deployment.sh", os.path.join("scripts", "test_deployment.sh"))
    
    # Move contents of testing/ directory if it exists
    if os.path.exists("testing") and os.path.isdir("testing"):
        for file in os.listdir("testing"):
            src = os.path.join("testing", file)
            dest = os.path.join("scripts", file)
            move_file(src, dest)


def move_to_config():
    """Move files to config directory."""
    print_header("Moving Files to config")
    
    if os.path.exists("secure_production_config.json"):
        move_file("secure_production_config.json", os.path.join("config", "secure_production_config.json"))


def remove_empty_directories():
    """Remove any empty directories."""
    print_header("Removing Empty Directories")
    
    directories_to_check = [
        "documentation",
        "testing"
    ]
    
    for directory in directories_to_check:
        if os.path.exists(directory) and os.path.isdir(directory) and not os.listdir(directory):
            try:
                os.rmdir(directory)
                print_success(f"Removed empty directory: {directory}")
            except Exception as e:
                print_error(f"Failed to remove directory {directory}: {e}")


def main():
    """Main function to organize files."""
    print_header("MCP Server File Organization")
    print("This script will organize files according to FILE_ORGANIZATION_PLAN.md")
    print("Working directory:", os.getcwd())
    
    # Create directories
    create_directories()
    
    # Move files in phases
    move_to_docs_migration()
    move_to_examples()
    move_to_archive_deprecated()
    move_to_archive_tests()
    move_to_archive_deployment()
    move_to_archive_documentation()
    move_to_scripts()
    move_to_config()
    
    # Clean up
    remove_empty_directories()
    
    print_header("Organization Complete")
    print("Files have been organized according to the plan.")
    print("Please check for any issues and update import paths if needed.")


if __name__ == "__main__":
    main()

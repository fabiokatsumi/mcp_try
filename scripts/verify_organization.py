#!/usr/bin/env python3
"""
Final Verification Script - MCP Server Project

This script verifies that the project is properly organized and ready for production.
"""

import os
import sys
from pathlib import Path


def print_header(message):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"🔍 {message}")
    print("=" * 80)


def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")


def print_warning(message):
    """Print a warning message."""
    print(f"⚠️  {message}")


def print_error(message):
    """Print an error message."""
    print(f"❌ {message}")


def check_essential_files():
    """Check that essential root files exist."""
    print_header("Checking Essential Root Files")
    
    essential_files = [
        "README.md",
        "requirements.txt",
        "requirements-dev.txt",
        "setup.py",
        "Dockerfile.production",
        "deploy_dokploy.sh",
        ".dockerignore"
    ]
    
    missing_files = []
    for file in essential_files:
        if os.path.exists(file):
            print_success(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            missing_files.append(file)
    
    if not missing_files:
        print_success("All essential files present")
    
    return len(missing_files) == 0


def check_directory_structure():
    """Check that the expected directory structure exists."""
    print_header("Checking Directory Structure")
    
    expected_dirs = [
        "src",
        "src/server",
        "src/tools",
        "src/utils",
        "config",
        "deployment",
        "deployment/dokploy",
        "deployment/env",
        "docs",
        "docs/api",
        "docs/deployment",
        "docs/security",
        "tests",
        "tests/unit",
        "tests/integration",
        "tests/security",
        "scripts",
        "examples",
        "archive"
    ]
    
    missing_dirs = []
    for dir_path in expected_dirs:
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            print_success(f"Found directory: {dir_path}")
        else:
            print_error(f"Missing directory: {dir_path}")
            missing_dirs.append(dir_path)
    
    if not missing_dirs:
        print_success("All expected directories present")
    
    return len(missing_dirs) == 0


def check_core_source_files():
    """Check that core source files exist."""
    print_header("Checking Core Source Files")
    
    core_files = [
        "src/__init__.py",
        "src/__main__.py",
        "src/server.py",
        "src/server/__init__.py",
        "src/server/secure_server.py",
        "src/server/auth.py",
        "src/server/middleware.py",
        "src/server/rate_limiter.py",
        "src/tools/__init__.py",
        "src/tools/registry.py",
        "src/utils/__init__.py",
        "src/utils/helpers.py"
    ]
    
    missing_files = []
    for file in core_files:
        if os.path.exists(file):
            print_success(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            missing_files.append(file)
    
    if not missing_files:
        print_success("All core source files present")
    
    return len(missing_files) == 0


def check_configuration_files():
    """Check that configuration files exist."""
    print_header("Checking Configuration Files")
    
    config_files = [
        "config/__init__.py",
        "config/settings.py",
        "config/mcp_config.json"
    ]
    
    missing_files = []
    for file in config_files:
        if os.path.exists(file):
            print_success(f"Found: {file}")
        else:
            print_error(f"Missing: {file}")
            missing_files.append(file)
    
    if not missing_files:
        print_success("All configuration files present")
    
    return len(missing_files) == 0


def check_deployment_files():
    """Check that deployment files exist."""
    print_header("Checking Deployment Files")
    
    deployment_files = [
        "deployment/dokploy/docker-compose.dokploy.yml",
        "deployment/dokploy/DOKPLOY_DEPLOYMENT_GUIDE.md",
        "deployment/env/.env.example"
    ]
    
    missing_files = []
    for file in deployment_files:
        if os.path.exists(file):
            print_success(f"Found: {file}")
        else:
            print_warning(f"Missing: {file}")
            missing_files.append(file)
    
    if not missing_files:
        print_success("All deployment files present")
    
    return len(missing_files) == 0


def check_test_files():
    """Check that test files exist."""
    print_header("Checking Test Files")
    
    test_files = [
        "tests/__init__.py",
        "tests/unit/__init__.py",
        "tests/integration/__init__.py",
        "tests/security/__init__.py"
    ]
    
    missing_files = []
    for file in test_files:
        if os.path.exists(file):
            print_success(f"Found: {file}")
        else:
            print_warning(f"Missing: {file}")
            missing_files.append(file)
    
    if not missing_files:
        print_success("All test files present")
    
    return len(missing_files) == 0


def check_documentation():
    """Check that documentation exists."""
    print_header("Checking Documentation")
    
    doc_files = [
        "docs/DOCUMENTATION_INDEX.md",
        "docs/api/API.md",
        "docs/security/SECURITY.md"
    ]
    
    missing_files = []
    for file in doc_files:
        if os.path.exists(file):
            print_success(f"Found: {file}")
        else:
            print_warning(f"Missing: {file}")
            missing_files.append(file)
    
    if not missing_files:
        print_success("All documentation files present")
    
    return len(missing_files) == 0


def check_no_unwanted_files():
    """Check that unwanted files are not in root."""
    print_header("Checking for Unwanted Files in Root")
    
    # Files that should NOT be in root
    unwanted_patterns = [
        "*.pyc",
        "__pycache__",
        "*.tmp",
        "*.log",
        "test_*.py",
        "*_test.py"
    ]
    
    unwanted_found = []
    for item in os.listdir('.'):
        if os.path.isfile(item):
            # Check specific patterns
            if any(item.endswith(pattern.replace('*', '')) for pattern in unwanted_patterns if not pattern.startswith('__')):
                unwanted_found.append(item)
            elif item.startswith('test_') or item.endswith('_test.py'):
                unwanted_found.append(item)
        elif item == "__pycache__":
            unwanted_found.append(item)
    
    if unwanted_found:
        for item in unwanted_found:
            print_warning(f"Unwanted file in root: {item}")
    else:
        print_success("No unwanted files in root directory")
    
    return len(unwanted_found) == 0


def verify_imports():
    """Verify that key imports work."""
    print_header("Verifying Key Imports")
    
    imports_to_test = [
        ("src.server.secure_server", "SecureMCPServer"),
        ("src.tools.registry", "ToolRegistry"),
        ("src.utils.helpers", None),
        ("config.settings", None)
    ]
    
    import_errors = []
    original_path = sys.path.copy()
    
    try:
        # Add current directory to Python path
        if '.' not in sys.path:
            sys.path.insert(0, '.')
        
        for module_name, class_name in imports_to_test:
            try:
                module = __import__(module_name, fromlist=[class_name] if class_name else [''])
                if class_name:
                    getattr(module, class_name)
                print_success(f"Import successful: {module_name}")
            except ImportError as e:
                print_error(f"Import failed: {module_name} - {e}")
                import_errors.append(module_name)
            except Exception as e:
                print_warning(f"Import warning: {module_name} - {e}")
    
    finally:
        # Restore original Python path
        sys.path = original_path
    
    if not import_errors:
        print_success("All key imports working")
    
    return len(import_errors) == 0


def main():
    """Run all verification checks."""
    print_header("MCP Server Project - Final Verification")
    print("Verifying project organization and production readiness...")
    
    checks = [
        ("Essential Files", check_essential_files),
        ("Directory Structure", check_directory_structure),
        ("Core Source Files", check_core_source_files),
        ("Configuration Files", check_configuration_files),
        ("Deployment Files", check_deployment_files),
        ("Test Files", check_test_files),
        ("Documentation", check_documentation),
        ("No Unwanted Files", check_no_unwanted_files),
        ("Import Verification", verify_imports)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print_error(f"Check '{check_name}' failed with error: {e}")
            results.append((check_name, False))
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        if result:
            print_success(f"{check_name}: PASSED")
        else:
            print_error(f"{check_name}: FAILED")
    
    print(f"\n📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print_success("🎉 Project is ready for production deployment!")
        return 0
    else:
        print_error("❌ Project needs attention before deployment")
        return 1


if __name__ == "__main__":
    exit(main())

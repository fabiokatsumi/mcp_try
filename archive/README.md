# Archive Directory

This directory contains deprecated and legacy files from the MCP Server project.

## Subdirectories

### deprecated/
Contains old server implementations and utilities that have been superseded:
- Old HTTP servers (http_server.py, cloud_server.py)
- Legacy deployment files
- Deprecated test scripts

### legacy/
Contains the original project files for historical reference:
- app.py - Original MCP server implementation (superseded by src/server/secure_server.py)

### documentation/
Contains outdated documentation that has been replaced by the current docs/ structure.

### tests/
Contains deprecated test files that have been replaced by the current test framework.

### empty_files/
Contains empty files (0 bytes) from the initial cleanup:
- All files moved here were completely empty and provided no functionality
- Preserved for historical reference and project evolution tracking
- Total empty files archived: 45+ files

### empty_files_new/
Contains empty files found during the latest cleanup scan (July 8, 2025):
- cleanup_root.py - Empty organization script
- final_organize.py - Empty organization script  
- CLOUD_DEPLOYMENT.md - Empty documentation file (content now in docs/deployment/)
- FINAL_ORGANIZATION_PLAN.md - Empty organization plan
- dokploy-quickstart.md - Empty deployment guide (now has content)
- dokploy-troubleshooting.md - Empty troubleshooting guide (now has content)
- dokploy.config - Empty configuration file (now has content)
- DOKPLOY_DEPLOYMENT_GUIDE.md - Empty deployment guide (now has content)
- DOKPLOY_DOCUMENTATION_INDEX.md - Empty documentation index
- API.md - Empty API documentation (now has content)
- Various setup and GitHub files that were duplicated or unused

## Purpose

These files are preserved for:
- Historical reference
- Understanding project evolution
- Potential code reuse or comparison
- Maintaining complete project history

All active development should use the files in the main project structure.

## Note

`__init__.py` files are kept in their original locations as they are required for Python package structure, even if empty.
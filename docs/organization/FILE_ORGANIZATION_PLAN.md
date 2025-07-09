# 📂 MCP Server File Organization Plan

This document outlines a plan to organize all files in the MCP Server project root directory. The goal is to have only essential files in the root folder while moving everything else to appropriate subdirectories.

## 🗂️ Current Situation

The project root currently contains many files that should be properly organized according to their purpose and usage status.

## 🔄 Organization Strategy

Files will be organized into the following categories:

### 1️⃣ Essential Root Files (Stay in Root)

These files should remain in the project root as they're essential for project identification, building, or dependency management:

- `README.md` - Project introduction and documentation entry point
- `Dockerfile.production` - Production Docker configuration
- `.dockerignore` - Docker build optimization
- `requirements.txt` - Production dependencies
- `requirements-dev.txt` - Development dependencies
- `setup.py` - Python package installation
- `pyproject.toml` (if exists) - Python packaging configuration
- `.gitignore` - Git exclusion rules

### 2️⃣ Source Code (`src/` Directory)

All source code should be in the `src/` directory, properly organized into:

- `src/server/` - Server implementation
- `src/tools/` - MCP tools
- `src/utils/` - Utility functions

### 3️⃣ Configuration (`config/` Directory)

Configuration files should be in the `config/` directory:

- `config/mcp_config.json` - Server configuration
- `config/settings.py` - Settings loader

### 4️⃣ Documentation (`docs/` Directory)

Documentation files should be in the `docs/` directory:

- `docs/api/` - API documentation
- `docs/security/` - Security documentation
- `docs/deployment/` - Deployment guides
- `docs/migration/` - Project reorganization documents

### 5️⃣ Tests (`tests/` Directory)

Test files should be in the `tests/` directory:

- `tests/unit/` - Unit tests
- `tests/integration/` - Integration tests
- `tests/security/` - Security tests

### 6️⃣ Deployment (`deployment/` Directory)

Deployment-related files should be in the `deployment/` directory:

- `deployment/dokploy/` - Dokploy deployment files
- `deployment/env/` - Environment templates

### 7️⃣ Examples (`examples/` Directory)

Example code should be in the `examples/` directory:

- Example clients
- Demo scripts
- Tutorial code

### 8️⃣ Scripts (`scripts/` Directory)

Utility scripts should be in the `scripts/` directory:

- API key generators
- Testing scripts
- Deployment helpers

### 9️⃣ Archive (`archive/` Directory)

Deprecated or unused files should be archived for reference:

- `archive/deprecated/` - Old server implementations
- `archive/deployment/` - Old deployment configs
- `archive/documentation/` - Old documentation
- `archive/tests/` - Old test files

## 📋 File Movement Plan

The following files need to be moved:

### To Move to `docs/migration/`

- `MIGRATION_CHECKLIST.md`
- `migration_script.py`
- `REORGANIZATION_PLAN.md`
- `REORGANIZATION_SUMMARY.md`
- `REORGANIZATION_UPDATE.md`
- `validate_structure.py`

### To Move to `examples/`

- `agent_example.py`
- `agent_test.txt`
- `interactive_demo.py`
- `simple_test.py`

### To Move to `archive/deprecated/`

- `app.py` - Old server implementation
- `cloud_server.py` - Old server implementation
- `http_server.py` - Old server implementation
- `make_global.py` - Old server utility
- `server_manager.py` - Old server utility
- `start_server.bat` - Old server script
- `secure_production_config.py` - Old config loader

### To Move to `archive/tests/`

- `test_client.py` - Old test client
- `test_dynamic_tools.py` - Old test script
- `test_http_client.py` - Old test client
- `test_lan_client.py` - Old test client
- `test_web_content.py` - Old test script
- `test_suite.py` - Old test suite

### To Move to `archive/deployment/`

- `deployment_.env.template` - Old environment template
- `deployment_cloud-run-service.yaml` - Old cloud deployment
- `deployment_k8s-deployment.yaml` - Old Kubernetes deployment
- `deployment_Procfile` - Old Procfile
- `deployment_railway_start.sh` - Old railway script
- `Dockerfile` - Old Dockerfile
- `Procfile` - Old Procfile
- `render.yaml` - Old render configuration

### To Move to `archive/documentation/`

- `CLOUD_DEPLOYMENT.md` - Old cloud deployment guide
- `DEPLOYMENT_GUIDE.md` - Old deployment guide
- `LAN_ACCESS_GUIDE.md` - Old LAN guide
- `SUMMARY.md` - Old summary
- `DOCUMENTATION_INDEX.md` - Old documentation index
- Contents of `documentation/` directory

### To Move to `scripts/`

- `test_deployment.sh` - Deployment test script
- Contents of `testing/` directory (if they're utility scripts)

### To Move to `config/`

- `secure_production_config.json` - Configuration file

## 💻 Execution Plan

1. **Create Missing Directories**
   - Create `archive/deprecated`
   - Create `archive/tests`
   - Create `archive/deployment`
   - Create `archive/documentation`
   - Create `docs/migration`

2. **Move Files in Phases**
   - First move non-critical files (docs, examples, archive)
   - Then move test files
   - Then move deployment files
   - Finally move any remaining files

3. **Update References**
   - Update any references to moved files in documentation
   - Update import statements in code

4. **Clean Up**
   - Remove empty directories
   - Remove duplicate files

## 🚀 Future Maintenance Rules

To maintain this organization:

1. All new source code goes in the appropriate `src/` subdirectory
2. All new tests go in the appropriate `tests/` subdirectory
3. All new documentation goes in the appropriate `docs/` subdirectory
4. All new deployment files go in the appropriate `deployment/` subdirectory
5. Only essential files remain in the root directory

# 📦 MCP Server Migration Checklist

Use this checklist to track progress as you implement the project reorganization.

## 🗂️ Directory Structure

- [ ] Create root directories
  - [ ] `src/`
  - [ ] `config/`
  - [ ] `deployment/`
  - [ ] `docs/`
  - [ ] `tests/`
  - [ ] `scripts/`

- [ ] Create subdirectories
  - [ ] `src/server/`
  - [ ] `src/tools/`
  - [ ] `src/utils/`
  - [ ] `src/tools/implementations/`
  - [ ] `deployment/dokploy/`
  - [ ] `deployment/env/`
  - [ ] `docs/deployment/`
  - [ ] `docs/security/`
  - [ ] `docs/api/`
  - [ ] `tests/unit/`
  - [ ] `tests/integration/`
  - [ ] `tests/security/`

- [ ] Create package markers
  - [ ] `src/__init__.py`
  - [ ] `src/server/__init__.py`
  - [ ] `src/tools/__init__.py`
  - [ ] `src/utils/__init__.py`
  - [ ] `src/tools/implementations/__init__.py`
  - [ ] `config/__init__.py`
  - [ ] `tests/__init__.py`
  - [ ] `tests/unit/__init__.py`
  - [ ] `tests/integration/__init__.py`
  - [ ] `tests/security/__init__.py`

## 📄 File Migration

### Core Server Files

- [ ] Secure Server
  - [ ] Move `secure_server.py` → `src/server/secure_server.py`
  - [ ] Extract authentication to `src/server/auth.py`
  - [ ] Extract rate limiting to `src/server/rate_limiter.py`
  - [ ] Extract monitoring to `src/server/monitoring.py`
  - [ ] Create `src/server/middleware.py`

- [ ] Tools
  - [ ] Create `src/tools/registry.py`
  - [ ] Move tool implementations to `src/tools/implementations/`

- [ ] Utilities
  - [ ] Create `src/utils/helpers.py`

### Configuration Files

- [ ] Move `secure_production_config.py` logic to `config/settings.py`
- [ ] Move `mcp_config.json` to `config/mcp_config.json`
- [ ] Create `.env.example`
- [ ] Create `.env.production.template`

### Deployment Files

- [ ] Move Dokploy Files
  - [ ] `Dockerfile.production` → `deployment/dokploy/Dockerfile.production`
  - [ ] `dokploy.config` → `deployment/dokploy/dokploy.config`
  - [ ] `docker-compose.dokploy.yml` → `deployment/dokploy/docker-compose.dokploy.yml`
  - [ ] `deploy_dokploy.sh` → `deployment/dokploy/deploy_dokploy.sh`
  - [ ] `dokploy-health-check.sh` → `deployment/dokploy/dokploy-health-check.sh`
  - [ ] `dokploy-health-check.ps1` → `deployment/dokploy/dokploy-health-check.ps1`

- [ ] Project Root Files
  - [ ] Create `.dockerignore`
  - [ ] Update `.gitignore`
  - [ ] Create root `Dockerfile.production` (simplified)
  - [ ] Update `requirements.txt`
  - [ ] Create `requirements-dev.txt`
  - [ ] Create `setup.py`

### Documentation

- [ ] Move VPS Deployment Docs
  - [ ] `DOKPLOY_DEPLOYMENT_GUIDE.md` → `docs/deployment/DOKPLOY_DEPLOYMENT_GUIDE.md`
  - [ ] `dokploy-quickstart.md` → `docs/deployment/dokploy-quickstart.md`
  - [ ] `dokploy-troubleshooting.md` → `docs/deployment/dokploy-troubleshooting.md`

- [ ] Move Security Docs
  - [ ] `SECURITY.md` → `docs/security/SECURITY.md`
  - [ ] `SECURITY_IMPLEMENTATION.md` → `docs/security/SECURITY_IMPLEMENTATION.md`
  - [ ] `SECURITY_CHECKLIST.md` → `docs/security/SECURITY_CHECKLIST.md`

- [ ] Other Documentation
  - [ ] Update `DOCUMENTATION_INDEX.md` → `docs/DOCUMENTATION_INDEX.md`
  - [ ] Create API documentation in `docs/api/API.md`
  - [ ] Update main `README.md` with new structure

### Tests

- [ ] Move and Update Tests
  - [ ] `test_secure_client.py` → `tests/integration/test_secure_client.py`
  - [ ] Security tests → `tests/security/`
  - [ ] Create unit tests in `tests/unit/`

### Scripts

- [ ] Create/Move Scripts
  - [ ] Extract key generation to `scripts/key_generator.py`
  - [ ] Move `test_deployment.sh` → `scripts/test_deployment.sh`

## 🧹 Cleanup

- [ ] Remove Unused Servers
  - [ ] `app.py`
  - [ ] `http_server.py`
  - [ ] `cloud_server.py`

- [ ] Remove Unused Deployment Files
  - [ ] Non-Dokploy deployment files

- [ ] Mark or Remove Alternative Docs
  - [ ] Legacy deployment documentation

## ✅ Verification

- [ ] Structure Verification
  - [ ] Import test: `python -c "import src"`
  - [ ] Verify directory structure matches plan

- [ ] Test Suite
  - [ ] Run all tests
  - [ ] Verify all tests pass

- [ ] Documentation Check
  - [ ] Verify all links work
  - [ ] Check for path references

- [ ] Deployment Test
  - [ ] Test Docker build
  - [ ] Test deployment scripts
  - [ ] Verify Dokploy setup works

## 📝 Final Steps

- [ ] Update README with new structure
- [ ] Document any deviations from original plan
- [ ] Create migration notes for team members
- [ ] Tag new structure version in Git

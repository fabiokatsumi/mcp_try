#!/usr/bin/env python3
"""
Secure Cloud Server Configuration 🔒
Production-ready MCP server with enhanced security for cloud deployment.
"""

import os
import sys
import json
import secrets
import logging
from datetime import datetime

# Production security configurations
SECURITY_CONFIG = {
    "api_key_length": 32,
    "rate_limit_per_minute": 100,
    "max_file_size_mb": 10,
    "allowed_file_extensions": [".txt", ".json", ".csv", ".log", ".md"],
    "restricted_directories": ["/etc", "/var", "/usr", "/bin", "/sbin", "/root"],
    "session_timeout_minutes": 60,
    "enable_request_logging": True,
    "enable_cors": True,
    "enforce_https": True
}

def generate_production_config():
    """Generate production configuration with secure defaults"""
    config = {
        "server": {
            "name": "Secure MCP Server",
            "version": "1.0.0",
            "environment": "production",
            "port": int(os.environ.get("PORT", 8443)),
            "host": "0.0.0.0"
        },
        "security": SECURITY_CONFIG,
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s [%(levelname)s] %(message)s",
            "file": "mcp_server.log"
        },
        "mcp": {
            "protocol_version": "2024-11-05",
            "max_request_size": 1048576,  # 1MB
            "timeout_seconds": 30
        }
    }
    
    return config

def setup_production_logging():
    """Setup production logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler('mcp_server.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Create logger
    logger = logging.getLogger('secure_mcp_server')
    return logger

def validate_environment():
    """Validate production environment variables"""
    required_vars = []
    optional_vars = {
        "MCP_API_KEYS": "Comma-separated list of API keys",
        "PORT": "Server port (default: 8443)",
        "MCP_LOG_LEVEL": "Logging level (default: INFO)",
        "MCP_ENABLE_MONITORING": "Enable monitoring (default: false)"
    }
    
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    print("✅ Environment validation passed!")
    print("\nOptional environment variables:")
    for var, description in optional_vars.items():
        value = os.environ.get(var, "Not set")
        print(f"   - {var}: {value} ({description})")
    
    return True

def generate_deployment_files():
    """Generate deployment files for various cloud platforms"""
    
    # Heroku Procfile
    procfile_content = "web: python secure_server.py --port $PORT --env-keys"
    
    # Railway/Render start command
    railway_start = "python secure_server.py --port $PORT --env-keys"
    
    # Docker environment file template
    docker_env = """# Secure MCP Server Environment Variables
MCP_API_KEYS=your-secure-api-key-here
PORT=8443
MCP_LOG_LEVEL=INFO
MCP_ENABLE_MONITORING=true
"""
    
    # Kubernetes deployment template
    k8s_deployment = """apiVersion: apps/v1
kind: Deployment
metadata:
  name: secure-mcp-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: secure-mcp-server
  template:
    metadata:
      labels:
        app: secure-mcp-server
    spec:
      containers:
      - name: mcp-server
        image: your-registry/secure-mcp-server:latest
        ports:
        - containerPort: 8443
        env:
        - name: MCP_API_KEYS
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: api-keys
        - name: PORT
          value: "8443"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
---
apiVersion: v1
kind: Service
metadata:
  name: secure-mcp-service
spec:
  selector:
    app: secure-mcp-server
  ports:
  - port: 80
    targetPort: 8443
  type: LoadBalancer
"""
    
    # Google Cloud Run service.yaml
    cloud_run_config = """apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: secure-mcp-server
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/cpu-throttling: "false"
    spec:
      containerConcurrency: 100
      containers:
      - image: gcr.io/PROJECT_ID/secure-mcp-server
        ports:
        - containerPort: 8443
        env:
        - name: MCP_API_KEYS
          valueFrom:
            secretKeyRef:
              name: mcp-api-keys
              key: keys
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
"""
    
    return {
        "Procfile": procfile_content,
        "railway_start.sh": railway_start,
        ".env.template": docker_env,
        "k8s-deployment.yaml": k8s_deployment,
        "cloud-run-service.yaml": cloud_run_config
    }

def create_security_checklist():
    """Create a security checklist for production deployment"""
    checklist = """
# 🔒 PRODUCTION SECURITY CHECKLIST

## Pre-Deployment Security ✅

- [ ] Generate strong API keys (32+ characters)
- [ ] Set up environment variables for all secrets
- [ ] Enable HTTPS/TLS encryption
- [ ] Configure rate limiting (100 req/min recommended)
- [ ] Set up request logging and monitoring
- [ ] Restrict file access to safe directories only
- [ ] Validate all input parameters
- [ ] Set up CORS policies
- [ ] Configure firewall rules
- [ ] Set up backup and recovery procedures

## Cloud Platform Security ✅

- [ ] Use managed SSL certificates
- [ ] Enable DDoS protection
- [ ] Set up Web Application Firewall (WAF)
- [ ] Configure load balancing
- [ ] Enable auto-scaling with limits
- [ ] Set up health checks
- [ ] Configure monitoring and alerting
- [ ] Set up log aggregation
- [ ] Enable audit logging
- [ ] Configure secrets management

## API Security ✅

- [ ] Implement API key rotation strategy
- [ ] Set up IP whitelisting (if needed)
- [ ] Configure request size limits
- [ ] Implement timeout policies
- [ ] Set up error handling without information disclosure
- [ ] Enable request/response logging (sanitized)
- [ ] Configure CORS appropriately
- [ ] Implement circuit breakers
- [ ] Set up API versioning
- [ ] Document security policies

## Monitoring & Maintenance ✅

- [ ] Set up uptime monitoring
- [ ] Configure performance monitoring
- [ ] Set up security incident response
- [ ] Enable vulnerability scanning
- [ ] Set up dependency monitoring
- [ ] Configure backup testing
- [ ] Set up disaster recovery procedures
- [ ] Enable compliance monitoring
- [ ] Set up regular security audits
- [ ] Document incident response procedures

## Post-Deployment Verification ✅

- [ ] Test authentication with valid/invalid keys
- [ ] Verify rate limiting is working
- [ ] Test HTTPS redirect and certificate
- [ ] Verify CORS policies
- [ ] Test error handling
- [ ] Verify logging is working
- [ ] Test health endpoints
- [ ] Verify monitoring alerts
- [ ] Test backup procedures
- [ ] Document access procedures
"""
    
    return checklist

def main():
    """Generate secure deployment configuration"""
    print("🔒 SECURE MCP SERVER - PRODUCTION CONFIGURATION")
    print("=" * 60)
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Generate configuration
    config = generate_production_config()
    
    # Save configuration
    with open("secure_production_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✅ Configuration saved to: secure_production_config.json")
    
    # Generate deployment files
    deployment_files = generate_deployment_files()
    
    print("\n📁 Generating deployment files...")
    for filename, content in deployment_files.items():
        with open(f"deployment_{filename}", "w", encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ {filename}")
    
    # Create security checklist
    checklist = create_security_checklist()
    with open("SECURITY_CHECKLIST.md", "w", encoding='utf-8') as f:
        f.write(checklist)
    
    print(f"   ✅ SECURITY_CHECKLIST.md")
    
    # Generate sample API keys
    print("\n🔑 Sample API keys for production:")
    for i in range(3):
        api_key = secrets.token_urlsafe(32)
        print(f"   Key {i+1}: {api_key}")
    
    print("\n🚀 READY FOR SECURE PRODUCTION DEPLOYMENT!")
    print("\nNext steps:")
    print("1. Review SECURITY_CHECKLIST.md")
    print("2. Set MCP_API_KEYS environment variable")
    print("3. Deploy using your preferred cloud platform")
    print("4. Run security tests with test_secure_client.py")
    print("5. Set up monitoring and alerting")

if __name__ == "__main__":
    main()

# 🛠️ Dokploy Deployment Troubleshooting Guide

This guide helps you diagnose and fix common issues when deploying the secure MCP server with Dokploy.

## 🔍 Quick Diagnostics

### 1. Check System Status
```bash
# SSH to your VPS
ssh your-username@YOUR_VPS_IP

# Check Docker status
sudo systemctl status docker

# Check Dokploy containers
docker ps | grep dokploy

# Check your application container
docker ps | grep mcp-server
```

### 2. Review Logs
```bash
# Dokploy application logs
docker logs -f $(docker ps -q --filter "name=secure-mcp-server")

# Dokploy system logs
docker logs -f dokploy-app

# Traefik (reverse proxy) logs
docker logs -f traefik
```

## 🚫 Common Issues and Solutions

### Issue 1: Deployment Fails - Build Error

**Symptoms:**
- Build fails in Dokploy dashboard
- Error messages about missing files or dependencies

**Diagnosis:**
```bash
# Check build logs in Dokploy dashboard
# Look for specific error messages

# Test build locally
git clone YOUR_REPO_URL
cd YOUR_REPO
docker build -t test-mcp -f Dockerfile.production .
```

**Solutions:**
1. **Missing Dockerfile:**
   ```bash
   # Ensure Dockerfile.production exists in repository root
   ls -la Dockerfile.production
   ```

2. **Incorrect requirements.txt:**
   ```bash
   # Verify requirements.txt includes all dependencies
   cat requirements.txt
   # Should include at least:
   # psutil==7.0.0
   # aiohttp==3.9.1
   ```

3. **Python version mismatch:**
   ```dockerfile
   # In Dockerfile.production, ensure compatible Python version
   FROM python:3.11-slim  # Use stable, supported version
   ```

### Issue 2: Application Won't Start

**Symptoms:**
- Container starts but immediately exits
- Health checks fail
- 502 Bad Gateway errors

**Diagnosis:**
```bash
# Check container logs for startup errors
docker logs $(docker ps -a -q --filter "name=secure-mcp-server")

# Check if process is running
docker exec -it $(docker ps -q --filter "name=secure-mcp-server") ps aux
```

**Solutions:**
1. **Missing environment variables:**
   ```bash
   # In Dokploy dashboard, verify all required variables:
   MCP_API_KEYS=your-keys-here
   PORT=8443
   MCP_LOG_LEVEL=INFO
   MCP_ENABLE_MONITORING=true
   ```

2. **Port configuration:**
   ```bash
   # Ensure PORT matches in:
   # - Environment variables (PORT=8443)
   # - Dockerfile EXPOSE directive
   # - Application startup command
   ```

3. **File permissions:**
   ```dockerfile
   # In Dockerfile.production
   RUN chown -R mcpuser:mcpuser /app
   USER mcpuser
   ```

### Issue 3: SSL/HTTPS Issues

**Symptoms:**
- Site not accessible via HTTPS
- SSL certificate errors
- "Not secure" warnings in browser

**Diagnosis:**
```bash
# Check certificate status
curl -I https://mcp.yourdomain.com

# Check DNS resolution
nslookup mcp.yourdomain.com

# Check Traefik configuration
docker logs traefik | grep -i certificate
```

**Solutions:**
1. **DNS configuration:**
   ```bash
   # Ensure A record points to VPS IP
   dig mcp.yourdomain.com
   # Should return your VPS IP address
   ```

2. **Domain in Dokploy:**
   ```bash
   # In Dokploy dashboard:
   # - Domain: mcp.yourdomain.com
   # - Enable HTTPS: ✅
   # - Certificate Provider: Let's Encrypt
   ```

3. **Firewall rules:**
   ```bash
   # Ensure ports 80 and 443 are open
   sudo ufw status
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   ```

### Issue 4: Authentication Failures

**Symptoms:**
- 401 Unauthorized errors
- API requests failing despite correct keys

**Diagnosis:**
```bash
# Test without authentication (should fail)
curl -v https://mcp.yourdomain.com/api/tools

# Test with authentication
curl -v -H "Authorization: Bearer YOUR_API_KEY" \
     https://mcp.yourdomain.com/api/tools
```

**Solutions:**
1. **API key format:**
   ```bash
   # Ensure proper Bearer token format
   curl -H "Authorization: Bearer your-api-key-here"
   # NOT: curl -H "Authorization: your-api-key-here"
   ```

2. **Environment variable format:**
   ```bash
   # Multiple keys separated by commas
   MCP_API_KEYS=key1,key2,key3
   # NOT: MCP_API_KEYS="key1","key2","key3"
   ```

3. **Key generation:**
   ```bash
   # Generate new API keys
   python3 -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

### Issue 5: Performance Issues

**Symptoms:**
- Slow response times
- High memory/CPU usage
- Application timeouts

**Diagnosis:**
```bash
# Check resource usage
docker stats --no-stream $(docker ps -q --filter "name=secure-mcp-server")

# Check response times
curl -w "@curl-format.txt" -o /dev/null -s https://mcp.yourdomain.com/health
```

**Solutions:**
1. **Resource limits:**
   ```bash
   # In Dokploy dashboard, adjust:
   # Memory: 512MB → 1GB
   # CPU: 0.5 → 1.0 cores
   ```

2. **VPS resources:**
   ```bash
   # Check VPS resources
   free -h  # Memory
   df -h    # Disk space
   top      # CPU usage
   ```

3. **Application optimization:**
   ```python
   # Add to secure_server.py
   import uvloop
   asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
   ```

### Issue 6: High Memory Usage

**Symptoms:**
- Container killed (OOMKilled)
- VPS becomes unresponsive
- Out of memory errors

**Diagnosis:**
```bash
# Check memory usage
free -h
docker stats --no-stream

# Check for memory leaks
docker exec -it $(docker ps -q --filter "name=secure-mcp-server") \
  python -c "import psutil; print(f'Memory: {psutil.virtual_memory().percent}%')"
```

**Solutions:**
1. **Increase VPS memory:**
   ```bash
   # Upgrade VPS to higher memory tier
   # Minimum 2GB, recommended 4GB for production
   ```

2. **Add swap space:**
   ```bash
   # Create swap file (emergency measure)
   sudo fallocate -l 1G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

3. **Memory limits:**
   ```bash
   # Set memory limits in Dokploy
   # Memory Limit: 512MB (adjust based on VPS)
   ```

### Issue 7: Database Connection Issues

**Symptoms:**
- Database connection errors
- Timeouts connecting to external services

**Diagnosis:**
```bash
# Test network connectivity
docker exec -it $(docker ps -q --filter "name=secure-mcp-server") \
  ping google.com

# Check DNS resolution
docker exec -it $(docker ps -q --filter "name=secure-mcp-server") \
  nslookup your-database-host.com
```

**Solutions:**
1. **Network configuration:**
   ```bash
   # Ensure container can access external networks
   # Check firewall rules on VPS and destination
   ```

2. **Environment variables:**
   ```bash
   # Add database connection variables
   DATABASE_URL=postgresql://user:pass@host:port/db
   REDIS_URL=redis://host:port/0
   ```

## 🔧 Advanced Troubleshooting

### Container Shell Access
```bash
# Access running container shell
docker exec -it $(docker ps -q --filter "name=secure-mcp-server") /bin/bash

# Or if bash is not available
docker exec -it $(docker ps -q --filter "name=secure-mcp-server") /bin/sh
```

### Manual Container Testing
```bash
# Stop current container
docker stop $(docker ps -q --filter "name=secure-mcp-server")

# Run container manually for debugging
docker run -it --rm \
  -e MCP_API_KEYS=your-test-key \
  -e PORT=8443 \
  -p 8443:8443 \
  your-image-name \
  python secure_server.py --port 8443 --env-keys --debug
```

### Log Analysis
```bash
# Search logs for specific errors
docker logs $(docker ps -q --filter "name=secure-mcp-server") 2>&1 | grep -i error

# Save logs for analysis
docker logs $(docker ps -q --filter "name=secure-mcp-server") > mcp-server.log

# Real-time log monitoring with timestamps
docker logs -f --timestamps $(docker ps -q --filter "name=secure-mcp-server")
```

### Network Debugging
```bash
# Check if application is listening on correct port
docker exec -it $(docker ps -q --filter "name=secure-mcp-server") netstat -tlnp

# Test internal connectivity
docker exec -it $(docker ps -q --filter "name=secure-mcp-server") \
  curl -v http://localhost:8443/health
```

## 🆘 Emergency Recovery

### Quick Rollback
```bash
# In Dokploy dashboard:
# 1. Go to Deployments tab
# 2. Find last successful deployment
# 3. Click "Rollback" button
# 4. Confirm rollback
```

### Manual Service Restart
```bash
# Restart application container
docker restart $(docker ps -q --filter "name=secure-mcp-server")

# If that fails, restart all Dokploy services
cd /path/to/dokploy
docker-compose restart
```

### Backup Recovery
```bash
# Restore from backup (if configured)
# In Dokploy dashboard:
# 1. Go to Backups tab
# 2. Select backup to restore
# 3. Click "Restore" button
```

## 📞 Getting Help

### Collect Diagnostic Information
Before seeking help, collect:

```bash
# System information
uname -a
docker --version
free -h
df -h

# Container information
docker ps -a
docker images
docker logs $(docker ps -q --filter "name=secure-mcp-server") --tail 100

# Network information
curl -I https://mcp.yourdomain.com/health
nslookup mcp.yourdomain.com
```

### Support Channels
- **Dokploy Discord**: Join the community for platform-specific help
- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Check official Dokploy documentation

### Escalation Path
1. Check this troubleshooting guide
2. Review Dokploy dashboard logs
3. Test components individually
4. Collect diagnostic information
5. Seek community help
6. Open support ticket with detailed information

Remember: Most issues are configuration-related and can be resolved by carefully reviewing the setup steps and environment variables.

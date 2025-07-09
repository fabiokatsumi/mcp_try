# 🚀 Secure MCP Server Deployment with Dokploy on VPS

This comprehensive guide provides step-by-step instructions for deploying your secure MCP server on a VPS using Dokploy, a modern Docker-based deployment platform that simplifies application deployment and management.

## 📋 Overview

**Dokploy** is an open-source platform that provides a simple way to deploy applications on your VPS with:
- Docker-based deployments with built-in orchestration
- Built-in reverse proxy (Traefik) with automatic HTTPS
- SSL certificate management (Let's Encrypt integration)
- Environment variable management and secrets
- Real-time monitoring, logs, and metrics
- Database management (PostgreSQL, MySQL, MongoDB, Redis)
- Automated backup and restore capabilities
- Web-based dashboard for easy management
- Git integration with auto-deployment

## 🎯 What You'll Achieve

By following this guide, you'll have:
- ✅ A production-ready secure MCP server running on your VPS
- ✅ HTTPS/SSL encryption with automatic certificate renewal
- ✅ Professional domain setup (mcp.yourdomain.com)
- ✅ API key authentication and rate limiting
- ✅ Real-time monitoring and logging
- ✅ Automated deployments from Git
- ✅ Backup and disaster recovery setup
- ✅ Production-grade security configurations

## 🔧 Prerequisites

### VPS Requirements
- **OS**: Ubuntu 20.04+ or Debian 11+ (recommended)
- **RAM**: Minimum 2GB (4GB+ recommended for production)
- **Storage**: Minimum 20GB SSD (50GB+ recommended)
- **CPU**: 1 vCPU minimum (2+ recommended for production)
- **Network**: Public IP address with ports 80, 443, and 3000 accessible
- **Domain**: Strongly recommended for SSL and professional setup

### Local Requirements
- Git installed on your local machine
- SSH access to your VPS (SSH key recommended)
- Domain name pointing to your VPS IP (optional but recommended)
- Basic knowledge of command line and Git

### Domain Setup (Recommended)
Before starting, set up these DNS records:
```
A     mcp.yourdomain.com      -> YOUR_VPS_IP
A     dokploy.yourdomain.com  -> YOUR_VPS_IP
```

## 🏗️ Phase 1: VPS Setup and Dokploy Installation

### Step 1: Initial VPS Access and Security Setup
```bash
# Connect via SSH (replace with your VPS IP)
ssh root@YOUR_VPS_IP

# Or with custom user
ssh your-username@YOUR_VPS_IP

# Create a new user for better security (if using root)
adduser dokploy
usermod -aG sudo dokploy
# Switch to the new user for subsequent steps
su - dokploy
```

### Step 2: System Preparation
```bash
# Update package lists and upgrade system
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git ufw htop unzip software-properties-common

# Set timezone (optional)
sudo timedatectl set-timezone UTC
```

### Step 3: Security Configuration
```bash
# Configure UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 3000/tcp  # Dokploy admin panel
sudo ufw --force enable

# Check firewall status
sudo ufw status numbered

# Optional: Change SSH port for security (if desired)
# sudo nano /etc/ssh/sshd_config
# Change Port 22 to Port 2222
# sudo systemctl restart ssh
# sudo ufw allow 2222/tcp
```

### Step 4: Docker Installation
```bash
# Remove any old Docker installations
sudo apt remove docker docker-engine docker.io containerd runc

# Install Docker using the official script
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to docker group
sudo usermod -aG docker $USER

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Log out and back in to apply group changes
exit
# ssh back in

# Test Docker installation
docker --version
docker run hello-world
```

### Step 5: Install Docker Compose (if not included)
```bash
# Check if docker-compose is installed
docker-compose --version

# If not installed, install it
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 6: Install Dokploy
```bash
# Install Dokploy using the official installer
curl -sSL https://dokploy.com/install.sh | sh

# The installer will:
# - Download and run Dokploy containers
# - Set up Traefik reverse proxy
# - Configure SSL certificate management
# - Initialize the database
# - Start the admin panel on port 3000

# Wait for installation to complete (may take 2-5 minutes)
echo "Waiting for Dokploy to start..."
sleep 60

# Check if Dokploy is running
docker ps | grep dokploy
```

### Step 7: Initial Dokploy Access
```bash
# Get the initial admin password
sudo docker logs dokploy-app 2>&1 | grep -i password

# Access Dokploy admin panel
echo "Dokploy admin panel: http://YOUR_VPS_IP:3000"
echo "Or with domain: http://dokploy.YOUR_DOMAIN.com"

# Test if Dokploy is responding
curl -I http://localhost:3000
```

## 🌐 Phase 2: Domain and SSL Configuration

### Step 1: DNS Configuration
If you have a domain, configure these DNS records in your domain provider's panel:

```bash
# DNS Records to create:
Type    Name                Value           TTL
A       mcp                 YOUR_VPS_IP     300
A       dokploy            YOUR_VPS_IP     300
A       @                   YOUR_VPS_IP     300  (optional)
CNAME   www                 @               300  (optional)
```

### Step 2: Wait for DNS Propagation
```bash
# Check DNS propagation (may take up to 24 hours)
nslookup mcp.YOUR_DOMAIN.com
nslookup dokploy.YOUR_DOMAIN.com

# Alternative check
dig mcp.YOUR_DOMAIN.com
dig dokploy.YOUR_DOMAIN.com
```

### Step 3: Access Dokploy with Domain
Once DNS has propagated:
```bash
# Access via domain
http://dokploy.YOUR_DOMAIN.com

# The admin panel should be accessible
```

## 🔒 Phase 3: Prepare MCP Server for Deployment

### Step 1: Clone Your Repository
```bash
# Create a deployment directory
mkdir -p ~/deployments
cd ~/deployments

# Clone your MCP server repository
git clone https://github.com/YOUR_USERNAME/YOUR_MCP_REPO.git
cd YOUR_MCP_REPO

# Or if you're uploading files manually
# Create the directory and upload your files via SCP/SFTP
```

### Step 2: Generate API Keys
```bash
# Generate secure API keys for production
python3 -c "
import secrets
print('Generated API Keys:')
for i in range(3):
    key = secrets.token_urlsafe(32)
    print(f'  Key {i+1}: {key}')
"

# Save these keys securely - you'll need them for configuration
```

### Step 3: Verify Production Files
Ensure these files exist in your repository:
```bash
ls -la
# Should show:
# - Dockerfile.production
# - secure_server.py
# - requirements.txt
# - dokploy.config
# - docker-compose.dokploy.yml (optional)
```

### Step 4: Review Production Files
Ensure you have the following files ready for deployment:

**1. Dockerfile.production** (production-optimized):
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONOPTIMIZE=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first (for better Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app
USER mcpuser

# Expose port
EXPOSE 8443

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8443/health || exit 1

# Start secure server
CMD ["python", "secure_server.py", "--port", "8443", "--env-keys"]
```

**2. .dockerignore** (optimize build):
```plaintext
__pycache__/
*.pyc
*.pyo
*.pyd
.git/
.gitignore
*.md
.env
.venv/
venv/
node_modules/
.DS_Store
Thumbs.db
*.log
tmp/
test_*.py
*_test.py
```

**3. Environment Variables File** (for Dokploy):
Create a `.env.production` file with:
```bash
# Production Environment Variables
MCP_API_KEYS=YOUR_GENERATED_API_KEYS_HERE
PORT=8443
MCP_LOG_LEVEL=INFO
MCP_ENABLE_MONITORING=true
PYTHONUNBUFFERED=1
PYTHONDONTWRITEBYTECODE=1
PYTHONOPTIMIZE=1
```

## 📦 Phase 4: Dokploy Application Setup

### Step 1: Access Dokploy Admin Panel
```bash
# Open your browser and navigate to:
http://YOUR_VPS_IP:3000
# Or with domain:
http://dokploy.YOUR_DOMAIN.com

# Login with the credentials from installation
```

### Step 2: Create New Application
1. **Click "Create Application"**
2. **Fill in Application Details**:
   - **Name**: `secure-mcp-server`
   - **Description**: `Production MCP Server with Enterprise Security`
   - **Application Type**: `Application`

### Step 3: Configure Source
1. **Select Source Type**: `Git`
2. **Repository Configuration**:
   - **Repository URL**: `https://github.com/YOUR_USERNAME/YOUR_MCP_REPO.git`
   - **Branch**: `main` (or your production branch)
   - **Auto Deploy**: ✅ (enable for automatic deployments)

### Step 4: Configure Build Settings
1. **Build Type**: `Dockerfile`
2. **Dockerfile Path**: `Dockerfile.production`
3. **Build Context**: `/` (root of repository)
4. **Build Arguments** (if needed): Leave empty for now

### Step 5: Configure Environment Variables
Add these environment variables in the Dokploy interface:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `MCP_API_KEYS` | `key1,key2,key3` | Your generated API keys |
| `PORT` | `8443` | Application port |
| `MCP_LOG_LEVEL` | `INFO` | Logging level |
| `MCP_ENABLE_MONITORING` | `true` | Enable monitoring |
| `PYTHONUNBUFFERED` | `1` | Python output buffering |
| `PYTHONDONTWRITEBYTECODE` | `1` | Prevent .pyc files |
| `PYTHONOPTIMIZE` | `1` | Python optimization |

### Step 6: Configure Domain and SSL
1. **Domain Configuration**:
   - **Domain**: `mcp.YOUR_DOMAIN.com`
   - **Enable HTTPS**: ✅
   - **Certificate Provider**: `Let's Encrypt`
   - **Force HTTPS**: ✅

2. **Port Configuration**:
   - **Container Port**: `8443`
   - **Host Port**: `80` (will be proxied by Traefik)

### Step 7: Configure Resource Limits
1. **Memory Limit**: `512MB` (adjust based on your needs)
2. **CPU Limit**: `0.5` (half a CPU core)
3. **Restart Policy**: `always`

### Step 8: Configure Health Checks
1. **Health Check URL**: `/health`
2. **Health Check Interval**: `30s`
3. **Health Check Timeout**: `10s`
4. **Health Check Retries**: `3`

## 🚀 Phase 5: Deploy Application

### Step 1: Deploy the Application
1. **Review Configuration**: Double-check all settings
2. **Click "Deploy"**: Start the deployment process
3. **Monitor Deployment**: Watch the build logs in real-time

### Step 2: Monitor Deployment Logs
```bash
# In Dokploy interface, monitor:
# - Build logs
# - Container logs
# - Health check status

# Or via command line on VPS:
docker logs -f $(docker ps -q --filter "name=secure-mcp-server")
```

### Step 3: Verify Deployment
```bash
# Test health endpoint
curl https://mcp.YOUR_DOMAIN.com/health

# Expected response:
# {"status": "healthy", "timestamp": "...", "uptime": "..."}

# Test API with authentication
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://mcp.YOUR_DOMAIN.com/api/tools

# Expected response: JSON with available tools
```
.env
.venv/
venv/
.pytest_cache/
.coverage
htmlcov/
.tox/
.cache/
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.DS_Store
Thumbs.db
```

### Step 4: Create Environment Template
```bash
# .env.production.template
MCP_API_KEYS=your-secure-api-key-here
PORT=8443
MCP_LOG_LEVEL=INFO
MCP_ENABLE_MONITORING=true
PYTHONUNBUFFERED=1
```

## 🚀 Phase 4: Deploy with Dokploy

### Step 1: Access Dokploy Dashboard
1. Open browser to `http://YOUR_VPS_IP:3000` or `http://dokploy.YOUR_DOMAIN.com`
2. Complete initial setup wizard
3. Set admin credentials

### Step 2: Create New Project
1. Click **"Create Project"**
2. Choose **"Application"**
3. Fill in project details:
   - **Name**: `secure-mcp-server`
   - **Description**: `Production MCP Server with Enterprise Security`

### Step 3: Configure Git Repository
1. In project settings, go to **"Source"**
2. Choose **"Git Repository"**
3. Enter your repository URL:
   ```
   https://github.com/your-username/mcp-server.git
   ```
4. Set branch to `main` or `master`
5. Set build context to `/` (root)

### Step 4: Configure Build Settings
1. Go to **"Build"** settings
2. Set **Dockerfile path**: `Dockerfile.production`
3. Enable **"Auto Deploy"** for automatic deployments

### Step 5: Configure Environment Variables
1. Go to **"Environment"** settings
2. Add the following variables:

```bash
# Required Environment Variables
MCP_API_KEYS=your-generated-secure-api-key-1,your-generated-secure-api-key-2
PORT=8443
MCP_LOG_LEVEL=INFO
MCP_ENABLE_MONITORING=true
PYTHONUNBUFFERED=1
```

### Step 6: Configure Network and Domain
1. Go to **"Domains"** settings
2. Add domain configuration:
   - **Domain**: `mcp.YOUR_DOMAIN.com` (or use VPS IP)
   - **Port**: `8443`
   - **Enable SSL**: ✅ (if using domain)

### Step 7: Deploy Application
1. Click **"Deploy"** button
2. Monitor deployment logs in real-time
3. Wait for successful deployment

## ✅ Phase 6: Post-Deployment Verification

### Step 1: Check Application Status
```bash
# SSH into your VPS
ssh your-username@YOUR_VPS_IP

# Check running containers
docker ps | grep mcp-server

# Check application logs
docker logs -f $(docker ps -q --filter "name=secure-mcp-server")
```

### Step 2: Test Health Endpoint
```bash
# Test health check (no authentication required)
curl https://mcp.YOUR_DOMAIN.com/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "uptime": "0:05:23",
  "version": "1.0.0"
}
```

### Step 3: Test API Authentication
```bash
# Should fail without API key (401 Unauthorized)
curl -v https://mcp.YOUR_DOMAIN.com/api/tools

# Should succeed with valid API key
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://mcp.YOUR_DOMAIN.com/api/tools

# Expected response: JSON with available tools list
```

### Step 4: Comprehensive Security Test
Run the security test client:
```bash
# From your local machine with test client
python test_secure_client.py \
  --url https://mcp.YOUR_DOMAIN.com \
  --api-key YOUR_API_KEY \
  --comprehensive
```

## 📊 Phase 7: Monitoring and Management

### Step 1: Dokploy Dashboard Monitoring
Access comprehensive monitoring in Dokploy:

1. **Application Metrics**:
   - CPU usage and trends
   - Memory consumption
   - Network I/O
   - Request rates

2. **Real-time Logs**:
   - Application logs
   - Access logs
   - Error logs
   - Security events

3. **Health Monitoring**:
   - Automatic health checks
   - Uptime tracking
   - Response time metrics
   - Failure notifications

### Step 2: Set Up Alerts
Configure alerts in Dokploy:

1. **Health Check Failures**: Get notified when health checks fail
2. **Resource Usage**: Alert when CPU/memory exceeds thresholds
3. **Deployment Events**: Notifications for successful/failed deployments
4. **SSL Certificate Expiry**: Alerts before certificate renewal

### Step 3: Log Analysis
```bash
# Access logs via command line
docker logs --tail 100 -f $(docker ps -q --filter "name=secure-mcp-server")

# Filter for specific events
docker logs $(docker ps -q --filter "name=secure-mcp-server") | grep "ERROR"
docker logs $(docker ps -q --filter "name=secure-mcp-server") | grep "unauthorized"
```

## 🔄 Phase 8: Automated Updates and CI/CD

### Step 1: Git-based Auto-deployment
Dokploy automatically deploys when you push changes:

```bash
# Local development workflow
git add .
git commit -m "feat: add new MCP tool for database queries"
git push origin main

# Dokploy will automatically:
# 1. Detect the push
# 2. Build new Docker image
# 3. Deploy with zero downtime
# 4. Run health checks
# 5. Notify of deployment status
```

### Step 2: Environment-specific Deployments
Set up different branches for different environments:

```bash
# Production branch
git checkout main
git push origin main  # Auto-deploys to production

# Staging branch (if you set up staging environment)
git checkout staging
git push origin staging  # Auto-deploys to staging
```

### Step 3: Rollback Capabilities
If issues occur after deployment:

1. **Access Dokploy Dashboard**
2. **Go to Deployments History**
3. **Select Previous Successful Deployment**
4. **Click "Rollback"**
5. **Confirm Rollback Operation**

```bash
# Or via CLI (if Dokploy CLI is installed)
dokploy app rollback secure-mcp-server --version previous
```

## 🛡️ Phase 9: Production Security Hardening

### Step 1: Advanced Firewall Configuration
```bash
# Additional firewall rules for production
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow only necessary ports
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Restrict Dokploy admin access to specific IPs
sudo ufw allow from YOUR_OFFICE_IP to any port 3000

# Enable UFW logging
sudo ufw logging on

# Check status
sudo ufw status verbose
```

### Step 2: Fail2Ban Configuration
```bash
# Install and configure Fail2Ban
sudo apt install -y fail2ban

# Create custom jail for Dokploy
sudo nano /etc/fail2ban/jail.local
```

Add to jail.local:
```ini
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 5

[sshd]
enabled = true
port = ssh
filter = sshd
logpath = /var/log/auth.log

[dokploy]
enabled = true
port = 3000
filter = dokploy
logpath = /var/log/dokploy/access.log
maxretry = 3
```

### Step 3: SSL Security Enhancement
```bash
# Check SSL configuration
curl -I https://mcp.YOUR_DOMAIN.com

# Test SSL security rating
# Use online tools like SSL Labs (https://www.ssllabs.com/ssltest/)
```

### Step 4: API Key Rotation Strategy
```bash
# Generate new API keys monthly
python3 -c "
import secrets
import datetime
print(f'Generated on: {datetime.datetime.now()}')
for i in range(3):
    print(f'Key {i+1}: {secrets.token_urlsafe(32)}')
"

# Update in Dokploy environment variables
# Deploy to apply changes
# Update client applications with new keys
# Deactivate old keys after grace period
```

## 📈 Phase 10: Performance Optimization

### Step 1: Resource Monitoring and Tuning
```bash
# Monitor resource usage
docker stats $(docker ps -q --filter "name=secure-mcp-server")

# Check application performance
curl -w "@curl-format.txt" -o /dev/null -s https://mcp.YOUR_DOMAIN.com/health
```

Create `curl-format.txt`:
```
     time_namelookup:  %{time_namelookup}s\n
        time_connect:  %{time_connect}s\n
     time_appconnect:  %{time_appconnect}s\n
    time_pretransfer:  %{time_pretransfer}s\n
       time_redirect:  %{time_redirect}s\n
  time_starttransfer:  %{time_starttransfer}s\n
                     ----------\n
          time_total:  %{time_total}s\n
```

### Step 2: Application Performance Optimization
Update your `secure_server.py` with production optimizations:

```python
# Add to secure_server.py for production
import uvloop
import asyncio

# Use uvloop for better performance
if __name__ == "__main__":
    if hasattr(asyncio, 'set_event_loop_policy'):
        asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
```

### Step 3: Caching and CDN Setup
For high-traffic scenarios:

1. **Enable Response Caching**:
   - Configure cache headers for static responses
   - Use Redis for session storage (if needed)

2. **CDN Integration**:
   - Use Cloudflare or similar CDN
   - Configure for API endpoint caching where appropriate

## 🆘 Troubleshooting Guide

### Common Issues and Solutions

#### 1. Deployment Fails
**Symptoms**: Build fails, container won't start
```bash
# Check build logs in Dokploy dashboard
# Review Dockerfile syntax
docker build -t test-mcp -f Dockerfile.production .

# Common fixes:
# - Verify all dependencies in requirements.txt
# - Check environment variable names
# - Ensure base image is accessible
# - Review Python version compatibility
```

#### 2. Application Won't Start
**Symptoms**: Container exits immediately, health checks fail
```bash
# Check container logs
docker logs $(docker ps -a -q --filter "name=secure-mcp-server")

# Common fixes:
# - Verify PORT environment variable
# - Check API key format
# - Ensure all required files are included
# - Review Python import errors
```

#### 3. SSL Certificate Issues
**Symptoms**: HTTPS not working, certificate errors
```bash
# Check certificate status in Dokploy
# Verify DNS is pointing to correct IP
nslookup mcp.YOUR_DOMAIN.com

# Force certificate renewal if needed
# Contact support if Let's Encrypt fails
```

#### 4. High Memory Usage
**Symptoms**: Container killed, out of memory errors
```bash
# Check memory usage
docker stats --no-stream

# Solutions:
# - Increase VPS memory
# - Optimize application code
# - Add memory limits to prevent system issues
# - Review for memory leaks
```

#### 5. Rate Limiting Issues
**Symptoms**: 429 errors, requests being blocked
```bash
# Check rate limiting configuration
# Review application logs for rate limit hits

# Solutions:
# - Adjust rate limits in secure_server.py
# - Implement request queuing
# - Add multiple API keys for different clients
```

#### 6. Database Connection Issues (if using external DB)
**Symptoms**: Database connection errors, timeouts
```bash
# Check database connectivity
docker exec -it $(docker ps -q --filter "name=secure-mcp-server") \
  python -c "import psycopg2; print('DB connection test')"

# Solutions:
# - Verify database credentials
# - Check network connectivity
# - Review database server status
# - Check firewall rules
```

### Emergency Procedures

#### 1. Quick Rollback
```bash
# Via Dokploy dashboard:
# 1. Go to Deployments
# 2. Select last known good deployment
# 3. Click Rollback
# 4. Confirm action

# Service should be restored within 2-3 minutes
```

#### 2. Manual Container Restart
```bash
# SSH to VPS
ssh your-username@YOUR_VPS_IP

# Restart application container
docker restart $(docker ps -q --filter "name=secure-mcp-server")

# Check status
docker ps | grep mcp-server
```

#### 3. Emergency Maintenance Mode
```bash
# Temporarily disable application
docker stop $(docker ps -q --filter "name=secure-mcp-server")

# Put up maintenance page (if configured)
# Or redirect traffic to backup server
```

## 📚 Additional Resources

### Documentation Links
- [Dokploy Official Documentation](https://dokploy.com/docs)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Let's Encrypt Documentation](https://letsencrypt.org/docs/)
- [Traefik Configuration Guide](https://doc.traefik.io/traefik/)

### Support and Community
- **Dokploy Discord**: Join the community for support
- **GitHub Issues**: Report bugs and feature requests
- **Documentation Updates**: Contribute to documentation

### Next Steps
- Set up monitoring alerts
- Configure automated backups
- Implement log aggregation
- Set up staging environment
- Plan disaster recovery procedures

## 🎉 Conclusion

Congratulations! You now have a production-ready, secure MCP server running on your VPS with Dokploy. Your setup includes:

✅ **Enterprise-grade security** with API key authentication and rate limiting  
✅ **Automatic HTTPS** with SSL certificate management  
✅ **Professional domain setup** with proper DNS configuration  
✅ **Real-time monitoring** and logging capabilities  
✅ **Automated deployments** from Git repository  
✅ **Health checks** and automatic recovery  
✅ **Backup and restore** capabilities  
✅ **Performance optimization** for production workloads  

Your MCP server is now ready to handle production traffic and can be easily maintained and scaled as your needs grow.

For ongoing support and updates, refer to the troubleshooting section and keep your dependencies up to date. Regular monitoring and maintenance will ensure optimal performance and security.

# Common fixes:
# - Verify environment variables are set
# - Check port conflicts
# - Validate API key format
```

#### 3. SSL Certificate Issues
```bash
# Check domain DNS configuration
nslookup mcp.YOUR_DOMAIN.com

# Force certificate renewal in Dokploy
# Check firewall allows ports 80 and 443
```

#### 4. Performance Issues
```bash
# Monitor resource usage in Dokploy dashboard
# Check for:
# - High memory usage
# - CPU throttling
# - Network latency
# - Rate limiting false positives
```

### Emergency Procedures

#### Quick Rollback
```bash
# Via Dokploy dashboard:
1. Go to "Deployments"
2. Select last working version
3. Click "Rollback"
4. Confirm operation
```

#### Manual Container Restart
```bash
# SSH to VPS
ssh root@YOUR_VPS_IP

# Restart container
docker restart dokploy-secure-mcp-server

# Check status
docker ps | grep mcp
```

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] ✅ VPS configured with sufficient resources
- [ ] ✅ Domain DNS configured (if using custom domain)
- [ ] ✅ Dokploy installed and configured
- [ ] ✅ Git repository prepared with production files
- [ ] ✅ API keys generated and stored securely

### Deployment
- [ ] ✅ Dokploy project created
- [ ] ✅ Git repository connected
- [ ] ✅ Environment variables configured
- [ ] ✅ Domain and SSL configured
- [ ] ✅ Application deployed successfully

### Post-Deployment
- [ ] ✅ Health check endpoint responding
- [ ] ✅ Authentication working correctly
- [ ] ✅ Rate limiting functioning
- [ ] ✅ SSL certificate valid
- [ ] ✅ Monitoring and logging active
- [ ] ✅ Backup configuration tested

### Security Verification
- [ ] ✅ API endpoints require authentication
- [ ] ✅ Rate limiting prevents abuse
- [ ] ✅ No sensitive information in logs
- [ ] ✅ HTTPS enforced
- [ ] ✅ Admin panel access restricted

## 🎯 Example Production URLs

After successful deployment, your secure MCP server will be available at:

```bash
# Health check (public)
https://mcp.YOUR_DOMAIN.com/health

# API endpoints (require authentication)
https://mcp.YOUR_DOMAIN.com/api/tools
https://mcp.YOUR_DOMAIN.com/api/status
https://mcp.YOUR_DOMAIN.com/mcp

# Dokploy admin panel
https://dokploy.YOUR_DOMAIN.com

# Example authenticated request
curl -X POST https://mcp.YOUR_DOMAIN.com/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "calculate",
      "arguments": {"expression": "2**10 + 5"}
    }
  }'
```

## 🎉 Conclusion

Your secure MCP server is now successfully deployed on a VPS using Dokploy! You have:

- ✅ **Production-ready deployment** with enterprise security
- ✅ **Automated SSL certificate management**
- ✅ **Built-in monitoring and logging**
- ✅ **Easy scaling and management**
- ✅ **Automated deployments** from Git
- ✅ **Backup and rollback capabilities**
- ✅ **Professional domain setup** with HTTPS

**Your MCP server is now running securely in production and ready for enterprise use! 🚀**

For ongoing maintenance, regularly monitor the Dokploy dashboard, update your application as needed, and follow the security best practices outlined in this guide.

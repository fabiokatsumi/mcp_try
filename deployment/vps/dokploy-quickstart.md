# 🚀 Dokploy Quick Start Guide

This is a condensed guide for experienced developers who want to deploy the secure MCP server quickly using Dokploy.

## ⚡ Prerequisites Checklist

- [ ] VPS with Ubuntu 20.04+ (2GB+ RAM, 20GB+ SSD)
- [ ] Domain name (optional but recommended)
- [ ] SSH access to VPS
- [ ] Git repository with MCP server code

## 🏃‍♂️ 15-Minute Setup

### 1. VPS Setup (5 minutes)
```bash
# SSH to VPS
ssh root@YOUR_VPS_IP

# Update and secure
apt update && apt upgrade -y
ufw allow ssh && ufw allow 80 && ufw allow 443 && ufw allow 3000 && ufw --force enable

# Install Docker
curl -fsSL https://get.docker.com | sh

# Install Dokploy
curl -sSL https://dokploy.com/install.sh | sh

# Wait for startup
sleep 60
```

### 2. Generate API Keys (1 minute)
```bash
python3 -c "import secrets; [print(f'Key {i+1}: {secrets.token_urlsafe(32)}') for i in range(3)]"
```

### 3. Dokploy Configuration (5 minutes)
1. Access: `http://YOUR_VPS_IP:3000`
2. Complete setup wizard
3. Create new application: `secure-mcp-server`
4. Set Git repository: `https://github.com/YOUR_USERNAME/YOUR_REPO`
5. Set Dockerfile path: `Dockerfile.production`

### 4. Environment Variables (2 minutes)
Add in Dokploy:
```
MCP_API_KEYS=your-generated-keys-here
PORT=8443
MCP_LOG_LEVEL=INFO
MCP_ENABLE_MONITORING=true
PYTHONUNBUFFERED=1
```

### 5. Domain & Deploy (2 minutes)
1. Set domain: `mcp.yourdomain.com`
2. Enable SSL: ✅
3. Click **Deploy**
4. Monitor build logs

## ✅ Quick Verification

```bash
# Test health endpoint
curl https://mcp.yourdomain.com/health

# Test API with auth
curl -H "Authorization: Bearer YOUR_API_KEY" https://mcp.yourdomain.com/api/tools
```

## 🔧 Common Issues

| Issue | Solution |
|-------|----------|
| Build fails | Check Dockerfile.production exists |
| 502 errors | Verify PORT=8443 in environment |
| SSL issues | Ensure DNS points to VPS IP |
| Auth fails | Check API key format and headers |

## 📚 Next Steps

- Set up monitoring alerts
- Configure backups
- Implement rate limiting tuning
- Set up staging environment

For detailed instructions, see [DOKPLOY_DEPLOYMENT_GUIDE.md](./DOKPLOY_DEPLOYMENT_GUIDE.md).

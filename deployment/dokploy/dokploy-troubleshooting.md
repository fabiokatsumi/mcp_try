# Dokploy Troubleshooting

## Common Deployment Issues

### 1. Build Failures

**Problem:** Docker build fails
**Solution:**
```bash
# Check Dockerfile syntax
docker build -f Dockerfile.production -t test-build .

# Verify dependencies
pip install -r requirements.txt
```

### 2. Port Conflicts

**Problem:** Port already in use
**Solution:**
```bash
# Change port in .env file
PORT=8081

# Or check what's using the port
netstat -tulpn | grep :8080
```

### 3. SSL Certificate Issues

**Problem:** SSL/TLS certificate not working
**Solution:**
- Verify domain points to your VPS IP
- Check DNS propagation: `nslookup your-domain.com`
- Wait 5-10 minutes for certificate generation

### 4. Health Check Failures

**Problem:** Health checks failing
**Solution:**
```bash
# Test health endpoint locally
curl http://localhost:8080/health

# Check application logs
dokploy logs mcp-server
```

### 5. API Key Authentication Issues

**Problem:** 401/403 errors
**Solution:**
```bash
# Verify API key is set
echo $API_KEYS

# Test with curl
curl -H "Authorization: Bearer YOUR_API_KEY" https://your-domain.com/api/tools
```

## Getting Help

1. Check Dokploy dashboard logs
2. Verify environment variables
3. Test locally with Docker first
4. Check firewall settings (ports 80, 443, 8080)

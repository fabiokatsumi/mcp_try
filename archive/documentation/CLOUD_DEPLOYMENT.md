# MCP Server Cloud Deployment Guide 🌍

This guide shows you how to deploy your MCP server to the cloud with **enterprise-grade security** so it's accessible from anywhere in the world.

## ⚠️ Security Notice

**CRITICAL**: Always use the **secure server** (`secure_server.py`) for cloud deployment!

| Server Type | Security Level | Cloud Deployment |
|-------------|----------------|------------------|
| `http_server.py` | ❌ None | **❌ NEVER** |
| `cloud_server.py` | ❌ None | **❌ DEMO ONLY** |
| **`secure_server.py`** | **� Enterprise** | **✅ RECOMMENDED** |

## 🔒 Secure Deployment Prerequisites

Before deploying, ensure you have:

1. **Generated API Keys:**
```bash
python secure_server.py --generate-key
```

2. **Prepared Environment Variables:**
```bash
MCP_API_KEYS=your-secure-key1,your-secure-key2
PORT=8443
MCP_LOG_LEVEL=INFO
```

3. **Updated Dependencies:**
```
psutil==7.0.0
aiohttp==3.9.1
```

## 🚀 Secure Deployment Options

### Option 1: Railway (Easiest - Free Tier Available) 🔒

1. **Create `requirements.txt`:**
```
psutil==7.0.0
aiohttp==3.9.1
```

2. **Create `Procfile`:**
```
web: python secure_server.py --port $PORT --env-keys
```

3. **Set Environment Variables in Railway:**
   - `MCP_API_KEYS`: `your-secure-key1,your-secure-key2`
   - `PORT`: `8443` (or Railway's assigned port)

4. **Deploy:**
   - Push to GitHub
   - Connect Railway to your repo
   - Set environment variables
   - Deploy automatically

### Option 2: Heroku (Popular) 🔒

1. **Install Heroku CLI**
2. **Create app:**
```bash
heroku create your-secure-mcp-server
```

3. **Set environment variables:**
```bash
heroku config:set MCP_API_KEYS=your-secure-key1,your-secure-key2
```

4. **Deploy:**
```bash
git add .
git commit -m "Deploy secure MCP server"
git push heroku main
```

### Option 3: Render (Modern) 🔒

1. **Create `render.yaml`:**
```yaml
services:
  - type: web
    name: secure-mcp-server
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python secure_server.py --port $PORT --env-keys
    plan: free
    envVars:
      - key: MCP_API_KEYS
        value: your-secure-key1,your-secure-key2
```

2. **Connect GitHub repo to Render**

### Option 4: Google Cloud Run (Scalable) 🔒

1. **Create `Dockerfile`:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8443
CMD ["python", "secure_server.py", "--port", "8443", "--env-keys"]
```

2. **Set environment variables:**
```bash
gcloud run deploy secure-mcp-server --source . \
  --set-env-vars MCP_API_KEYS=your-secure-key1,your-secure-key2
```

### Option 5: Docker (Any Platform) 🔒

1. **Use existing `Dockerfile` with secure configuration**
2. **Run with environment variables:**
```bash
docker build -t secure-mcp-server .
docker run -p 8443:8443 \
  -e MCP_API_KEYS=your-secure-key1,your-secure-key2 \
  secure-mcp-server
```

## 🔍 Post-Deployment Security Testing

After deployment, test your secure server:

### 1. Health Check (No Auth Required)
```bash
curl https://your-secure-server.com/health
```

### 2. Authentication Test
```bash
# Should fail without API key
curl https://your-secure-server.com/api/tools

# Should succeed with API key
curl -H "Authorization: Bearer your-api-key" \
  https://your-secure-server.com/api/tools
```

### 3. Comprehensive Security Test
```bash
python test_secure_client.py --url https://your-secure-server.com --api-key your-api-key
```

## 🌐 After Deployment

Once deployed, you'll get a public URL like:
- `https://your-secure-mcp-server.railway.app`
- `https://your-secure-mcp-server.herokuapp.com`
- `https://your-secure-mcp-server.onrender.com`

**🔒 Remember**: All MCP protocol requests now require API key authentication!

## 🤖 Secure Agent Integration

Configure your AI agents to use the secure public endpoint:

### For Authenticated Requests:
```bash
curl -X POST https://your-secure-server.com/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{"jsonrpc": "2.0", "method": "tools/list"}'
```

### For Claude Desktop (with proxy script):
Create a proxy script that adds authentication:
```python
# mcp_proxy.py
import sys
import json
import requests

def main():
    data = json.load(sys.stdin)
    
    response = requests.post(
        "https://your-secure-server.com/mcp",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer your-api-key"
        },
        json=data
    )
    
    print(response.text)

if __name__ == "__main__":
    main()
```

Then configure:
```json
{
  "mcpServers": {
    "secure-cloud-mcp": {
      "command": "python",
      "args": ["mcp_proxy.py"]
    }
  }
}
```

### For Custom Agents:
```python
import requests

# Your agent can call the MCP server like this:
response = requests.post(
    "https://your-server.com/mcp",
    json={
        "jsonrpc": "2.0",
        "id": "1",
        "method": "tools/call",
        "params": {
            "name": "calculate",
            "arguments": {"expression": "2**10"}
        }
    }
)
```

## 🔒 Security Considerations

1. **API Key Authentication** (recommended for production)
2. **Rate Limiting** 
3. **CORS Configuration**
4. **HTTPS Only**

## 💰 Costs

- **Railway**: Free tier available
- **Heroku**: $7/month for basic
- **Render**: Free tier available  
- **Google Cloud**: Pay per use

## 🚀 Choose Your Platform

| Platform | Difficulty | Free Tier | Setup Time |
|----------|------------|-----------|------------|
| Railway | ⭐ Easy | ✅ Yes | 5 minutes |
| Render | ⭐ Easy | ✅ Yes | 5 minutes |
| Heroku | ⭐⭐ Medium | ❌ No | 10 minutes |
| Google Cloud | ⭐⭐⭐ Hard | ✅ Credits | 15 minutes |

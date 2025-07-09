# 🔒 Secure MCP Server

A production-ready Model Context Protocol (MCP) server implementation in Python with enterprise-grade security features, designed for scalable deployment on cloud platforms and VPS environments.

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)
[![Security](https://img.shields.io/badge/Security-Enterprise-green)](docs/security/SECURITY.md)
[![Deployment](https://img.shields.io/badge/Deployment-Automated-green)](deployment/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

## 🚀 Features

### 🔐 Security First
- **API Key Authentication**: Multi-key support with secure token validation
- **Rate Limiting**: Configurable request throttling (default: 100 req/min)
- **Request Validation**: Input sanitization and schema validation
- **CORS Protection**: Configurable cross-origin resource sharing
- **Security Headers**: Production-ready HTTP security headers

### 🌐 MCP Protocol Compliance
- **Full MCP Support**: Complete Model Context Protocol implementation
- **Tool Registry**: Dynamic tool registration and management
- **JSON-RPC 2.0**: Standard JSON-RPC protocol support
- **Extensible Architecture**: Easy to add custom tools and handlers

### 📊 Monitoring & Observability
- **Health Checks**: Built-in health and readiness endpoints
- **Performance Metrics**: Request timing and resource usage tracking
- **Detailed Logging**: Structured logging with configurable levels
- **Error Tracking**: Comprehensive error handling and reporting

### 🚀 Deployment Ready
- **Docker Support**: Production-optimized containerization
- **One-Command Deploy**: Automated Dokploy VPS deployment
- **Environment Management**: Secure configuration handling
- **Auto-scaling**: Container orchestration support

## 📂 Project Architecture

```
mcp-server/
├── 📄 Essential Files
│   ├── README.md              # Project documentation
│   ├── requirements.txt       # Production dependencies
│   ├── Dockerfile.production  # Production container
│   └── deploy_dokploy.sh     # Deployment automation
│
├── 🔧 Source Code
│   ├── src/server/           # Core server implementation
│   ├── src/tools/            # MCP tool implementations
│   └── src/utils/            # Utility functions
│
├── ⚙️ Configuration
│   ├── config/               # Application settings
│   └── deployment/           # Deployment configurations
│
├── 📚 Documentation
│   ├── docs/api/             # API documentation
│   ├── docs/security/        # Security guidelines
│   └── docs/deployment/      # Deployment guides
│
├── 🧪 Testing
│   ├── tests/unit/           # Unit tests
│   ├── tests/integration/    # Integration tests
│   └── tests/security/       # Security tests
│
└── 💡 Examples & Scripts
    ├── examples/             # Usage examples
    └── scripts/              # Utility scripts
```

## ⚡ Quick Start

### 🐳 Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mcp-server.git
cd mcp-server

# Build and run with Docker
docker build -f Dockerfile.production -t mcp-server .
docker run -p 8080:8080 -e API_KEYS="your-secure-api-key" mcp-server
```

### 🚀 One-Command VPS Deployment

```bash
# Deploy to Dokploy VPS
./deploy_dokploy.sh
```

### 🔧 Development Setup

```bash
# 1. Clone and setup
git clone https://github.com/YOUR_USERNAME/mcp-server.git
cd mcp-server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements-dev.txt

# 3. Generate API key
python scripts/key_generator.py

# 4. Start server with tools (recommended)
python start_server.py --api-keys YOUR_API_KEY --port 8080

# Alternative: Run module directly
python -m src.server.secure_server --api-keys YOUR_API_KEY --port 8080
```

### 🛠️ Starting with Tools

The server automatically loads example tools from `src/tools/example_tools.py`:

```bash
# Start server with your API key
python start_server.py --api-keys LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4

# The server will show:
# ✅ Loaded 2 default tools
# 🔧 Available tools: ['system_info', 'echo']
```

**Default Tools Included:**
- **`system_info`**: Get system information (OS, CPU, memory, disk)
- **`echo`**: Echo back messages for testing

## 🔑 Authentication

The server uses API key authentication. Include your key in requests:

### Unix/Linux/Mac (bash/zsh)
```bash
# Health check (public endpoint)
curl http://localhost:8080/health

# List tools (requires authentication)
curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8080/api/tools

# MCP request (requires authentication)
curl -X POST http://localhost:8080/mcp \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

### Windows PowerShell
```powershell
# Health check (public endpoint)
Invoke-WebRequest -Uri http://localhost:8080/health

# List tools (requires authentication)
Invoke-WebRequest -Uri http://localhost:8080/api/tools -Headers @{"Authorization" = "Bearer YOUR_API_KEY"}

# MCP request (requires authentication)
Invoke-WebRequest -Uri http://localhost:8080/mcp -Method POST `
  -Headers @{"Authorization" = "Bearer YOUR_API_KEY"; "Content-Type" = "application/json"} `
  -Body '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

### Windows Command Prompt
```cmd
# Health check (public endpoint)
curl http://localhost:8080/health

# List tools (requires authentication)
curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8080/api/tools

# MCP request (requires authentication)
curl -X POST http://localhost:8080/mcp ^
  -H "Authorization: Bearer YOUR_API_KEY" ^
  -H "Content-Type: application/json" ^
  -d "{\"jsonrpc\": \"2.0\", \"method\": \"tools/list\", \"id\": 1}"
```

## 📋 API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/health` | GET | No | Health check and server status |
| `/api/tools` | GET | Yes | List available MCP tools |
| `/mcp` | POST | Yes | MCP JSON-RPC endpoint |

### Expected API Responses

#### Health Endpoint
```json
{
  "status": "healthy",
  "timestamp": "2025-07-09T10:30:00Z",
  "uptime": 3600.5,
  "version": "1.0.0"
}
```

#### Tools Endpoint
```json
{
  "tools": []
}
```
*Note: Empty array `[]` is normal for a fresh installation. Tools can be added by registering them in the server configuration.*

#### MCP Endpoint
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": []
  },
  "id": 1
}
```

### 🔧 Adding Tools

To add MCP tools to your server, you can:

1. **Add tool definitions** in `src/tools/` directory
2. **Register tools** in the server configuration
3. **Use the tool registry** API to dynamically add tools

Example tool registration:
```python
# In your server setup
from src.tools.example_tool import ExampleTool

# Register the tool
server.register_tool(ExampleTool())
```

See [Tool Development Guide](docs/api/TOOLS.md) for details.

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEYS` | Comma-separated API keys | - | ✅ |
| `PORT` | Server port | 8080 | ❌ |
| `HOST` | Server host | 0.0.0.0 | ❌ |
| `ENVIRONMENT` | Environment (dev/prod) | development | ❌ |
| `LOG_LEVEL` | Logging level | INFO | ❌ |
| `RATE_LIMIT` | Requests per minute | 100 | ❌ |

### Production Configuration

```bash
# .env file
API_KEYS=key1,key2,key3
PORT=8080
HOST=0.0.0.0
ENVIRONMENT=production
LOG_LEVEL=INFO
RATE_LIMIT=100
```

## 🚀 Deployment Options

### 1. **Dokploy VPS** (Recommended)
- ✅ One-command deployment
- ✅ Automatic SSL/TLS
- ✅ Health monitoring
- ✅ Rolling updates

### 2. **Docker**
- ✅ Containerized deployment
- ✅ Environment isolation
- ✅ Scalable architecture

### 3. **Cloud Platforms**
- ✅ AWS ECS/Fargate
- ✅ Google Cloud Run
- ✅ Railway, Heroku
- ✅ See [Cloud Deployment Guide](docs/deployment/CLOUD_DEPLOYMENT.md)

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test categories
python -m pytest tests/unit/           # Unit tests
python -m pytest tests/integration/   # Integration tests
python -m pytest tests/security/      # Security tests

# Run with coverage
python -m pytest --cov=src tests/
```

## 🔒 Security Features

- **🔐 Authentication**: Multi-API key support with secure validation
- **🛡️ Rate Limiting**: Configurable request throttling per IP
- **🚫 Input Validation**: Request sanitization and schema validation
- **🔒 Secure Headers**: HSTS, CSP, and other security headers
- **📊 Monitoring**: Request logging and abuse detection
- **🔍 Audit Trail**: Comprehensive access and error logging

See [Security Documentation](docs/security/SECURITY.md) for details.

## 📚 Documentation

- **[API Documentation](docs/api/API.md)** - Complete API reference
- **[Security Guide](docs/security/SECURITY.md)** - Security implementation
- **[Deployment Guide](docs/deployment/)** - Deployment instructions
- **[Cloud Deployment](docs/deployment/CLOUD_DEPLOYMENT.md)** - Cloud platform guides

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📊 Project Status

- **🎯 Status**: Production Ready
- **🔒 Security**: Enterprise Grade
- **📈 Performance**: Optimized
- **🚀 Deployment**: Automated
- **📚 Documentation**: Complete

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Model Context Protocol (MCP) specification
- Python HTTP server community
- Docker and containerization ecosystem
- Security best practices community

---

**🚀 Ready to deploy? Use `./deploy_dokploy.sh` for instant VPS deployment!**

## 🌐 Browser API Testing

You can test the MCP server API directly from your browser using various methods:

### 🔧 Browser Developer Console (JavaScript)

Open your browser's Developer Console (F12) and use these JavaScript snippets:

#### Health Check (No Authentication)
```javascript
fetch('http://localhost:8080/health')
  .then(response => response.json())
  .then(data => console.log('Health:', data))
  .catch(error => console.error('Error:', error));
```

#### List Tools (With Authentication)
```javascript
fetch('http://localhost:8080/api/tools', {
  headers: {
    'Authorization': 'Bearer LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4'
  }
})
.then(response => response.json())
.then(data => console.log('Tools:', data))
.catch(error => console.error('Error:', error));
```

#### Execute Echo Tool via MCP
```javascript
fetch('http://localhost:8080/mcp', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "echo",
      "arguments": {"message": "Hello from browser!"}
    },
    "id": 1
  })
})
.then(response => response.json())
.then(data => console.log('Echo Result:', data))
.catch(error => console.error('Error:', error));
```

#### Execute System Info Tool
```javascript
fetch('http://localhost:8080/mcp', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "system_info",
      "arguments": {"detail_level": "basic"}
    },
    "id": 2
  })
})
.then(response => response.json())
.then(data => console.log('System Info:', data))
.catch(error => console.error('Error:', error));
```

### 🌐 Browser Extensions (REST Client)

Use browser extensions like **REST Client**, **Postman**, or **Insomnia**:

#### Setup
1. **URL**: `http://localhost:8080/mcp`
2. **Method**: `POST`
3. **Headers**:
   - `Authorization`: `Bearer LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4`
   - `Content-Type`: `application/json`

#### Request Body (Echo Tool)
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "echo",
    "arguments": {
      "message": "Hello from REST client!"
    }
  },
  "id": 1
}
```

#### Request Body (System Info Tool)
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "system_info",
    "arguments": {
      "detail_level": "detailed"
    }
  },
  "id": 2
}
```

### 📱 Simple HTML Test Page

Create an HTML file to test the API:

```html
<!DOCTYPE html>
<html>
<head>
    <title>MCP Server API Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        button { margin: 10px; padding: 10px; }
        pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
        input[type="text"] { padding: 8px; margin: 5px; width: 300px; }
    </style>
</head>
<body>
    <h1>🔒 MCP Server API Test</h1>
    
    <button onclick="testHealth()">Test Health</button>
    <button onclick="testTools()">List Tools</button>
    <button onclick="testEcho()">Test Echo Tool</button>
    <button onclick="testSystemInfo()">Test System Info</button>
    
    <h3>Results:</h3>
    <pre id="results"></pre>

    <script>
        const API_KEY = 'LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4';
        const BASE_URL = 'http://localhost:8080';
        
        function log(message) {
            document.getElementById('results').textContent += message + '\n';
        }
        
        async function testHealth() {
            try {
                const response = await fetch(`${BASE_URL}/health`);
                const data = await response.json();
                log('✅ Health: ' + JSON.stringify(data, null, 2));
            } catch (error) {
                log('❌ Health Error: ' + error.message);
            }
        }
        
        async function testTools() {
            try {
                const response = await fetch(`${BASE_URL}/api/tools`, {
                    headers: { 'Authorization': `Bearer ${API_KEY}` }
                });
                const data = await response.json();
                log('🔧 Tools: ' + JSON.stringify(data, null, 2));
            } catch (error) {
                log('❌ Tools Error: ' + error.message);
            }
        }
        
        async function testEcho() {
            try {
                const response = await fetch(`${BASE_URL}/mcp`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${API_KEY}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        "jsonrpc": "2.0",
                        "method": "tools/call",
                        "params": {
                            "name": "echo",
                            "arguments": {"message": "Hello from browser!"}
                        },
                        "id": 1
                    })
                });
                const data = await response.json();
                log('📢 Echo: ' + JSON.stringify(data, null, 2));
            } catch (error) {
                log('❌ Echo Error: ' + error.message);
            }
        }
        
        async function testSystemInfo() {
            try {
                const response = await fetch(`${BASE_URL}/mcp`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${API_KEY}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        "jsonrpc": "2.0",
                        "method": "tools/call",
                        "params": {
                            "name": "system_info",
                            "arguments": {"detail_level": "basic"}
                        },
                        "id": 2
                    })
                });
                const data = await response.json();
                log('💻 System Info: ' + JSON.stringify(data, null, 2));
            } catch (error) {
                log('❌ System Info Error: ' + error.message);
            }
        }
    </script>
</body>
</html>
```

### 🔍 Available Tool Methods

#### List All Tools
```javascript
// Method: tools/list
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}
```

#### Call Echo Tool
```javascript
// Method: tools/call
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "echo",
    "arguments": {
      "message": "Your message here"
    }
  },
  "id": 1
}
```

#### Call System Info Tool
```javascript
// Method: tools/call  
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "system_info",
    "arguments": {
      "detail_level": "basic"  // or "detailed"
    }
  },
  "id": 2
}
```

### ⚠️ CORS Note

If you encounter CORS errors when testing from a browser, the server includes CORS headers. If issues persist, you can:

1. **Use browser extensions** that disable CORS for testing
2. **Start Chrome with CORS disabled**: `chrome --disable-web-security --user-data-dir=/tmp/chrome_dev`
3. **Use the server's built-in CORS support** (already enabled)

### 🚨 Browser "Failed to fetch" Error

If you get "Failed to fetch" when testing from browser:

#### **Quick Fixes:**
1. **Try different URLs**:
   ```javascript
   // Instead of localhost, try:
   'http://127.0.0.1:8080'  // Often works when localhost fails
   'http://your-actual-ip:8080'  // For network access
   ```

2. **Check server is running**:
   ```bash
   # Windows
   netstat -an | findstr :8080
   
   # Should show: TCP 0.0.0.0:8080 ... LISTENING
   ```

3. **Test with curl first**:
   ```bash
   curl http://localhost:8080/health
   curl http://127.0.0.1:8080/health
   ```

#### **Browser-Specific Solutions:**

##### **Chrome CORS Issues**
```bash
# Start Chrome with CORS disabled (for testing only)
chrome.exe --disable-web-security --user-data-dir=c:\temp\chrome --allow-running-insecure-content
```

##### **Firefox Network Issues**
1. Open `about:config`
2. Set `network.dns.disableIPv6` to `true`
3. Restart Firefox

##### **Edge/Safari Issues**
- Use the updated `test_browser.html` with better error handling
- Check browser console (F12) for detailed error messages
- Try incognito/private mode

#### **Network Troubleshooting:**
```bash
# 1. Check if server responds
curl -v http://localhost:8080/health

# 2. Check firewall
# Windows: Check Windows Defender Firewall
# Allow Python through firewall if prompted

# 3. Try different port
python start_server.py --api-keys YOUR_KEY --port 8081
```

#### **Alternative Testing Methods:**
1. **Browser Extensions**: Install REST Client, Postman, or Thunder Client
2. **Command Line**: Use curl or PowerShell (working examples above)
3. **Different Browser**: Try Chrome, Firefox, Edge to isolate issues
4. **Network Tools**: Use browser DevTools Network tab to see exact error

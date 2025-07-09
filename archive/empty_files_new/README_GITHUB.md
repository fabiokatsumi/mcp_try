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

# 4. Run development server
python -m src.server.secure_server --api-keys YOUR_API_KEY --port 8080
```

## 🔑 Authentication

The server uses API key authentication. Include your key in requests:

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

## 📋 API Endpoints

| Endpoint | Method | Auth Required | Description |
|----------|--------|---------------|-------------|
| `/health` | GET | No | Health check and server status |
| `/api/tools` | GET | Yes | List available MCP tools |
| `/mcp` | POST | Yes | MCP JSON-RPC endpoint |

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

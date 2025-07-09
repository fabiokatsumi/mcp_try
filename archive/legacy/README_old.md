# 🔒 Secure MCP Server

A production-ready Model Context Protocol (MCP) server implementation in Python with API key authentication, designed for secure deployment on Dokploy VPS.

## 🚀 Features

- **🔐 API Key Authentication**: Secure access control with API keys
- **🔄 Rate Limiting**: Protection against abuse (100 requests per minute per IP)
- **📊 Monitoring**: Detailed request logging and performance monitoring
- **🌐 MCP Protocol**: Full compliance with the Model Context Protocol
- **🔧 Tool Registry**: Dynamically register and manage MCP tools
- **🛡️ Security**: Best practices for production deployment

## � Project Structure

```
mcp_try/
├── src/                    # Source code
│   ├── server/            # Server implementations
│   ├── tools/             # MCP tool implementations
│   └── utils/             # Utility functions
├── config/                # Configuration files
├── deployment/            # Deployment scripts and configs
├── docs/                  # Documentation
├── tests/                 # Test suites
├── scripts/               # Utility scripts
├── examples/              # Example code
└── archive/               # Archived/legacy files
```

## �📋 Getting Started

### Requirements

- Python 3.9+
- Docker (for containerization)
- Dokploy-compatible VPS (for production deployment)

### Development Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp_try
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Generate API keys:
   ```bash
   python scripts/key_generator.py
   ```

4. Run the server:
   ```bash
   python -m src.server.secure_server --api-keys YOUR_API_KEY
   ```

## 🚀 Deployment

### Dokploy VPS Deployment

We provide a streamlined deployment process for Dokploy VPS:

1. Run the deployment script:
   ```bash
   cd deployment/dokploy
   ./deploy_dokploy.sh
   ```

2. Follow the instructions in `docs/deployment/DOKPLOY_DEPLOYMENT_GUIDE.md`

### Manual Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t secure-mcp-server -f Dockerfile.production .
   ```

2. Run the container:
   ```bash
   docker run -p 8443:8443 -e MCP_API_KEYS=YOUR_API_KEY secure-mcp-server
   ```

## 📚 Documentation

- **[API Documentation](docs/api/API.md)**: Detailed API reference
- **[Security Implementation](docs/security/SECURITY_IMPLEMENTATION.md)**: Security features
- **[Deployment Guide](docs/deployment/DOKPLOY_DEPLOYMENT_GUIDE.md)**: Production deployment

## 🧪 Testing

Run tests:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test category
python -m unittest discover tests/integration
python -m unittest discover tests/security
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

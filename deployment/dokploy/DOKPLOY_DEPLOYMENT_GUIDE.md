# Dokploy Deployment Guide

## Quick Start

Deploy your MCP server to a VPS using Dokploy with one command:

```bash
./deploy_dokploy.sh
```

## Prerequisites

- VPS with Dokploy installed
- Docker support
- Domain name (optional, for SSL)

## Environment Variables

Create `.env` file:
```bash
API_KEYS=your-secure-api-key
PORT=8080
HOST=0.0.0.0
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Deployment Steps

1. **Configure Environment**
   ```bash
   cp deployment/env/.env.example .env
   # Edit .env with your settings
   ```

2. **Deploy**
   ```bash
   ./deploy_dokploy.sh
   ```

3. **Verify Deployment**
   ```bash
   curl https://your-domain.com/health
   ```

## Monitoring

- Health checks at `/health`
- Logs via Dokploy dashboard
- Automatic SSL/TLS certificates

## Troubleshooting

### Common Issues

1. **Port conflicts** - Change PORT in .env
2. **Domain not resolving** - Check DNS settings
3. **SSL certificate issues** - Verify domain ownership

### Support

Check the deployment logs in Dokploy dashboard for detailed error information.

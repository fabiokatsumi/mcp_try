# 🌐 Cloud Deployment Guide

This guide covers deploying the MCP Server to various cloud platforms for production use.

## 🎯 Overview

The MCP Server project is designed for secure, scalable cloud deployment with:
- **Docker containerization** for consistent environments
- **Environment-based configuration** for security
- **Health checks and monitoring** for reliability
- **Dokploy VPS integration** for easy deployment

## 🚀 Deployment Options

### 1. Dokploy VPS (Recommended)

The easiest deployment method using our automated scripts:

```bash
# One-command deployment
./deploy_dokploy.sh
```

**Features:**
- Automated Docker build and deploy
- Environment variable management
- Health check monitoring
- Automatic SSL/TLS certificates
- Rolling deployments

**Prerequisites:**
- Dokploy-compatible VPS
- Docker installed
- Domain name (optional, for SSL)

**Configuration:**
1. Copy environment template:
   ```bash
   cp deployment/env/.env.example .env
   ```

2. Configure your environment variables:
   ```bash
   # .env file
   API_KEYS=your-secure-api-key-here
   PORT=8080
   HOST=0.0.0.0
   ENVIRONMENT=production
   LOG_LEVEL=INFO
   ```

3. Deploy:
   ```bash
   ./deploy_dokploy.sh
   ```

### 2. Docker Deployment

For manual Docker deployment:

```bash
# Build production image
docker build -f Dockerfile.production -t mcp-server:latest .

# Run with environment variables
docker run -d \
  --name mcp-server \
  -p 8080:8080 \
  -e API_KEYS="your-api-key" \
  -e ENVIRONMENT="production" \
  mcp-server:latest
```

### 3. AWS ECS

Deploy to Amazon Elastic Container Service:

1. **Build and push to ECR:**
   ```bash
   # Create ECR repository
   aws ecr create-repository --repository-name mcp-server

   # Build and tag
   docker build -f Dockerfile.production -t mcp-server .
   docker tag mcp-server:latest 123456789012.dkr.ecr.region.amazonaws.com/mcp-server:latest

   # Push to ECR
   docker push 123456789012.dkr.ecr.region.amazonaws.com/mcp-server:latest
   ```

2. **Create ECS task definition:**
   ```json
   {
     "family": "mcp-server",
     "cpu": "256",
     "memory": "512",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "executionRoleArn": "arn:aws:iam::account:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "mcp-server",
         "image": "123456789012.dkr.ecr.region.amazonaws.com/mcp-server:latest",
         "portMappings": [
           {
             "containerPort": 8080,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "ENVIRONMENT",
             "value": "production"
           }
         ],
         "secrets": [
           {
             "name": "API_KEYS",
             "valueFrom": "arn:aws:secretsmanager:region:account:secret:mcp-server-api-keys"
           }
         ]
       }
     ]
   }
   ```

### 4. Google Cloud Run

Deploy to Google Cloud Run:

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/mcp-server

# Deploy to Cloud Run
gcloud run deploy mcp-server \
  --image gcr.io/PROJECT_ID/mcp-server \
  --platform managed \
  --region us-central1 \
  --set-env-vars ENVIRONMENT=production \
  --set-secrets API_KEYS=mcp-server-api-keys:latest
```

### 5. Railway

Deploy using Railway platform:

1. **Create `Procfile`:**
   ```
   web: python -m src.server.secure_server --port $PORT
   ```

2. **Deploy:**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli

   # Login and deploy
   railway login
   railway init
   railway up
   ```

### 6. Heroku

Deploy to Heroku:

```bash
# Create Heroku app
heroku create your-mcp-server

# Set environment variables
heroku config:set API_KEYS="your-api-key" --app your-mcp-server
heroku config:set ENVIRONMENT="production" --app your-mcp-server

# Deploy
git push heroku main
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEYS` | Comma-separated API keys | - | ✅ |
| `PORT` | Server port | 8080 | ❌ |
| `HOST` | Server host | 0.0.0.0 | ❌ |
| `ENVIRONMENT` | Deployment environment | development | ❌ |
| `LOG_LEVEL` | Logging level | INFO | ❌ |
| `RATE_LIMIT` | Requests per minute | 100 | ❌ |
| `CORS_ORIGINS` | Allowed CORS origins | * | ❌ |

### Health Checks

The server provides health check endpoints:

- **`/health`** - Basic health check
- **`/ready`** - Readiness probe
- **`/metrics`** - Application metrics

Example health check configuration:
```yaml
healthCheck:
  path: /health
  port: 8080
  intervalSeconds: 30
  timeoutSeconds: 5
  healthyThreshold: 2
  unhealthyThreshold: 3
```

## 🔐 Security Considerations

### 1. API Keys
- Use strong, randomly generated API keys
- Store in secure environment variables or secrets management
- Rotate keys regularly
- Monitor for unauthorized usage

### 2. Network Security
- Use HTTPS in production
- Configure proper CORS origins
- Implement IP whitelisting if needed
- Use VPC/private networks when available

### 3. Monitoring
- Enable application logs
- Set up error alerting
- Monitor performance metrics
- Track API usage patterns

## 📊 Monitoring and Logging

### Application Logs
```bash
# View logs (Docker)
docker logs mcp-server

# View logs (Dokploy)
dokploy logs mcp-server

# View logs (Cloud platforms)
# Follow platform-specific logging
```

### Metrics
The server exposes metrics at `/metrics` endpoint:
- Request count and duration
- Error rates
- Active connections
- Resource usage

### Alerting
Set up alerts for:
- High error rates (>5%)
- Slow response times (>500ms)
- High memory usage (>80%)
- API key abuse

## 🔄 Deployment Best Practices

### 1. Blue-Green Deployment
- Deploy to staging environment first
- Run health checks and tests
- Switch traffic gradually
- Keep rollback capability

### 2. Database Migrations
- Run migrations before deployment
- Use database versioning
- Test migrations in staging
- Have rollback procedures

### 3. Secrets Management
- Never commit secrets to version control
- Use platform-native secrets management
- Rotate secrets regularly
- Audit secret access

### 4. Scaling
- Monitor resource usage
- Set up auto-scaling rules
- Load test before scaling
- Use container orchestration

## 🚨 Troubleshooting

### Common Issues

**Container won't start:**
```bash
# Check logs
docker logs mcp-server

# Common causes:
# - Missing environment variables
# - Port conflicts
# - Resource constraints
```

**Health check failures:**
```bash
# Test health endpoint
curl http://localhost:8080/health

# Check server logs for errors
```

**High response times:**
- Check resource usage
- Review rate limiting settings
- Optimize application code
- Scale horizontally

### Getting Help

1. **Check logs** first for error messages
2. **Review documentation** in `docs/` directory
3. **Run tests** to verify functionality
4. **Contact support** with detailed error information

## 📚 Additional Resources

- [Deployment Documentation](docs/deployment/)
- [Security Guide](docs/security/SECURITY.md)
- [API Documentation](docs/api/API.md)
- [Troubleshooting Guide](deployment/dokploy/dokploy-troubleshooting.md)

---

**Next Steps:**
1. Choose your deployment platform
2. Configure environment variables
3. Deploy using provided scripts
4. Set up monitoring and alerts
5. Test the deployment thoroughly
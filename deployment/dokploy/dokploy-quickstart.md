# Dokploy Quick Start

## Deploy MCP Server in 5 Minutes

1. **Prerequisites**
   - VPS with Dokploy installed
   - Domain name pointed to your VPS

2. **One-Command Deploy**
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp-server.git
   cd mcp-server
   ./deploy_dokploy.sh
   ```

3. **Configure Environment**
   ```bash
   # Set your API key
   export API_KEYS="your-secure-api-key"
   ```

4. **Verify**
   ```bash
   curl https://your-domain.com/health
   ```

## That's it! 🚀

Your secure MCP server is now running with:
- ✅ SSL/TLS encryption
- ✅ API key authentication  
- ✅ Rate limiting protection
- ✅ Health monitoring
- ✅ Automatic updates

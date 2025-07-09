# API Documentation

## MCP Server API Reference

### Authentication

All API endpoints (except `/health`) require authentication using API keys.

**Authorization Header:**
```
Authorization: Bearer YOUR_API_KEY
```

### Endpoints

#### Health Check
- **URL:** `/health`
- **Method:** `GET`
- **Auth Required:** No
- **Description:** Server health status

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-07-08T10:30:00",
  "uptime": "00:15:30",
  "version": "1.0.0"
}
```

#### List Tools
- **URL:** `/api/tools`
- **Method:** `GET`
- **Auth Required:** Yes
- **Description:** List available MCP tools

**Response:**
```json
{
  "tools": ["tool1", "tool2"]
}
```

#### MCP JSON-RPC Endpoint
- **URL:** `/mcp`
- **Method:** `POST`
- **Auth Required:** Yes
- **Description:** Main MCP protocol endpoint

**Request:**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "result": {
    "tools": ["tool1", "tool2"]
  },
  "id": 1
}
```

### Error Responses

#### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "API key required. Use Authorization: Bearer <api_key>"
}
```

#### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Invalid API key"
}
```

#### 429 Rate Limited
```json
{
  "error": "Too many requests",
  "message": "Rate limit exceeded. Please try again later."
}
```

### Rate Limiting

- **Limit:** 100 requests per minute per IP
- **Headers:** `Retry-After: 60` when rate limited

### CORS Support

The server includes CORS headers for web client compatibility:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization`

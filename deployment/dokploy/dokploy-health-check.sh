#!/bin/bash
# Health check script for Dokploy MCP Server

# Set the server URL (port 8443 is default for secure server)
SERVER_URL="http://localhost:8443/health"

# Send a request to the health check endpoint
response=$(curl -s -o /dev/null -w "%{http_code}" "$SERVER_URL")

# Check if the response is 200 OK
if [ "$response" = "200" ]; then
    echo "Health check passed: HTTP 200 OK"
    exit 0
else
    echo "Health check failed: HTTP $response"
    exit 1
fi

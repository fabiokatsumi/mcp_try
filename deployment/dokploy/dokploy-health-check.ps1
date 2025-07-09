# PowerShell Health Check Script for Dokploy MCP Server

# Set the server URL (port 8443 is default for secure server)
$serverUrl = "http://localhost:8443/health"

try {
    # Send a request to the health check endpoint
    $response = Invoke-WebRequest -Uri $serverUrl -UseBasicParsing -ErrorAction Stop
    
    # Check if the response is 200 OK
    if ($response.StatusCode -eq 200) {
        Write-Output "Health check passed: HTTP 200 OK"
        exit 0
    } else {
        Write-Output "Health check failed: HTTP $($response.StatusCode)"
        exit 1
    }
} catch {
    Write-Output "Health check failed: $_"
    exit 1
}

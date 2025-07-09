# Dokploy MCP Server Health Check Script (PowerShell Version)
# Use this script to verify your deployment is working correctly on Windows

param(
    [string]$ServerUrl = "https://mcp.yourdomain.com",
    [string]$ApiKey = "your-api-key-here",
    [int]$Timeout = 30,
    [switch]$Help
)

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    White = "White"
}

function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Colors.Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[PASS] $Message" -ForegroundColor $Colors.Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor $Colors.Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor $Colors.Red
}

function Show-Usage {
    Write-Host "Usage: ./dokploy-health-check.ps1 [OPTIONS]" -ForegroundColor $Colors.White
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  -ServerUrl URL     Server URL (default: $ServerUrl)"
    Write-Host "  -ApiKey KEY        API key for authentication"
    Write-Host "  -Timeout SEC       Request timeout in seconds (default: $Timeout)"
    Write-Host "  -Help              Show this help message"
    Write-Host ""
    Write-Host "Example:"
    Write-Host "  ./dokploy-health-check.ps1 -ServerUrl https://mcp.example.com -ApiKey your-api-key"
}

function Test-Endpoint {
    param(
        [string]$Url,
        [int]$ExpectedStatus,
        [string]$Description,
        [hashtable]$Headers = @{}
    )
    
    Write-Status "Testing: $Description"
    
    try {
        $response = Invoke-WebRequest -Uri $Url -Method GET -Headers $Headers -TimeoutSec $Timeout -UseBasicParsing -ErrorAction Stop
        $statusCode = $response.StatusCode
        
        if ($statusCode -eq $ExpectedStatus) {
            Write-Success "$Description (HTTP $statusCode)"
            return $true
        } else {
            Write-Error "$Description (Expected: $ExpectedStatus, Got: $statusCode)"
            return $false
        }
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode -eq $ExpectedStatus) {
            Write-Success "$Description (HTTP $statusCode)"
            return $true
        } else {
            Write-Error "$Description (Expected: $ExpectedStatus, Got: $statusCode)"
            if ($_.Exception.Message) {
                Write-Host "Error: $($_.Exception.Message)" -ForegroundColor $Colors.Red
            }
            return $false
        }
    }
}

function Main {
    Write-Host "========================================" -ForegroundColor $Colors.White
    Write-Host "🏥 MCP Server Health Check" -ForegroundColor $Colors.White
    Write-Host "========================================" -ForegroundColor $Colors.White
    Write-Host "Server URL: $ServerUrl" -ForegroundColor $Colors.White
    Write-Host "Timeout: ${Timeout}s" -ForegroundColor $Colors.White
    Write-Host "========================================" -ForegroundColor $Colors.White
    
    $failures = 0
    
    # Test 1: Health endpoint (no auth required)
    if (-not (Test-Endpoint -Url "$ServerUrl/health" -ExpectedStatus 200 -Description "Health Check Endpoint")) {
        $failures++
    }
    
    # Test 2: API without authentication (should fail)
    if (-not (Test-Endpoint -Url "$ServerUrl/api/tools" -ExpectedStatus 401 -Description "API Endpoint (No Auth)")) {
        $failures++
    }
    
    # Test 3: API with authentication (should succeed)
    $authHeaders = @{ "Authorization" = "Bearer $ApiKey" }
    if (-not (Test-Endpoint -Url "$ServerUrl/api/tools" -ExpectedStatus 200 -Description "API Endpoint (With Auth)" -Headers $authHeaders)) {
        $failures++
    }
    
    # Test 4: Invalid API key (should fail)
    $invalidHeaders = @{ "Authorization" = "Bearer invalid-key" }
    if (-not (Test-Endpoint -Url "$ServerUrl/api/tools" -ExpectedStatus 401 -Description "API Endpoint (Invalid Auth)" -Headers $invalidHeaders)) {
        $failures++
    }
    
    # Test 5: Rate limiting test
    Write-Status "Testing rate limiting..."
    $rateLimitHits = 0
    for ($i = 1; $i -le 20; $i++) {
        try {
            $response = Invoke-WebRequest -Uri "$ServerUrl/api/tools" -Method GET -Headers $authHeaders -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
        }
        catch {
            if ($_.Exception.Response.StatusCode.value__ -eq 429) {
                $rateLimitHits++
                break
            }
        }
        Start-Sleep -Milliseconds 100
    }
    
    if ($rateLimitHits -gt 0) {
        Write-Success "Rate Limiting (Triggered after multiple requests)"
    } else {
        Write-Warning "Rate Limiting (Not triggered - may need tuning)"
    }
    
    # Test 6: SSL Certificate
    Write-Status "Testing SSL certificate..."
    try {
        $response = Invoke-WebRequest -Uri "$ServerUrl/health" -Method HEAD -TimeoutSec $Timeout -UseBasicParsing -ErrorAction Stop
        Write-Success "SSL Certificate (Valid)"
    }
    catch {
        Write-Error "SSL Certificate (Connection failed)"
        $failures++
    }
    
    # Test 7: Response time
    Write-Status "Testing response time..."
    try {
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        $response = Invoke-WebRequest -Uri "$ServerUrl/health" -Method GET -TimeoutSec $Timeout -UseBasicParsing -ErrorAction Stop
        $stopwatch.Stop()
        
        $responseMs = $stopwatch.ElapsedMilliseconds
        
        if ($responseMs -lt 1000) {
            Write-Success "Response Time (${responseMs}ms)"
        } elseif ($responseMs -lt 3000) {
            Write-Warning "Response Time (${responseMs}ms - Consider optimization)"
        } else {
            Write-Error "Response Time (${responseMs}ms - Too slow)"
            $failures++
        }
    }
    catch {
        Write-Error "Response Time (Timeout after ${Timeout}s)"
        $failures++
    }
    
    # Summary
    Write-Host "========================================" -ForegroundColor $Colors.White
    if ($failures -eq 0) {
        Write-Success "🎉 All health checks passed!"
        Write-Host "Your MCP server is running correctly." -ForegroundColor $Colors.Green
    } else {
        Write-Error "❌ $failures health check(s) failed."
        Write-Host "Please review the issues above and check your deployment." -ForegroundColor $Colors.Red
        exit 1
    }
    Write-Host "========================================" -ForegroundColor $Colors.White
}

# Show usage if help requested
if ($Help) {
    Show-Usage
    exit 0
}

# Validate configuration
if ([string]::IsNullOrEmpty($ServerUrl)) {
    Write-Error "Server URL is required. Use -ServerUrl parameter."
    exit 1
}

if ([string]::IsNullOrEmpty($ApiKey) -or $ApiKey -eq "your-api-key-here") {
    Write-Error "Valid API key is required. Use -ApiKey parameter."
    exit 1
}

# Run health checks
Main

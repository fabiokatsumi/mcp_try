# PowerShell API Test Script for MCP Server
# This script tests the MCP server endpoints with proper PowerShell syntax

$baseUrl = "http://localhost:8080"
$apiKey = "LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4"

Write-Host "🧪 MCP Server API Test" -ForegroundColor Green
Write-Host "=" * 50

# Test health endpoint (no auth required)
Write-Host "`n🏥 Testing health endpoint..." -ForegroundColor Yellow
try {
    $healthResponse = Invoke-WebRequest -Uri "$baseUrl/health" -UseBasicParsing
    Write-Host "   Status: $($healthResponse.StatusCode)" -ForegroundColor Green
    Write-Host "   Response: $($healthResponse.Content)"
    $healthOk = $true
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    $healthOk = $false
}

# Test tools endpoint (auth required)
Write-Host "`n🔧 Testing tools endpoint..." -ForegroundColor Yellow
try {
    $headers = @{"Authorization" = "Bearer $apiKey"}
    $toolsResponse = Invoke-WebRequest -Uri "$baseUrl/api/tools" -Headers $headers -UseBasicParsing
    Write-Host "   Status: $($toolsResponse.StatusCode)" -ForegroundColor Green
    Write-Host "   Response: $($toolsResponse.Content)"
    $toolsOk = $true
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    $toolsOk = $false
}

# Test MCP endpoint (auth required)
Write-Host "`n🎯 Testing MCP endpoint..." -ForegroundColor Yellow
try {
    $headers = @{
        "Authorization" = "Bearer $apiKey"
        "Content-Type" = "application/json"
    }
    $body = @{
        "jsonrpc" = "2.0"
        "method" = "tools/list"
        "id" = 1
    } | ConvertTo-Json
    
    $mcpResponse = Invoke-WebRequest -Uri "$baseUrl/mcp" -Method POST -Headers $headers -Body $body -UseBasicParsing
    Write-Host "   Status: $($mcpResponse.StatusCode)" -ForegroundColor Green
    Write-Host "   Response: $($mcpResponse.Content)"
    $mcpOk = $true
} catch {
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    $mcpOk = $false
}

# Results summary
Write-Host "`n📊 Test Results:" -ForegroundColor Cyan
Write-Host "   Health endpoint: $(if ($healthOk) { '✅ PASS' } else { '❌ FAIL' })"
Write-Host "   Tools endpoint:  $(if ($toolsOk) { '✅ PASS' } else { '❌ FAIL' })"
Write-Host "   MCP endpoint:    $(if ($mcpOk) { '✅ PASS' } else { '❌ FAIL' })"

if ($healthOk -and $toolsOk -and $mcpOk) {
    Write-Host "`n🎉 All tests passed! Your MCP server is working correctly." -ForegroundColor Green
} else {
    Write-Host "`n❌ Some tests failed. Check server status and configuration." -ForegroundColor Red
}

# Usage examples
Write-Host "`n💡 Usage Examples:" -ForegroundColor Cyan
Write-Host "   Health check:"
Write-Host "   Invoke-WebRequest -Uri $baseUrl/health"
Write-Host ""
Write-Host "   List tools:"
Write-Host "   Invoke-WebRequest -Uri $baseUrl/api/tools -Headers @{`"Authorization`" = `"Bearer YOUR_API_KEY`"}"
Write-Host ""
Write-Host "   MCP request:"
Write-Host "   `$headers = @{`"Authorization`" = `"Bearer YOUR_API_KEY`"; `"Content-Type`" = `"application/json`"}"
Write-Host "   `$body = '{`"jsonrpc`": `"2.0`", `"method`": `"tools/list`", `"id`": 1}'"
Write-Host "   Invoke-WebRequest -Uri $baseUrl/mcp -Method POST -Headers `$headers -Body `$body"

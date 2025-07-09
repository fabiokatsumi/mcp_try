@echo off
REM MCP Server API Test Script for Windows
REM Usage: test_api_curl.bat [API_KEY] [SERVER_URL]

SET API_KEY=%1
SET SERVER_URL=%2

REM Set defaults if not provided
IF "%API_KEY%"=="" SET API_KEY=LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4
IF "%SERVER_URL%"=="" SET SERVER_URL=http://localhost:8080

echo ================================================
echo 🔒 MCP Server API Test Script
echo ================================================
echo API Key: %API_KEY%
echo Server URL: %SERVER_URL%
echo.

echo ================================================
echo 🏥 Testing Health Endpoint (no auth required)
echo ================================================
curl -s "%SERVER_URL%/health" | python -m json.tool
echo.

echo ================================================
echo 🔧 Testing Tools List Endpoint
echo ================================================
curl -s -H "Authorization: Bearer %API_KEY%" "%SERVER_URL%/api/tools" | python -m json.tool
echo.

echo ================================================
echo 📡 Testing Echo Tool via MCP
echo ================================================
curl -s -X POST "%SERVER_URL%/mcp" ^
  -H "Authorization: Bearer %API_KEY%" ^
  -H "Content-Type: application/json" ^
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"echo\",\"arguments\":{\"message\":\"Hello from curl!\"}},\"id\":1}" | python -m json.tool
echo.

echo ================================================
echo 💻 Testing System Info Tool via MCP
echo ================================================
curl -s -X POST "%SERVER_URL%/mcp" ^
  -H "Authorization: Bearer %API_KEY%" ^
  -H "Content-Type: application/json" ^
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"tools/call\",\"params\":{\"name\":\"system_info\",\"arguments\":{}},\"id\":2}" | python -m json.tool
echo.

echo ================================================
echo ✅ API Testing Complete
echo ================================================
echo To test in browser:
echo 1. Open test_browser.html in your web browser
echo 2. Or use browser DevTools console with the examples in README.md
echo.
pause

@echo off
echo 🚀 Starting MCP Server with Tools...
echo.

REM Check if API key is provided
if "%1"=="" (
    echo ❌ Error: API key required
    echo Usage: start_server.bat YOUR_API_KEY
    echo Example: start_server.bat LKzvbSII_mpk5xyHArCOLO0kNT_N-3EVkGUX0JK-QU4
    pause
    exit /b 1
)

REM Start the server
python start_server.py --api-keys %1 --port 8080

echo.
echo ✅ Server stopped
pause

@echo off
REM Start MCP Server with LAN Access
REM This batch file starts the MCP HTTP server

echo.
echo ========================================
echo   MCP Server LAN Startup Script
echo ========================================
echo.

cd /d "%~dp0"

echo Starting MCP Server...
echo.
echo The server will be accessible at:
echo   Local:  http://localhost:8080
echo   LAN:    http://[YOUR_IP]:8080/
echo.
echo Press Ctrl+C to stop the server
echo.

python http_server.py

echo.
echo Server stopped.
pause

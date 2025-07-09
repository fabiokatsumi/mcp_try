@echo off
echo 🚀 MCP Server - GitHub Repository Setup Script
echo ================================================

echo.
echo 📋 Step 1: Checking Git installation...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git is not installed or not in PATH
    echo.
    echo 📥 Please install Git first:
    echo    - Download from: https://git-scm.com/download/win
    echo    - Or use winget: winget install Git.Git
    echo    - Or use Chocolatey: choco install git
    echo.
    echo After installing Git, run this script again.
    pause
    exit /b 1
) else (
    echo ✅ Git is installed
)

echo.
echo 📋 Step 2: Checking Git configuration...
git config --global user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Git user name not configured
    set /p username="Enter your full name: "
    git config --global user.name "%username%"
)

git config --global user.email >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Git email not configured
    set /p email="Enter your email address: "
    git config --global user.email "%email%"
)

echo ✅ Git configuration complete

echo.
echo 📋 Step 3: Initializing Git repository...
if not exist .git (
    git init
    echo ✅ Git repository initialized
) else (
    echo ℹ️  Git repository already exists
)

echo.
echo 📋 Step 4: Adding files to Git...
git add .
echo ✅ Files added to staging area

echo.
echo 📋 Step 5: Creating initial commit...
git commit -m "🎉 Initial commit: Production-ready MCP server

✨ Features:
- 🔒 Enterprise-grade security with API key authentication
- 🚀 One-command Dokploy deployment
- 📊 Comprehensive monitoring and health checks
- 🐳 Production-ready Docker containerization
- 🛡️ Rate limiting and request validation
- 📚 Complete documentation and examples
- 🧪 Full test suite coverage

🏗️ Architecture:
- Clean modular design
- Professional directory structure
- Secure configuration management
- Scalable deployment options"

echo ✅ Initial commit created

echo.
echo 🎯 Next Steps:
echo ================================================
echo.
echo 1. Create a repository on GitHub:
echo    - Go to https://github.com
echo    - Click "New repository"
echo    - Name: mcp-server (or your preferred name)
echo    - Description: 🔒 Production-ready MCP server with enterprise security features
echo    - Don't initialize with README, .gitignore, or license (we have them)
echo.
echo 2. Connect this repository to GitHub:
echo    Replace YOUR_USERNAME and REPO_NAME with your actual values:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Optional - Install GitHub CLI for easier management:
echo    winget install GitHub.cli
echo.
echo ✨ Your MCP server is ready for GitHub!
echo.
pause

# MCP Server - GitHub Repository Setup Script
# PowerShell version for better Windows integration

Write-Host "🚀 MCP Server - GitHub Repository Setup Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check Git installation
Write-Host "📋 Step 1: Checking Git installation..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>$null
    Write-Host "✅ Git is installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "📥 Please install Git first:" -ForegroundColor Yellow
    Write-Host "   - Download from: https://git-scm.com/download/win" -ForegroundColor White
    Write-Host "   - Or use winget: winget install Git.Git" -ForegroundColor White
    Write-Host "   - Or use Chocolatey: choco install git" -ForegroundColor White
    Write-Host ""
    Write-Host "After installing Git, run this script again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Step 2: Check Git configuration
Write-Host ""
Write-Host "📋 Step 2: Checking Git configuration..." -ForegroundColor Yellow

$userName = git config --global user.name 2>$null
if (-not $userName) {
    Write-Host "⚠️  Git user name not configured" -ForegroundColor Yellow
    $userName = Read-Host "Enter your full name"
    git config --global user.name "$userName"
}

$userEmail = git config --global user.email 2>$null
if (-not $userEmail) {
    Write-Host "⚠️  Git email not configured" -ForegroundColor Yellow
    $userEmail = Read-Host "Enter your email address"
    git config --global user.email "$userEmail"
}

Write-Host "✅ Git configuration complete" -ForegroundColor Green
Write-Host "   Name: $userName" -ForegroundColor White
Write-Host "   Email: $userEmail" -ForegroundColor White

# Step 3: Initialize Git repository
Write-Host ""
Write-Host "📋 Step 3: Initializing Git repository..." -ForegroundColor Yellow
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Git repository already exists" -ForegroundColor Blue
}

# Step 4: Add files to Git
Write-Host ""
Write-Host "📋 Step 4: Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "✅ Files added to staging area" -ForegroundColor Green

# Step 5: Create initial commit
Write-Host ""
Write-Host "📋 Step 5: Creating initial commit..." -ForegroundColor Yellow

$commitMessage = @"
🎉 Initial commit: Production-ready MCP server

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
- Scalable deployment options
"@

git commit -m $commitMessage
Write-Host "✅ Initial commit created" -ForegroundColor Green

# Next steps
Write-Host ""
Write-Host "🎯 Next Steps:" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create a repository on GitHub:" -ForegroundColor Yellow
Write-Host "   - Go to https://github.com" -ForegroundColor White
Write-Host "   - Click 'New repository'" -ForegroundColor White
Write-Host "   - Name: mcp-server (or your preferred name)" -ForegroundColor White
Write-Host "   - Description: 🔒 Production-ready MCP server with enterprise security features" -ForegroundColor White
Write-Host "   - Don't initialize with README, .gitignore, or license (we have them)" -ForegroundColor White
Write-Host ""
Write-Host "2. Connect this repository to GitHub:" -ForegroundColor Yellow
Write-Host "   Replace YOUR_USERNAME and REPO_NAME with your actual values:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "3. Optional - Install GitHub CLI for easier management:" -ForegroundColor Yellow
Write-Host "   winget install GitHub.cli" -ForegroundColor Cyan
Write-Host ""
Write-Host "4. Alternative - Use GitHub CLI to create repo directly:" -ForegroundColor Yellow
Write-Host "   gh repo create mcp-server --public --description '🔒 Production-ready MCP server'" -ForegroundColor Cyan
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/mcp-server.git" -ForegroundColor Cyan
Write-Host "   git branch -M main" -ForegroundColor Cyan
Write-Host "   git push -u origin main" -ForegroundColor Cyan
Write-Host ""
Write-Host "✨ Your MCP server is ready for GitHub!" -ForegroundColor Green
Write-Host ""

# Check if GitHub CLI is available
try {
    $ghVersion = gh --version 2>$null
    Write-Host "ℹ️  GitHub CLI detected: $($ghVersion[0])" -ForegroundColor Blue
    Write-Host "   You can use 'gh repo create' for easier repository setup" -ForegroundColor Blue
} catch {
    Write-Host "💡 Tip: Install GitHub CLI with 'winget install GitHub.cli' for easier GitHub management" -ForegroundColor Blue
}

Write-Host ""
Read-Host "Press Enter to exit"

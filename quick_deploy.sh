#!/bin/bash

echo "=========================================="
echo "🚀 Quick Deploy - Batch Query Tool"
echo "=========================================="
echo ""
echo "This script will deploy your app using Railway CLI"
echo ""

# Check if we're in the right directory
if [ ! -f "streamlit_app.py" ]; then
    echo "❌ Error: streamlit_app.py not found!"
    exit 1
fi

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Railway CLI not found. Installing..."
    echo ""

    # Try different installation methods
    if command -v brew &> /dev/null; then
        echo "Using Homebrew..."
        brew install railway
    elif command -v npm &> /dev/null; then
        echo "Using npm..."
        npm i -g @railway/cli
    else
        echo "Using curl..."
        curl -fsSL https://railway.app/install.sh | sh
    fi

    if ! command -v railway &> /dev/null; then
        echo "❌ Failed to install Railway CLI"
        echo "Please install manually: https://docs.railway.app/develop/cli"
        exit 1
    fi

    echo "✅ Railway CLI installed"
fi

# Login to Railway
echo ""
echo "🔐 Logging in to Railway..."
echo "This will open your browser for authentication"
echo ""
railway login

if [ $? -ne 0 ]; then
    echo "❌ Login failed"
    exit 1
fi

echo "✅ Logged in successfully"

# Initialize project if needed
if [ ! -f "railway.json" ]; then
    echo ""
    echo "📝 Creating railway.json..."
    cat > railway.json << 'RAILWAYJSON'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
RAILWAYJSON
    echo "✅ railway.json created"
fi

# Initialize Railway project
echo ""
echo "🎯 Initializing Railway project..."
railway init

# Deploy
echo ""
echo "🚀 Deploying to Railway..."
echo "This may take a few minutes..."
echo ""
railway up

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo "=========================================="
    echo ""
    echo "Your app is now live!"
    echo ""
    echo "Commands:"
    echo "  railway open    - Open app in browser"
    echo "  railway logs    - View logs"
    echo "  railway status  - Check status"
    echo ""
    echo "Opening app in browser..."
    sleep 2
    railway open
else
    echo ""
    echo "❌ Deployment failed"
    echo "Check logs with: railway logs"
    exit 1
fi

#!/bin/bash

echo "=========================================="
echo "Railway CLI Deployment"
echo "=========================================="

# Install Railway CLI
echo "Installing Railway CLI..."
npm i -g @railway/cli 2>/dev/null || brew install railway 2>/dev/null || curl -fsSL https://railway.app/install.sh | sh

# Login
echo ""
echo "Logging in to Railway..."
railway login

# Initialize project
echo ""
echo "Initializing Railway project..."
railway init

# Link or create project
echo ""
railway link || railway init

# Add environment variables (optional)
echo ""
echo "Setting environment variables..."
# railway variables set KEY=VALUE

# Deploy
echo ""
echo "Deploying to Railway..."
railway up

echo ""
echo "=========================================="
echo "✓ Deployment Complete!"
echo "=========================================="
echo ""
echo "Your app is now live!"
echo "Run 'railway open' to view it in browser"
echo ""

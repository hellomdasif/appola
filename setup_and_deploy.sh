#!/bin/bash

echo "=========================================="
echo "🚀 Setup and Deploy Batch Query Tool"
echo "=========================================="
echo ""

cd /Users/asif/Documents/latest/decoder/room_encoder

# Check Railway login
echo "Checking Railway login status..."
if railway whoami &>/dev/null; then
    echo "✅ Already logged in to Railway"
    railway whoami
else
    echo "❌ Not logged in to Railway"
    echo ""
    echo "Please run: railway login"
    echo "Then run this script again"
    exit 1
fi

echo ""
echo "=========================================="
echo "Setting up Git Repository"
echo "=========================================="
echo ""

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Add only necessary files
echo ""
echo "Adding deployment files..."
git add -f streamlit_app.py
git add -f requirements_streamlit.txt
git add -f .streamlit/config.toml
git add -f railway.json
git add -f README.md
git add -f .gitignore

echo "✅ Files staged"

# Show what will be committed
echo ""
echo "Files to be committed:"
git status --short

# Commit
echo ""
if git diff --cached --quiet; then
    echo "⚠️  No changes to commit"
else
    git commit -m "Deploy Batch Query Tool to Railway"
    echo "✅ Changes committed"
fi

echo ""
echo "=========================================="
echo "GitHub Repository Setup"
echo "=========================================="
echo ""

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "✅ GitHub remote already configured"
    git remote -v
    echo ""
    read -p "Do you want to update the remote URL? (y/n): " update_remote
    if [ "$update_remote" = "y" ]; then
        read -p "Enter new GitHub repository URL: " repo_url
        git remote set-url origin "$repo_url"
        echo "✅ Remote updated"
    fi
else
    echo "No GitHub remote found."
    echo ""
    echo "Options:"
    echo "1. Create new repo on GitHub: https://github.com/new"
    echo "2. Enter the repository URL here"
    echo ""
    read -p "Enter your GitHub repository URL (or press Enter to skip): " repo_url

    if [ ! -z "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote added: $repo_url"
    else
        echo "⚠️  Skipping GitHub setup (you can add it later)"
    fi
fi

# Push to GitHub if remote exists
if git remote | grep -q "origin"; then
    echo ""
    read -p "Push to GitHub now? (y/n): " push_now
    if [ "$push_now" = "y" ]; then
        echo "Pushing to GitHub..."
        git branch -M main
        git push -u origin main
        echo "✅ Pushed to GitHub"
    fi
fi

echo ""
echo "=========================================="
echo "Deploying to Railway"
echo "=========================================="
echo ""

read -p "Deploy to Railway now? (y/n): " deploy_now
if [ "$deploy_now" = "y" ]; then
    # Check if project is linked
    if railway status &>/dev/null; then
        echo "✅ Railway project already linked"
    else
        echo "Initializing Railway project..."
        railway init
    fi

    echo ""
    echo "🚀 Deploying to Railway..."
    railway up

    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "✅ DEPLOYMENT SUCCESSFUL!"
        echo "=========================================="
        echo ""
        railway status
        echo ""
        echo "Commands:"
        echo "  railway open    - Open app in browser"
        echo "  railway logs    - View deployment logs"
        echo "  railway status  - Check deployment status"
        echo ""
        read -p "Open app in browser now? (y/n): " open_now
        if [ "$open_now" = "y" ]; then
            railway open
        fi
    else
        echo ""
        echo "❌ Deployment failed"
        echo "Check logs with: railway logs"
    fi
else
    echo ""
    echo "Skipping deployment."
    echo "Run 'railway up' when ready to deploy"
fi

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "What's next:"
echo "  - railway open   : View your app"
echo "  - railway logs   : Check logs"
echo "  - git push       : Update GitHub"
echo "  - railway up     : Redeploy"
echo ""

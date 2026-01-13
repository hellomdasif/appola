#!/bin/bash

echo "=========================================="
echo "🚀 Complete Deployment Script"
echo "=========================================="
echo ""
echo "This will:"
echo "  1. Login to Railway"
echo "  2. Setup Git with only necessary files"
echo "  3. Help create GitHub repo"
echo "  4. Deploy to Railway"
echo ""
read -p "Continue? (y/n): " continue_deploy
if [ "$continue_deploy" != "y" ]; then
    exit 0
fi

cd /Users/asif/Documents/latest/decoder/room_encoder

# Step 1: Railway Login
echo ""
echo "=========================================="
echo "Step 1: Railway Login"
echo "=========================================="
echo ""

if railway whoami &>/dev/null; then
    echo "✅ Already logged in to Railway as:"
    railway whoami
else
    echo "Opening browser for Railway login..."
    echo ""
    railway login

    if [ $? -ne 0 ]; then
        echo "❌ Login failed. Please try again."
        exit 1
    fi

    echo "✅ Logged in successfully"
fi

# Step 2: Setup Git
echo ""
echo "=========================================="
echo "Step 2: Setup Git Repository"
echo "=========================================="
echo ""

# Initialize git
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Create .gitignore to exclude everything first
cat > .gitignore << 'GITIGNORE'
# Exclude everything by default
*

# Include only deployment files
!streamlit_app.py
!requirements_streamlit.txt
!railway.json
!README.md
!.gitignore
!.streamlit/
!.streamlit/config.toml
GITIGNORE

echo "✅ Created .gitignore"

# Add only necessary files
echo ""
echo "Adding deployment files..."
git add -f .gitignore
git add -f streamlit_app.py
git add -f requirements_streamlit.txt
git add -f railway.json
git add -f README.md
git add -f .streamlit/config.toml

echo ""
echo "📁 Files staged for deployment:"
git status --short

# Commit
echo ""
if git diff --cached --quiet; then
    echo "⚠️  No new changes to commit"
    if ! git log -1 &>/dev/null; then
        echo "Creating initial commit..."
        git commit --allow-empty -m "Initial commit: Batch Query Tool"
    fi
else
    git commit -m "Deploy Batch Query Tool"
    echo "✅ Changes committed"
fi

# Step 3: GitHub Setup
echo ""
echo "=========================================="
echo "Step 3: GitHub Repository"
echo "=========================================="
echo ""

if git remote | grep -q "origin"; then
    echo "✅ GitHub remote already exists:"
    git remote get-url origin
    echo ""
    read -p "Keep this remote? (y/n): " keep_remote
    if [ "$keep_remote" != "y" ]; then
        read -p "Enter new GitHub repository URL: " new_url
        git remote set-url origin "$new_url"
    fi
else
    echo "📝 Create a new repository on GitHub:"
    echo "   https://github.com/new"
    echo ""
    echo "Repository name: batch-query-tool"
    echo "Description: Batch Query Tool for API endpoints"
    echo "Public/Private: Your choice"
    echo "Do NOT initialize with README"
    echo ""
    read -p "Enter your GitHub repository URL: " repo_url

    if [ ! -z "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote added"
    else
        echo "❌ No URL provided. Skipping GitHub."
    fi
fi

# Push to GitHub
if git remote | grep -q "origin"; then
    echo ""
    echo "Pushing to GitHub..."
    git branch -M main

    if git push -u origin main; then
        echo "✅ Successfully pushed to GitHub"
    else
        echo "⚠️  Push failed. You may need to:"
        echo "   git push -u origin main --force"
    fi
fi

# Step 4: Deploy to Railway
echo ""
echo "=========================================="
echo "Step 4: Deploy to Railway"
echo "=========================================="
echo ""

# Initialize Railway project
if railway status &>/dev/null; then
    echo "✅ Railway project already linked"
    railway status
else
    echo "Creating new Railway project..."
    railway init

    if [ $? -ne 0 ]; then
        echo "❌ Failed to initialize Railway project"
        exit 1
    fi
fi

# Deploy
echo ""
echo "🚀 Deploying to Railway..."
echo "This will take a few minutes..."
echo ""

railway up

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ DEPLOYMENT SUCCESSFUL!"
    echo "=========================================="
    echo ""

    # Get deployment info
    railway status

    echo ""
    echo "🎉 Your app is now live!"
    echo ""
    echo "Useful commands:"
    echo "  railway open      - Open app in browser"
    echo "  railway logs      - View logs"
    echo "  railway status    - Check status"
    echo "  railway domain    - Manage custom domain"
    echo ""

    read -p "Open app in browser? (y/n): " open_browser
    if [ "$open_browser" = "y" ]; then
        railway open
    fi
else
    echo ""
    echo "❌ Deployment failed"
    echo ""
    echo "Troubleshooting:"
    echo "  railway logs      - Check error logs"
    echo "  railway status    - Check project status"
    echo "  railway up        - Try deploying again"
fi

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="

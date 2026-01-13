#!/bin/bash

echo "=========================================="
echo "Batch Query Tool - Streamlit Deployment"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "streamlit_app.py" ]; then
    echo "❌ Error: streamlit_app.py not found!"
    echo "Please run this script from the room_encoder directory"
    exit 1
fi

echo "✓ Found streamlit_app.py"

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo ""
    echo "Initializing git repository..."
    git init
    echo "✓ Git initialized"
fi

# Add files
echo ""
echo "Adding files to git..."
git add streamlit_app.py
git add requirements_streamlit.txt
git add .streamlit/config.toml
git add README.md
git add .gitignore

echo "✓ Files staged"

# Show status
echo ""
echo "Git status:"
git status --short

# Commit
echo ""
read -p "Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Deploy Batch Query Tool"
fi

git commit -m "$commit_msg"
echo "✓ Changes committed"

# Ask for GitHub repository
echo ""
echo "=========================================="
echo "GitHub Repository Setup"
echo "=========================================="
echo ""
echo "Please create a repository on GitHub:"
echo "  https://github.com/new"
echo ""
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git): " repo_url

if [ -z "$repo_url" ]; then
    echo "❌ No repository URL provided"
    exit 1
fi

# Check if remote exists
if git remote | grep -q "origin"; then
    echo "Updating existing remote..."
    git remote set-url origin "$repo_url"
else
    echo "Adding remote..."
    git remote add origin "$repo_url"
fi

echo "✓ Remote configured"

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "=========================================="
echo "✓ SUCCESS!"
echo "=========================================="
echo ""
echo "Your code is now on GitHub!"
echo ""
echo "Next steps:"
echo "1. Go to https://share.streamlit.io/"
echo "2. Click 'New app'"
echo "3. Select your repository"
echo "4. Set main file: streamlit_app.py"
echo "5. Click 'Deploy!'"
echo ""
echo "Your app will be live at: https://your-app-name.streamlit.app"
echo ""

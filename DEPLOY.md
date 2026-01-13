# Deploy Batch Query Tool to Streamlit Cloud

## Quick Deploy Guide

### 1. Test Locally (Optional)
```bash
pip install streamlit requests
streamlit run streamlit_app.py
```

### 2. Initialize Git Repository
```bash
cd /Users/asif/Documents/latest/decoder/room_encoder

# Initialize git
git init

# Add only the necessary files
git add streamlit_app.py
git add requirements_streamlit.txt
git add .streamlit/
git add README.md
git add .gitignore

# Commit
git commit -m "Initial commit: Batch Query Tool"
```

### 3. Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository (e.g., "batch-query-tool")
3. **Don't** initialize with README (we already have files)

### 4. Push to GitHub
```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/batch-query-tool.git

# Push to main branch
git branch -M main
git push -u origin main
```

### 5. Deploy on Streamlit Cloud

1. Visit: https://share.streamlit.io/
2. Click **"New app"**
3. Sign in with GitHub
4. Select your repository: `YOUR_USERNAME/batch-query-tool`
5. Set:
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
   - **Python version**: `3.9` or higher
6. Click **"Deploy!"**

### 6. Your App is Live! 🎉

Your app will be available at:
```
https://YOUR_APP_NAME.streamlit.app
```

## Files Included

- `streamlit_app.py` - Main application
- `requirements_streamlit.txt` - Dependencies (streamlit, requests)
- `.streamlit/config.toml` - App configuration
- `README.md` - Documentation

## Troubleshooting

If deployment fails:
1. Check requirements_streamlit.txt exists
2. Ensure streamlit_app.py is in the root directory
3. Check Streamlit Cloud logs for errors

## Update Deployed App

After making changes:
```bash
git add .
git commit -m "Update app"
git push
```

Streamlit will automatically redeploy!

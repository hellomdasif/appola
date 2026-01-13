# Deploy via CLI Only - Complete Guide

## 🚀 Option 1: Railway (Easiest, Recommended)

### Install Railway CLI
```bash
# Mac
brew install railway

# Or using npm
npm i -g @railway/cli

# Or using curl
curl -fsSL https://railway.app/install.sh | sh
```

### Deploy
```bash
cd /Users/asif/Documents/latest/decoder/room_encoder

# Login to Railway
railway login

# Initialize and deploy (one command)
railway init
railway up

# Open in browser
railway open
```

**Done! Your app is live at: `https://your-app.up.railway.app`**

---

## 🔧 Option 2: Render

### Install Render CLI
```bash
# Install
curl -fsSL https://render.com/install.sh | sh

# Or download from https://render.com/docs/cli
```

### Deploy
```bash
cd /Users/asif/Documents/latest/decoder/room_encoder

# Login
render login

# Create service
render services create web \
  --name batch-query-tool \
  --env python \
  --build-command "pip install -r requirements_streamlit.txt" \
  --start-command "streamlit run streamlit_app.py --server.port=\$PORT --server.address=0.0.0.0"

# Deploy
render services deploy
```

---

## 🐳 Option 3: Docker + Any Platform

### Create Dockerfile
Already created! Use the automated script:

```bash
cd /Users/asif/Documents/latest/decoder/room_encoder
./deploy_docker.sh
```

Then deploy to any platform that supports Docker.

---

## ⚡ Quick Deploy (One Command)

### Railway (Fastest)
```bash
cd /Users/asif/Documents/latest/decoder/room_encoder
./deploy_railway.sh
```

### All-in-One Script
```bash
# This script will try Railway first, then Render
cd /Users/asif/Documents/latest/decoder/room_encoder
./quick_deploy.sh
```

---

## 🌐 Deployment URLs

After deployment, your app will be available at:
- **Railway**: `https://your-app.up.railway.app`
- **Render**: `https://batch-query-tool.onrender.com`

---

## 📋 Comparison

| Platform | CLI? | Free Tier | Speed | Setup |
|----------|------|-----------|-------|-------|
| Railway  | ✅ Yes | 500hrs/mo | Fast | Easy |
| Render   | ✅ Yes | 750hrs/mo | Medium | Easy |
| Streamlit| ❌ No  | Unlimited | Fast | Web UI |

**Recommendation**: Use Railway for full CLI deployment!

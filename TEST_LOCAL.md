# 🧪 Test Your App Locally

## Quick Test (One Command)

```bash
./test_local.sh
```

Or manually:

```bash
cd /Users/asif/Documents/latest/decoder/room_encoder
streamlit run streamlit_app.py
```

---

## What Happens:

1. ✅ Streamlit starts a local server
2. 🌐 Opens your browser at **http://localhost:8501**
3. 🎨 You'll see your Batch Query Tool interface

---

## First Time Setup:

If you don't have Streamlit installed:

```bash
pip install streamlit requests
```

Then run:

```bash
streamlit run streamlit_app.py
```

---

## Testing the App:

1. **Open in browser**: http://localhost:8501

2. **Enter API details**:
   - Endpoint: `https://uaas.kaixindou.net/service/batchQuery`
   - User ID: `177307453`
   - App ID: `ikxd`
   - Type: `3`
   - With OA: `1`

3. **Click Query** and see the results!

---

## Stop the Server:

Press **Ctrl + C** in your terminal

---

## Common Issues:

### Port Already in Use
If you see "Port 8501 is already in use":

```bash
# Kill the process
lsof -ti:8501 | xargs kill -9

# Or use a different port
streamlit run streamlit_app.py --server.port=8502
```

### Module Not Found
```bash
pip install streamlit requests
```

---

## 🎯 Compare Both Versions:

### Test Flask Version:
```bash
python web_ui.py
```
Opens at: http://localhost:8081

### Test Streamlit Version:
```bash
streamlit run streamlit_app.py
```
Opens at: http://localhost:8501

---

## ✅ When Testing is Done:

Once you're happy with the app, deploy it:

```bash
./deploy_complete.sh
```

Your app will be live on the internet! 🚀

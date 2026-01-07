# Batch Query Tool

A web-based tool for querying user information from API endpoints.

## Features

- 🎯 Custom API endpoints
- 📊 Beautiful data visualization
- 📋 Easy data copying
- 🔐 Display device IDs and login information
- 🔗 Show linked third-party accounts

## Local Development

### Flask Version

```bash
pip install flask requests
python web_ui.py
```

Open http://localhost:8081

### Streamlit Version

```bash
pip install streamlit requests
streamlit run streamlit_app.py
```

Open http://localhost:8501

## Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to https://streamlit.io/cloud
3. Click "New app"
4. Select your repository
5. Set main file: `streamlit_app.py`
6. Click "Deploy"

## CLI Version

```bash
python batch_query.py --vals "177307453"
```

## Files

- `streamlit_app.py` - Streamlit web UI (for cloud deployment)
- `web_ui.py` - Flask web UI (for local use)
- `batch_query.py` - Command-line tool
- `requirements_streamlit.txt` - Python dependencies for Streamlit
- `requirements.txt` - Python dependencies for Flask

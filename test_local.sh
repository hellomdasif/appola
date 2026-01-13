#!/bin/bash

echo "=========================================="
echo "🧪 Test Streamlit App Locally"
echo "=========================================="
echo ""

cd /Users/asif/Documents/latest/decoder/room_encoder

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "Streamlit is not installed. Installing..."
    pip install streamlit requests
    echo ""
fi

echo "Starting Streamlit app on localhost..."
echo ""
echo "📍 Your app will open at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

# Run streamlit
streamlit run streamlit_app.py

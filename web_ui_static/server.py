#!/usr/bin/env python3
"""Serve static batch query UI and proxy requests without exposing upstream endpoint."""

import os
from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_from_directory

APP_ROOT = Path(__file__).parent.resolve()
app = Flask(__name__, static_folder=str(APP_ROOT), static_url_path="")

# Endpoint hardcoded here and never exposed to the client.
ENDPOINT_URL = "https://uaas.kaixindou.net/service/batchQuery"

HEADERS = {
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Ch-Ua": '"Chromium";v="143", "Not A(Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://uaas-test.kaixindou.net",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://uaas.kaixindou.net/html/tool.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i"
}


@app.route("/")
def index():
    """Serve the static UI."""
    return send_from_directory(APP_ROOT, "index.html")


@app.route("/api/query", methods=["POST"])
def api_query():
    """Proxy batch query requests to upstream without exposing the endpoint to the browser."""
    data = request.get_json(force=True, silent=True) or {}

    # Always use server-configured endpoint; client cannot override.
    endpoint_url = ENDPOINT_URL

    params = {
        "appId": data.get("appId", "ikxd"),
        "with_oa": data.get("with_oa", "1"),
        "type": data.get("type", "3"),
        "vals": data.get("vals", "")
    }

    try:
        print(f"\n[API Request] Endpoint: {endpoint_url}")
        print(f"[API Request] Params: {params}")

        response = requests.post(
            endpoint_url,
            data=params,
            headers=HEADERS,
            timeout=10
        )

        print(f"[API Response] Status: {response.status_code}")

        return jsonify({
            "success": True,
            "status_code": response.status_code,
            "response": response.json(),
            "endpoint_label": None
        })
    except requests.exceptions.RequestException as e:
        print(f"[API Error] {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
    except Exception as e:
        print(f"[API Error] {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8081))
    print("\n" + "=" * 60)
    print("🚀 Batch Query Web UI (static + proxy)")
    print("=" * 60)
    print(f"\n📍 Server running at: http://localhost:{port}")
    print(f"📍 Network access: http://0.0.0.0:{port}")
    print("\n💡 Press Ctrl+C to stop the server\n")
    print("=" * 60 + "\n")

    app.run(host="0.0.0.0", port=port, debug=True)

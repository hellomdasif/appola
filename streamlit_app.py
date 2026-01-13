#!/usr/bin/env python3
"""Streamlit UI for Batch Query with left panel form and styled results."""

import json
from datetime import datetime, timedelta, timezone

import requests
import streamlit as st
from streamlit.components.v1 import html as st_html

# Hardcoded upstream endpoint (kept server-side)
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
    "Priority": "u=1, i",
}


def translate(text):
    translations = {
        "普通账号": "Regular Account",
        "不存在": "Does Not Exist",
        "印度": "India",
        "男": "Male",
        "女": "Female",
    }
    if text is None:
        return None
    return translations.get(text, text)


def format_ist(value):
    if value is None or value == "":
        return "N/A"
    try:
        if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace(".", "", 1).isdigit()):
            value_num = float(value)
            timestamp = value_num if value_num > 1e12 else value_num * 1000
            dt = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
        else:
            dt = datetime.fromisoformat(str(value))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
        ist = timezone(timedelta(hours=5, minutes=30))
        dt_ist = dt.astimezone(ist)
        return dt_ist.strftime("%d %b %Y, %I:%M:%S %p")
    except Exception:
        return str(value)


def run_query(vals, app_id, type_choice, with_oa):
    params = {
        "appId": app_id,
        "with_oa": with_oa,
        "type": type_choice,
        "vals": vals.strip(),
    }
    resp = requests.post(
        ENDPOINT_URL,
        data=params,
        headers=HEADERS,
        timeout=15,
    )
    return resp


def render_result(info, full_response):
    login = info.get("loginInfo") or {}
    third = info.get("thirdpartyList") or []
    html = f"""
    <style>
    body {{ margin:0; padding:0; font-family:'Manrope','Inter',system-ui,sans-serif; }}
    .wrap {{
        background: linear-gradient(135deg, #0e1a2b 0%, #182f55 35%, #1f3c6d 100%);
        padding: 16px;
        color: #0d1a2b;
    }}
    .card {{
        background:#fff;
        border-radius:16px;
        padding:18px;
        box-shadow:0 14px 45px rgba(9,16,40,0.35);
        border:1px solid rgba(255,255,255,0.06);
        margin-bottom:12px;
    }}
    .header {{
        display:flex;
        align-items:center;
        gap:14px;
        background: linear-gradient(135deg, #0d1a2b 0%, #1c3053 100%);
        color:#f4f7ff;
        border-radius:14px;
        padding:14px;
    }}
    .avatar {{
        width:86px; height:86px; border-radius:14px; object-fit:cover;
        border:3px solid rgba(255,255,255,0.75);
    }}
    .pill {{
        display:inline-block;
        padding:8px 10px;
        background: rgba(255,255,255,0.12);
        border-radius:10px;
        color:#d9e5ff;
        margin-right:6px;
        font-size:12px;
    }}
    .grid {{
        display:grid;
        grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        gap:12px;
        margin-top:10px;
    }}
    .info-item {{
        background:#f6f8fb;
        border-radius:12px;
        padding:12px;
        border:1px solid #e3e8f2;
    }}
    .info-label {{ font-size:12px; color:#6b768b; text-transform:uppercase; margin-bottom:4px; }}
    .info-value {{ font-size:16px; font-weight:700; color:#0f1d33; word-break:break-all; }}
    .section-title {{ font-size:18px; font-weight:800; color:#0f1d33; margin:12px 0 6px 0; }}
    .third-list {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:8px; }}
    .third-item {{ border:1px solid #e3e8f2; border-radius:12px; padding:10px; background:#fff; }}
    a.ip-link {{ color:#5b8def; text-decoration:none; font-weight:700; }}
    a.ip-link:hover {{ text-decoration:underline; }}
    pre {{ background:#0e1624; color:#e0ecff; padding:12px; border-radius:12px; overflow:auto; }}
    </style>
    <div class="wrap">
        <div class="card header">
            {'<img src="'+info.get('avatar','')+'" class="avatar" />' if info.get('avatar') else ''}
            <div>
                <div style="font-size:22px;font-weight:800;">{info.get('nick') or 'N/A'}</div>
                <div>
                    <span class="pill">VID: {info.get('vid') or 'N/A'}</span>
                    <span class="pill">User ID: {info.get('uuid') or 'N/A'}</span>
                </div>
            </div>
        </div>
        <div class="card">
            <div class="section-title">Basic Information</div>
            <div class="grid">
                <div class="info-item"><div class="info-label">UUID</div><div class="info-value">{info.get('uuid') or 'N/A'}</div></div>
                <div class="info-item"><div class="info-label">Country</div><div class="info-value">{translate(info.get('country')) or info.get('country') or 'N/A'} ({(info.get('realCountry') or 'N/A').upper()})</div></div>
                <div class="info-item"><div class="info-label">Mobile</div><div class="info-value">{info.get('mobile') or 'N/A'}</div></div>
                <div class="info-item"><div class="info-label">Account Type</div><div class="info-value">{translate(info.get('type')) or 'N/A'}</div></div>
                <div class="info-item"><div class="info-label">Gender</div><div class="info-value">{translate(info.get('sex')) or 'N/A'}</div></div>
                <div class="info-item"><div class="info-label">Registered Device</div><div class="info-value">{info.get('device') or 'N/A'}</div></div>
                <div class="info-item"><div class="info-label">Account Status</div><div class="info-value">{'Enabled' if info.get('enabled') else 'Disabled'}</div></div>
                <div class="info-item"><div class="info-label">Birthday</div><div class="info-value">{info.get('birthday') or 'N/A'}</div></div>
                <div class="info-item"><div class="info-label">Created (IST 12h)</div><div class="info-value">{format_ist(info.get('createDate'))}</div></div>
            </div>
        </div>
        <div class="card">
            <div class="section-title">Login Information (IST 12h)</div>
            <div class="grid">
                <div class="info-item">
                    <div class="info-label">Last App Login</div>
                    <div class="info-value">{format_ist(login.get('appDate'))}</div>
                    {f'<div><a class="ip-link" href="https://whatismyipaddress.com/ip/{login.get("appIP")}" target="_blank" rel="noreferrer noopener">App Login IP</a></div>' if login.get('appIP') else ''}
                    <div class="info-label" style="margin-top:6px;">Device Type</div>
                    <div class="info-value">{login.get('appDevType') or 'N/A'}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Last Web Login</div>
                    <div class="info-value">{format_ist(login.get('webDate'))}</div>
                    {f'<div><a class="ip-link" href="https://whatismyipaddress.com/ip/{login.get("webIP")}" target="_blank" rel="noreferrer noopener">Web Login IP</a></div>' if login.get('webIP') else ''}
                    <div class="info-label" style="margin-top:6px;">App Type</div>
                    <div class="info-value">{login.get('appType') or 'N/A'}</div>
                </div>
            </div>
        </div>
        {'<div class="card"><div class="section-title">Linked Third-Party Accounts ('+str(len(third))+')</div><div class="third-list">' + ''.join([f'<div class=\"third-item\"><div class=\"info-label\">{(acc.get(\"thirdpartyType\") or \"Unknown\").title()}</div><div class=\"info-value\" style=\"font-size:14px;\">{acc.get(\"openId\") or \"N/A\"}</div></div>' for acc in third]) + '</div></div>' if third else ''}
        <div class="card">
            <div class="section-title">Full Response</div>
            <pre>{json.dumps(full_response, ensure_ascii=False, indent=2)}</pre>
        </div>
    </div>
    """
    return html


def main():
    st.set_page_config(page_title="Batch Query Tool", layout="wide", page_icon="🔍")

    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] { background: linear-gradient(135deg, #0e1a2b 0%, #182f55 35%, #1f3c6d 100%); }
        [data-testid="stSidebar"] { display: none; }
        .form-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 12px 40px rgba(9,16,40,0.35);
            border: 1px solid rgba(255,255,255,0.08);
            position: sticky;
            top: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col_form, col_result = st.columns([1, 2], gap="large")

    with col_form:
        st.markdown("### 🔍 Batch Query Tool  \nIST · 12h")
        with st.form("query-form", clear_on_submit=False):
            vals = st.text_input("User ID (vals)", value="177307453")
            app_id = st.text_input("App ID", value="ikxd")
            type_choice = st.selectbox(
                "Type",
                options=[
                    ("1", "Type 1"),
                    ("2", "Type 2"),
                    ("3", "Type 3 (User)"),
                    ("4", "Type 4"),
                ],
                index=2,
                format_func=lambda opt: opt[1],
            )[0]
            with_oa = st.selectbox(
                "With OA",
                options=[("0", "No"), ("1", "Yes")],
                index=1,
                format_func=lambda opt: opt[1],
            )[0]
            submitted = st.form_submit_button("Query")

    with col_result:
        if submitted and vals.strip():
            with st.spinner("Querying..."):
                try:
                    resp = run_query(vals, app_id, type_choice, with_oa)
                    st.session_state.status_code = resp.status_code
                    st.session_state.last_result = resp.json()
                    st.session_state.error = None
                except Exception as exc:
                    st.session_state.error = str(exc)
                    st.session_state.last_result = None
                    st.session_state.status_code = None

        if "last_result" not in st.session_state:
            st.session_state.last_result = None
            st.session_state.status_code = None
            st.session_state.error = None

        if st.session_state.error:
            st.error(f"Request failed: {st.session_state.error}")

        if st.session_state.status_code is not None:
            st.markdown(f"**Status:** {st.session_state.status_code}")

        data = st.session_state.last_result
        if data:
            info_list = data.get("info") or []
            info = info_list[0] if info_list else None
            if not info or translate(info.get("type")) == "Does Not Exist":
                st.warning("User not found.")
            else:
                html_str = render_result(info, data)
                st_html(html_str, height=900, scrolling=True)


if __name__ == "__main__":
    main()

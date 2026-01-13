#!/usr/bin/env python3
"""Modern Streamlit UI for User Batch Query Tool - Web UI Style with Sidebar."""

from datetime import datetime

import requests
import streamlit as st

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

TYPE_OPTIONS = {
    "1": "Type 1",
    "2": "Type 2",
    "3": "Type 3 (User)",
    "4": "Type 4",
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


def format_timestamp(value):
    if value is None or value == "":
        return "N/A"
    try:
        if isinstance(value, (int, float)):
            dt = datetime.fromtimestamp(value)
        else:
            dt = datetime.fromisoformat(str(value))
        return dt.strftime("%Y-%m-%d %I:%M:%S %p")
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


def main():
    st.set_page_config(page_title="Batch Query Tool", layout="wide", page_icon="🔍")

    # CSS styling to match Flask UI with sidebar
    st.markdown(
        """
        <style>
        /* Main background */
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }

        /* Main content area - white card */
        .block-container {
            padding: 2rem !important;
            max-width: calc(100% - 3rem) !important;
            background: white !important;
            border-radius: 15px !important;
            margin: 1.5rem 1.5rem 1.5rem 0 !important;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2) !important;
        }

        /* Ensure content fills the space */
        section.main > div {
            max-width: 100% !important;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: white !important;
            padding: 1.5rem !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: white;
        }


        /* Form inputs */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
        }

        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #667eea;
            box-shadow: none;
        }

        /* Button styling */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            font-weight: 600;
            border: none;
            border-radius: 8px;
            padding: 14px 30px;
            font-size: 16px;
            transition: all 0.3s;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        /* Secondary button */
        .stButton > button[kind="secondary"] {
            background: #6c757d;
        }

        .stButton > button[kind="secondary"]:hover {
            background: #5a6268;
        }

        /* Headers */
        h1, h2, h3, h4 {
            color: #333 !important;
        }

        .main h1 {
            text-align: center !important;
            font-size: 2em !important;
            margin-bottom: 20px !important;
        }

        /* Sidebar title */
        [data-testid="stSidebar"] h1 {
            font-size: 1.5em !important;
            text-align: left !important;
        }

        /* Metrics */
        [data-testid="stMetricValue"] {
            font-size: 15px;
            font-weight: 600;
            color: #333;
        }

        [data-testid="stMetricLabel"] {
            font-size: 11px;
            color: #6c757d;
            text-transform: uppercase;
        }

        div[data-testid="metric-container"] {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin-bottom: 10px;
        }

        /* Compact spacing */
        .stMarkdown {
            margin-bottom: 0.5rem;
        }

        /* Status messages */
        .stSuccess {
            background: #d1fae5;
            color: #065f46;
            padding: 12px;
            border-radius: 8px;
        }

        .stError {
            background: #fee2e2;
            color: #991b1b;
            padding: 12px;
            border-radius: 8px;
        }

        /* Avatar */
        img {
            border-radius: 50%;
            border: 4px solid #667eea;
        }

        /* Code blocks */
        code {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 12px;
        }

        pre {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 13px;
        }

        /* Labels */
        label {
            font-weight: 600 !important;
            color: #333 !important;
            font-size: 14px !important;
        }

        /* IP Link styling */
        a {
            color: #667eea !important;
            text-decoration: none !important;
            font-weight: 600 !important;
            font-size: 16px !important;
        }

        a:hover {
            text-decoration: underline !important;
            color: #764ba2 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar for query form
    with st.sidebar:
        st.markdown("# 🔍 Query Tool")
        st.markdown("---")

        vals = st.text_input("User ID (vals)", value="177307453")
        app_id = st.text_input("App ID", value="ikxd")
        type_choice = st.selectbox("Type", options=list(TYPE_OPTIONS.keys()),
                                  format_func=lambda x: TYPE_OPTIONS[x], index=2)
        with_oa = st.selectbox("With OA", options=["No", "Yes"], index=1)

        st.markdown("")
        submitted = st.button("🔍 Query", type="primary")

        if st.button("Clear", type="secondary"):
            st.session_state.clear()
            st.rerun()

    # Main content area
    st.markdown("# 🔍 Batch Query Tool")

    # Handle query
    if submitted and vals.strip():
        with st.spinner("Loading..."):
            try:
                resp = run_query(vals, app_id, type_choice, "1" if with_oa == "Yes" else "0")
                st.session_state.status_code = resp.status_code
                st.session_state.last_result = resp.json()
                st.session_state.error = None
            except Exception as exc:
                st.session_state.error = str(exc)
                st.session_state.last_result = None
                st.session_state.status_code = None

    # Display results
    if hasattr(st.session_state, 'status_code') and st.session_state.status_code:
        st.markdown(f"### Results")

        if st.session_state.status_code == 200:
            st.success(f"✅ Status: {st.session_state.status_code}")
        else:
            st.warning(f"⚠️ Status: {st.session_state.status_code}")

        if st.session_state.error:
            st.error(f"❌ Request failed: {st.session_state.error}")
        elif st.session_state.last_result:
            data = st.session_state.last_result
            info_list = data.get("info") or []
            info = info_list[0] if info_list else None

            if not info or translate(info.get("type")) == "Does Not Exist":
                st.error("**User Not Found:** The requested user ID does not exist in the system.")
            else:
                # User Header
                col1, col2 = st.columns([1, 5])
                with col1:
                    if info.get('avatar'):
                        st.image(info['avatar'], width=100)
                with col2:
                    st.markdown(f"### {info.get('nick') or 'N/A'}")
                    st.caption(f"**VID:** `{info.get('vid') or 'N/A'}` | **UUID:** `{info.get('uuid') or 'N/A'}`")
                    status = "✓ Enabled" if info.get('enabled') else "✗ Disabled"
                    st.caption(f"**Status:** {status}")

                st.markdown("---")

                # Info Grid
                st.markdown("#### Basic Information")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("UUID", info.get('uuid') or 'N/A')
                    st.metric("Mobile", info.get('mobile') or 'N/A')

                with col2:
                    st.metric("Account Type", translate(info.get('type')) or 'N/A')
                    country = translate(info.get('country')) or info.get('country') or 'N/A'
                    real_country = (info.get('realCountry') or 'N/A').upper()
                    st.metric("Country", f"{country} ({real_country})")

                with col3:
                    st.metric("Gender", translate(info.get('sex')) or 'N/A')
                    st.metric("Device", info.get('device') or 'N/A')

                with col4:
                    st.metric("Birthday", info.get('birthday') or 'N/A')
                    st.metric("Created", format_timestamp(info.get('createDate')))

                # Login info
                login = info.get("loginInfo") or {}
                if login:
                    st.markdown("---")
                    st.markdown("#### Login Activity")

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric("Last App Login", format_timestamp(login.get('appDate')))

                    with col2:
                        app_ip = login.get('appIP')
                        if app_ip:
                            st.markdown('<div style="background: #f8f9fa; padding: 10px; border-radius: 8px; border-left: 4px solid #667eea; margin-bottom: 10px;">', unsafe_allow_html=True)
                            st.markdown('<div style="font-size: 11px; color: #6c757d; text-transform: uppercase; margin-bottom: 5px;">APP IP</div>', unsafe_allow_html=True)
                            st.markdown(f'<div><a href="https://whatismyipaddress.com/ip/{app_ip}" target="_blank">{app_ip}</a></div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.metric("App IP", "N/A")

                    with col3:
                        st.metric("Last Web Login", format_timestamp(login.get('webDate')))

                    with col4:
                        web_ip = login.get('webIP')
                        if web_ip:
                            st.markdown('<div style="background: #f8f9fa; padding: 10px; border-radius: 8px; border-left: 4px solid #667eea; margin-bottom: 10px;">', unsafe_allow_html=True)
                            st.markdown('<div style="font-size: 11px; color: #6c757d; text-transform: uppercase; margin-bottom: 5px;">WEB IP</div>', unsafe_allow_html=True)
                            st.markdown(f'<div><a href="https://whatismyipaddress.com/ip/{web_ip}" target="_blank">{web_ip}</a></div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.metric("Web IP", "N/A")

                    if login.get('appDevID'):
                        st.caption("**Device ID:**")
                        st.code(login.get('appDevID'), language=None)

                # Third-party accounts
                third = info.get("thirdpartyList") or []
                if third:
                    st.markdown("---")
                    st.markdown(f"#### 🔗 Linked Third-Party Accounts ({len(third)})")

                    cols = st.columns(min(4, len(third)))
                    for idx, acc in enumerate(third):
                        with cols[idx % len(cols)]:
                            account_type = (acc.get("thirdpartyType") or "Unknown").title()
                            st.caption(f"**{account_type}**")
                            st.code(acc.get("openId") or "N/A", language=None)

                # Full JSON Response
                st.markdown("---")
                with st.expander("📄 Full Response"):
                    st.json(data)
    else:
        # Welcome message
        st.markdown("### Welcome")
        st.info("👈 Enter a search value in the sidebar and click **Query** to view user information")


if __name__ == "__main__":
    main()

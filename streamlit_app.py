#!/usr/bin/env python3
"""Streamlit Web UI for batch query requests."""

import json
import requests
import streamlit as st

# Configuration
DEFAULT_URL = "https://uaas.kaixindou.net/service/batchQuery"

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

# Translation mapping
TRANSLATIONS = {
    '普通账号': 'Regular Account',
    '不存在': 'Does Not Exist',
    '印度': 'India',
    '男': 'Male',
    '女': 'Female'
}

def translate(text):
    """Translate Chinese text to English."""
    if not text:
        return text
    return TRANSLATIONS.get(text, text)

def make_query(endpoint_url, params):
    """Make the API request."""
    try:
        response = requests.post(
            endpoint_url,
            data=params,
            headers=HEADERS,
            timeout=10
        )
        return {
            'success': True,
            'status_code': response.status_code,
            'response': response.json()
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def display_user_info(info):
    """Display user information in a nice format."""
    if not info or translate(info.get('type', '')) == 'Does Not Exist':
        st.error("User Not Found: The requested user ID does not exist in the system.")
        return

    # User header with avatar
    col1, col2 = st.columns([1, 3])
    with col1:
        if info.get('avatar'):
            st.image(info['avatar'], width=100)
    with col2:
        st.subheader(info.get('nick', 'N/A'))
        st.text(f"VID: {info.get('vid', 'N/A')}")

    st.markdown("---")

    # Device ID (highlighted)
    if info.get('loginInfo', {}).get('appDevID'):
        st.success("🔑 Device ID")
        device_id = info['loginInfo']['appDevID']
        st.code(device_id, language=None)
        st.caption("Click the copy button on the right to copy →")

    # Basic Information
    st.subheader("📋 Basic Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("UUID", info.get('uuid', 'N/A'))
        st.metric("Account Type", translate(info.get('type', 'N/A')))
        st.metric("Gender", translate(info.get('sex', 'N/A')))

    with col2:
        country = translate(info.get('country', 'N/A'))
        country_code = info.get('realCountry', 'N/A').upper()
        st.metric("Country", f"{country} ({country_code})")
        st.metric("Registered Device", info.get('device', 'N/A'))
        st.metric("Account Status", "✓ Enabled" if info.get('enabled') else "✗ Disabled")

    with col3:
        mobile = info.get('mobile', 'N/A')
        if mobile and '*' in mobile:
            st.metric("Mobile Number (Masked)", mobile)
            if mobile.startswith('91'):
                st.caption("🇮🇳 Indian number")
        else:
            st.metric("Mobile Number", mobile)
        st.metric("Birthday", info.get('birthday', 'N/A'))
        if info.get('createDate'):
            st.metric("Account Created", info['createDate'][:10])

    # Login Information
    if info.get('loginInfo'):
        st.subheader("🔐 Login Information")
        login_info = info['loginInfo']

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**App Login**")
            if login_info.get('appDate'):
                import datetime
                app_login = datetime.datetime.fromtimestamp(login_info['appDate'])
                st.text(f"Last Login: {app_login.strftime('%Y-%m-%d %H:%M:%S')}")
            st.text(f"IP: {login_info.get('appIP', 'N/A')}")
            st.text(f"Device Type: {login_info.get('appDevType', 'N/A')}")
            st.text(f"App Type: {login_info.get('appType', 'N/A').capitalize()}")

        with col2:
            st.markdown("**Web Login**")
            if login_info.get('webDate'):
                import datetime
                web_login = datetime.datetime.fromtimestamp(login_info['webDate'])
                st.text(f"Last Login: {web_login.strftime('%Y-%m-%d %H:%M:%S')}")
            st.text(f"IP: {login_info.get('webIP', 'N/A')}")

    # Third-party accounts
    if info.get('thirdpartyList'):
        st.subheader(f"🔗 Linked Third-Party Accounts ({len(info['thirdpartyList'])})")

        for account in info['thirdpartyList']:
            account_type = account.get('thirdpartyType', 'Unknown').capitalize()
            open_id = account.get('openId', 'N/A')

            with st.expander(f"{account_type}: {open_id}"):
                st.code(open_id, language=None)

    # Full JSON response
    st.subheader("📄 Full Response")
    st.json(info)

def main():
    """Main Streamlit app."""
    st.set_page_config(
        page_title="Batch Query Tool",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 Batch Query Tool")
    st.markdown("Query user information from the API endpoint")

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")

        endpoint = st.text_input(
            "API Endpoint URL",
            value=DEFAULT_URL,
            help="Enter the API endpoint URL"
        )

        if st.button("Reset to Default"):
            endpoint = DEFAULT_URL
            st.rerun()

        st.markdown("---")

        vals = st.text_input(
            "User ID (vals)",
            value="177307453",
            help="Enter the user ID to query"
        )

        app_id = st.text_input(
            "App ID",
            value="ikxd"
        )

        query_type = st.selectbox(
            "Type",
            options=[1, 2, 3, 4],
            index=2,
            help="Query type (3 = User)"
        )

        with_oa = st.selectbox(
            "With OA",
            options=[0, 1],
            index=1
        )

        st.markdown("---")

        query_button = st.button("🚀 Query", type="primary", use_container_width=True)

    # Main content area
    if query_button:
        if not vals:
            st.error("Please enter a User ID")
            return

        params = {
            'appId': app_id,
            'with_oa': str(with_oa),
            'type': str(query_type),
            'vals': vals
        }

        with st.spinner('Querying API...'):
            result = make_query(endpoint, params)

        if result['success']:
            st.success(f"✓ Status Code: {result['status_code']}")
            st.caption(f"Endpoint: {endpoint}")

            st.markdown("---")

            if result['response'].get('info'):
                info = result['response']['info'][0]
                display_user_info(info)
            else:
                st.warning("No user information found in response")
                st.json(result['response'])
        else:
            st.error(f"Request Failed: {result['error']}")
    else:
        # Welcome message
        st.info("👈 Configure the query parameters in the sidebar and click **Query** to start")

        st.markdown("### Features")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**🎯 Custom Endpoints**")
            st.markdown("Query any API endpoint")

        with col2:
            st.markdown("**📊 Rich Display**")
            st.markdown("Beautiful data visualization")

        with col3:
            st.markdown("**📋 Easy Copy**")
            st.markdown("Copy data with one click")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Streamlit UI for Batch Query with left-side control panel and IST 12h times."""

import json
from datetime import datetime, timezone, timedelta

import requests
import streamlit as st

# Hardcoded upstream endpoint (not exposed to end users).
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


def format_ist(value):
    """Format timestamps to IST 12-hour with seconds."""
    if value is None or value == "":
        return "N/A"
    try:
        # Accept seconds or ms.
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

    st.markdown(
        """
        <style>
        body {
            background: linear-gradient(135deg, #0e1a2b 0%, #182f55 35%, #1f3c6d 100%) !important;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
        }
        .card {
            background: #ffffff;
            border-radius: 14px;
            padding: 18px;
            box-shadow: 0 14px 45px rgba(9,16,40,0.35);
            border: 1px solid rgba(255,255,255,0.06);
        }
        .pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 12px;
            background: rgba(255,255,255,0.08);
            border-radius: 12px;
            color: #dce7ff;
            border: 1px solid rgba(255,255,255,0.12);
        }
        .header {
            background: linear-gradient(135deg, #0d1a2b 0%, #1c3053 100%);
            color: #f4f7ff;
            border-radius: 14px;
            padding: 14px;
        }
        a.ip-link {
            color: #5b8def !important;
            font-weight: 700;
            text-decoration: none;
        }
        a.ip-link:hover {
            text-decoration: underline;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    left_col, right_col = st.columns([1, 2])

    with left_col:
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
            clear = st.form_submit_button("Clear")

        if clear:
            st.experimental_rerun()

    with right_col:
        if "last_result" not in st.session_state:
            st.session_state.last_result = None
            st.session_state.status_code = None
            st.session_state.error = None

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
                with st.container():
                    st.markdown('<div class="card header">', unsafe_allow_html=True)
                    avatar = info.get("avatar")
                    cols = st.columns([1, 4])
                    if avatar:
                        cols[0].image(avatar, width=90)
                    with cols[1]:
                        st.markdown(f"#### {info.get('nick') or 'N/A'}")
                        st.markdown(
                            f"""<div class="pill">VID: {info.get('vid') or 'N/A'}</div>
                            <div class="pill" style="margin-left:8px;">User ID: {info.get('uuid') or 'N/A'}</div>""",
                            unsafe_allow_html=True,
                        )
                    st.markdown('</div>', unsafe_allow_html=True)

                st.markdown("#### Basic Information")
                basic_cols = st.columns(3)
                basic_cols[0].metric("UUID", info.get("uuid") or "N/A")
                basic_cols[1].metric("Country", f"{translate(info.get('country')) or info.get('country') or 'N/A'} ({(info.get('realCountry') or 'N/A').upper()})")
                basic_cols[2].metric("Mobile", info.get("mobile") or "N/A")

                basic_cols2 = st.columns(3)
                basic_cols2[0].metric("Account Type", translate(info.get("type")) or "N/A")
                basic_cols2[1].metric("Gender", translate(info.get("sex")) or "N/A")
                basic_cols2[2].metric("Registered Device", info.get("device") or "N/A")

                basic_cols3 = st.columns(3)
                basic_cols3[0].metric("Account Status", "Enabled" if info.get("enabled") else "Disabled")
                basic_cols3[1].metric("Birthday", info.get("birthday") or "N/A")
                basic_cols3[2].metric("Created (IST 12h)", format_ist(info.get("createDate")))

                login_info = info.get("loginInfo") or {}
                st.markdown("#### Login Information (IST 12h)")
                login_cols = st.columns(2)
                login_cols[0].markdown(f"**Last App Login:** {format_ist(login_info.get('appDate'))}")
                app_ip = login_info.get("appIP")
                if app_ip:
                    login_cols[0].markdown(f"[App Login IP]({f'https://whatismyipaddress.com/ip/{app_ip}'})", unsafe_allow_html=True)
                login_cols[0].markdown(f"Device Type: {login_info.get('appDevType') or 'N/A'}")

                login_cols[1].markdown(f"**Last Web Login:** {format_ist(login_info.get('webDate'))}")
                web_ip = login_info.get("webIP")
                if web_ip:
                    login_cols[1].markdown(f"[Web Login IP]({f'https://whatismyipaddress.com/ip/{web_ip}'})", unsafe_allow_html=True)
                login_cols[1].markdown(f"App Type: {login_info.get('appType') or 'N/A'}")

                third_list = info.get("thirdpartyList") or []
                if third_list:
                    st.markdown("#### Linked Third-Party Accounts")
                    for account in third_list:
                        cols_tp = st.columns([1, 3])
                        cols_tp[0].write(account.get("thirdpartyType", "Unknown"))
                        cols_tp[1].write(account.get("openId") or "N/A")

                st.markdown("#### Full Response")
                st.code(json.dumps(data, ensure_ascii=False, indent=2), language="json")


if __name__ == "__main__":
    main()

import streamlit as st

ENTRY_LOGIN_KEY = "smartems_force_login_first_v1"

st.set_page_config(page_title="SmartEMS-AI", page_icon="EMS", layout="wide")

if not st.session_state.get(ENTRY_LOGIN_KEY):
    st.title("SmartEMS-AI \u7cfb\u7edf\u767b\u5f55")
    st.caption("\u8bf7\u5148\u8f93\u5165\u8d26\u53f7\u548c\u5bc6\u7801\uff0c\u767b\u5f55\u540e\u8fdb\u5165\u7cfb\u7edf\u3002")
    username = st.text_input("\u8d26\u53f7")
    password = st.text_input("\u5bc6\u7801", type="password")
    if st.button("\u767b\u5f55", type="primary"):
        if username == "admin" and password == "123456":
            st.session_state[ENTRY_LOGIN_KEY] = True
            st.rerun()
        else:
            st.error("\u8d26\u53f7\u6216\u5bc6\u7801\u9519\u8bef\u3002")
    st.info("\u6f14\u793a\u8d26\u53f7\uff1aadmin\uff0c\u5bc6\u7801\uff1a123456")
    st.stop()

from src.ui import app_main as ui

ui.apply_theme()
page = ui.render_sidebar()

if page == "\u7cfb\u7edf\u603b\u89c8":
    ui.render_overview()
elif page == "\u6570\u636e\u7ba1\u7406":
    ui.render_data_management()
elif page == "\u7279\u5f81\u5de5\u7a0b":
    ui.render_feature_engineering()
elif page == "\u6a21\u578b\u8bad\u7ec3\u9884\u6d4b":
    ui.render_model_training()
elif page == "\u7b56\u7565\u56de\u6d4b":
    ui.render_backtest()
else:
    ui.render_reports()

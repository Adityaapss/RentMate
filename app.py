import streamlit as st
from utils.auth import authenticate_user
from utils.db import init_db

def main():
    st.set_page_config(
        page_title="RentMate",
        page_icon="🏠",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    required_keys = ['logged_in', 'user_id', 'household_id', 'email']
    for key in required_keys:
        if key not in st.session_state:
            st.session_state[key] = None

    init_db()

    # Sidebar for logout
    if st.session_state.get('logged_in'):
        with st.sidebar:
            st.write(f"🔐 Logged in as: {st.session_state.email}")
            if st.button("🚪 Logout"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

    if not st.session_state.logged_in:
        from pages.login import show_login_page
        show_login_page()
    else:
        if st.session_state.household_id:
            st.switch_page("pages/0_🏠_Dashboard.py")
        else:
            st.switch_page("pages/1_👥_Household.py")

if __name__ == "__main__":
    main()

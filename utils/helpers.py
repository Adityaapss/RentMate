import streamlit as st
from utils.auth import authenticate_user


def main():
    st.set_page_config(page_title="RentMate", page_icon="🏠", layout="centered")

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        from pages.login import show_login_page
        show_login_page()
    else:
        st.switch_page("pages/0_🏠_Dashboard.py")


if __name__ == "__main__":
    main()
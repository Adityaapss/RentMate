import streamlit as st
from utils.auth import register_user, authenticate_user


def show_login_page():
    st.title("Welcome to RentMate 🏠")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")

            if st.form_submit_button("Login"):
                if authenticate_user(email, password):
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Invalid credentials")

    with tab2:
        with st.form("register_form"):
            name = st.text_input("Full Name", key="reg_name")
            email = st.text_input("Email", key="reg_email")
            password = st.text_input("Password", type="password", key="reg_pass")

            if st.form_submit_button("Register"):
                if register_user(name, email, password):
                    st.success("Account created! Please login")
                else:
                    st.error("Email already exists")
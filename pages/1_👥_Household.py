import streamlit as st
import random
import string
from utils.db import get_db


def generate_invite_code() -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def show_household_page():
    # ✅ Must be logged in
    if not st.session_state.get("logged_in"):
        st.warning("Please login first")
        st.page_link("app.py", label="Go to Login")
        return

    st.title("👥 Household Setup")

    # ✅ Invite code just created
    if st.session_state.get("created_invite_code"):
        st.success(f"✅ Household created! Invite code: {st.session_state.created_invite_code}")
        st.info("Share this code with your roommates to join this household.")
        st.button("Go to Dashboard", on_click=lambda: st.switch_page("pages/0_🏠_Dashboard.py"))
        return

    # ✅ Already in household
    if st.session_state.get("household_id"):
        st.switch_page("pages/0_🏠_Dashboard.py")

    # Tabs
    tab1, tab2 = st.tabs(["Create Household", "Join Household"])

    # ✅ CREATE
    with tab1:
        with st.form("create_form"):
            name = st.text_input("Household Name")
            submit = st.form_submit_button("Create Household")

            if submit and name:
                with get_db() as conn:
                    code = generate_invite_code()

                    conn.execute(
                        "INSERT INTO households (name, owner_id, invite_code) VALUES (?, ?, ?)",
                        (name, st.session_state.user_id, code)
                    )
                    household_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

                    conn.execute(
                        "INSERT INTO household_members (user_id, household_id, role) VALUES (?, ?, ?)",
                        (st.session_state.user_id, household_id, 'owner')
                    )

                    conn.commit()

                    st.session_state.household_id = household_id
                    st.session_state.created_invite_code = code
                    st.rerun()

    # ✅ JOIN
    with tab2:
        with st.form("join_form"):
            code = st.text_input("Enter 6-digit Invite Code").strip().upper()
            join = st.form_submit_button("Join Household")

            if join and code:
                with get_db() as conn:
                    household = conn.execute(
                        "SELECT id FROM households WHERE invite_code = ?", (code,)
                    ).fetchone()

                    if not household:
                        st.error("Invalid code.")
                        return

                    household_id = household['id']
                    existing = conn.execute(
                        "SELECT 1 FROM household_members WHERE user_id = ? AND household_id = ?",
                        (st.session_state.user_id, household_id)
                    ).fetchone()

                    if existing:
                        st.warning("Already a member of this household.")
                    else:
                        conn.execute(
                            "INSERT INTO household_members (user_id, household_id) VALUES (?, ?)",
                            (st.session_state.user_id, household_id)
                        )
                        conn.commit()
                        st.session_state.household_id = household_id
                        st.success("Joined household!")
                        st.rerun()


show_household_page()

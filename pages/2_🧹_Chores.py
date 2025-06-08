import streamlit as st
from utils.db import get_db


def get_household_members():
    if 'household_id' not in st.session_state:
        return []
    household_id = st.session_state.household_id
    with get_db() as conn:
        members = conn.execute(
            """
            SELECT users.name FROM users
            JOIN household_members ON users.id = household_members.user_id
            WHERE household_members.household_id = ?
            """,
            (household_id,)
        ).fetchall()
        return [m['name'] for m in members]


def get_active_chores():
    if 'household_id' not in st.session_state:
        return []
    household_id = st.session_state.household_id
    with get_db() as conn:
        chores = conn.execute(
            """
            SELECT id, name, frequency, assigned_to FROM chores
            WHERE household_id = ? AND completed = 0
            """,
            (household_id,)
        ).fetchall()
        return chores


def add_chore(name, frequency, assigned_to):
    if 'household_id' not in st.session_state:
        st.error("No household selected")
        return
    household_id = st.session_state.household_id
    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO chores (household_id, name, frequency, assigned_to, completed)
            VALUES (?, ?, ?, ?, 0)
            """,
            (household_id, name, frequency, assigned_to)
        )
        conn.commit()


def complete_chore(chore_id):
    with get_db() as conn:
        conn.execute(
            "UPDATE chores SET completed = 1 WHERE id = ?", (chore_id,)
        )
        conn.commit()


def show_chores_page():
    if not st.session_state.get('logged_in'):
        st.warning("Please login first")
        st.page_link("app.py", label="Go to Login")
        return

    if 'household_id' not in st.session_state:
        st.warning("Please join a household first")
        st.page_link("pages/1_👥_Household.py", label="← Household Setup")
        return

    st.title("🧹 Chore Management")

    with st.expander("➕ Add New Chore"):
        with st.form("new_chore"):
            name = st.text_input("Chore Name")
            frequency = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly"])
            assigned_to = st.selectbox("First Assignment", get_household_members())

            if st.form_submit_button("Save Chore"):
                if not name.strip():
                    st.error("Chore name cannot be empty")
                else:
                    add_chore(name.strip(), frequency, assigned_to)
                    st.success("Chore added successfully!")
                st.rerun()

    st.subheader("Active Chores")
    chores = get_active_chores()
    if not chores:
        st.info("No active chores.")
    for chore in chores:
        with st.container():
            cols = st.columns([3, 2, 1])
            cols[0].write(f"**{chore['name']}** ({chore['frequency']})")
            cols[1].write(f"Assigned to: {chore['assigned_to']}")
            if cols[2].button("Mark Done", key=f"done_{chore['id']}"):
                complete_chore(chore['id'])
                st.success("Chore marked as done!")
                st.rerun()


if __name__ == "__main__":
    show_chores_page()

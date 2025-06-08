import streamlit as st
from utils.db import get_db


def get_household_name(household_id: int) -> str:
    with get_db() as conn:
        household = conn.execute(
            "SELECT name FROM households WHERE id = ?",
            (household_id,)
        ).fetchone()
        return household['name'] if household else "Unknown"


def show_dashboard():
    # ✅ Authentication check
    if not st.session_state.get('logged_in'):
        st.warning("Please login first")
        st.page_link("app.py", label="Go to Login")
        return

    # ✅ Household check
    if not st.session_state.get('household_id'):
        st.warning("No household selected")
        st.page_link("pages/1_👥_Household.py", label="Create or Join Household")
        return

    # ✅ Main dashboard
    household_name = get_household_name(st.session_state.household_id)
    st.title(f"🏠 {household_name}")

    # ✅ Navigation section
    st.subheader("Quick Actions")
    cols = st.columns(3)
    cols[0].page_link("pages/2_🧹_Chores.py", label="Manage Chores", icon="🧹")
    cols[1].page_link("pages/3_💸_Expenses.py", label="Track Expenses", icon="💸")
    cols[2].page_link("pages/4_📅_Calendar.py", label="View Calendar", icon="📅")

    # ✅ Recent Activity placeholder
    st.subheader("Recent Activity")
    st.info("Recent chores and expenses will appear here.")  # Placeholder

    # Optional: Debug
    # st.write("Session State:", st.session_state)


# ✅ Ensure it runs
show_dashboard()

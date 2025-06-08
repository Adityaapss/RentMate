import streamlit as st
from streamlit_calendar import calendar
from utils.db import get_db


def get_chore_events():
    if 'household_id' not in st.session_state:
        return []
    household_id = st.session_state.household_id
    with get_db() as conn:
        chores = conn.execute(
            """
            SELECT name, next_due_date as start FROM chores
            WHERE household_id = ? AND completed = 0
            """,
            (household_id,)
        ).fetchall()
        # Format events for calendar
        return [{"title": chore['name'], "start": chore['start']} for chore in chores]


def get_expense_events():
    if 'household_id' not in st.session_state:
        return []
    household_id = st.session_state.household_id
    with get_db() as conn:
        expenses = conn.execute(
            """
            SELECT description, date as start FROM expenses
            WHERE household_id = ?
            """,
            (household_id,)
        ).fetchall()
        # Format events for calendar
        return [{"title": exp['description'], "start": exp['start']} for exp in expenses]


def show_calendar_page():
    if not st.session_state.get('logged_in'):
        st.warning("Please login first")
        st.page_link("app.py", label="Go to Login")
        return

    if 'household_id' not in st.session_state:
        st.warning("Please join a household first")
        st.page_link("pages/1_👥_Household.py", label="← Household Setup")
        return

    st.title("📅 Household Calendar")

    chores = get_chore_events()
    expenses = get_expense_events()

    calendar_options = {
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek",
        },
        "initialView": "dayGridMonth",
        "events": chores + expenses,
    }

    calendar(events=chores + expenses, options=calendar_options)


if __name__ == "__main__":
    show_calendar_page()

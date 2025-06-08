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


def add_expense(amount, description, date, payer, participants):
    if 'household_id' not in st.session_state:
        st.error("No household selected")
        return
    household_id = st.session_state.household_id
    with get_db() as conn:
        # Insert expense
        conn.execute(
            """
            INSERT INTO expenses (household_id, amount, description, date, payer)
            VALUES (?, ?, ?, ?, ?)
            """,
            (household_id, amount, description, date.isoformat(), payer)
        )
        expense_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        # Insert expense participants
        for participant in participants:
            conn.execute(
                """
                INSERT INTO expense_participants (expense_id, user_name)
                VALUES (?, ?)
                """,
                (expense_id, participant)
            )
        conn.commit()


def get_recent_expenses():
    if 'household_id' not in st.session_state:
        return []
    household_id = st.session_state.household_id
    with get_db() as conn:
        expenses = conn.execute(
            """
            SELECT amount, description, date, payer FROM expenses
            WHERE household_id = ?
            ORDER BY date DESC
            LIMIT 5
            """,
            (household_id,)
        ).fetchall()
        return expenses


def show_expenses_page():
    if not st.session_state.get('logged_in'):
        st.warning("Please login first")
        st.page_link("app.py", label="Go to Login")
        return

    if 'household_id' not in st.session_state:
        st.warning("Please join a household first")
        st.page_link("pages/1_👥_Household.py", label="← Household Setup")
        return

    st.title("💸 Expense Tracking")

    with st.expander("➕ Add New Expense"):
        with st.form("new_expense"):
            amount = st.number_input("Amount", min_value=0.01, step=0.01)
            description = st.text_input("Description")
            date = st.date_input("Date")
            payer = st.selectbox("Paid By", get_household_members())
            participants = st.multiselect("Split Between", get_household_members())

            if st.form_submit_button("Save Expense"):
                if amount <= 0:
                    st.error("Amount must be positive")
                elif not description.strip():
                    st.error("Description cannot be empty")
                elif not participants:
                    st.error("Select at least one participant")
                else:
                    add_expense(amount, description.strip(), date, payer, participants)
                    st.success("Expense added successfully!")
                st.rerun()

    st.subheader("Recent Expenses")
    expenses = get_recent_expenses()
    if not expenses:
        st.info("No recent expenses.")
    for exp in expenses:
        st.write(f"**{exp['amount']}** for {exp['description']} on {exp['date']} (paid by {exp['payer']})")


if __name__ == "__main__":
    show_expenses_page()

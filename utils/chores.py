from utils.db import get_db
from datetime import datetime, timedelta

def add_chore(name: str, frequency: str, assigned_to: int):
    db = get_db()
    due_date = calculate_due_date(frequency)
    db.execute(
        """INSERT INTO chores 
        (name, frequency, household_id, assignee_id, next_due) 
        VALUES (?, ?, ?, ?, ?)""",
        (name, frequency.lower(), st.session_state.household_id, assigned_to, due_date)
    )
    db.commit()

def calculate_due_date(frequency: str) -> str:
    today = datetime.now()
    if frequency == "Daily":
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif frequency == "Weekly":
        return (today + timedelta(weeks=1)).strftime("%Y-%m-%d")
    return (today.replace(day=1) + timedelta(days=32)).strftime("%Y-%m-%d")  # Next month
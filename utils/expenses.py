from utils.db import get_db


def add_expense(amount: float, description: str, date: str, payer_id: int, participant_ids: list):
    db = get_db()

    # Insert main expense
    db.execute(
        """INSERT INTO expenses 
        (amount, description, date, payer_id, household_id)
        VALUES (?, ?, ?, ?, ?)""",
        (amount, description, date, payer_id, st.session_state.household_id)
    )
    expense_id = db.lastrowid

    # Calculate shares
    share = amount / len(participant_ids) if participant_ids else 0

    # Insert participant shares
    for user_id in participant_ids:
        if user_id != payer_id:  # Payer doesn't owe themselves
            db.execute(
                """INSERT INTO expense_shares 
                (expense_id, user_id, share_amount)
                VALUES (?, ?, ?)""",
                (expense_id, user_id, share)
            )

    db.commit()
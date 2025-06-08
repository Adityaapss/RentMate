import streamlit as st
import pandas as pd
from utils.db import get_db


def show_history_page():
    st.title("📜 Activity History")

    # Date range filter
    col1, col2 = st.columns(2)
    start_date = col1.date_input("Start Date")
    end_date = col2.date_input("End Date")

    # Fetch data
    chores = get_chore_history(start_date, end_date)
    expenses = get_expense_history(start_date, end_date)

    # Display tables
    st.subheader("Chore History")
    st.dataframe(pd.DataFrame(chores))

    st.subheader("Expense History")
    st.dataframe(pd.DataFrame(expenses))

    # Export button
    if st.button("Export to CSV"):
        export_history(start_date, end_date)
        st.success("Exported successfully!")
        show_history_page()
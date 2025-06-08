import sqlite3
import os
from contextlib import contextmanager

# Database path
DB_PATH = "data/rentmate.db"

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Households table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS households (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            owner_id INTEGER NOT NULL,
            invite_code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users (id)
        )
        ''')

        # Memberships table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS memberships (
            user_id INTEGER NOT NULL,
            household_id INTEGER NOT NULL,
            role TEXT DEFAULT 'member',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, household_id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (household_id) REFERENCES households (id)
        )
        ''')

        # Chores table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS chores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            assigned_to INTEGER,
            due_date DATE NOT NULL,
            completed_at TIMESTAMP,
            household_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (assigned_to) REFERENCES users (id),
            FOREIGN KEY (household_id) REFERENCES households (id)
        )
        ''')

        # Expenses table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            date DATE NOT NULL,
            payer_id INTEGER NOT NULL,
            household_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (payer_id) REFERENCES users (id),
            FOREIGN KEY (household_id) REFERENCES households (id)
        )
        ''')

        # Expense participants table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS expense_participants (
            expense_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            percentage REAL DEFAULT 100,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (expense_id, user_id),
            FOREIGN KEY (expense_id) REFERENCES expenses (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        # Settlements table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS settlements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_user_id INTEGER NOT NULL,
            to_user_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            date DATE NOT NULL,
            household_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (from_user_id) REFERENCES users (id),
            FOREIGN KEY (to_user_id) REFERENCES users (id),
            FOREIGN KEY (household_id) REFERENCES households (id)
        )
        ''')

        conn.commit()

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

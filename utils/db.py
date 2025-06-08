import sqlite3
from typing import Optional

DATABASE_PATH = "rentmate.db"

def get_db():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    tables = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS households (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            owner_id INTEGER NOT NULL,
            invite_code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (owner_id) REFERENCES users (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS household_members (
            user_id INTEGER NOT NULL,
            household_id INTEGER NOT NULL,
            role TEXT CHECK(role IN ('owner', 'member')) NOT NULL DEFAULT 'member',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, household_id),
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (household_id) REFERENCES households (id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS chores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            household_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            assigned_to TEXT NOT NULL,
            next_due_date TEXT,
            completed INTEGER DEFAULT 0,
            FOREIGN KEY (household_id) REFERENCES households(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            household_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            description TEXT NOT NULL,
            date TEXT NOT NULL,
            payer TEXT NOT NULL,
            FOREIGN KEY (household_id) REFERENCES households(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS expense_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_id INTEGER NOT NULL,
            user_name TEXT NOT NULL,
            FOREIGN KEY (expense_id) REFERENCES expenses(id)
        )
        """
    ]

    with get_db() as conn:
        cursor = conn.cursor()
        for table in tables:
            cursor.execute(table)
        conn.commit()

def get_user_id(email: str) -> Optional[int]:
    with get_db() as conn:
        user = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
        return user['id'] if user else None

def get_user_household(user_id: int) -> Optional[int]:
    with get_db() as conn:
        result = conn.execute(
            "SELECT household_id FROM household_members WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        return result['household_id'] if result else None

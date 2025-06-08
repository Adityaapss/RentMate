import sqlite3
import bcrypt
import streamlit as st
from utils.db import get_db, get_user_household

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed)
    except Exception:
        return False

def register_user(name: str, email: str, password: str) -> bool:
    try:
        with get_db() as conn:
            conn.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hash_password(password))
            )
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(email: str, password: str) -> bool:
    with get_db() as conn:
        user = conn.execute(
            "SELECT id, password FROM users WHERE email = ?",
            (email,)
        ).fetchone()

        if user and verify_password(password, user['password']):
            household_id = get_user_household(user['id'])
            st.session_state.update({
                'user_id': user['id'],
                'email': email,
                'logged_in': True,
                'household_id': household_id
            })
            return True

    return False

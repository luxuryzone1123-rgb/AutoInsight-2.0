import sqlite3
import os

DB_PATH = "autoin_sight.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    
    # Analysis History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            file_name TEXT NOT NULL,
            data_summary TEXT,
            executive_report TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

def register_user(email: str, password: str) -> bool:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email.strip().lower(), password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def authenticate_user(email: str, password: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email.strip().lower(), password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def save_analysis_history(user_email: str, file_name: str, data_summary: str, executive_report: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO history (user_email, file_name, data_summary, executive_report)
        VALUES (?, ?, ?, ?)
    """, (user_email.strip().lower(), file_name, data_summary, executive_report))
    conn.commit()
    conn.close()

def get_user_history(user_email: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT file_name, data_summary, executive_report, created_at
        FROM history WHERE user_email = ? ORDER BY created_at DESC
    """, (user_email.strip().lower(),))
    rows = cursor.fetchall()
    conn.close()
    
    records = []
    for row in rows:
        records.append({
            "file_name": row[0],
            "data_summary": row[1],
            "executive_report": row[2],
            "created_at": row[3]
        })
    return records
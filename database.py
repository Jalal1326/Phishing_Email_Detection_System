import sqlite3
from datetime import datetime

DATABASE_NAME = "phishing_analysis.db"

def create_database():
    """Create the results table if it doesn’t exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email_text TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                analysis_timestamp TEXT NOT NULL
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database creation error: {e}")
    finally:
        conn.close()

def save_analysis_result(email_text, prediction, confidence):
    """
    Insert a new analysis record.
    Uses parameterized queries to prevent SQL injection.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO analysis_results
            (email_text, prediction, confidence, analysis_timestamp)
            VALUES (?, ?, ?, ?);
        """, (email_text, prediction, confidence, timestamp))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Failed to save result: {e}")
    finally:
        conn.close()

# Ensure table is ready on import
create_database()

"""
Database Service

Handles all database operations for emotion history.
Uses SQLite for simplicity and portability.

TODO: Add connection pooling for better performance
TODO: Add database migrations support
TODO: Consider PostgreSQL for production
"""
import logging
import sqlite3
from typing import List, Dict, Any

from app.core.config import DB_PATH

logger = logging.getLogger(__name__)

def get_connection():
    """Get database connection."""
    return sqlite3.connect(str(DB_PATH))


def create_table():
    """Create necessary tables if they don't exist.
    Currently this handles both the emotion history and the
    simple user store used for authentication.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # emotions table (existing)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                emotion TEXT NOT NULL,
                confidence REAL NOT NULL
            )
        """)

        # users table for authentication
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise


def save_emotion(emotion: str, confidence: float, date: str) -> bool:
    """
    Save emotion prediction to database.
    
    Args:
        emotion: Predicted emotion label
        confidence: Confidence score (0-1)
        date: Timestamp string
        
    Returns:
        True if successful
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO emotions (date, emotion, confidence) VALUES (?, ?, ?)",
            (date, emotion, confidence)
        )

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error saving emotion to database: {str(e)}")
        raise


def get_history() -> List[Dict[str, Any]]:
    """
    Get all emotion history records.
    
    Returns:
        List of emotion records with date, emotion, and confidence
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT date, emotion, confidence FROM emotions ORDER BY date DESC"
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "date": row[0],
                "emotion": row[1],
                "confidence": row[2]
            }
            for row in rows
        ]
    except Exception as e:
        logger.error(f"Error fetching emotion history: {str(e)}")
        raise


# --------------------
# USERS / AUTH HELPERS
# --------------------

def create_user(email: str, password_hash: str) -> bool:
    """Insert a new user record into the database."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password_hash)
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Email already exists
        return False
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise


def get_user_by_email(email: str) -> Dict[str, Any] | None:
    """Retrieve a user record by email address.

    Returns a dictionary with keys `id`, `email`, and `password` (hashed)
    or None if the user does not exist.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, email, password FROM users WHERE email = ?",
            (email,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"id": row[0], "email": row[1], "password": row[2]}
        return None
    except Exception as e:
        logger.error(f"Error fetching user by email: {str(e)}")
        raise

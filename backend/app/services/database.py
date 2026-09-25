"""
Database Service

Handles all database operations for emotion history and user authentication.
Uses SQLite for simplicity and portability.

TODO: Add connection pooling for better performance
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
    """
    Create necessary tables if they don't exist, and run any pending migrations.

    Tables:
      - emotions : per-user emotion history (user_id scoped)
      - users    : user accounts for authentication
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # emotions table — user_id scoped
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emotions (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id  INTEGER NOT NULL,
                date     TEXT    NOT NULL,
                emotion  TEXT    NOT NULL,
                confidence REAL  NOT NULL
            )
        """)

        # users table for authentication
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                email    TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        conn.commit()

        # ── Migration: add user_id to existing emotions tables ────────────────
        # SQLite doesn't support IF NOT EXISTS for columns, so we catch the
        # OperationalError that fires when the column already exists.
        try:
            cursor.execute("ALTER TABLE emotions ADD COLUMN user_id INTEGER NOT NULL DEFAULT 0")
            conn.commit()
            logger.info("Migration applied: added user_id column to emotions table")
        except sqlite3.OperationalError:
            pass  # Column already exists — nothing to do

        conn.close()
        logger.info("Database tables created/verified successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise


def save_emotion(emotion: str, confidence: float, date: str, user_id: int) -> bool:
    """
    Save emotion prediction to database for a specific user.

    Args:
        emotion:    Predicted emotion label
        confidence: Confidence score (0–1)
        date:       Timestamp string
        user_id:    ID of the authenticated user

    Returns:
        True if successful
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO emotions (user_id, date, emotion, confidence) VALUES (?, ?, ?, ?)",
            (user_id, date, emotion, confidence)
        )

        conn.commit()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Error saving emotion to database: {str(e)}")
        raise


def get_history(user_id: int) -> List[Dict[str, Any]]:
    """
    Get emotion history records for a specific user.

    Args:
        user_id: ID of the authenticated user

    Returns:
        List of emotion records (date, emotion, confidence) ordered newest first
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT date, emotion, confidence FROM emotions "
            "WHERE user_id = ? ORDER BY date DESC",
            (user_id,)
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "date":       row[0],
                "emotion":    row[1],
                "confidence": row[2],
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

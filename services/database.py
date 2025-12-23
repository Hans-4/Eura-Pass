#API
import sqlite3
from typing import Optional, List, Tuple

class Database:
    def __init__(self, db_name="passwords.db"):
        """Initializes the database connection and creates necessary tables if they don't exist."""

        self.db_name = db_name
        self.init_tables() # Initialize database tables

    def init_tables(self):
        """Creates the necessary tables in the database if they do not already exist."""

        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        # Passwords Tabelle for storing user passwords
        cur.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                username TEXT NOT NULL,
                password BLOB NOT NULL,
                two_fa_key BLOB,
                website TEXT,
                notes TEXT,
                salt BLOB NOT NULL
            )
        ''')

        # User Tabelle for login credentials
        cur.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()

    def save_password(self, user_id: int, title: str, username: str, encrypted_password: bytes, two_fa_key: str, website: str, notes: str, salt: bytes):
        """Saves a new password entry to the database."""

        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO passwords (user_id, title, username, password, two_fa_key, website, notes, salt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, title, username, encrypted_password, two_fa_key, website, notes, salt))
            conn.commit()

    def get_passwords_by_user(self, user_id: int) -> List[Tuple]:
        """Retrieves all password entries for a specific user."""

        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT id, title, username, password, two_fa_key, website, notes, salt 
                FROM passwords WHERE user_id = ?
            ''', (user_id,))
            return cur.fetchall()

    def get_password_titles_by_user(self, user_id: int) -> List[Tuple]:
        """Retrieves the titles, usernames, and salts of all password entries for a specific user."""

        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        query = """
        SELECT id, title, username, salt
        FROM passwords
        WHERE user_id = ?
        """

        cur.execute(query, (user_id,))
        result = cur.fetchall()

        conn.close()

        return result

    def create_user(self, email: str, username: str, password_hash: str):
        """Creates a new user in the database after registration."""

        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO user (email, username, password)
                VALUES (?, ?, ?)
            ''', (email, username, password_hash))
            conn.commit()

    def get_user_by_credentials(self, username_or_email: str, password_hash: str) -> Optional[Tuple]:
        """Retrieves a user by their username or email and password hash for login."""

        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT id, email, username FROM user 
                WHERE (username = ? OR email = ?) AND password = ?
            ''', (username_or_email, username_or_email, password_hash))
            return cur.fetchone()

    def delete_password(self, password_id: int) -> bool:
        """Deletes a password entry from the database by its ID."""

        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('SELECT id FROM passwords WHERE id = ?', (password_id,))
            if not cur.fetchone():
                return False # Password ID does not exist

            cur.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
            conn.commit()
            return True # Password successfully deleted
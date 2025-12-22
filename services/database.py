import sqlite3
from typing import Optional, List, Tuple

class Database:
    def __init__(self, db_name="passwords.db"):
        self.db_name = db_name
        self.init_tables()

    def init_tables(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()

        # Passwords Tabelle
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

        # User Tabelle
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

    def save_password(self, user_id: int, title: str, username: str,
                      encrypted_password: bytes, two_fa_key: str, website: str,
                      notes: str, salt: bytes):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO passwords (user_id, title, username, password, two_fa_key, website, notes, salt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, title, username, encrypted_password, two_fa_key, website, notes, salt))
            conn.commit()

    def get_passwords_by_user(self, user_id: int) -> List[Tuple]:
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT id, title, username, password, two_fa_key, website, notes, salt 
                FROM passwords WHERE user_id = ?
            ''', (user_id,))
            return cur.fetchall()

    def get_password_titles_by_user(self, user_id: int) -> List[Tuple]:
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
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO user (email, username, password)
                VALUES (?, ?, ?)
            ''', (email, username, password_hash))
            conn.commit()

    def get_user_by_credentials(self, username_or_email: str, password_hash: str) -> Optional[Tuple]:
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('''
                SELECT id, email, username FROM user 
                WHERE (username = ? OR email = ?) AND password = ?
            ''', (username_or_email, username_or_email, password_hash))
            return cur.fetchone()

    def delete_password(self, password_id: int) -> bool:
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('SELECT id FROM passwords WHERE id = ?', (password_id,))
            if not cur.fetchone():
                return False
            cur.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
            conn.commit()
            return True
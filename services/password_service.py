import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from typing import List, Dict, Tuple, Optional
from services.database import Database

class PasswordService:
    def __init__(self, database: Database):
        self.db = database

    def generate_key(self, password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        password_bytes = password.encode()
        key_raw = kdf.derive(password_bytes)
        return base64.urlsafe_b64encode(key_raw)

    def encrypt_data(self, title: str, username: str, password: str, two_fa_key: str, website: str, notes: str, master_password: str) -> Tuple[bytes, bytes, bytes, bytes, bytes, bytes, bytes]:
        salt = secrets.token_bytes(16)
        key = self.generate_key(master_password, salt)
        f = Fernet(key)
        encrypted_title = f.encrypt(title.encode())
        encrypted_username = f.encrypt(username.encode())
        encrypted_password = f.encrypt(password.encode())
        encrypted_two_fa_key = f.encrypt(two_fa_key.encode())
        encrypted_website = f.encrypt(website.encode())
        encrypted_notes = f.encrypt(notes.encode())
        return encrypted_title, encrypted_username, encrypted_password, encrypted_two_fa_key, encrypted_website, encrypted_notes, salt

    def decrypt_data(
            self,
            encrypted_title: bytes,
            encrypted_username: bytes,
            encrypted_password: bytes,
            encrypted_two_fa_key: bytes,
            encrypted_website: bytes,
            encrypted_notes: bytes,
            master_password: str,
            salt: bytes
    ) -> Tuple[str, str, str, str, str, str]:

        key = self.generate_key(master_password, salt)
        f = Fernet(key)

        title = f.decrypt(encrypted_title).decode()
        username = f.decrypt(encrypted_username).decode()
        password = f.decrypt(encrypted_password).decode()
        two_fa_key = f.decrypt(encrypted_two_fa_key).decode()
        website = f.decrypt(encrypted_website).decode()
        notes = f.decrypt(encrypted_notes).decode()

        return title, username, password, two_fa_key, website, notes

    def save_password(
            self,
            user_id: int,
            title: str,
            username: str,
            password: str,
            master_password: str,
            two_fa_key: str = "",
            website: str = "",
            notes: str = ""
    ):
        encrypted_title, encrypted_username, encrypted_password, encrypted_two_fa_key, encrypted_website, encrypted_notes, salt = self.encrypt_data(
            title, username, password, two_fa_key, website, notes, master_password
        )

        self.db.save_password(
            user_id=user_id,
            title=encrypted_title,
            username=encrypted_username,
            encrypted_password=encrypted_password,
            two_fa_key=encrypted_two_fa_key,
            website=encrypted_website,
            notes=encrypted_notes,
            salt=salt
        )

    def load_passwords(self, user_id: int, master_password: str) -> List[Dict]:
        passwords = []
        rows = self.db.get_passwords_by_user(user_id)

        for row in rows:
            # Now includes id as first element
            password_id, encrypted_title, encrypted_username, encrypted_password, encrypted_two_fa_key, encrypted_website, encrypted_notes, salt = row
            try:
                title, username, password, two_fa_key, website, notes = self.decrypt_data(
                    encrypted_title, encrypted_username, encrypted_password,
                    encrypted_two_fa_key, encrypted_website, encrypted_notes,
                    master_password, salt
                )
                passwords.append({
                    "id": password_id,  # Include the ID
                    "title": title,
                    "username": username,
                    "password": password,
                    "two_fa_key": two_fa_key,
                    "website": website,
                    "notes": notes,
                })
            except Exception:
                continue

        return passwords

    def get_password_overview(self, user_id: int, master_password: str) -> List[Tuple[str, str]]:
        overview = []
        rows = self.db.get_password_titles_by_user(user_id)

        for password_id, encrypted_title, encrypted_username, salt in rows:
            try:
                key = self.generate_key(master_password, salt)
                f = Fernet(key)
                title = f.decrypt(encrypted_title).decode()
                username = f.decrypt(encrypted_username).decode()
                overview.append((title, username))
            except Exception:
                continue

        return overview

    def find_password(self, passwords: List[Dict], title: str, username: str) -> Optional[Dict]:
        return next(
            (item for item in passwords if item["title"] == title and item["username"] == username),
            None
        )

    def validate_password_data(self, title: str, password: str) -> Tuple[bool, str]:
        if not title or not password:
            return False, "Titel und Passwort sind Pflicht!"

        return True, ""

    def delete_password(self, password_id: int) -> bool:
        return self.db.delete_password(password_id)  # Fixed: was self.database, now self.db
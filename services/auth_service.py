import hashlib
from typing import Optional, Tuple
from services.database import Database

class AuthService:
    def __init__(self, database: Database):
        self.db = database

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, email: str, username: str, password: str) -> bool:
        try:
            password_hash = self.hash_password(password)
            self.db.create_user(email, username, password_hash)
            return True
        except Exception as e:
            return False

    def authenticate_user(self, username_or_email: str, password: str) -> Optional[Tuple[int, str, str]]:
        password_hash = self.hash_password(password)
        user = self.db.get_user_by_credentials(username_or_email, password_hash)
        return user

    def validate_registration_data(self, email: str, username: str,
                                   password1: str, password2: str) -> Tuple[bool, str]:
        if not email or not username or not password1 or not password2:
            return False, "Bitte geben Sie alle Felder ein."

        if password1 != password2:
            return False, "Beide Passwörter müssen gleich sein."

        return True, ""

    def validate_login_data(self, username: str, password: str) -> Tuple[bool, str]:
        if not username or not password:
            return False, "Bitte geben Sie sowohl Benutzername als auch Passwort ein."

        return True, ""
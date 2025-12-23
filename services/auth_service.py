#API
import hashlib
from typing import Optional, Tuple

#Services
from services.database import Database

class AuthService:
    def __init__(self, database: Database):
        """Initializes the authentication service with a database connection."""
        self.db = database

    def hash_password(self, password: str) -> str:
        """Hashes the password using SHA-256 algorithm."""
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, email: str, username: str, password: str) -> bool:
        """Registers a new user with the provided email, username, and password."""

        # Hashes the password before storing it
        try:
            password_hash = self.hash_password(password)
            self.db.create_user(email, username, password_hash)
            return True

        # Catches any exception that occurs during user registration
        except Exception as e:
            return False

    def authenticate_user(self, username_or_email: str, password: str) -> Optional[Tuple[int, str, str]]:
        """Authenticates a user with the provided username and password."""

        password_hash = self.hash_password(password)
        user = self.db.get_user_by_credentials(username_or_email, password_hash)
        return user

    def validate_registration_data(self, email: str, username: str, password1: str, password2: str) -> Tuple[bool, str]:
        """Validates the registration data provided by the user."""

        # Checks if all fields are filled
        if not email or not username or not password1 or not password2:
            return False, "Bitte geben Sie alle Felder ein."

        # Checks if passwords match
        if password1 != password2:
            return False, "Beide Passwörter müssen gleich sein."

        # If no issues, return True
        return True, ""

    def validate_login_data(self, username: str, password: str) -> Tuple[bool, str]:
        """Validates the login data provided by the user."""

        # Checks if all fields are filled
        if not username or not password:
            return False, "Bitte geben Sie sowohl Benutzername als auch Passwort ein."

        # If no issues, return True
        return True, ""
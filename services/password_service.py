# API
import secrets
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from typing import List, Dict, Tuple, Optional

# Services
from services.database import Database

class PasswordService:
    def __init__(self, database: Database):
        """Handles encryption, decryption, and storage of password data using Fernet and PBKDF2HMAC."""

        self.db = database

    def generate_key(self, password: str, salt: bytes) -> bytes:
        """Generates a Fernet key from the given password and salt."""

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), #Use SHA256 hash algorithm
            length=32, #Lenght of the key in bytes (32 bytes = 256 bits)
            salt=salt, #Use provided salt
            iterations=480000, #Password gets hashed 480000 times
        )
        password_bytes = password.encode() #Convert password to bytes
        key_raw = kdf.derive(password_bytes) #Derive the key
        return base64.urlsafe_b64encode(key_raw) #Encode the key in a URL-safe base64 format

    def encrypt_data(self, title: str, username: str, password: str, two_fa_key: str, website: str, notes: str, master_password: str) -> Tuple[bytes, bytes, bytes, bytes, bytes, bytes, bytes]:
        """Encrypts the provided data using the master password."""

        salt = secrets.token_bytes(16) #Generate a random 16-byte salt
        key = self.generate_key(master_password, salt) #Generate key from master password and salt
        f = Fernet(key) #Create Fernet object with the generated key

        encrypted_title = f.encrypt(title.encode()) #Encrypt title
        encrypted_username = f.encrypt(username.encode()) #Encrypt username
        encrypted_password = f.encrypt(password.encode()) #Encrypt password
        encrypted_two_fa_key = f.encrypt(two_fa_key.encode()) #Encrypt 2FA key
        encrypted_website = f.encrypt(website.encode()) #Encrypt website
        encrypted_notes = f.encrypt(notes.encode()) #Encrypt notes
        return encrypted_title, encrypted_username, encrypted_password, encrypted_two_fa_key, encrypted_website, encrypted_notes, salt #Return encrypted data and salt

    def decrypt_data(self, encrypted_title: bytes, encrypted_username: bytes, encrypted_password: bytes, encrypted_two_fa_key: bytes, encrypted_website: bytes, encrypted_notes: bytes, master_password: str,salt: bytes) -> Tuple[str, str, str, str, str, str]:
        """Decrypts the provided encrypted data using the master password.

        Raises:
            cryptography.fernet.InvalidToken: If decryption fails (wrong key or corrupted data).
        """

        key = self.generate_key(master_password, salt) #Generate key from master password and salt
        f = Fernet(key) #Create Fernet object with the generated key

        title = f.decrypt(encrypted_title).decode() #Decrypt title
        username = f.decrypt(encrypted_username).decode() #Decrypt username
        password = f.decrypt(encrypted_password).decode() #Decrypt password
        two_fa_key = f.decrypt(encrypted_two_fa_key).decode() #Decrypt 2FA key
        website = f.decrypt(encrypted_website).decode() #Decrypt website
        notes = f.decrypt(encrypted_notes).decode() #Decrypt notes

        return title, username, password, two_fa_key, website, notes #Return decrypted data

    def save_password(self,user_id: int,title: str,username: str,password: str,master_password: str,two_fa_key: str = "",website: str = "",notes: str = ""):
        """Saves the encrypted password data to the database."""

        encrypted_title, encrypted_username, encrypted_password, encrypted_two_fa_key, encrypted_website, encrypted_notes, salt = self.encrypt_data(
            title, username, password, two_fa_key, website, notes, master_password
        )

        # Save encrypted data to the database
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
        """Loads and decrypts all passwords for the given user.
            All data is only safed in th RAM and never stored unencrypted on disk.
        """

        passwords = [] #Empty list to store decrypted passwords
        rows = self.db.get_passwords_by_user(user_id)

        # Decrypt each password and add to the list
        for row in rows:
            password_id, encrypted_title, encrypted_username, encrypted_password, encrypted_two_fa_key, encrypted_website, encrypted_notes, salt = row
            try:
                title, username, password, two_fa_key, website, notes = self.decrypt_data(
                    encrypted_title, encrypted_username, encrypted_password,
                    encrypted_two_fa_key, encrypted_website, encrypted_notes,
                    master_password, salt
                )
                passwords.append({
                    "id": password_id,
                    "title": title,
                    "username": username,
                    "password": password,
                    "two_fa_key": two_fa_key,
                    "website": website,
                    "notes": notes,
                })
            except Exception: #If decryption fails (e.g., wrong master password), skip this entry
                continue

        return passwords

    def get_password_overview(self, user_id: int, master_password: str) -> List[Tuple[str, str]]:
        """Retrieves an overview of titles and usernames for the given user (without decrypting full entries)."""

        overview = [] #Empty list to store overview
        rows = self.db.get_password_titles_by_user(user_id)

        for password_id, encrypted_title, encrypted_username, salt in rows:
            try:
                key = self.generate_key(master_password, salt)
                f = Fernet(key)

                title = f.decrypt(encrypted_title).decode() #Decrypt title
                username = f.decrypt(encrypted_username).decode() #Decrypt username
                overview.append((title, username)) #Add to overview list

            except Exception: #If decryption fails, skip this entry
                continue

        return overview

    def find_password(self, passwords: List[Dict], title: str, username: str) -> Optional[Dict]:
        """Finds a password entry by title and username.

        Example:
            password = find_password(passwords, "Google", "user@example.com")
        """

        return next(
            (item for item in passwords if item["title"] == title and item["username"] == username),
            None
        )

    def validate_password_data(self, title: str, password: str) -> Tuple[bool, str]:
        """Validates the password data before saving.

        Rules:
            - Title and password must not be empty.
            - (Optional) Password must be at least 8 characters long.
        """

        # Check required fields
        if not title or not password:
            return False, "Titel und Passwort sind Pflicht!"

        return True, ""

    def delete_password(self, password_id: int) -> bool:
        """Deletes a password entry by its ID.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """

        return self.db.delete_password(password_id) #Return True if deletion was successful
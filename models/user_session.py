class UserSession:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserSession, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.user_id = 1
        self.master_password = None
        self.username = None
        self.email = None

    def login(self, user_id, master_password, username=None, email=None):
        self.user_id = user_id
        self.master_password = master_password
        self.username = username
        self.email = email

    def logout(self):
        self.user_id = None
        self.master_password = None
        self.username = None
        self.email = None
        print("✓ User ausgeloggt")

    def is_logged_in(self):
        return self.user_id is not None and self.master_password is not None

    def get_user_id(self):
        if not self.is_logged_in():
            raise ValueError("Kein User eingeloggt!")
        return self.user_id

    def get_master_password(self):
        if not self.is_logged_in():
            raise ValueError("Kein User eingeloggt!")
        return self.master_password

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

def get_session():
    return UserSession()
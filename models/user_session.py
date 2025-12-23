class UserSession:
    """Singleton class to manage user session data and authentication state."""

    _instance = None

    def __new__(cls):
        """Ensures only one instance exists (Singleton pattern). Creates a new instance if none exists."""

        if cls._instance is None:
            cls._instance = super(UserSession, cls).__new__(cls)
            cls._instance._initialized = False # To prevent re-initialization
        return cls._instance

    def __init__(self):
        """Initializes user session attributes if not already done (prevents re-initialization)."""

        if self._initialized:
            return
        self._initialized = True
        self.user_id = None
        self.master_password = None
        self.username = None
        self.email = None

    def login(self, user_id, master_password, username=None, email=None):
        """
        Set user session data upon login.

        Args:
            user_id: Unique identifier for the user.
            master_password: User's master password for encryption.
            username (optional): User's username.
            email (optional): User's email address.
        """

        self.user_id = user_id
        self.master_password = master_password
        self.username = username
        self.email = email

    def logout(self):
        """Clear user session data upon logout."""

        self.user_id = None
        self.master_password = None
        self.username = None
        self.email = None

    def is_logged_in(self):
        """Check if a user is currently logged in.

        Returns:
            bool: True if user is logged in, False otherwise.
        """

        return self.user_id is not None and self.master_password is not None

    def get_user_id(self):
        """Returns the logged-in user's ID.

        Returns:
            int: User ID.

        Raises:
            ValueError: If no user is logged in.
        """

        if not self.is_logged_in():
            raise ValueError("No user logged in!")
        return self.user_id

    def get_master_password(self):
        """Get the logged-in user's master password."""

        if not self.is_logged_in():
            raise ValueError("No user logged in!")
        return self.master_password

    def get_username(self):
        """Get the logged-in user's username."""

        return self.username

    def get_email(self):
        """Get the logged-in user's email."""

        return self.email

def get_session():
    """Returns the singleton UserSession instance (creates it if necessary)."""

    return UserSession()
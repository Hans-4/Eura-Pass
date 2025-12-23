# API
import customtkinter as ctk

# Config
import config.colors as colors

# Services
from services.password_service import PasswordService

# Models
from models import user_session

class PasswordOverviewUI:
    def __init__(self, master, password_service: PasswordService):
        """Initializes the Password Overview UI component.
        Args:
            master: The parent tkinter widget.
            password_service (PasswordService): Service for managing passwords.
        """
        self.master = master
        self.password_service = password_service

        self.scroll_frame = ctk.CTkScrollableFrame(
            master=master,
            width=300,
            corner_radius=0,
            fg_color=colors.background_color,
        )
        self.scroll_frame.grid(column=0, row=1, sticky="nsew")

        self.passwords = [] # Empty list to hold password data
        self.load_passwords() # Load passwords on initialization

    def load_passwords(self):
        """Loads passwords from the password service and displays them."""

        # Attempt to load passwords for the logged-in user
        try:
            session = user_session.get_session()

            # Check if a user is logged in
            if session.is_logged_in():
                user_id = session.get_user_id()
                master_password = session.get_master_password()
                self.passwords = self.password_service.get_password_overview(user_id, master_password)

            # If no user is logged in, set passwords to an empty list
            else:
                self.passwords = []

        # Handle potential errors during password loading to prevent crashes
        except Exception as e:
            print(f"Fehler beim Laden der Passwörter: {e}")
            self.passwords = []

        self.display_password_cards() # Display the loaded passwords

    def refresh_passwords(self):
        """Refreshes the password list by reloading and displaying passwords."""

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.load_passwords()

    def display_password_cards(self):
        """Displays password cards in the scrollable frame.
            (title, username) pairs are shown for each password.
            Details can be accessed by clicking on the cards.
        """

        for i, (title, username) in enumerate(self.passwords):
            password_frame = ctk.CTkFrame(
                self.scroll_frame,
                fg_color="transparent",
                corner_radius=0,
                border_width=1,
                border_color=colors.border_color,
                width=280,
                height=100
            )
            password_frame.grid(row=i, column=0, sticky="ew")

            title_label = ctk.CTkButton(
                password_frame,
                text=title,
                font=("Manrope", 20, "bold"),
                text_color=colors.secondary_text_color,
                fg_color="transparent",
                corner_radius=0,
                width=280,
                hover=False,
                cursor="hand2",
                command=lambda t=title, u=username: self.on_password_click(t, u)
            )
            title_label.pack(side="top", pady=(10, 3), padx=20)

            username_label = ctk.CTkButton(
                password_frame,
                text=username,
                font=("Manrope", 15),
                text_color=colors.secondary_text_color,
                width=280,
                fg_color="transparent",
                corner_radius=0,
                hover=False,
                cursor="hand2",
                command=lambda t=title, u=username: self.on_password_click(t, u)
            )
            username_label.pack(side="top", pady=(2, 10), padx=20)

    def on_password_click(self, title: str, username: str):
        """Handles the event when a password card is clicked."""
        self.master.show_password_details(title, username)
# API
import webbrowser
import customtkinter as ctk
from tkinter import messagebox

#Config
import config.colors as colors

# Models
from models import user_session

# Services
from services.auth_service import AuthService


class LoginWindow(ctk.CTkToplevel):
    def __init__(self, master, auth_service: AuthService):
        """
        Initializes the login and registration window.

        - Configures window properties (title, size, appearance).
        -Sets up login and registration tabs with input fields and buttons.
        """
        super().__init__(master)
        self.master = master
        self.auth_service = auth_service

        self.title("Eura Pass - Anmeldung")
        self.geometry("400x500")
        self.resizable(False, False)
        self.configure(fg_color=colors.background_color)
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Close the main window on close

        self.create_login_tab()
        self.create_registration_tab()

        self.login_tab_open = True # Start with login tab
        self.main_login_frame.lift() # Show login tab

    def switch_tab(self):
        """Switches between the login and registration tabs."""
        self.login_tab_open = not self.login_tab_open # Toggle tab state
        if self.login_tab_open:
            self.main_registration_frame.lift()
            self._clear_registration_fields()
        else:
            self.main_login_frame.lift()
            self._clear_login_fields()

    def _clear_login_fields(self):
        """Clears the input fields in the login tab after switching tabs."""
        self.username_login_entry.delete(0, 'end')
        self.password_login_entry.delete(0, 'end')

    def _clear_registration_fields(self):
        """Clears the input fields in the registration tab after switching tabs."""
        self.email_registration_entry.delete(0, 'end')
        self.username_registration_entry.delete(0, 'end')
        self.password_registration_entry_1.delete(0, 'end')
        self.password_registration_entry_2.delete(0, 'end')

    def create_login_tab(self):
        """Creates the login tab UI components."""

        self.main_login_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_login_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        login_title_label = ctk.CTkLabel(
            self.main_login_frame,
            text="Willkommen zurück",
            font=("Manrope", 24, "bold"),
            text_color=colors.text_color
        )
        login_title_label.pack(pady=(100, 20))

        self.username_login_entry = ctk.CTkEntry(
            self.main_login_frame,
            placeholder_text="E-Mail oder Benutzername",
            width=300, height=40,
            font=("Manrope", 16),
            fg_color=colors.second_button_color,
            text_color=colors.text_color,
            border_color=colors.border_color,
            border_width=1,
            corner_radius=40
        )
        self.username_login_entry.pack(pady=10)

        self.password_login_entry = ctk.CTkEntry(
            self.main_login_frame,
            placeholder_text="Passwort",
            width=300, height=40,
            font=("Manrope", 16),
            fg_color=colors.second_button_color,
            text_color=colors.text_color,
            show="*",
            border_color=colors.border_color,
            border_width=1,
            corner_radius=40
        )
        self.password_login_entry.pack(pady=10)

        self.check_show_password_checkbox_state = ctk.IntVar(value=0)
        self.show_password_checkbox = ctk.CTkCheckBox(
            self.main_login_frame,
            text="Passwort anzeigen",
            font=("Manrope", 13),
            text_color=colors.text_color,
            border_width=1,
            border_color=colors.border_color,
            width=300,
            checkbox_height=20,
            checkbox_width=20,
            corner_radius=40,
            command=self.toggle_password_visibility,
            variable=self.check_show_password_checkbox_state,
            onvalue=1, offvalue=0
        )
        self.show_password_checkbox.pack(pady=5)

        login_button = ctk.CTkButton(
            self.main_login_frame,
            text="Anmelden",
            command=self.handle_login,
            width=300, height=40,
            font=("Manrope", 16, "bold"),
            text_color=colors.text_color,
            fg_color=colors.primary_color,
            hover_color=colors.hover_color,
            corner_radius=40
        )
        login_button.pack(pady=(30, 25))

        switch_to_registration_tab = ctk.CTkButton(
            self.main_login_frame,
            text="Neu bei Eura? Konto erstellen",
            command=self.switch_tab,
            font=("Manrope", 14),
            text_color=colors.text_color,
            fg_color="transparent",
            hover=False,
        )
        switch_to_registration_tab.pack(pady=15)

        self.bind("<Return>", lambda event: self.handle_login()) # Bind Enter key to login

    def create_registration_tab(self):
        """Creates the registration tab UI components."""

        self.main_registration_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_registration_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)

        login_title_label = ctk.CTkLabel(
            self.main_registration_frame,
            text="Erstelle dein Konto",
            font=("Manrope", 24, "bold"),
            text_color=colors.text_color
        )
        login_title_label.pack(pady=(20, 20))

        self.email_registration_entry = ctk.CTkEntry(
            self.main_registration_frame,
            placeholder_text="E-Mail",
            width=300, height=40,
            font=("Manrope", 16),
            fg_color=colors.second_button_color,
            text_color=colors.text_color,
            border_color=colors.border_color,
            border_width=1,
            corner_radius=40
        )
        self.email_registration_entry.pack(pady=10)

        self.username_registration_entry = ctk.CTkEntry(
            self.main_registration_frame,
            placeholder_text="Benutzername",
            width=300, height=40,
            font=("Manrope", 16),
            fg_color=colors.second_button_color,
            text_color=colors.text_color,
            border_color=colors.border_color,
            border_width=1,
            corner_radius=40
        )
        self.username_registration_entry.pack(pady=10)

        self.password_registration_entry_1 = ctk.CTkEntry(
            self.main_registration_frame,
            placeholder_text="Passwort",
            width=300, height=40,
            font=("Manrope", 16),
            fg_color=colors.second_button_color,
            text_color=colors.text_color,
            border_color=colors.border_color,
            border_width=1,
            corner_radius=40
        )
        self.password_registration_entry_1.pack(pady=10)

        self.password_registration_entry_2 = ctk.CTkEntry(
            self.main_registration_frame,
            placeholder_text="Passwort bestätigen",
            width=300, height=40,
            font=("Manrope", 16),
            fg_color=colors.second_button_color,
            text_color=colors.text_color,
            border_color=colors.border_color,
            border_width=1,
            corner_radius=40
        )
        self.password_registration_entry_2.pack(pady=10)

        registrate_button = ctk.CTkButton(
            self.main_registration_frame,
            text="Registrieren",
            command=self.handle_registration,
            width=300, height=40,
            font=("Manrope", 16, "bold"),
            text_color=colors.text_color,
            fg_color=colors.primary_color,
            hover_color=colors.hover_color,
            corner_radius=40
        )
        registrate_button.pack(pady=(30, 25))

        switch_to_login_tab = ctk.CTkButton(
            self.main_registration_frame,
            text="Du hast bereits ein Konto? Anmelden",
            command=self.switch_tab,
            font=("Manrope", 14),
            text_color=colors.text_color,
            fg_color="transparent",
            hover=False,
        )
        switch_to_login_tab.pack(pady=5)

        read_terms_button = ctk.CTkButton(
            self.main_registration_frame,
            text="Wenn du fortfährst, erklärst du dich mit unseren Allgemeinen\n Geschäftsbedingungen und Datenschutzerklärung einverstanden.",
            command=lambda: webbrowser.open("https://eurapass.com/terms-of-use/"),
            font=("Manrope", 10),
            text_color=colors.secondary_text_color,
            fg_color="transparent",
            hover=False,
        )
        read_terms_button.pack(pady=0)

        self.bind("<Return>", lambda event: self.handle_registration()) # Bind Enter key to registration

    def handle_login(self):
        """Handles the login process when the login button is clicked."""

        username = self.username_login_entry.get()
        password = self.password_login_entry.get()

        # Checks validity of login data
        is_valid, error_msg = self.auth_service.validate_login_data(username, password)
        if not is_valid:
            messagebox.showwarning("Eingabe fehlt", error_msg)
            return

        user = self.auth_service.authenticate_user(username, password)

        if user:
            user_id, email, username_db = user

            # Initialize user session
            session = user_session.get_session()
            session.login(
                user_id=user_id,
                master_password=password,
                username=username_db,
                email=email
            )

            self.destroy() # Close login window
            self.master.deiconify() # Show main application window

            # Refresh password overview UI after login
            if hasattr(self.master, 'password_overview_ui'):
                self.master.password_overview_ui.refresh_passwords()

        else:
            messagebox.showerror("Fehler", "Ungültiger Benutzername/E-Mail oder Passwort.")

    def handle_registration(self):
        """Handles the registration process when the register button is clicked."""

        email = self.email_registration_entry.get()
        username = self.username_registration_entry.get()
        password_1 = self.password_registration_entry_1.get()
        password_2 = self.password_registration_entry_2.get()

        # Checks validity of registration data
        is_valid, error_msg = self.auth_service.validate_registration_data(
            email, username, password_1, password_2
        )
        if not is_valid:
            messagebox.showwarning("Eingabe fehlt", error_msg)
            return

        success = self.auth_service.register_user(email, username, password_1)

        if success:
            messagebox.showinfo("Erfolg", "Du wurdest registriert!")
            self.login_tab_open = True
            self.main_login_frame.lift()
            self._clear_registration_fields()
        else:
            messagebox.showerror("Fehler", "Benutzername oder E-Mail ist bereits vergeben.")
            self.username_registration_entry.delete(0, 'end')

    def toggle_password_visibility(self):
        """Toggles the visibility of the password in the login tab."""

        show_password = self.check_show_password_checkbox_state.get()
        self.password_login_entry.configure(show="" if show_password == 1 else "*")

    def on_closing(self):
        """Handles the window close event by closing the main application."""
        self.master.destroy()
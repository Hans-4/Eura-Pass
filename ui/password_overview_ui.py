import customtkinter as ctk
import config.app as app
from services.password_service import PasswordService
from models import user_session


class PasswordOverviewUI:
    def __init__(self, master, password_service: PasswordService):
        self.master = master
        self.password_service = password_service

        self.scroll_frame = ctk.CTkScrollableFrame(
            master=master,
            width=300,
            corner_radius=0,
            border_width=1,
            border_color=app.border_color,
            fg_color=app.background_color,
        )
        self.scroll_frame.grid(column=0, row=1, sticky="nsew")

        self.passwords = []
        self.load_passwords()

    def load_passwords(self):
        try:
            session = user_session.get_session()
            if session.is_logged_in():
                user_id = session.get_user_id()
                master_password = session.get_master_password()
                self.passwords = self.password_service.get_password_overview(user_id, master_password)
            else:
                self.passwords = []
        except Exception as e:
            print(f"Fehler beim Laden der Passwörter: {e}")
            self.passwords = []

        self.display_password_cards()

    def refresh_passwords(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.load_passwords()

    def display_password_cards(self):
        for i, (title, username) in enumerate(self.passwords):
            password_frame = ctk.CTkFrame(
                self.scroll_frame,
                fg_color="transparent",
                corner_radius=0,
                border_width=1,
                border_color=app.border_color,
                width=280,
                height=100
            )
            password_frame.grid(row=i, column=0, sticky="ew")

            title_label = ctk.CTkButton(
                password_frame,
                text=title,
                font=("Manrope", 20, "bold"),
                text_color=app.secondary_text_color,
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
                text_color=app.secondary_text_color,
                width=280,
                fg_color="transparent",
                corner_radius=0,
                hover=False,
                cursor="hand2",
                command=lambda t=title, u=username: self.on_password_click(t, u)
            )
            username_label.pack(side="top", pady=(2, 10), padx=20)

    def on_password_click(self, title: str, username: str):
        self.master.show_password_details(title, username)
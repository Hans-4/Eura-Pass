import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import config.colors as colors
from services.password_service import PasswordService
from models import user_session

class AddPasswordWindow(ctk.CTkFrame):
    def __init__(self, master, password_service: PasswordService):
        super().__init__(
            master,
            fg_color=colors.background_color,
            corner_radius=0,
            border_width=1,
            border_color=colors.border_color,
            width=460
        )

        self.password_service = password_service
        self.master = master
        self.grid_propagate(False)

        self.add_window_close_icon = ctk.CTkImage(
            light_image=Image.open("assets/close_icon.png"),
            size=(15, 15)
        )

        self.grid_columnconfigure(0, weight=1)
        self.entries = []
        self.create_ui()

    def create_ui(self):
        close_button = ctk.CTkButton(
            self,
            text="",
            fg_color=colors.primary_color,
            hover_color=colors.hover_color,
            image=self.add_window_close_icon,
            width=25,
            height=25,
            corner_radius=15,
            command=self.master.toggle_add_sidebar,
        )
        close_button.grid(row=0, column=0, padx=(0, 20), pady=(27, 20), sticky="e")

        save_button = ctk.CTkButton(
            self,
            text="Login erstellen",
            font=("Manrope", 13),
            fg_color=colors.primary_color,
            hover_color=colors.hover_color,
            corner_radius=40,
            width=40,
            height=25,
            bg_color="transparent",
            command=self.handle_save
        )
        save_button.grid(row=0, column=0, padx=(25, 150), pady=(30, 20), sticky="w")

        self.input_fields = [
            "Titel",
            "E-Mail-Adresse oder Benutzername",
            "Passwort",
            "Geheimer 2FA-Schlüssel (TOTP)",
            "Webseite",
            "Notiz",
        ]

        for i, placeholder in enumerate(self.input_fields):
            entry = ctk.CTkEntry(
                self,
                placeholder_text=placeholder,
                fg_color=colors.second_button_color,
                border_color=colors.border_color,
                font=("Manrope", 16),
                border_width=1,
                corner_radius=10,
                width=420,
                height=50,
            )
            entry.grid(row=i + 1, column=0, padx=20, pady=10, sticky="ew")
            self.entries.append(entry)

    def get_input_values(self) -> dict:
        return {
            "Titel": self.entries[0].get(),
            "E-Mail-Adresse oder Benutzername": self.entries[1].get(),
            "Passwort": self.entries[2].get(),
            "Geheimer 2FA-Schlüssel (TOTP)": self.entries[3].get(),
            "Webseite": self.entries[4].get(),
            "Notiz": self.entries[5].get(),
        }

    def handle_save(self):
        values = self.get_input_values()

        is_valid, error_msg = self.password_service.validate_password_data(
            values["Titel"],
            values["Passwort"]
        )

        if not is_valid:
            messagebox.showwarning("Fehler", error_msg)
            return

        session = user_session.get_session()
        if not session.is_logged_in():
            messagebox.showerror("Fehler", "Sie sind nicht angemeldet!")
            return

        try:
            self.password_service.save_password(
                user_id=session.get_user_id(),
                title=values["Titel"],
                username=values["E-Mail-Adresse oder Benutzername"],
                password=values["Passwort"],
                master_password=session.get_master_password(),
                two_fa_key=values["Geheimer 2FA-Schlüssel (TOTP)"],
                website=values["Webseite"],
                notes=values["Notiz"]
            )

            messagebox.showinfo("Erfolg", "Passwort erfolgreich gespeichert!")
            self.clear_fields()

            if hasattr(self.master, 'password_overview_ui'):
                self.master.password_overview_ui.refresh_passwords()

        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {str(e)}")

    def clear_fields(self):
        for entry in self.entries:
            entry.delete(0, 'end')
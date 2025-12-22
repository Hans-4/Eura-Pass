import customtkinter as ctk
import config.colors as colors
from services.password_service import PasswordService
import webbrowser
import services.database
from tkinter import messagebox

class PasswordDetailsUI(ctk.CTkFrame):
    def __init__(self, master, password_service: PasswordService):
        super().__init__(
            master=master,
            fg_color=colors.background_color,
            corner_radius=0
        )
        self.password_service = password_service
        self.grid(column=1, row=1, sticky="nsew")
        self.grid_columnconfigure(0, minsize=400)

        self.current_password = None
        self.show_placeholder()

    def show_placeholder(self):
        self._clear_frame()

        placeholder_label = ctk.CTkLabel(
            self,
            text="Wähle ein Passwort aus der Liste aus",
            font=("Manrope", 16),
            text_color=colors.secondary_text_color
        )
        placeholder_label.pack(expand=True)

    def display_password_details(self, password_dict: dict):
        self._clear_frame()
        self.current_password = password_dict

        detail_container = ctk.CTkFrame(self, fg_color="transparent")
        detail_container.pack(pady=40, padx=40, fill="both", expand=True)

        ctk.CTkLabel(
            detail_container,
            text=password_dict["title"],
            font=("Manrope", 24, "bold"),
            text_color=colors.text_color
        ).pack(pady=(0, 20))

        self._create_detail_row(
            detail_container,
            "Benutzername:",
            password_dict["username"]
        )

        self._create_detail_row(
            detail_container,
            "Passwort:",
            password_dict["password"]
        )

        if password_dict.get("website"):
            self._create_detail_row(
                detail_container,
                "Website:",
                password_dict["website"],
                is_link=True
            )

        if password_dict.get("two_fa_key"):
            self._create_detail_row(
                detail_container,
                "2FA-Schlüssel:",
                password_dict["two_fa_key"]
            )

        if password_dict.get("notes"):
            ctk.CTkLabel(
                detail_container,
                text="Notizen:",
                font=("Manrope", 14, "bold"),
                text_color=colors.text_color
            ).pack(pady=(15, 5), anchor="w")

            notes_textbox = ctk.CTkTextbox(
                detail_container,
                font=("Manrope", 14),
                fg_color=colors.second_button_color,
                border_color=colors.border_color,
                border_width=1,
                height=100
            )
            notes_textbox.pack(pady=5, fill="x")
            notes_textbox.insert("1.0", password_dict["notes"])
            notes_textbox.configure(state="disabled")

        self.delete_button = ctk.CTkButton(
            detail_container,
            text="Passwort löschen",
            command=self.delete_password,
            fg_color=colors.delete_button_color,
            hover_color=colors.delete_button_hover_color,
        )
        self.delete_button.pack(pady=10)

    def _create_detail_row(self, parent, label: str, value: str, is_link: bool = False):
        row_frame = ctk.CTkFrame(parent, fg_color="transparent", bg_color=colors.background_color, border_width=1, corner_radius=15, )
        row_frame.pack(pady=5, fill="x")

        ctk.CTkLabel(
            row_frame,
            text=label,
            font=("Manrope", 14, "bold"),
            text_color=colors.text_color,
        ).pack(side="left", padx=(20,10), pady=1)

        text_color = "#3498db" if is_link else colors.text_color

        if is_link:

            link_button = ctk.CTkButton(
                row_frame,
                text=value,
                font=("Manrope", 14),
                text_color=text_color,
                fg_color=colors.background_color,
                corner_radius=0,
                hover=False,
                cursor="hand2",
                command=lambda url=value: webbrowser.open(value),
                anchor="w"
            )
            link_button.pack(side="left" , pady=1)

        else:

            textbox = ctk.CTkTextbox(
                row_frame,
                font=("Manrope", 14),
                text_color=text_color,
                height=14,
                fg_color=colors.background_color,
                corner_radius=0,
            )
            textbox.insert("1.0", value)
            textbox.pack(side="left" , pady=1)
            textbox.configure(state="disabled")

    def _clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def delete_password(self):
        if not self.current_password:
            return

        result = messagebox.askyesno(
            "Passwort löschen",
            f"Möchten Sie das Passwort für '{self.current_password['title']}' wirklich löschen?"
        )

        if result:
            password_id = self.current_password.get('id')

            if password_id:
                success = self.password_service.delete_password(password_id)

                if success:
                    messagebox.showinfo("Erfolg", "Passwort erfolgreich gelöscht")
                    self.show_placeholder()
                    if hasattr(self.master, 'password_overview_ui'):
                        self.master.password_overview_ui.refresh_passwords()
                else:
                    messagebox.showerror("Fehler", "Passwort konnte nicht gelöscht werden")

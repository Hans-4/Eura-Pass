# API
import customtkinter as ctk
import webbrowser
from tkinter import messagebox

# Services
from services.password_service import PasswordService

# Config
import config.colors as colors

class PasswordDetailsUI(ctk.CTkFrame):
    def __init__(self, master, password_service: PasswordService):
        """UI component to display detailed information about a selected password."""

        super().__init__(
            master=master,
            fg_color=colors.background_color,
            corner_radius=0
        )
        self.password_service = password_service
        self.grid(column=1, row=1, sticky="nsew")
        self.grid_columnconfigure(0, minsize=400)

        self.current_password = None # Holds the currently displayed password details
        self.show_placeholder() # Shows placeholder if no password is selected

    def show_placeholder(self):
        """Displays a placeholder message when no password is selected."""

        self._clear_frame() # Clear existing content

        placeholder_label = ctk.CTkLabel(
            self,
            text="Wähle ein Passwort aus der Liste aus",
            font=("Manrope", 16),
            text_color=colors.secondary_text_color
        )
        placeholder_label.pack(expand=True)

    def display_password_details(self, password_dict: dict):
        """
        Displays the details of the selected password.
            - Title, Username, Password don't need a check as they are mandatory
            - Website, 2FA Key, Notes are optional and displayed only if available
           """

        self._clear_frame() # Clear existing content
        self.current_password = password_dict # Store current password details

        detail_container = ctk.CTkFrame(self, fg_color="transparent")
        detail_container.pack(pady=40, padx=40, fill="both", expand=True)

        # Title
        ctk.CTkLabel(
            detail_container,
            text=password_dict["title"],
            font=("Manrope", 24, "bold"),
            text_color=colors.text_color
        ).pack(pady=(0, 20))

        # Username
        self._create_detail_row(
            detail_container,
            "Benutzername:",
            password_dict["username"]
        )

        # Password
        self._create_detail_row(
            detail_container,
            "Passwort:",
            password_dict["password"]
        )

        # Website (if available)
        if password_dict.get("website"):
            self._create_detail_row(
                detail_container,
                "Website:",
                password_dict["website"],
                is_link=True
            )

        # 2FA Key (if available)
        if password_dict.get("two_fa_key"):
            self._create_detail_row(
                detail_container,
                "2FA-Schlüssel:",
                password_dict["two_fa_key"]
            )

        # Notes (if available)
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
        """
        Sets the values to a frame and an object.
        Links get a button so that you can open the link directly with them.
        """

        row_frame = ctk.CTkFrame(parent, fg_color="transparent", bg_color=colors.background_color, border_width=1, corner_radius=15, )
        row_frame.pack(pady=5, fill="x")

        ctk.CTkLabel(
            row_frame,
            text=label,
            font=("Manrope", 14, "bold"),
            text_color=colors.text_color,
        ).pack(side="left", padx=(20,10), pady=1)

        text_color = "#3498db" if is_link else colors.text_color

        # Check if the value is a link and if true create a clickable button that opens the link in the default web browser
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
            # Using a textbox to allow easy copying values because the label doesn't support it
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
            textbox.configure(state="disabled") # Make the textbox read-only

    def _clear_frame(self):
        """Clears all widgets from the frame."""
        for widget in self.winfo_children():
            widget.destroy() # Remove each widget

    def delete_password(self):
        """Deletes the currently displayed password after user confirmation."""
        if not self.current_password:
            return

        # Ask for user confirmation before deletion
        result = messagebox.askyesno(
            "Passwort löschen",
            f"Möchten Sie das Passwort für '{self.current_password['title']}' wirklich löschen?"
        )

        # If user confirmed deletion or not
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

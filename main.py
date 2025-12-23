#API
import customtkinter as ctk
from PIL import Image

# Services
from services.database import Database
from services.auth_service import AuthService
from services.password_service import PasswordService

# UI
from ui.login_ui import LoginWindow
from ui.password_overview_ui import PasswordOverviewUI
from ui.password_details_ui import PasswordDetailsUI
from ui.add_password_ui import AddPasswordWindow

# Models
from models import user_session

# Config
import config.colors as app


class App(ctk.CTk):
    def __init__(self):
        """
        Initializes the main application window and core components.

        - Configures window properties (title, size, appearance).
        - Sets up services:
            - Database connection
            - Authentication service
            - Password management service
        - Initializes UI components:
            - Title bar and icons
            - Password overview, details, and add windows
        - Configures grid layout for responsive design.
        """
        super().__init__()

        self.title("Eura Pass") #Set window title
        self.geometry("1080x720") #Set window size
        self.minsize(1080, 600) #Set minimum window size
        ctk.set_appearance_mode("dark") #Set appearance mode
        self.configure(fg_color=app.background_color) #Set background color

        self.withdraw()

        self.database = Database()
        self.auth_service = AuthService(self.database)
        self.password_service = PasswordService(self.database)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self._create_title_bar_frame()
        self._load_icons()

        self.password_overview_ui = PasswordOverviewUI(self, self.password_service)
        self.password_details_ui = PasswordDetailsUI(self, self.password_service)
        self.add_window = AddPasswordWindow(self, self.password_service)

        self.distance_to_search_bar = 50 # Initial the default distance from title elements to search bar
        self.is_add_sidebar_open = False # State variable for add sidebar visibility

    def _create_title_bar_frame(self):
        """Creates the title bar frame for the application."""
        self.title_bar = ctk.CTkFrame(
            self,
            fg_color=app.background_color,
            corner_radius=0,
            height=90,
            border_width=1,
            border_color=app.border_color,
        )

    def _load_icons(self):
        """Loads images for various icons used in the application."""
        self.home_screen_search_bar_icon = ctk.CTkImage( # Magnifying glass icon for the search bar
            light_image=Image.open("assets/home_screen_search_bar_icon.png"),
            size=(20, 20)
        )
        self.add_button_icon = ctk.CTkImage( # Plus icon for the add password button
            light_image=Image.open("assets/plus_icon.png"),
            size=(15, 15)
        )
        self.logo_title_icon = ctk.CTkImage( # Logo icon for the title bar
            light_image=Image.open("assets/logo_title_icon.png"),
            size=(30, 30)
        )

    def create_title_bar(self):
        """Creates and configures the title bar with logo, title, search bar, and add button."""
        self.title_bar.grid(column=0, row=0, columnspan=2, sticky="nsew")

        self.title_bar.grid_columnconfigure(0, weight=0)
        self.title_bar.grid_columnconfigure(1, weight=1)
        self.title_bar.grid_columnconfigure(2, weight=1)
        self.title_bar.grid_columnconfigure(3, weight=1)
        self.title_bar.grid_columnconfigure(4, weight=0)

        logo_label = ctk.CTkLabel(
            self.title_bar,
            image=self.logo_title_icon,
            text="",
            fg_color="transparent",
        )
        logo_label.grid(row=0, column=0, padx=(50, 0), pady=(10, 10), sticky="w")

        self.app_title = ctk.CTkLabel(
            self.title_bar,
            text="Eura Pass",
            font=("Manrope", 25, "bold"),
            text_color=app.secondary_text_color,
            fg_color="transparent",
        )
        self.app_title.grid(
            row=0, column=0,
            padx=(90, self.distance_to_search_bar),
            pady=(10, 10),
            sticky="w"
        )

        self._create_search_bar()

        self.add_new_password_button = ctk.CTkButton(
            self.title_bar,
            text="Passwort hinzufügen",
            text_color=app.text_color,
            fg_color=app.primary_color,
            hover_color=app.hover_color,
            bg_color="transparent",
            image=self.add_button_icon,
            corner_radius=40,
            font=("Manrope", 13),
            command=self.toggle_add_sidebar,
        )
        self.add_new_password_button.grid(
            row=0, column=4,
            padx=(self.distance_to_search_bar, 50),
            pady=(10, 10),
            sticky="e"
        )

    def _create_search_bar(self):
        search_frame = ctk.CTkFrame(
            self.title_bar,
            fg_color=app.second_button_color,
            corner_radius=40,
            width=500,
            height=40,
        )
        search_frame.grid(row=0, column=2, pady=(10, 10))

        search_frame.grid_columnconfigure(0, weight=0)
        search_frame.grid_columnconfigure(1, weight=1)

        search_icon_label = ctk.CTkLabel(
            search_frame,
            image=self.home_screen_search_bar_icon,
            text="",
            fg_color="transparent",
            width=20,
            height=20,
        )
        search_icon_label.grid(row=0, column=0, padx=(10, 0))

        self.password_search_bar = ctk.CTkEntry(
            search_frame,
            placeholder_text="Nach Passwörtern suchen",
            placeholder_text_color=app.secondary_text_color,
            width=500,
            height=40,
            text_color=app.secondary_text_color,
            font=("Manrope", 17),
            fg_color="transparent",
            corner_radius=40,
            border_width=0,
        )
        self.password_search_bar.grid(row=0, column=1, padx=(0, 15), pady=0, sticky="ew")

    def toggle_add_sidebar(self):
        """Toggles the visibility of the add password sidebar."""
        self.is_add_sidebar_open = not self.is_add_sidebar_open

        if self.is_add_sidebar_open:
            self.add_window.place(relx=1, rely=0, relheight=1, anchor="ne")
            self.add_window.lift()
            self.password_search_bar.configure(state="disabled")
        else:
            self.add_window.place_forget()
            self.password_search_bar.configure(state="normal")

    def show_password_details(self, title: str, username: str):
        """Displays the details of a selected password."""
        session = user_session.get_session()

        if not session.is_logged_in():
            return

        master_password = session.get_master_password()
        user_id = session.get_user_id()

        all_passwords = self.password_service.load_passwords(user_id, master_password)

        selected_password = self.password_service.find_password(
            all_passwords, title, username
        )

        if selected_password:
            self.password_details_ui.display_password_details(selected_password)

    def on_resize(self, event):
        """Handles window resize events to adjust layout dynamically."""
        if event.widget != self:
            return

        width = self.winfo_width()
        height = self.winfo_height()

        if height < 100:
            return

        distance_result = max(0, width - 1080)
        self.distance_to_search_bar = 50 + distance_result / 2

        if hasattr(self, 'app_title') and self.app_title is not None:
            self.app_title.grid_configure(
                padx=(90, self.distance_to_search_bar)
            )

        if hasattr(self, 'add_new_password_button') and self.add_new_password_button is not None:
            self.add_new_password_button.grid_configure(
                padx=(self.distance_to_search_bar, 50)
            )

    def start(self):
        self.create_title_bar()
        self.bind("<Configure>", self.on_resize)

        login_window = LoginWindow(self, self.auth_service)


if __name__ == "__main__":
    app_instance = App()
    app_instance.start()
    app_instance.mainloop()
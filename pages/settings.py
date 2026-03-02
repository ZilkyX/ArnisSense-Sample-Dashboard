import customtkinter as ctk
import json
import os

SETTINGS_FILE = "settings.json"

if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        data = json.load(f)
        ctk.set_appearance_mode(data.get("theme", "System"))
else:
    ctk.set_appearance_mode("System")

ctk.set_default_color_theme("blue")


class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ctk.CTkLabel(
            self,
            text="⚙ Settings",
            font=("Arial", 32, "bold")
        ).pack(pady=(20, 10))

        theme_frame = ctk.CTkFrame(self, corner_radius=15)
        theme_frame.pack(fill="x", padx=20, pady=(10, 10))
        theme_frame.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            theme_frame,
            text="Theme",
            font=("Arial", 18, "bold")
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.theme_option = ctk.CTkOptionMenu(
            theme_frame,
            values=["Light", "Dark", "System"],
            width=150,
            command=self.change_theme
        )
        self.theme_option.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        ctk.CTkButton(
            self,
            text="Back",
            command=lambda: controller.show_page("HomePage"),
            fg_color="#4A90E2",
            hover_color="#357ABD"
        ).pack(pady=(20, 20), ipadx=20)

        self.load_theme()

    def load_theme(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                theme = data.get("theme", "System")
        else:
            theme = "System"

        self.theme_option.set(theme)

    def save_theme(self, theme):
        with open(SETTINGS_FILE, "w") as f:
            json.dump({"theme": theme}, f)

    def change_theme(self, choice):
        ctk.set_appearance_mode(choice)
        self.save_theme(choice)
import customtkinter as ctk

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ctk.CTkLabel(
            self,
            text="Settings",
            font=("Arial", 32)
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Back",
            command=lambda: controller.show_page("HomePage")
        ).pack(pady=10)

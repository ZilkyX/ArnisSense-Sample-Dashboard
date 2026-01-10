import customtkinter as ctk

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ctk.CTkLabel(
            self,
            text="Welcome",
            font=("Arial", 36, "bold")
        ).pack(pady=40)

        ctk.CTkButton(
            self,
            text="Start Match",
            font=("Arial", 24),
            command=lambda: controller.show_page("DashboardPage")
        ).pack(pady=20)

        
        ctk.CTkButton(
            self,
            text="Logs",
            font=("Arial", 24),
            command=lambda: controller.show_page("LogsPage")
        ).pack(pady=20)


        ctk.CTkButton(
            self,
            text="Settings",
            font=("Arial", 24),
            command=lambda: controller.show_page("SettingsPage")
        ).pack(pady=20)
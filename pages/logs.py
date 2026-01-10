import customtkinter as ctk

class LogsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Logs").pack(anchor=ctk.CENTER)

        ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("HomePage")).pack(anchor=ctk.CENTER)
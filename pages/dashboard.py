import customtkinter as ctk

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=1)

        self.grid_columnconfigure((0,1), weight=1)

        self.score_panel = ctk.CTkFrame(self, corner_radius=20)
        self.score_panel.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

        title = ctk.CTkLabel(
            self.score_panel,
            text="Live Dashboard",
            font=("Arial", 32)
        )
        title.pack(anchor=ctk.CENTER)

        self.card("Player 1", 1).grid(row=1, column=0, padx=10, sticky="nsew")
        self.card("Player 2", 2).grid(row=1, column=1, padx=10, sticky="nsew")

    def card(self, title, value):
        frame = ctk.CTkFrame(self, corner_radius=20)
        frame.grid_rowconfigure((0,1), weight=1)
        frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Arial", 22)
        ).grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text=str(value),
            font=("Arial", 36, "bold")
        ).grid(row=1, column=0, sticky="nsew")

        return frame


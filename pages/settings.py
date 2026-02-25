import customtkinter as ctk

class SettingsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ----------------------------
        # Page Title
        # ----------------------------
        ctk.CTkLabel(
            self,
            text="⚙ Settings",
            font=("Arial", 32, "bold")
        ).pack(pady=(20, 10))

        # ----------------------------
        # Theme Settings
        # ----------------------------
        theme_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E1E2F")
        theme_frame.pack(fill="x", padx=20, pady=(10, 10))
        theme_frame.grid_columnconfigure(0, weight=1)
        theme_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(theme_frame, text="Theme", font=("Arial", 18, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.theme_option = ctk.CTkOptionMenu(theme_frame, values=["Light", "Dark", "System"], width=150)
        self.theme_option.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        # ----------------------------
        # Match Settings
        # ----------------------------
        match_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E1E2F")
        match_frame.pack(fill="x", padx=20, pady=(10, 10))
        match_frame.grid_columnconfigure((0,1), weight=1)

        ctk.CTkLabel(match_frame, text="Default Match Rounds", font=("Arial", 18, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.rounds_entry = ctk.CTkEntry(match_frame, placeholder_text="e.g. 5")
        self.rounds_entry.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        ctk.CTkLabel(match_frame, text="Default Match Type", font=("Arial", 18, "bold")).grid(row=1, column=0, sticky="w", padx=10, pady=10)
        self.match_type_entry = ctk.CTkEntry(match_frame, placeholder_text="e.g. Standard")
        self.match_type_entry.grid(row=1, column=1, sticky="e", padx=10, pady=10)

        # ----------------------------
        # Database / Backup Settings
        # ----------------------------
        db_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E1E2F")
        db_frame.pack(fill="x", padx=20, pady=(10, 10))
        db_frame.grid_columnconfigure((0,1), weight=1)

        ctk.CTkLabel(db_frame, text="Database Backup Path", font=("Arial", 18, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=10)
        self.db_entry = ctk.CTkEntry(db_frame, placeholder_text="e.g. C:/backup/")
        self.db_entry.grid(row=0, column=1, sticky="e", padx=10, pady=10)

        self.backup_btn = ctk.CTkButton(db_frame, text="Backup Now", fg_color="#4A90E2", hover_color="#357ABD")
        self.backup_btn.grid(row=1, column=0, columnspan=2, pady=(10, 15), padx=10, sticky="ew")

        # ----------------------------
        # Reset / Restore Defaults
        # ----------------------------
        reset_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="#1E1E2F")
        reset_frame.pack(fill="x", padx=20, pady=(10, 10))
        reset_frame.grid_columnconfigure((0,1), weight=1)

        self.reset_btn = ctk.CTkButton(reset_frame, text="Reset Settings", fg_color="#E24A4A", hover_color="#B73737")
        self.reset_btn.grid(row=0, column=0, padx=10, pady=15, sticky="ew")

        self.restore_btn = ctk.CTkButton(reset_frame, text="Restore Defaults", fg_color="#FFD700", hover_color="#FFC107")
        self.restore_btn.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        # ----------------------------
        # Back Button
        # ----------------------------
        ctk.CTkButton(
            self,
            text="Back",
            command=lambda: controller.show_page("HomePage"),
            fg_color="#4A90E2",
            hover_color="#357ABD"
        ).pack(pady=(10, 20), ipadx=20)

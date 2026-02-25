import customtkinter as ctk
from tkinter import ttk

class LogsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # ----------------------------
        # Page Header
        # ----------------------------
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 10), padx=20)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(header_frame, text="📊 Match Logs", font=("Arial", 24, "bold")).grid(row=0, column=0, sticky="w")
        self.total_matches_label = ctk.CTkLabel(header_frame, text="Total Matches: 0", font=("Arial", 16))
        self.total_matches_label.grid(row=0, column=1, sticky="e")

        # ----------------------------
        # Filters
        # ----------------------------
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(0, 10), padx=20)
        filter_frame.grid_columnconfigure((0,1,2,3), weight=1)

        self.search_entry = ctk.CTkEntry(filter_frame, placeholder_text="Search Player / Team")
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=5)

        self.date_entry = ctk.CTkEntry(filter_frame, placeholder_text="Date (YYYY-MM-DD)")
        self.date_entry.grid(row=0, column=1, sticky="ew", padx=5)

        self.type_entry = ctk.CTkEntry(filter_frame, placeholder_text="Match Type")
        self.type_entry.grid(row=0, column=2, sticky="ew", padx=5)

        self.apply_btn = ctk.CTkButton(filter_frame, text="Apply", width=80)
        self.apply_btn.grid(row=0, column=3, sticky="ew", padx=5)

        # ----------------------------
        # Table Frame
        # ----------------------------
        table_frame = ctk.CTkFrame(self, fg_color="#1E1E2F", corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        columns = ["Match ID", "Date", "Player 1", "Player 2", "Score", "Winner", "Type", "View"]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#2B2B2B",
                        foreground="#FFFFFF",
                        rowheight=30,
                        fieldbackground="#2B2B2B",
                        font=("Arial", 12))
        style.configure("Treeview.Heading",
                        font=("Arial", 12, "bold"),
                        background="#3B3B3B",
                        foreground="#FFFFFF")
        style.map("Treeview",
                  background=[('selected', '#4A90E2')],
                  foreground=[('selected', '#FFFFFF')])

        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=100 if col != "View" else 60)

        # ----------------------------
        # Bottom Action Buttons
        # ----------------------------
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.pack(fill="x", pady=10, padx=20)
        action_frame.grid_columnconfigure((0,1,2,3), weight=1)

        ctk.CTkButton(action_frame, text="Export CSV").grid(row=0, column=0, padx=5, sticky="ew")
        ctk.CTkButton(action_frame, text="Backup").grid(row=0, column=1, padx=5, sticky="ew")
        ctk.CTkButton(action_frame, text="Delete Selected").grid(row=0, column=2, padx=5, sticky="ew")
        ctk.CTkButton(action_frame, text="Refresh").grid(row=0, column=3, padx=5, sticky="ew")

        # ----------------------------
        # Back Button
        # ----------------------------
        back_btn = ctk.CTkButton(self, text="Back", command=lambda: controller.show_page("HomePage"))
        back_btn.pack(pady=10)

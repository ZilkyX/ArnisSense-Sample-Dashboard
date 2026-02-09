import customtkinter as ctk
from tkinter import ttk

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.scores = [0, 0]
        self.playing = False
        self.timer_seconds = 0

        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_columnconfigure((0, 1), weight=1)

        self.details_panel = ctk.CTkFrame(self, corner_radius=20, fg_color="#1E1E2F")
        self.details_panel.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=(20, 10))
        self.details_panel.grid_columnconfigure(0, weight=1)
        self.details_panel.grid_columnconfigure(1, weight=1)
        self.details_panel.grid_columnconfigure(2, weight=1)

        self.player1_info = ctk.CTkLabel(self.details_panel, text="Player 1: --", font=("Arial", 16), text_color="#4A90E2")
        self.player1_info.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 5))

        self.rounds_label = ctk.CTkLabel(self.details_panel, text="Round --", font=("Arial", 24, "bold"), text_color="#FFFFFF")
        self.rounds_label.grid(row=0, column=1, sticky="nsew")

        self.timer_label = ctk.CTkLabel(self.details_panel, text="00:00", font=("Arial", 18, "bold"), text_color="#FFD700")
        self.timer_label.grid(row=1, column=1, sticky="n", pady=(0, 10))

        self.player2_info = ctk.CTkLabel(self.details_panel, text="Player 2: --", font=("Arial", 16), text_color="#E24A4A")
        self.player2_info.grid(row=0, column=2, sticky="e", padx=20, pady=(10, 5))

        button_frame = ctk.CTkFrame(self.details_panel, fg_color="transparent")
        button_frame.grid(row=3, column=0, columnspan=3, pady=(0, 10))
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.play_pause_btn = ctk.CTkButton(button_frame, text="Play", command=self.toggle_timer,
                                            fg_color="#4A90E2", hover_color="#357ABD", font=("Arial", 16, "bold"),
                                            corner_radius=12)
        self.play_pause_btn.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.reset_btn = ctk.CTkButton(button_frame, text="Reset Timer", command=self.reset_timer,
                                       fg_color="#F39C12", hover_color="#D68910", font=("Arial", 16, "bold"),
                                       corner_radius=12)
        self.reset_btn.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.end_game_btn = ctk.CTkButton(button_frame, text="End Game", command=self.end_game,
                                          fg_color="#E24A4A", hover_color="#B73737", font=("Arial", 16, "bold"),
                                          corner_radius=12)
        self.end_game_btn.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        table_frame = ctk.CTkFrame(self.details_panel, corner_radius=15, fg_color="transparent")
        table_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=20, pady=(10, 15))
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self.num_rounds = 5 
        columns = ["Player"] + [f"R{i+1}" for i in range(self.num_rounds)]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=2)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2B2B2B", foreground="#FFFFFF", rowheight=40,
                        fieldbackground="#2B2B2B", font=("Arial", 14))
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"), background="#3B3B3B", foreground="#FFFFFF")
        style.map("Treeview", background=[('selected', '#4A90E2')], foreground=[('selected', '#FFFFFF')])

        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=80 if col != "Player" else 120)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.player1_card = self.create_card("Player 1", 0, "#2B2B2B", "#4A90E2")
        self.player1_card.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=(0, 20))

        self.player2_card = self.create_card("Player 2", 0, "#2B2B2B", "#E24A4A")
        self.player2_card.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=(0, 20))

    def create_card(self, title, value, bg_color, accent_color):
        frame = ctk.CTkFrame(self, corner_radius=20, fg_color=bg_color)
        frame.grid_rowconfigure((0,1), weight=1)
        frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(frame, text=title, font=("Arial", 20, "bold"), text_color=accent_color).grid(row=0, column=0, sticky="nsew", pady=(15,0))
        frame.score_label = ctk.CTkLabel(frame, text=str(value), font=("Arial", 48, "bold"), text_color="#FFFFFF")
        frame.score_label.grid(row=1, column=0, sticky="nsew", pady=(10,15))
        return frame

    def refresh_match_data(self):
        md = self.controller.match_data
        self.player1_info.configure(text=f"Player 1: {md.get('player1_team_name','--')}")
        self.player2_info.configure(text=f"Player 2: {md.get('player2_team_name','--')}")
        self.rounds_label.configure(text=f"Round 1 / {md.get('no_of_rounds', 5)}")
        self.num_rounds = int(md.get('no_of_rounds', 5))

        cols = ["Player"] + [f"R{i+1}" for i in range(self.num_rounds)]
        self.tree.config(columns=cols)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=80 if col != "Player" else 120)

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.scores = [0, 0]
        self.tree.insert("", "end", values=[md.get('player1','Player 1')]+[""]*self.num_rounds, tags=("player1",))
        self.tree.insert("", "end", values=[md.get('player2','Player 2')]+[""]*self.num_rounds, tags=("player2",))
        self.tree.tag_configure("player1", foreground="#4A90E2")
        self.tree.tag_configure("player2", foreground="#E24A4A")

        self.player1_card.score_label.configure(text="0")
        self.player2_card.score_label.configure(text="0")

    def toggle_timer(self):
        self.playing = not self.playing
        self.play_pause_btn.configure(text="Pause" if self.playing else "Play")
        if self.playing:
            self.update_timer_label()

    def reset_timer(self):
        self.timer_seconds = 0
        self.update_timer_label()

    def end_game(self):
        self.playing = False
        self.play_pause_btn.configure(text="Play")

    def update_timer_label(self):
        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
        if self.playing:
            self.timer_seconds += 1
            self.after(1000, self.update_timer_label)

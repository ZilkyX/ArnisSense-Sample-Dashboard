import customtkinter as ctk
from tkinter import ttk
from database.database_handler.db_handler import DatabaseHandler


class MatchDetailsPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.db = DatabaseHandler()

        self.match_id = None

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=15)

        self.title_label = ctk.CTkLabel(
            header,
            text="Match Details",
            font=("Arial", 26, "bold")
        )
        self.title_label.pack(side="left")

        ctk.CTkButton(
            header,
            text="← Back",
            width=90,
            command=lambda: controller.show_page("LogsPage")
        ).pack(side="right")

        # Info Panel
        self.info_panel = ctk.CTkFrame(self, corner_radius=15)
        self.info_panel.pack(fill="x", padx=20, pady=10)

        self.info_text = ctk.CTkLabel(
            self.info_panel,
            text="Match Information",
            font=("Arial", 16)
        )
        self.info_text.pack(pady=15)

        # Round Table Panel
        table_frame = ctk.CTkFrame(self, corner_radius=15)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ["Round", "Player 1 Score", "Player 2 Score", "Winner"]

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#252525",
            foreground="white",
            rowheight=35,
            fieldbackground="#252525"
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 12, "bold"),
            background="#1f1f1f",
            foreground="white"
        )

        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(fill="both", expand=True, padx=15, pady=15)

    # ------------------------------------------------
    # Load Match Details
    # ------------------------------------------------

    def load_match(self, match_id):

        self.match_id = match_id

        match = self.db.conn.execute(
            "SELECT * FROM Matches WHERE MatchID=?",
            (match_id,)
        ).fetchone()

        if not match:
            return

        self.title_label.configure(
            text=f"Match Details — ID {match_id}"
        )

        # Match summary
        self.info_text.configure(
            text=f"""
Player 1: {match['Player1Name']} ({match['Player1Team']})
Player 2: {match['Player2Name']} ({match['Player2Team']})
Match Type: {match['MatchType']}
Rounds: {match['NumberOfRounds']}
Date: {str(match['CreatedAt'])[:10]}
"""
        )

        # Load rounds
        self.refresh_round_table()

    # ------------------------------------------------

    def refresh_round_table(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        rounds = self.db.get_rounds(self.match_id)

        for r in rounds:

            p1 = r["Player1Score"] or 0
            p2 = r["Player2Score"] or 0

            if p1 == 0 and p2 == 0:
                winner = ""
            else:
                if p1 > p2:
                    winner = "Player 1"
                elif p2 > p1:
                    winner = "Player 2"
                else:
                    winner = "Draw"

            self.tree.insert(
                "",
                "end",
                values=[
                    f"Round {r['RoundNumber']}",
                    p1,
                    p2,
                    winner
                ]
            )
import customtkinter as ctk
from tkinter import ttk
from tkcalendar import Calendar
from database.database_handler.db_handler import DatabaseHandler

class LogsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        self.db = DatabaseHandler()

        # -------------------------
        # MAIN CONTAINER (Compact)
        # -------------------------
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # -------------------------
        # HEADER
        # -------------------------
        header = ctk.CTkFrame(main_frame, fg_color="transparent")
        header.pack(fill="x", pady=3)

        left = ctk.CTkFrame(header, fg_color="transparent")
        left.pack(side="left")

        ctk.CTkButton(
            left,
            text="←",
            width=32,
            height=28,
            font=("Arial", 14, "bold"),
            command=lambda: controller.show_page("HomePage")
        ).pack(side="left")

        ctk.CTkLabel(
            left,
            text="Match Logs",
            font=("Arial", 18, "bold")
        ).pack(side="left", padx=8)

        self.total_matches_label = ctk.CTkLabel(
            header,
            text="Total Matches: 0",
            font=("Arial", 13),
            text_color="gray"
        )
        self.total_matches_label.pack(side="right")

        # -------------------------
        # FILTER BAR (Single Row Compact)
        # -------------------------
        filter_card = ctk.CTkFrame(main_frame, corner_radius=10)
        filter_card.pack(fill="x", pady=5)

        filter_inner = ctk.CTkFrame(filter_card, fg_color="transparent")
        filter_inner.pack(fill="x", padx=10, pady=8)

        filter_inner.grid_columnconfigure((0,1,2), weight=1)

        self.search_entry = ctk.CTkEntry(
            filter_inner,
            placeholder_text="Search Player / Team"
        )
        self.search_entry.grid(row=0, column=0, padx=5, sticky="ew")

        date_frame = ctk.CTkFrame(filter_inner, fg_color="transparent")
        date_frame.grid(row=0, column=1, padx=5, sticky="ew")
        date_frame.grid_columnconfigure(0, weight=1)

        self.date_entry = ctk.CTkEntry(
            date_frame,
            placeholder_text="Date",
            state="readonly"
        )
        self.date_entry.grid(row=0, column=0, sticky="ew")

        ctk.CTkButton(
            date_frame,
            text="📅",
            width=32,
            command=self.open_calendar
        ).grid(row=0, column=1, padx=3)

        ctk.CTkButton(
            filter_inner,
            text="Apply Filter",
            height=30,
            command=self.apply_filter
        ).grid(row=0, column=2, padx=5, sticky="ew")

        # -------------------------
        # TABLE AREA
        # -------------------------
        table_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        table_frame.pack(fill="both", expand=True, pady=5)

        columns = ["Match ID", "Date", "Player 1", "Player 2", "Score", "Winner", "Type"]

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=4
        )

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#252525",
            foreground="white",
            rowheight=20,
            fieldbackground="#252525",
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold"),
            background="#1f1f1f",
            foreground="white"
        )

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, anchor="center", width=90)

        # -------------------------
        # ACTION BAR
        # -------------------------
        action = ctk.CTkFrame(main_frame, fg_color="transparent")
        action.pack(fill="x", pady=5)

        action.grid_columnconfigure((0), weight=1)

        ctk.CTkButton(
            action,
            text="Delete Selected",
            height=32,
            fg_color="#C0392B",
            hover_color="#A93226"
        ).grid(row=0, column=0, padx=5, sticky="ew")

        self.load_logs()
        self.tree.bind("<Double-1>", self.on_tree_double_click)

    # -------------------------
    # LOGIC FUNCTIONS
    # -------------------------
    def on_tree_double_click(self, event):

        selected = self.tree.selection()

        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item["values"]

        match_id = values[0]

        # Navigate to details page
        details_page = self.controller.pages["MatchDetailsPage"]
        details_page.load_match(match_id)

        self.controller.show_page("MatchDetailsPage")

    def apply_filter(self):

        keyword = self.search_entry.get().strip()
        date = self.date_entry.get().strip()

        if keyword == "":
            keyword = None

        if date == "":
            date = None

        matches = self.db.filter_matches(keyword, date)

        self.refresh_table(matches)

    def load_logs(self):

        if not hasattr(self, "tree"):
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        matches = self.db.get_matches()

        total = 0

        for match in matches:

            match_id = match["MatchID"]
            date = match["CreatedAt"]

            player1 = match["Player1Name"]
            player2 = match["Player2Name"]

            score_row = self.db.get_final_score(match_id)

            p1 = score_row["P1"] or 0 if score_row else 0
            p2 = score_row["P2"] or 0 if score_row else 0

            if p1 == 0 and p2 == 0:
                score = ""
                winner = ""
            else:
                score = f"{p1}-{p2}"

                if p1 > p2:
                    winner = "Player 1"
                elif p2 > p1:
                    winner = "Player 2"
                else:
                    winner = "Draw"

            match_type = match["MatchType"]

            self.tree.insert(
                "",
                "end",
                values=[
                    match_id,
                    str(date)[:10],
                    player1,
                    player2,
                    score,
                    winner,
                    match_type
                ]
            )

            total += 1

        self.total_matches_label.configure(
            text=f"Total Matches: {total}"
        )

    def open_calendar(self):

        self.calendar_window = ctk.CTkToplevel(self)
        self.calendar_window.title("Select Date")
        self.calendar_window.geometry("260x300")
        self.calendar_window.grab_set()

        self.calendar = Calendar(
            self.calendar_window,
            selectmode="day",
            date_pattern="yyyy-mm-dd"
        )
        self.calendar.pack(pady=15)

        ctk.CTkButton(
            self.calendar_window,
            text="Select",
            command=self.get_date,
            height=30
        ).pack()

    def get_date(self):
        selected = self.calendar.get_date()

        self.date_entry.configure(state="normal")
        self.date_entry.delete(0, "end")
        self.date_entry.insert(0, selected)
        self.date_entry.configure(state="readonly")

        self.calendar_window.destroy()

    def refresh_table(self, matches):

        for row in self.tree.get_children():
            self.tree.delete(row)

        total = 0

        for match in matches:

            match_id = match["MatchID"]
            date = match["CreatedAt"]

            player1 = match["Player1Name"]
            player2 = match["Player2Name"]

            score_row = self.db.get_final_score(match_id)

            p1 = score_row["P1"] or 0 if score_row else 0
            p2 = score_row["P2"] or 0 if score_row else 0

            if p1 == 0 and p2 == 0:
                score = ""
                winner = ""
            else:
                score = f"{p1}-{p2}"

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
                    match_id,
                    str(date)[:10],
                    player1,
                    player2,
                    score,
                    winner,
                    match["MatchType"]
                ]
            )

            total += 1

        self.total_matches_label.configure(
            text=f"Total Matches: {total}"
        )
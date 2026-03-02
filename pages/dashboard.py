import customtkinter as ctk
from PIL import Image


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.scores = [3, 2]
        self.playing = False
        self.timer_seconds = 0
        self.round_number = 1

        self.card_images = {}
        self.score_frames = [[], []]

        self._build_layout()

        self.update_score_display()

    def _build_layout(self):

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.details_panel = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color="#1E1E2F"
        )

        self.details_panel.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=10,
            pady=10
        )

        for i in range(3):
            self.details_panel.grid_columnconfigure(i, weight=1)

        self.player1_info = ctk.CTkLabel(
            self.details_panel,
            text="Player 1: --",
            font=("Arial", 16),
            text_color="#4A90E2"
        )
        self.player1_info.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        self.rounds_label = ctk.CTkLabel(
            self.details_panel,
            text="Round: 1/5",
            font=("Arial", 24, "bold")
        )
        self.rounds_label.grid(row=0, column=1)

        self.timer_label = ctk.CTkLabel(
            self.details_panel,
            text="00:00",
            font=("Arial", 18, "bold"),
            text_color="#FFD700"
        )
        self.timer_label.grid(row=1, column=1)

        self.player2_info = ctk.CTkLabel(
            self.details_panel,
            text="Player 2: --",
            font=("Arial", 16),
            text_color="#E24A4A"
        )
        self.player2_info.grid(row=0, column=2, padx=20, pady=10, sticky="e")

        self._create_score_boxes(self.details_panel, 0)
        self._create_score_boxes(self.details_panel, 1)

        self.player1_card = self.create_card(
            "assets/body_parts/Whole.png", 1, 0
        )

        self.player2_card = self.create_card(
            "assets/body_parts/Whole.png", 1, 1
        )

        self.change_hitpoint(0, "RighHand_Hit")
    def _create_score_boxes(self, parent, player_index):

        holder = ctk.CTkFrame(parent, fg_color="transparent")

        column_map = [0, 2]

        holder.grid(
            row=1,
            column=column_map[player_index],
            pady=5,
            sticky="n"
        )

        parent.grid_columnconfigure(column_map[player_index], weight=1)

        boxes = []

        for _ in range(5):

            box = ctk.CTkLabel(
                holder,
                text="",
                width=32,
                height=32,
                corner_radius=6,
                fg_color="#2B2B2B"
            )

            box.pack(side="left", padx=3)
            boxes.append(box)

        self.score_frames[player_index] = boxes

    def create_card(self, file_path, row, column):

        frame = ctk.CTkFrame(
            self,
            corner_radius=20,
            fg_color="#FFFFFF"
        )

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        img = ctk.CTkImage(
            Image.open(file_path),
            Image.open(file_path),
            size=(180, 220)
        )

        label = ctk.CTkLabel(frame, image=img, text="")
        label.image = img
        label.grid(pady=15)

        self.card_images[file_path] = img

        frame.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=10,
            pady=10
        )

        return frame

    def update_timer_label(self):

        minutes = self.timer_seconds // 60
        seconds = self.timer_seconds % 60

        self.timer_label.configure(
            text=f"{minutes:02d}:{seconds:02d}"
        )

        if self.playing:
            self.timer_seconds += 1
            self.after(1000, self.update_timer_label)

    def refresh_match_data(self):

        data = self.controller.match_data

        self.player1_info.configure(
            text=f"Player 1: {data.get('player1','--')} | "
                 f"{data.get('player1_team_name','--')}"
        )

        self.player2_info.configure(
            text=f"Player 2: {data.get('player2','--')} | "
                 f"{data.get('player2_team_name','--')}"
        )

    def add_score(self, player_index):

        if player_index not in [0, 1]:
            return

        if self.scores[player_index] >= 5:
            return

        self.scores[player_index] += 1
        self.update_score_display()

    def update_score_display(self):

        for player_index in range(2):

            score = self.scores[player_index]
            boxes = self.score_frames[player_index]

            for i, box in enumerate(boxes):

                box.configure(
                    fg_color="#FFD700" if i < score else "#2B2B2B"
                )

    def change_hitpoint(self, player_index, body_part="Whole"):

        try:
            path = f"assets/body_parts/{body_part}.png"

            img = ctk.CTkImage(
                Image.open(path),
                Image.open(path),
                size=(190, 220)
            )

            target_card = (
                self.player1_card if player_index == 0
                else self.player2_card
            )

            for widget in target_card.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(image=img)
                    widget.image = img

            self.card_images[path] = img

        except Exception as e:
            print("Hit image update error:", e)
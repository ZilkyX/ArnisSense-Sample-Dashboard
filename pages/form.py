import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from datetime import datetime
from PIL import Image

class FormPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller
        today = datetime.now().strftime("%B %d, %Y")

        scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True)
        # ================= HEADER WITH CENTERED LOGO =================
        header_frame = ctk.CTkFrame(scrollable_frame, fg_color="transparent")
        header_frame.pack(pady=(20, 15), fill="x")

        # Create inner frame to truly center content
        center_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        center_frame.pack(anchor="center")

        # Configure grid inside center frame
        center_frame.grid_columnconfigure(1, weight=1)

        # Load Logo
        logo_image = ctk.CTkImage(
            light_image=Image.open("assets/logo/Arnisense_Logo-removebg-preview.png"),
            dark_image=Image.open("assets/logo/Arnisense_Logo-removebg-preview.png"),
            size=(70, 70)
        )

        logo_label = ctk.CTkLabel(
            center_frame,
            image=logo_image,
            text=""
        )
        logo_label.grid(row=0, column=0, rowspan=2, padx=(0, 15))

        # Title
        title_label = ctk.CTkLabel(
            center_frame,
            text="ARNIS MATCH REGISTRATION",
            font=("Segoe UI", 24, "bold")
        )
        title_label.grid(row=0, column=1)

        subtitle_label = ctk.CTkLabel(
            center_frame,
            text="Official Match Setup Form",
            font=("Segoe UI", 12),
            text_color="gray60"
        )
        subtitle_label.grid(row=1, column=1)

        container = ctk.CTkFrame(scrollable_frame, corner_radius=12)
        container.pack(padx=40, pady=10, fill="both", expand=True)

        match_frame = ctk.CTkFrame(container, corner_radius=10)
        match_frame.pack(padx=20, pady=15, fill="x")

        for i in range(4):
            match_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(
            match_frame,
            text="Match Information",
            font=("Segoe UI", 15, "bold")
        ).grid(row=0, column=0, columnspan=4, pady=(10, 12))

        ctk.CTkLabel(match_frame, text="Match ID", font=("Segoe UI", 12)).grid(
            row=1, column=0, sticky="w", padx=15
        )

        self.match_id = ctk.CTkEntry(
            match_frame,
            height=32,
            placeholder_text="Enter match ID (e.g. M-001)"
        )
        self.match_id.grid(
            row=2, column=0, padx=15, pady=(3, 12), sticky="ew"
        )

        ctk.CTkLabel(match_frame, text="Date", font=("Segoe UI", 12)).grid(
            row=1, column=2, sticky="w", padx=15
        )

        ctk.CTkLabel(
            match_frame,
            text=today,
            font=("Segoe UI", 12, "bold")
        ).grid(
            row=2, column=2, padx=15, pady=(3, 12), sticky="w"
        )

        p1_frame = ctk.CTkFrame(container, corner_radius=10)
        p1_frame.pack(padx=20, pady=10, fill="x")

        for i in range(4):
            p1_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(
            p1_frame,
            text="Player 1 (Red Corner)",
            font=("Segoe UI", 15, "bold"),
            text_color="#e53935"
        ).grid(row=0, column=0, columnspan=4, pady=(10, 12))

        ctk.CTkLabel(p1_frame, text="Full Name", font=("Segoe UI", 12)).grid(
            row=1, column=0, sticky="w", padx=15
        )

        self.p1_name = ctk.CTkEntry(
            p1_frame,
            height=32,
            placeholder_text="e.g. Juan Dela Cruz"
        )
        self.p1_name.grid(
            row=2, column=0, padx=15, pady=(3, 12), sticky="ew"
        )

        ctk.CTkLabel(p1_frame, text="School / Team", font=("Segoe UI", 12)).grid(
            row=1, column=2, sticky="w", padx=15
        )

        self.p1_team = ctk.CTkEntry(
            p1_frame,
            height=32,
            placeholder_text="e.g. Manila Arnis Club"
        )
        self.p1_team.grid(
            row=2, column=2, padx=15, pady=(3, 12), sticky="ew"
        )

        # =====================================================
        # ================= PLAYER 2 ==========================
        # =====================================================

        p2_frame = ctk.CTkFrame(container, corner_radius=10)
        p2_frame.pack(padx=20, pady=10, fill="x")

        for i in range(4):
            p2_frame.grid_columnconfigure(i, weight=1)

        ctk.CTkLabel(
            p2_frame,
            text="Player 2 (Blue Corner)",
            font=("Segoe UI", 15, "bold"),
            text_color="#1e88e5"
        ).grid(row=0, column=0, columnspan=4, pady=(10, 12))

        ctk.CTkLabel(p2_frame, text="Full Name", font=("Segoe UI", 12)).grid(
            row=1, column=0, sticky="w", padx=15
        )

        self.p2_name = ctk.CTkEntry(
            p2_frame,
            height=32,
            placeholder_text="e.g. Pedro Santos"
        )
        self.p2_name.grid(
            row=2, column=0, padx=15, pady=(3, 12), sticky="ew"
        )

        ctk.CTkLabel(p2_frame, text="School / Team", font=("Segoe UI", 12)).grid(
            row=1, column=2, sticky="w", padx=15
        )

        self.p2_team = ctk.CTkEntry(
            p2_frame,
            height=32,
            placeholder_text="e.g. Cebu Warriors"
        )
        self.p2_team.grid(
            row=2, column=2, padx=15, pady=(3, 12), sticky="ew"
        )


        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(pady=20)

        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start Match",
            width=180,
            height=40,
            font=("Segoe UI", 13, "bold"),
            corner_radius=10,    
            command=self.confirm_match   
        )
        self.start_button.grid(row=0, column=0, padx=10)

        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="Cancel",
            width=150,
            height=40,
            font=("Segoe UI", 12),
            fg_color="#444",
            hover_color="#2a2a2a",
            corner_radius=10,
            command=self.cancel
        )
        self.cancel_button.grid(row=0, column=1, padx=10)


    def confirm_match(self):
        data = self.controller.match_data

        # Get values from entries
        data["match_id"] = self.match_id.get().strip()
        data["player1"] = self.p1_name.get().strip()
        data["player1_team_name"] = self.p1_team.get().strip()
        data["player2"] = self.p2_name.get().strip()
        data["player2_team_name"] = self.p2_team.get().strip()

        if not all(data.values()):
            CTkMessagebox(
                title="Error",
                message="Please fill in all fields!",
                icon="warning"
            )
            return

        confirm = CTkMessagebox(
            title="Confirm",
            message="Are you sure you want to continue?\n\nTake note: All the data entered will be saved in the database.",
            icon="question",
            option_1="Yes",
            option_2="No"
        )

        if confirm.get() != "Yes":
            return

        print(data)

        self.controller.show_page("DashboardPage")
        self.controller.pages["DashboardPage"].refresh_match_data()

        self.reset_match_data()

    def cancel(self):
        self.controller.show_page("HomePage")

    def reset_match_data(self):

        for key in self.controller.match_data:
            self.controller.match_data[key] = ""
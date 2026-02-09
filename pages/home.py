import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox


class HomePage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        main_frame = ctk.CTkFrame(
            self,
            corner_radius=20
        )
        main_frame.pack(
            pady=80,
            padx=100,
            fill="both",
            expand=True
        )

        try:
            logo_img = ctk.CTkImage(
                Image.open("assets/logo/Arnisense_Logo-removebg-preview.png"),
                size=(120, 120)
            )

            ctk.CTkLabel(
                main_frame,
                image=logo_img,
                text=""
            ).pack(pady=(30, 10))

            self.logo_img = logo_img

        except:
            ctk.CTkLabel(
                main_frame,
                text="🎮",
                font=("Arial", 60)
            ).pack(pady=(30, 10))

        ctk.CTkLabel(
            main_frame,
            text="ArniSense",
            font=("Arial", 36, "bold")
        ).pack(pady=(10, 5))

        btn_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        btn_frame.pack(pady=20)

        ctk.CTkButton(
            btn_frame,
            text="▶ Start Match",
            font=("Arial", 20, "bold"),
            width=260,
            height=50,
            corner_radius=12,
            command=self.open_form_popup
        ).pack(pady=10)

        ctk.CTkButton(
            btn_frame,
            text="📄 View Logs",
            font=("Arial", 16),
            width=220,
            height=40,
            corner_radius=10,
            fg_color="#2B2B2B",
            hover_color="#3A3A3A",
            command=lambda: controller.show_page("LogsPage")
        ).pack(pady=8)

        ctk.CTkButton(
            btn_frame,
            text="⚙ Settings",
            font=("Arial", 16),
            width=220,
            height=40,
            corner_radius=10,
            fg_color="#2B2B2B",
            hover_color="#3A3A3A",
            command=lambda: controller.show_page("SettingsPage")
        ).pack(pady=8)

        ctk.CTkLabel(
            main_frame,
            text="© 2026 ArniSense",
            font=("Arial", 12),
            text_color="gray"
        ).pack(pady=(25, 15))

    def reset_match_data(self):

        for key in self.controller.match_data:
            self.controller.match_data[key] = ""

    def open_form_popup(self):

        popup = ctk.CTkToplevel(self)
        popup.title("Match Setup")
        popup.geometry("520x450")

        popup.grab_set()

        ctk.CTkLabel(
            popup,
            text="Enter Match Details",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        match_frame = ctk.CTkFrame(popup, fg_color="transparent")
        match_frame.pack(pady=(0, 20), padx=20, fill="x")

        ctk.CTkLabel(match_frame, text="Type of Match", font=("Arial", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10)
        type_option = ctk.CTkOptionMenu(
            match_frame,
            values=["Sparring", "Forms", "Team Match"],
            width=180
        )
        type_option.grid(row=1, column=0, padx=10, pady=5)

        ctk.CTkLabel(match_frame, text=f"Number of Rounds", font=("Arial", 14, "bold")).grid(row=0, column=1, sticky="w", padx=10)
        rounds_value_label = ctk.CTkLabel(match_frame, text="3", font=("Arial", 20, "bold"))
        rounds_value_label.grid(row=0, column=2, sticky="w", padx=10)

        rounds_slider = ctk.CTkSlider(
            match_frame,
            from_=1,
            to=10,
            number_of_steps=9,
            width=180,
            command=lambda value: rounds_value_label.configure(text=str(int(value)))
        )
        rounds_slider.set(3)
        rounds_slider.grid(row=1, column=1, padx=10, pady=5)

        main_frame = ctk.CTkFrame(popup, fg_color="transparent")
        main_frame.pack(padx=20, pady=10, fill="both")

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        p1_frame = ctk.CTkFrame(main_frame)
        p1_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            p1_frame,
            text="Player 1",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        ctk.CTkLabel(p1_frame, text="Team").pack()
        p1_team_entry = ctk.CTkEntry(p1_frame, width=200)
        p1_team_entry.pack(pady=5)

        ctk.CTkLabel(p1_frame, text="Name").pack(pady=(10, 0))
        p1_entry = ctk.CTkEntry(p1_frame, width=200)
        p1_entry.pack(pady=10)

        p2_frame = ctk.CTkFrame(main_frame)
        p2_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(
            p2_frame,
            text="Player 2",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        ctk.CTkLabel(p2_frame, text="Team").pack()
        p2_team_entry = ctk.CTkEntry(p2_frame, width=200)
        p2_team_entry.pack(pady=5)

        ctk.CTkLabel(p2_frame, text="Name").pack(pady=(10, 0))
        p2_entry = ctk.CTkEntry(p2_frame, width=200)
        p2_entry.pack(pady=10)

        btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
        btn_frame.pack(pady=20)

        ctk.CTkButton(
            btn_frame,
            text="▶ Start Match",
            width=160,
            height=50,
            corner_radius=12,
            font=("Arial", 16, "bold"),
            command=lambda: self.confirm_match(
                popup,
                p1_team_entry,
                p2_team_entry,
                p1_entry,
                p2_entry,
                rounds_slider,
                type_option
            )
        ).grid(row=0, column=0, padx=10, pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=140,
            height=50,
            corner_radius=12,
            fg_color="gray",
            hover_color="#555555",
            command=popup.destroy
        ).grid(row=0, column=1, padx=10, pady=10)


    def confirm_match(self, popup, p1_team, p2_team, p1, p2, rounds_slider, type_option):

        data = self.controller.match_data

        data["player1_team_name"] = p1_team.get().strip()
        data["player2_team_name"] = p2_team.get().strip()
        data["player1"] = p1.get().strip()
        data["player2"] = p2.get().strip()
        data["no_of_rounds"] = int(rounds_slider.get())
        data["type_of_match"] = type_option.get()

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
        
        popup.destroy()
        self.controller.show_page("DashboardPage")
        self.controller.pages["DashboardPage"].refresh_match_data()
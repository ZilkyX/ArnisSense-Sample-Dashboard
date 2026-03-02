import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox

class HomePage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        main_frame = ctk.CTkFrame(
            self
        )
        main_frame.pack(
            fill="both",
            expand=True
        )

        logo_img = ctk.CTkImage(
            Image.open("assets/logo/Arnisense_Logo-removebg-preview.png"),
            size=(60, 60)
        )

        ctk.CTkLabel(
            main_frame,
            image=logo_img,
            text=""
        ).pack(pady=(30, 10))

        self.logo_img = logo_img
    
        ctk.CTkLabel(
            main_frame,
            text="ArniSense",
            font=("Arial", 24, "bold")
        ).pack(pady=(10, 5))

        btn_frame = ctk.CTkFrame(
            main_frame,
            fg_color="transparent"
        )
        btn_frame.pack(pady=20)

        ctk.CTkButton(
            btn_frame,
            text="▶ Start Match",
            font=("Arial", 14, "bold"),
            width=180,
            height=50,
            corner_radius=12,
            command=lambda: controller.show_page("FormPage")
        ).pack(pady=8)

        ctk.CTkButton(
            btn_frame,
            text="📄 View Logs",
            font=("Arial", 12),
            width=140,
            height=40,
            corner_radius=10,
            fg_color="#2B2B2B",
            hover_color="#3A3A3A",
            command=lambda: controller.show_page("LogsPage")
        ).pack(pady=6)

        ctk.CTkButton(
            btn_frame,
            text="⚙ Settings",
            font=("Arial", 12),
            width=140,
            height=40,
            corner_radius=10,
            fg_color="#2B2B2B",
            hover_color="#3A3A3A",
            command=lambda: controller.show_page("SettingsPage")
        ).pack(pady=6)

        ctk.CTkLabel(
            main_frame,
            text="© 2026 ArniSense",
            font=("Arial", 12),
            text_color="gray"
        ).pack(pady=(14, 15))


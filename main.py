import customtkinter as ctk
from pages.home import HomePage
from pages.dashboard import DashboardPage
from pages.settings import SettingsPage
from pages.logs import LogsPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
ctk.set_widget_scaling(1.0)
ctk.set_window_scaling(1.0)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # self.attributes("-fullscreen", True)
        # self.configure(cursor="none")

        self.container = ctk.CTkFrame(self)
        self.geometry("1280x720")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.pages = {}

        for Page in (HomePage, DashboardPage, SettingsPage, LogsPage):
            page = Page(self.container, self)
            self.pages[Page.__name__] = page
            page.grid(row=0, column=0, sticky="nsew")

        self.show_page("HomePage")

    def show_page(self, name):
        self.pages[name].tkraise()

app = App()
app.mainloop()

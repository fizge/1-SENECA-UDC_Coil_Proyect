import tkinter as tk
import customtkinter as ctk


class ChargingWindow:
    def __init__(self, app):
        self.app = app
        self.charging_window = None

    def bar(self):
        self.charging_window = ctk.CTkToplevel(self.app.v)
        self.charging_window.title("Loading")
        self.charging_window.geometry("300x100+600+200")
        self.charging_window.lift()
        self.charging_window.grab_set()
        self.charging_window.protocol("WM_DELETE_WINDOW", self.do_nothing)

        label = ctk.CTkLabel(
            self.charging_window, text="Loading... Please wait", font=("Arial", 17, "bold"))
        label.pack(pady=20)

        progress_bar = ctk.CTkProgressBar(
            self.charging_window, mode='indeterminate')
        progress_bar.pack(fill="x", padx=20, pady=10)
        progress_bar.start()

    def close_bar(self):
        if self.charging_window:
            self.charging_window.destroy()

    def do_nothing(self):
        pass

import tkinter as tk
import customtkinter as ctk


class ChargingWindow:
    """
    A class representing a loading popup window with an animated progress bar.

    This class uses `customtkinter` to display a temporary modal window indicating 
    that a process is in progress. It includes a label with a message and an indeterminate 
    progress bar. The window is designed to block interaction with other windows while active.
    """

    def __init__(self, app):
        """
        Initializes the `ChargingWindow` class.

        :param app: The main application object to which the loading window belongs.
                    It must contain a reference to the main container (`app.v`).
        """
        self.app = app  # Reference to the main application
        self.charging_window = None  # The loading popup window (initialized later)

    def bar(self):
        """
        Creates and displays the loading window with the progress bar.

        The window includes:
        - A title ("Loading").
        - A message informing the user to wait.
        - An animated indeterminate progress bar.
        """
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
        """
        Closes and destroys the loading window if it exists.
        """
        if self.charging_window:
            self.charging_window.destroy()

    def do_nothing(self):
        """
        A placeholder method to prevent any action when trying to close the window 
        manually. This ensures that the user cannot close the loading window.
        """
        pass
